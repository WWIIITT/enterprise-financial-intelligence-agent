from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_chat_shape() -> None:
    response = client.post("/api/chat", json={"message": "What is Aurelia Ledger?"})
    body = response.json()
    assert response.status_code == 200
    assert set(body.keys()) == {"answer", "agent", "sources", "trace", "metrics"}
