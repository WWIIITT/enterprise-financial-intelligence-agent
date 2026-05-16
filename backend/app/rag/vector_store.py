from __future__ import annotations

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, FieldCondition, Filter, MatchValue, PointStruct, VectorParams

from app.core.config import settings
from app.core.network import can_open_tcp_connection
from app.rag.store import StoredChunk


COLLECTION_NAME = "aurelia_ledger_chunks"


class QdrantVectorStoreError(RuntimeError):
    pass


class QdrantVectorStore:
    def __init__(self) -> None:
        self._client: QdrantClient | None = None

    def available(self) -> bool:
        if settings.testing:
            return False
        return bool(settings.qdrant_url and can_open_tcp_connection(settings.qdrant_url)) and self._get_client() is not None

    def upsert(self, chunks: list[StoredChunk], vectors: list[list[float]]) -> bool:
        if not self.available():
            return False

        client = self._get_client()
        if client is None or not chunks:
            return False
        if len(chunks) != len(vectors):
            raise QdrantVectorStoreError("Chunk and vector counts do not match.")

        try:
            vector_size = _vector_size(vectors)
            self._ensure_collection(client, vector_size)
            client.upsert(
                collection_name=COLLECTION_NAME,
                points=[
                    PointStruct(
                        id=chunk.id,
                        vector=vector,
                        payload={
                            "title": chunk.title,
                            "text": chunk.text,
                            "source_type": chunk.source_type,
                            "source": chunk.source,
                            "citation": chunk.citation,
                            "url": chunk.url,
                        },
                    )
                    for chunk, vector in zip(chunks, vectors)
                ],
            )
        except QdrantVectorStoreError:
            raise
        except Exception as exc:
            raise QdrantVectorStoreError(f"Qdrant upsert failed: {exc}") from exc

        return True

    def recreate_collection(self, vector_size: int) -> bool:
        if not self.available():
            return False

        client = self._get_client()
        if client is None:
            return False

        try:
            client.recreate_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )
        except Exception as exc:
            raise QdrantVectorStoreError(f"Qdrant collection reset failed: {exc}") from exc

        return True

    def delete_by_source_type(self, source_type: str) -> bool:
        if not self.available():
            return False

        client = self._get_client()
        if client is None:
            return False

        try:
            client.delete(
                collection_name=COLLECTION_NAME,
                points_selector=Filter(
                    must=[
                        FieldCondition(
                            key="source_type",
                            match=MatchValue(value=source_type),
                        )
                    ]
                ),
            )
        except Exception:
            return False

        return True

    def search(self, query_vector: list[float], limit: int = 5) -> list[StoredChunk]:
        if not self.available():
            return []

        client = self._get_client()
        if client is None:
            return []

        try:
            self._validate_collection(client, len(query_vector))
            results = client.search(
                collection_name=COLLECTION_NAME,
                query_vector=query_vector,
                limit=limit,
                with_payload=True,
            )
        except QdrantVectorStoreError:
            raise
        except Exception as exc:
            raise QdrantVectorStoreError(f"Qdrant search failed: {exc}") from exc

        chunks: list[StoredChunk] = []
        for result in results:
            payload = result.payload or {}
            chunks.append(
                StoredChunk(
                    id=str(result.id),
                    title=str(payload.get("title", "Untitled Source")),
                    text=str(payload.get("text", "")),
                    source_type=str(payload.get("source_type", "unknown")),
                    source=str(payload.get("source", "")),
                    citation=str(payload.get("citation", "")),
                    url=payload.get("url") if isinstance(payload.get("url"), str) else None,
                    score=float(result.score or 0.0),
                )
            )
        return chunks

    def _get_client(self) -> QdrantClient | None:
        if self._client is not None:
            return self._client
        if not settings.qdrant_url:
            return None
        try:
            self._client = QdrantClient(url=settings.qdrant_url, timeout=1)
        except Exception:
            self._client = None
        return self._client

    def _ensure_collection(self, client: QdrantClient, vector_size: int) -> None:
        collections = client.get_collections().collections
        if any(collection.name == COLLECTION_NAME for collection in collections):
            self._validate_collection(client, vector_size)
            return
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

    @staticmethod
    def _validate_collection(client: QdrantClient, vector_size: int) -> None:
        try:
            info = client.get_collection(collection_name=COLLECTION_NAME)
        except Exception as exc:
            raise QdrantVectorStoreError(f"Qdrant collection is unavailable: {exc}") from exc

        vectors_config = info.config.params.vectors
        existing_size = getattr(vectors_config, "size", None)
        if existing_size is None and isinstance(vectors_config, dict):
            first_config = next(iter(vectors_config.values()), None)
            existing_size = getattr(first_config, "size", None)
        if existing_size and int(existing_size) != vector_size:
            raise QdrantVectorStoreError(
                f"Qdrant collection vector size is {existing_size}, but embedding model returned {vector_size}. "
                "Reset the Qdrant collection before re-ingesting."
            )


def _vector_size(vectors: list[list[float]]) -> int:
    if not vectors or not vectors[0]:
        raise QdrantVectorStoreError("Embedding vector is empty.")
    vector_size = len(vectors[0])
    if any(len(vector) != vector_size for vector in vectors):
        raise QdrantVectorStoreError("Embedding vectors have inconsistent dimensions.")
    return vector_size


qdrant_vector_store = QdrantVectorStore()
