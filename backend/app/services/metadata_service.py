from app.core.database import get_session_factory, initialize_database
from app.models import DocumentChunkRecord, DocumentRecord, RequestLogRecord
from app.rag.store import StoredChunk


def record_ingested_chunks(source_type: str, source: str, title: str, chunks: list[StoredChunk]) -> bool:
    if not initialize_database():
        return False

    session_factory = get_session_factory()
    if session_factory is None:
        return False

    try:
        with session_factory() as session:
            document = DocumentRecord(source_type=source_type, source=source, title=title)
            session.add(document)
            session.flush()
            for index, chunk in enumerate(chunks):
                session.add(
                    DocumentChunkRecord(
                        document_id=document.id,
                        chunk_id=chunk.id,
                        chunk_index=index,
                        citation=chunk.citation,
                        text=chunk.text,
                    )
                )
            session.commit()
    except Exception:
        return False

    return True


def record_request_log(
    message: str,
    selected_agent: str,
    sources_count: int,
    latency_ms: int,
    estimated_cost_usd: float = 0,
) -> bool:
    if not initialize_database():
        return False

    session_factory = get_session_factory()
    if session_factory is None:
        return False

    try:
        with session_factory() as session:
            session.add(
                RequestLogRecord(
                    message=message,
                    selected_agent=selected_agent,
                    sources_count=sources_count,
                    latency_ms=latency_ms,
                    estimated_cost_usd=estimated_cost_usd,
                )
            )
            session.commit()
    except Exception:
        return False

    return True
