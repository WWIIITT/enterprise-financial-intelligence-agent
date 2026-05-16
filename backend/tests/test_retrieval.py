from app.rag.store import StoredChunk
from app.services.rag_service import _compose_grounded_answer, _has_enough_evidence, _rerank_chunks


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

    assert [chunk.source_type for chunk in ranked] == ["sec"]


def test_company_risk_intent_filters_non_sec_chunks() -> None:
    candidates = [
        StoredChunk(
            id="policy-1",
            title="Model Risk Policy",
            text="AI model risk governance and review policy.",
            source_type="policy",
            source="policy",
            citation="policy chunk 1",
            score=0.95,
        ),
        StoredChunk(
            id="sec-1",
            title="SEC Filing: AAPL",
            text="Apple reports revenue risk from interest rates and supply chain constraints.",
            source_type="sec",
            source="sec",
            citation="AAPL SEC chunk 1",
            score=0.40,
        ),
    ]

    ranked = _rerank_chunks("What risks are mentioned for Apple?", candidates, limit=5)

    assert [chunk.source_type for chunk in ranked] == ["sec"]


def test_risk_query_prefers_risk_factors_section() -> None:
    business_chunk = StoredChunk(
        id="business",
        title="SEC Filing: AAPL",
        text="Apple describes products and services in its business section.",
        source_type="sec",
        source="sec",
        citation="AAPL 10-K 2025-10-31 0000320193-25-000079 Business chunk 10",
        score=0.90,
    )
    risk_chunk = StoredChunk(
        id="risk",
        title="SEC Filing: AAPL",
        text="Apple faces cybersecurity risk, tax risk, and supply chain risk.",
        source_type="sec",
        source="sec",
        citation="AAPL 10-K 2025-10-31 0000320193-25-000079 Risk Factors chunk 50",
        score=0.60,
    )

    ranked = _rerank_chunks("What risks are mentioned for Apple?", [business_chunk, risk_chunk], limit=2)

    assert ranked[0].citation and "Risk Factors" in ranked[0].citation


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


def test_sec_risk_answer_uses_key_risks_section() -> None:
    chunk = StoredChunk(
        id="risk",
        title="SEC Filing: AAPL",
        text=(
            "Item 1A. Risk Factors. Apple faces supply chain risk and cybersecurity risk. "
            "These risks could adversely affect business results."
        ),
        source_type="sec",
        source="sec",
        citation="AAPL 10-K 2025-10-31 0000320193-25-000079 Risk Factors chunk 1",
        score=0.90,
    )

    answer = _compose_grounded_answer("What risks are mentioned for Apple?", [chunk])

    assert "## Key Risks" in answer
    assert "supply chain risk" in answer
    assert "0000320193-25-000079" in answer
