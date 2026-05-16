from fastapi.testclient import TestClient

from app.main import app
from app.rag.store import rag_store


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


def test_low_confidence_question_returns_no_answer() -> None:
    response = client.post("/api/chat", json={"message": "Explain unrelated quantum battery patents in detail."})
    body = response.json()

    assert response.status_code == 200
    assert body["agent"] in {"rag-orchestrator-empty-index", "rag-orchestrator-low-confidence"}
    if body["agent"] == "rag-orchestrator-low-confidence":
        assert body["sources"] == []
        assert "not contain enough relevant evidence" in body["answer"]
