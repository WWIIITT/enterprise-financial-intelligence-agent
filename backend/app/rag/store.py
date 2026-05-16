from __future__ import annotations

import math
import re
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
    score: float = 0.0


class InMemoryRagStore:
    def __init__(self) -> None:
        self._chunks: dict[str, StoredChunk] = {}

    def upsert(self, chunks: list[StoredChunk]) -> int:
        for chunk in chunks:
            self._chunks[chunk.id] = chunk
        return len(chunks)

    def delete_by_source_type(self, source_type: str) -> int:
        ids_to_delete = [chunk_id for chunk_id, chunk in self._chunks.items() if chunk.source_type == source_type]
        for chunk_id in ids_to_delete:
            del self._chunks[chunk_id]
        return len(ids_to_delete)

    def search(self, query: str, limit: int = 5) -> list[StoredChunk]:
        return rank_chunks(query, list(self._chunks.values()), limit)

    def count(self) -> int:
        return len(self._chunks)


def stable_chunk_id(source_type: str, source: str, chunk_index: int, text: str) -> str:
    digest = sha256(f"{source_type}:{source}:{chunk_index}:{text}".encode("utf-8")).hexdigest()
    return str(UUID(hex=digest[:32]))


def _terms(value: str) -> set[str]:
    return {term.lower() for term in re.findall(r"[a-zA-Z0-9]+", value) if len(term) > 2}


def rank_chunks(query: str, chunks: list[StoredChunk], limit: int = 5) -> list[StoredChunk]:
    scored = score_chunks(query, chunks)
    return [chunk for _, chunk in scored[:limit]]


def score_chunks(query: str, chunks: list[StoredChunk]) -> list[tuple[float, StoredChunk]]:
    query_terms = _terms(query)
    if not query_terms:
        return []

    scored: list[tuple[float, StoredChunk]] = []
    for chunk in chunks:
        text_terms = _terms(f"{chunk.title} {chunk.text}")
        if not text_terms:
            continue
        overlap = query_terms.intersection(text_terms)
        score = len(overlap) / math.sqrt(len(text_terms))
        score += _source_intent_boost(query_terms, chunk)
        if score > 0:
            scored.append((score, chunk))

    scored.sort(key=lambda item: item[0], reverse=True)
    return scored


def _source_intent_boost(query_terms: set[str], chunk: StoredChunk) -> float:
    sec_terms = {"apple", "aapl", "filing", "revenue", "risk", "risks", "interest", "rates", "demand"}
    policy_terms = {"policy", "privacy", "pii", "compliance", "approved", "prohibited", "governance"}

    if chunk.source_type == "sec" and query_terms.intersection(sec_terms):
        return 3.0
    if chunk.source_type == "policy" and query_terms.intersection(policy_terms):
        return 1.2
    return 0.0


rag_store = InMemoryRagStore()
