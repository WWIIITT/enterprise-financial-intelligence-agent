from pathlib import Path

from app.api.schemas import IngestRequest, IngestResponse
from app.core.config import ROOT_DIR
from app.rag.chunking import chunk_text
from app.rag.embedding_client import EmbeddingConfigurationError, EmbeddingProviderError, embedding_client
from app.rag.store import StoredChunk, rag_store, stable_chunk_id
from app.rag.vector_store import QdrantVectorStoreError, qdrant_vector_store
from app.services.metadata_service import record_ingested_chunks
from app.services.sec_edgar_client import SecEdgarError, SecFilingDocument, fetch_latest_filing


POLICY_DIR = ROOT_DIR / "data" / "policies"
LIVE_SEC_SOURCES = {"edgar", "live", "sec-edgar", "sec_edgar"}


def ingest_policy_documents(request: IngestRequest) -> IngestResponse:
    files = _resolve_policy_files(request.source, request.limit)
    stored_chunks: list[StoredChunk] = []

    for path in files:
        text = path.read_text(encoding="utf-8")
        title = path.stem.replace("-", " ").title()
        for chunk in chunk_text(text):
            stored_chunks.append(
                StoredChunk(
                    id=stable_chunk_id("policy", str(path.relative_to(ROOT_DIR)), chunk.chunk_index, chunk.text),
                    title=title,
                    text=chunk.text,
                    source_type="policy",
                    source=str(path.relative_to(ROOT_DIR)),
                    citation=f"{path.name} chunk {chunk.chunk_index + 1}",
                )
            )

    rag_store.delete_by_source_type("policy")
    qdrant_vector_store.delete_by_source_type("policy")
    indexed = rag_store.upsert(stored_chunks)
    qdrant_enabled = _upsert_qdrant(stored_chunks)
    if files:
        record_ingested_chunks("policy", request.source, "Internal Policy Documents", stored_chunks)
    return IngestResponse(
        status="completed",
        source_type="policy",
        source=request.source,
        documents_indexed=len(files),
        chunks_indexed=indexed,
        vector_backend="qdrant-provider-embeddings" if qdrant_enabled else "in-memory-dev-store",
        message=_ingestion_message(qdrant_enabled),
    )


def ingest_sec_document(request: IngestRequest) -> IngestResponse:
    if _is_live_sec_request(request):
        filing = _fetch_live_sec_filing(request)
        stored_chunks = _build_live_sec_chunks(filing)
        title = f"SEC Filing: {filing.ticker} {filing.form_type} {filing.filing_date}"
        source = filing.document_url
        message_suffix = (
            f" Live SEC EDGAR filing indexed: {filing.ticker} {filing.form_type} "
            f"{filing.filing_date} {filing.accession_number}."
        )
    else:
        text = _load_sec_text(request)
        title = request.ticker or request.cik or request.source
        source = request.source
        stored_chunks = _build_sample_sec_chunks(request, text, title)
        message_suffix = ""

    rag_store.delete_by_source_type("sec")
    qdrant_vector_store.delete_by_source_type("sec")
    indexed = rag_store.upsert(stored_chunks)
    qdrant_enabled = _upsert_qdrant(stored_chunks)
    record_ingested_chunks("sec", source, f"SEC Filing: {title}", stored_chunks)
    return IngestResponse(
        status="completed",
        source_type="sec",
        source=source,
        documents_indexed=1 if stored_chunks else 0,
        chunks_indexed=indexed,
        vector_backend="qdrant-provider-embeddings" if qdrant_enabled else "in-memory-dev-store",
        message=f"{_ingestion_message(qdrant_enabled)}{message_suffix}",
    )


def _is_live_sec_request(request: IngestRequest) -> bool:
    return request.source.lower() in LIVE_SEC_SOURCES


def _fetch_live_sec_filing(request: IngestRequest) -> SecFilingDocument:
    try:
        form_type = request.source_type or "10-K"
        return fetch_latest_filing(ticker=request.ticker, cik=request.cik, form_type=form_type)
    except SecEdgarError as exc:
        raise RuntimeError(str(exc)) from exc


def _build_live_sec_chunks(filing: SecFilingDocument) -> list[StoredChunk]:
    chunks: list[StoredChunk] = []
    for chunk in chunk_text(filing.text):
        section = _infer_sec_section(chunk.text)
        citation = f"{filing.citation_prefix} {section} chunk {chunk.chunk_index + 1}"
        chunks.append(
            StoredChunk(
                id=stable_chunk_id("sec", filing.document_url, chunk.chunk_index, chunk.text),
                title=f"SEC Filing: {filing.ticker} {filing.form_type} {filing.filing_date}",
                text=chunk.text,
                source_type="sec",
                source=filing.document_url,
                citation=citation,
                url=filing.document_url,
            )
        )
    return chunks


def _build_sample_sec_chunks(request: IngestRequest, text: str, title: str) -> list[StoredChunk]:
    return [
        StoredChunk(
            id=stable_chunk_id("sec", request.source, chunk.chunk_index, chunk.text),
            title=f"SEC Filing: {title}",
            text=chunk.text,
            source_type="sec",
            source=request.source,
            citation=f"{title} SEC sample chunk {chunk.chunk_index + 1}",
            url=request.source if request.source.startswith("http") else None,
        )
        for chunk in chunk_text(text)
    ]


def _infer_sec_section(text: str) -> str:
    lowered = text.lower()
    if "risk factor" in lowered:
        return "Risk Factors"
    if "management" in lowered and "discussion" in lowered:
        return "MD&A"
    if "business" in lowered:
        return "Business"
    return "Filing"


def _upsert_qdrant(chunks: list[StoredChunk]) -> bool:
    if not chunks:
        return False
    if not qdrant_vector_store.available():
        return False

    try:
        vectors = embedding_client.embed_texts([chunk.text for chunk in chunks])
        return qdrant_vector_store.upsert(chunks, vectors)
    except (EmbeddingConfigurationError, EmbeddingProviderError, QdrantVectorStoreError) as exc:
        raise RuntimeError(str(exc)) from exc


def _ingestion_message(qdrant_enabled: bool) -> str:
    if qdrant_enabled:
        return "Documents indexed with provider embeddings in Qdrant and mirrored in the local development store."
    return (
        "Documents indexed in the local development store. Qdrant was not reachable, so persistent vector retrieval "
        "was skipped for this run."
    )


def _resolve_policy_files(source: str, limit: int) -> list[Path]:
    if source.lower() in {"all", "data/policies", "policies"}:
        return sorted(POLICY_DIR.glob("*.md"))[:limit]

    candidate = (ROOT_DIR / source).resolve()
    policy_root = POLICY_DIR.resolve()
    if candidate.is_file() and policy_root in candidate.parents:
        return [candidate]

    named = POLICY_DIR / source
    if named.is_file():
        return [named]

    return sorted(POLICY_DIR.glob("*.md"))[:limit]


def _load_sec_text(request: IngestRequest) -> str:
    if request.content:
        return request.content

    candidate = (ROOT_DIR / request.source).resolve()
    data_root = (ROOT_DIR / "data").resolve()
    if candidate.is_file() and data_root in candidate.parents:
        return candidate.read_text(encoding="utf-8")

    company = request.ticker or "the company"
    return (
        f"Sample SEC filing excerpt for {company}. "
        "This local fallback represents management discussion, revenue trends, risk factors, liquidity, "
        "capital allocation, interest rate exposure, and forward-looking statements. "
        "Replace this sample with SEC EDGAR filing text for production-grade analysis."
    )
