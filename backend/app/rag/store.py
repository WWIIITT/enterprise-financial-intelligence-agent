from __future__ import annotations

import math
from dataclasses import dataclass
from hashlib import sha256
from uuid import UUID


@dataclass(frozen=True)
class StoredChunk:
    id: str
    title: str
    text: str
    source_type: str
    source: str
    citation: str
    url: str | None = None


class InMemoryRagStore:
    def __init__(self) -> None:
        self._chunks: dict[str, StoredChunk] = {}

    def upsert(self, chunks: list[StoredChunk]) -> int:
        for chunk in chunks:
            self._chunks[chunk.id] = chunk
        return len(chunks)

    def search(self, query: str, limit: int = 5) -> list[StoredChunk]:
        query_terms = _terms(query)
        if not query_terms:
            return []

        scored: list[tuple[float, StoredChunk]] = []
        for chunk in self._chunks.values():
            text_terms = _terms(f"{chunk.title} {chunk.text}")
            if not text_terms:
                continue
            overlap = query_terms.intersection(text_terms)
            score = len(overlap) / math.sqrt(len(text_terms))
            if score > 0:
                scored.append((score, chunk))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [chunk for _, chunk in scored[:limit]]

    def count(self) -> int:
        return len(self._chunks)


def stable_chunk_id(source_type: str, source: str, chunk_index: int, text: str) -> str:
    digest = sha256(f"{source_type}:{source}:{chunk_index}:{text}".encode("utf-8")).hexdigest()
    return str(UUID(hex=digest[:32]))


def _terms(value: str) -> set[str]:
    return {term.lower() for term in value.replace("/", " ").replace("-", " ").split() if len(term) > 2}


rag_store = InMemoryRagStore()
