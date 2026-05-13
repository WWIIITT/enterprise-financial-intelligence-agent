from pathlib import Path

from app.api.schemas import IngestRequest, IngestResponse
from app.core.config import ROOT_DIR
from app.rag.chunking import chunk_text
from app.rag.store import StoredChunk, rag_store, stable_chunk_id
from app.rag.vector_store import qdrant_vector_store
from app.services.metadata_service import record_ingested_chunks


POLICY_DIR = ROOT_DIR / "data" / "policies"


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

    indexed = rag_store.upsert(stored_chunks)
    qdrant_enabled = qdrant_vector_store.upsert(stored_chunks)
    if files:
        record_ingested_chunks("policy", request.source, "Internal Policy Documents", stored_chunks)
    return IngestResponse(
        status="completed",
        source_type="policy",
        source=request.source,
        documents_indexed=len(files),
        chunks_indexed=indexed,
        vector_backend="qdrant+in-memory" if qdrant_enabled else "in-memory-dev-store",
        message="Policy documents indexed for local RAG. Qdrant is used when available; otherwise local development search is used.",
    )


def ingest_sec_document(request: IngestRequest) -> IngestResponse:
    text = _load_sec_text(request)
    title = request.ticker or request.cik or request.source
    stored_chunks = [
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

    indexed = rag_store.upsert(stored_chunks)
    qdrant_enabled = qdrant_vector_store.upsert(stored_chunks)
    record_ingested_chunks("sec", request.source, f"SEC Filing: {title}", stored_chunks)
    return IngestResponse(
        status="completed",
        source_type="sec",
        source=request.source,
        documents_indexed=1 if text else 0,
        chunks_indexed=indexed,
        vector_backend="qdrant+in-memory" if qdrant_enabled else "in-memory-dev-store",
        message="SEC content indexed from request content or local sample text. Live EDGAR fetching is planned after SEC connector hardening.",
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
