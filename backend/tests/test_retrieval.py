from app.rag.store import StoredChunk
from app.services.rag_service import _has_enough_evidence, _rerank_chunks


def test_rerank_prefers_lexically_relevant_vector_candidate() -> None:
    policy_chunk = StoredChunk(
        id="policy-1",
        title="AI Usage Policy",
        text="Approved AI use requires review and citation controls.",
        source_type="policy",
        source="policy",
        citation="policy chunk 1",
        score=0.30,
    )
    sec_chunk = StoredChunk(
        id="sec-1",
        title="SEC Filing: AAPL",
        text="Apple reports revenue risk from interest rates, product demand, and supply chain constraints.",
        source_type="sec",
        source="sec",
        citation="AAPL SEC chunk 1",
        score=0.29,
    )

    ranked = _rerank_chunks("What risks are mentioned for Apple?", [policy_chunk, sec_chunk], limit=2)

    assert ranked[0].source_type == "sec"
    assert ranked[0].score > ranked[1].score


def test_low_vector_score_is_not_enough_evidence() -> None:
    chunk = StoredChunk(
        id="weak",
        title="Weak Match",
        text="This text is only weakly related.",
        source_type="policy",
        source="policy",
        citation="weak chunk",
        score=0.05,
    )

    assert not _has_enough_evidence([chunk], top_score=0.05)
