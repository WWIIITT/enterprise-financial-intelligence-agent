from dataclasses import dataclass


@dataclass(frozen=True)
class TextChunk:
    text: str
    chunk_index: int


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 120) -> list[TextChunk]:
    normalized = " ".join(text.split())
    if not normalized:
        return []

    chunks: list[TextChunk] = []
    start = 0
    index = 0

    while start < len(normalized):
        end = min(start + chunk_size, len(normalized))
        chunks.append(TextChunk(text=normalized[start:end], chunk_index=index))
        if end == len(normalized):
            break
        start = max(0, end - overlap)
        index += 1

    return chunks
