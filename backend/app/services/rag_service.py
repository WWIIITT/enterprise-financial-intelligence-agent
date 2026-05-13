from time import perf_counter

from app.api.schemas import ChatRequest, ChatResponse, Metrics, Source, TraceStep
from app.rag.store import StoredChunk, rag_store, rank_chunks
from app.rag.vector_store import qdrant_vector_store
from app.services.metadata_service import record_request_log


def build_rag_chat_response(request: ChatRequest) -> ChatResponse:
    start = perf_counter()
    retrieved = _retrieve_chunks(request.message, limit=5)

    if not retrieved:
        answer = (
            "I do not have indexed source material for this question yet. "
            "Run policy ingestion with source='all' or ingest SEC text, then ask again for a cited answer."
        )
        sources: list[Source] = []
        agent = "rag-orchestrator-empty-index"
    else:
        answer = _compose_grounded_answer(request.message, retrieved)
        sources = [
            Source(
                title=chunk.title,
                url=chunk.url,
                citation=chunk.citation,
                source_type=chunk.source_type,
            )
            for chunk in retrieved
        ]
        agent = _select_agent(retrieved)

    latency_ms = int((perf_counter() - start) * 1000)
    response = ChatResponse(
        answer=answer,
        agent=agent,
        sources=sources,
        trace=[
            TraceStep(step="receive", detail=f"Received {len(request.message)} characters."),
            TraceStep(step="retrieve", detail=f"Retrieved {len(retrieved)} chunks from local RAG store."),
            TraceStep(step="respond", detail="Returned citation-aware response shape."),
        ],
        metrics=Metrics(latency_ms=latency_ms),
    )
    record_request_log(request.message, response.agent, len(response.sources), latency_ms)
    return response


def _retrieve_chunks(query: str, limit: int) -> list[StoredChunk]:
    candidates = qdrant_vector_store.search(query, limit=limit) + rag_store.search(query, limit=limit)
    deduped: dict[str, StoredChunk] = {}
    for chunk in candidates:
        deduped[chunk.id] = chunk
    return rank_chunks(query, list(deduped.values()), limit)


def _select_agent(chunks) -> str:
    source_types = {chunk.source_type for chunk in chunks}
    if source_types == {"policy"}:
        return "policy-compliance-agent"
    if source_types == {"sec"}:
        return "document-research-agent"
    return "rag-orchestrator"


def _compose_grounded_answer(question: str, chunks) -> str:
    evidence_items = [f"- {_clean_evidence_text(chunk.text)[:420]}" for chunk in chunks[:3]]
    citations = "\n".join(f"- {chunk.citation}" for chunk in chunks[:3])
    return (
        f"## Summary\n"
        f"Based on the indexed sources, the relevant evidence for '{question}' is shown below.\n\n"
        f"## Evidence\n"
        f"{chr(10).join(evidence_items)}\n\n"
        f"## Sources\n"
        f"{citations}"
    )


def _clean_evidence_text(text: str) -> str:
    cleaned_lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        line = line.lstrip("#").strip()
        if line.startswith("- "):
            line = line[2:].strip()
        cleaned_lines.append(line)

    cleaned = " ".join(cleaned_lines) if cleaned_lines else text
    cleaned = cleaned.replace(" ## ", ". ").replace(" # ", ". ")
    cleaned = cleaned.replace(" - ", "; ")
    return " ".join(cleaned.split())
