from fastapi.testclient import TestClient

from app.main import app
from app.rag.store import rag_store
from app.services.ingestion_service import _build_live_sec_chunks
from app.services.sec_edgar_client import SecFilingDocument


client = TestClient(app)


def test_chat_empty_index_returns_guidance() -> None:
    response = client.post("/api/chat", json={"message": "What does the policy say about PII?"})
    body = response.json()

    assert response.status_code == 200
    assert body["agent"] in {"rag-orchestrator-empty-index", "policy-compliance-agent", "rag-orchestrator"}
    assert set(body.keys()) == {"answer", "agent", "sources", "trace", "metrics"}


def test_policy_ingestion_indexes_local_documents() -> None:
    rag_store.delete_by_source_type("policy")
    ingest_response = client.post("/api/ingest/policy", json={"source": "all"})
    ingest_body = ingest_response.json()

    assert ingest_response.status_code == 200
    assert ingest_body["status"] == "completed"
    assert ingest_body["source_type"] == "policy"
    assert ingest_body["documents_indexed"] >= 1
    assert ingest_body["chunks_indexed"] >= 1

    chat_response = client.post("/api/chat", json={"message": "What does the AI usage policy require?"})
    chat_body = chat_response.json()

    assert chat_response.status_code == 200
    assert chat_body["sources"]
    assert chat_body["metrics"]["latency_ms"] >= 0
    assert "placeholder for policy RAG development" not in chat_body["answer"]


def test_sec_ingestion_accepts_inline_content() -> None:
    rag_store.delete_by_source_type("sec")
    response = client.post(
        "/api/ingest/sec",
        json={
            "source": "sample-sec-inline",
            "ticker": "AAPL",
            "content": "Apple reports revenue risk from foreign exchange, interest rates, and product demand.",
        },
    )
    body = response.json()

    assert response.status_code == 200
    assert body["status"] == "completed"
    assert body["source_type"] == "sec"
    assert body["documents_indexed"] == 1
    assert body["chunks_indexed"] >= 1

    chat_response = client.post("/api/chat", json={"message": "What risks are mentioned for Apple?"})
    chat_body = chat_response.json()

    assert chat_response.status_code == 200
    assert chat_body["sources"][0]["source_type"] == "sec"


def test_sec_ingestion_accepts_mocked_live_edgar(monkeypatch) -> None:
    rag_store.delete_by_source_type("sec")

    def fake_fetch_latest_filing(
        ticker: str | None,
        cik: str | None,
        form_type: str,
        filing_year: int | None,
        accession_number: str | None,
    ) -> SecFilingDocument:
        assert ticker == "AAPL"
        assert cik is None
        assert form_type == "10-K"
        assert filing_year is None
        assert accession_number is None
        return SecFilingDocument(
            ticker="AAPL",
            cik="0000320193",
            company_name="Apple Inc.",
            form_type="10-K",
            accession_number="0000320193-24-000123",
            filing_date="2024-11-01",
            primary_document="aapl-20240928.htm",
            document_url="https://www.sec.gov/Archives/edgar/data/320193/000032019324000123/aapl-20240928.htm",
            text="Item 1A. Risk Factors Apple reports revenue risk, supply chain risk, and macroeconomic uncertainty.",
            raw_path="data/raw/sec/AAPL_10-K_0000320193-24-000123_aapl-20240928.htm",
        )

    monkeypatch.setattr("app.services.ingestion_service.fetch_latest_filing", fake_fetch_latest_filing)

    response = client.post("/api/ingest/sec", json={"source": "edgar", "ticker": "AAPL", "source_type": "10-K"})
    body = response.json()

    assert response.status_code == 200
    assert body["status"] == "completed"
    assert body["source_type"] == "sec"
    assert body["documents_indexed"] == 1
    assert body["chunks_indexed"] >= 1
    assert "Live SEC EDGAR filing indexed" in body["message"]

    chat_response = client.post("/api/chat", json={"message": "What risks are mentioned for Apple?"})
    chat_body = chat_response.json()

    assert chat_response.status_code == 200
    assert chat_body["sources"][0]["citation"].startswith("AAPL 10-K 2024-11-01 0000320193-24-000123")


def test_sec_ingestion_prefers_new_form_type_fields(monkeypatch) -> None:
    def fake_fetch_latest_filing(
        ticker: str | None,
        cik: str | None,
        form_type: str,
        filing_year: int | None,
        accession_number: str | None,
    ) -> SecFilingDocument:
        assert ticker == "AAPL"
        assert form_type == "10-Q"
        assert filing_year == 2025
        assert accession_number == "0000320193-25-000050"
        return SecFilingDocument(
            ticker="AAPL",
            cik="0000320193",
            company_name="Apple Inc.",
            form_type="10-Q",
            accession_number="0000320193-25-000050",
            filing_date="2025-05-01",
            primary_document="aapl-20250329.htm",
            document_url="https://www.sec.gov/Archives/edgar/data/320193/000032019325000050/aapl-20250329.htm",
            text="Item 1A. Risk Factors Apple faces quarterly supply risk and demand risk.",
            raw_path="data/raw/sec/AAPL_10-Q_0000320193-25-000050_aapl-20250329.htm",
        )

    monkeypatch.setattr("app.services.ingestion_service.fetch_latest_filing", fake_fetch_latest_filing)

    response = client.post(
        "/api/ingest/sec",
        json={
            "source": "edgar",
            "ticker": "AAPL",
            "source_type": "10-K",
            "form_type": "10-Q",
            "filing_year": 2025,
            "accession_number": "0000320193-25-000050",
        },
    )
    body = response.json()

    assert response.status_code == 200
    assert "AAPL 10-Q 2025-05-01 0000320193-25-000050" in body["message"]


def test_live_sec_chunk_citations_carry_forward_section() -> None:
    filing = SecFilingDocument(
        ticker="AAPL",
        cik="0000320193",
        company_name="Apple Inc.",
        form_type="10-K",
        accession_number="0000320193-24-000123",
        filing_date="2024-11-01",
        primary_document="aapl-20240928.htm",
        document_url="https://www.sec.gov/Archives/edgar/data/320193/000032019324000123/aapl-20240928.htm",
        text=(
            "Item 1A. Risk Factors. Apple faces cybersecurity risk and supply chain risk. "
            "Additional risk disclosure continues for a long paragraph. " * 20
        ),
        raw_path="data/raw/sec/AAPL_10-K_0000320193-24-000123_aapl-20240928.htm",
    )

    chunks = _build_live_sec_chunks(filing)

    assert chunks
    assert all("Risk Factors" in chunk.citation for chunk in chunks[:2])


def test_low_confidence_question_returns_no_answer() -> None:
    response = client.post("/api/chat", json={"message": "Explain unrelated quantum battery patents in detail."})
    body = response.json()

    assert response.status_code == 200
    assert body["agent"] in {"rag-orchestrator-empty-index", "rag-orchestrator-low-confidence"}
    if body["agent"] == "rag-orchestrator-low-confidence":
        assert body["sources"] == []
        assert "not contain enough relevant evidence" in body["answer"]
