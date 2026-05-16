from __future__ import annotations

from openai import OpenAI

from app.core.config import settings


class EmbeddingConfigurationError(RuntimeError):
    pass


class EmbeddingProviderError(RuntimeError):
    pass


class EmbeddingClient:
    def __init__(self) -> None:
        self._client: OpenAI | None = None

    def configured(self) -> bool:
        return bool(self._api_key() and settings.embedding_model)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        self._validate_embedding_settings()

        try:
            response = self._get_client().embeddings.create(
                model=settings.embedding_model,
                input=texts,
            )
        except Exception as exc:
            raise EmbeddingProviderError(f"Embedding provider request failed: {exc}") from exc

        vectors = [item.embedding for item in response.data]
        if len(vectors) != len(texts):
            raise EmbeddingProviderError("Embedding provider returned an unexpected number of vectors.")
        if not all(vectors):
            raise EmbeddingProviderError("Embedding provider returned an empty vector.")
        return vectors

    def embed_query(self, query: str) -> list[float]:
        return self.embed_texts([query])[0]

    def _validate_embedding_settings(self) -> None:
        if not settings.embedding_model:
            raise EmbeddingConfigurationError("EMBEDDING_MODEL is required for Sprint 2 Qdrant retrieval.")
        if not self._api_key():
            raise EmbeddingConfigurationError("EMBEDDING_API_KEY or LLM_API_KEY is required to call the embedding provider.")
        if "rerank" in settings.embedding_model.lower():
            raise EmbeddingConfigurationError(
                "EMBEDDING_MODEL appears to be a reranking model. Qdrant retrieval needs an embedding model, "
                "not a rerank model."
            )
        if "rerank" in self._base_url().lower():
            raise EmbeddingConfigurationError(
                "EMBEDDING_BASE_URL appears to point to a rerank endpoint. Use an OpenAI-compatible /v1 base URL "
                "that supports /embeddings."
            )

    @staticmethod
    def _api_key() -> str:
        return settings.embedding_api_key or settings.llm_api_key

    @staticmethod
    def _base_url() -> str:
        raw_url = settings.embedding_base_url or settings.llm_base_url
        return _normalize_openai_base_url(raw_url)

    def _get_client(self) -> OpenAI:
        if self._client is not None:
            return self._client

        kwargs: dict[str, str] = {"api_key": self._api_key()}
        if self._base_url():
            kwargs["base_url"] = self._base_url()
        self._client = OpenAI(**kwargs)
        return self._client


embedding_client = EmbeddingClient()


def _normalize_openai_base_url(raw_url: str) -> str:
    base_url = raw_url.rstrip("/")
    for suffix in ("/embeddings", "/chat/completions", "/completions"):
        if base_url.endswith(suffix):
            return base_url[: -len(suffix)]
    return base_url
