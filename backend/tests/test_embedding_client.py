import pytest

from app.rag.embedding_client import EmbeddingConfigurationError, EmbeddingClient, _normalize_openai_base_url


def test_embedding_client_requires_embedding_model(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.rag.embedding_client.settings.embedding_model", "")
    monkeypatch.setattr("app.rag.embedding_client.settings.llm_api_key", "test-key")

    client = EmbeddingClient()

    with pytest.raises(EmbeddingConfigurationError, match="EMBEDDING_MODEL"):
        client.embed_texts(["hello"])


def test_embedding_client_uses_provider_response(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.rag.embedding_client.settings.embedding_model", "test-embedding-model")
    monkeypatch.setattr("app.rag.embedding_client.settings.llm_api_key", "")
    monkeypatch.setattr("app.rag.embedding_client.settings.embedding_api_key", "test-embedding-key")

    class FakeEmbeddings:
        @staticmethod
        def create(model: str, input: list[str]):
            assert model == "test-embedding-model"
            assert input == ["alpha", "beta"]

            class Item:
                def __init__(self, embedding: list[float]) -> None:
                    self.embedding = embedding

            class Response:
                data = [Item([1.0, 0.0]), Item([0.0, 1.0])]

            return Response()

    class FakeOpenAI:
        embeddings = FakeEmbeddings()

    client = EmbeddingClient()
    monkeypatch.setattr(client, "_get_client", lambda: FakeOpenAI())

    assert client.embed_texts(["alpha", "beta"]) == [[1.0, 0.0], [0.0, 1.0]]


def test_embedding_client_rejects_rerank_model(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.rag.embedding_client.settings.embedding_model", "qwen3-rerank")
    monkeypatch.setattr("app.rag.embedding_client.settings.embedding_api_key", "test-key")
    monkeypatch.setattr("app.rag.embedding_client.settings.embedding_base_url", "https://api.example.com/v1")

    client = EmbeddingClient()

    with pytest.raises(EmbeddingConfigurationError, match="reranking model"):
        client.embed_texts(["hello"])


def test_openai_base_url_normalization() -> None:
    assert _normalize_openai_base_url("https://api.example.com/v1/embeddings") == "https://api.example.com/v1"
    assert _normalize_openai_base_url("https://api.example.com/v1/chat/completions") == "https://api.example.com/v1"
    assert _normalize_openai_base_url("https://api.example.com/v1") == "https://api.example.com/v1"
