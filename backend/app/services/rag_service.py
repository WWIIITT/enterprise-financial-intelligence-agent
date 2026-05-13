from time import perf_counter

from app.api.schemas import ChatRequest, ChatResponse, Metrics, Source, TraceStep
from app.rag.store import rag_store
from app.rag.vector_store import qdrant_vector_store
from app.services.metadata_service import record_request_log


def build_rag_chat_response(request: ChatRequest) -> ChatResponse:
    start = perf_counter()
    retrieved = qdrant_vector_store.search(request.message, limit=5) or rag_store.search(request.message, limit=5)

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


def _select_agent(chunks) -> str:
    source_types = {chunk.source_type for chunk in chunks}
    if source_types == {"policy"}:
        return "policy-compliance-agent"
    if source_types == {"sec"}:
        return "document-research-agent"
    return "rag-orchestrator"


def _compose_grounded_answer(question: str, chunks) -> str:
    evidence = " ".join(chunk.text for chunk in chunks[:3])
    excerpt = evidence[:900]
    citations = ", ".join(chunk.citation for chunk in chunks[:3])
    return (
        f"Based on the indexed sources, the relevant evidence for '{question}' is: {excerpt} "
        f"Sources: {citations}."
    )
