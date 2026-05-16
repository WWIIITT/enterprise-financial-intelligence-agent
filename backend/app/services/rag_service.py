from time import perf_counter

from app.api.schemas import ChatRequest, ChatResponse, Metrics, Source, TraceStep
from app.rag.embedding_client import EmbeddingConfigurationError, EmbeddingProviderError, embedding_client
from app.rag.store import StoredChunk, rag_store, rank_chunks, score_chunks
from app.rag.vector_store import QdrantVectorStoreError, qdrant_vector_store
from app.services.metadata_service import record_request_log


MIN_VECTOR_SCORE = 0.22
MIN_LEXICAL_SCORE = 0.10


def build_rag_chat_response(request: ChatRequest) -> ChatResponse:
    start = perf_counter()
    retrieved, retrieval_backend, top_score = _retrieve_chunks(request.message, limit=5)

    if not retrieved:
        answer = (
            "I do not have indexed source material for this question yet. "
            "Run policy ingestion with source='all' or ingest SEC text, then ask again for a cited answer."
        )
        sources: list[Source] = []
        agent = "rag-orchestrator-empty-index"
    elif not _has_enough_evidence(retrieved, top_score):
        answer = (
            "## Summary\n"
            "The indexed sources do not contain enough relevant evidence to answer this question confidently.\n\n"
            "## Evidence\n"
            "- Retrieval returned weak or indirect matches, so the system is not generating a sourced claim.\n\n"
            "## Sources\n"
            "- No sufficiently relevant source found."
        )
        sources = []
        agent = "rag-orchestrator-low-confidence"
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
            TraceStep(
                step="retrieve",
                detail=(
                    f"Retrieved {len(retrieved)} chunks using {retrieval_backend}; "
                    f"top score {top_score:.3f}."
                ),
            ),
            TraceStep(step="respond", detail="Returned citation-aware response shape."),
        ],
        metrics=Metrics(latency_ms=latency_ms),
    )
    record_request_log(request.message, response.agent, len(response.sources), latency_ms)
    return response


def _retrieve_chunks(query: str, limit: int) -> tuple[list[StoredChunk], str, float]:
    if qdrant_vector_store.available():
        try:
            query_vector = embedding_client.embed_query(query)
            candidates = qdrant_vector_store.search(query_vector, limit=limit * 2)
            ranked = _rerank_chunks(query, candidates, limit)
            top_score = ranked[0].score if ranked else 0.0
            return ranked, "qdrant-provider-embeddings", top_score
        except (EmbeddingConfigurationError, EmbeddingProviderError, QdrantVectorStoreError) as exc:
            raise RuntimeError(str(exc)) from exc

    ranked = rag_store.search(query, limit=limit)
    top_score = score_chunks(query, ranked[:1])[0][0] if ranked else 0.0
    return ranked, "in-memory-dev-store", top_score


def _rerank_chunks(query: str, candidates: list[StoredChunk], limit: int) -> list[StoredChunk]:
    deduped: dict[str, StoredChunk] = {}
    for chunk in candidates:
        deduped[chunk.id] = chunk

    source_intent = _query_source_intent(query)
    lexical_scores = {chunk.id: score for score, chunk in score_chunks(query, list(deduped.values()))}
    scored: list[tuple[float, StoredChunk]] = []
    for chunk in deduped.values():
        lexical_score = lexical_scores.get(chunk.id, 0.0)
        combined_score = chunk.score + (lexical_score * 0.15) + _source_intent_bonus(source_intent, chunk)
        if combined_score > 0:
            scored.append((combined_score, chunk))

    scored.sort(key=lambda item: item[0], reverse=True)
    if source_intent:
        intent_scored = [(score, chunk) for score, chunk in scored if chunk.source_type == source_intent]
        if intent_scored:
            scored = intent_scored
    return [
        StoredChunk(
            id=chunk.id,
            title=chunk.title,
            text=chunk.text,
            source_type=chunk.source_type,
            source=chunk.source,
            citation=chunk.citation,
            url=chunk.url,
            score=combined_score,
        )
        for combined_score, chunk in scored[:limit]
    ]


def _has_enough_evidence(chunks: list[StoredChunk], top_score: float) -> bool:
    if not chunks:
        return False
    if chunks[0].score >= MIN_VECTOR_SCORE:
        return True
    return top_score >= MIN_LEXICAL_SCORE


def _query_source_intent(query: str) -> str | None:
    terms = {term.lower() for term in query.replace("?", " ").split()}
    sec_terms = {"apple", "aapl", "company", "filing", "revenue", "risk", "risks", "valuation", "supply"}
    policy_terms = {"policy", "approved", "prohibited", "privacy", "pii", "compliance", "governance"}
    if terms.intersection(sec_terms) and not terms.intersection(policy_terms):
        return "sec"
    if terms.intersection(policy_terms):
        return "policy"
    return None


def _source_intent_bonus(source_intent: str | None, chunk: StoredChunk) -> float:
    if source_intent == chunk.source_type:
        return 0.35
    if source_intent and chunk.source_type != source_intent:
        return -0.20
    return 0.0


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
