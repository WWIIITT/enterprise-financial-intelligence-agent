from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings
from app.core.network import can_open_tcp_connection


class Base(DeclarativeBase):
    pass


@lru_cache
def get_engine() -> Engine | None:
    if not settings.database_url:
        return None
    connect_args = {"connect_timeout": 1} if settings.database_url.startswith("postgresql") else {}
    return create_engine(settings.database_url, pool_pre_ping=True, connect_args=connect_args)


@lru_cache
def get_session_factory() -> sessionmaker | None:
    engine = get_engine()
    if engine is None:
        return None
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)


def initialize_database() -> bool:
    if not settings.database_url or not can_open_tcp_connection(settings.database_url):
        return False

    engine = get_engine()
    if engine is None:
        return False

    try:
        Base.metadata.create_all(engine)
    except Exception:
        return False

    return True
