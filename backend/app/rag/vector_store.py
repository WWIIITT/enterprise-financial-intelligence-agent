from __future__ import annotations

from hashlib import blake2b

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, FieldCondition, Filter, MatchValue, PointStruct, VectorParams

from app.core.config import settings
from app.core.network import can_open_tcp_connection
from app.rag.store import StoredChunk


VECTOR_SIZE = 384
COLLECTION_NAME = "aurelia_ledger_chunks"


class QdrantVectorStore:
    def __init__(self) -> None:
        self._client: QdrantClient | None = None

    def available(self) -> bool:
        return bool(settings.qdrant_url and can_open_tcp_connection(settings.qdrant_url)) and self._get_client() is not None

    def upsert(self, chunks: list[StoredChunk]) -> bool:
        if not self.available():
            return False

        client = self._get_client()
        if client is None or not chunks:
            return False

        try:
            self._ensure_collection(client)
            client.upsert(
                collection_name=COLLECTION_NAME,
                points=[
                    PointStruct(
                        id=chunk.id,
                        vector=hash_embedding(chunk.text),
                        payload={
                            "title": chunk.title,
                            "text": chunk.text,
                            "source_type": chunk.source_type,
                            "source": chunk.source,
                            "citation": chunk.citation,
                            "url": chunk.url,
                        },
                    )
                    for chunk in chunks
                ],
            )
        except Exception:
            return False

        return True

    def delete_by_source_type(self, source_type: str) -> bool:
        if not self.available():
            return False

        client = self._get_client()
        if client is None:
            return False

        try:
            self._ensure_collection(client)
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

    def search(self, query: str, limit: int = 5) -> list[StoredChunk]:
        if not self.available():
            return []

        client = self._get_client()
        if client is None:
            return []

        try:
            self._ensure_collection(client)
            results = client.search(
                collection_name=COLLECTION_NAME,
                query_vector=hash_embedding(query),
                limit=limit,
            )
        except Exception:
            return []

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

    @staticmethod
    def _ensure_collection(client: QdrantClient) -> None:
        collections = client.get_collections().collections
        if any(collection.name == COLLECTION_NAME for collection in collections):
            return
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )


def hash_embedding(text: str) -> list[float]:
    vector = [0.0] * VECTOR_SIZE
    for token in text.lower().split():
        digest = blake2b(token.encode("utf-8"), digest_size=8).digest()
        index = int.from_bytes(digest[:4], "big") % VECTOR_SIZE
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vector[index] += sign

    magnitude = sum(value * value for value in vector) ** 0.5
    if magnitude == 0:
        return vector
    return [value / magnitude for value in vector]


qdrant_vector_store = QdrantVectorStore()
