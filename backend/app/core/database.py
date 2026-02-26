from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import get_settings


class Base(DeclarativeBase):
    pass


def get_engine(database_url: str | None = None):
    settings = get_settings()
    url = database_url or settings.database_url
    connect_args = {}
    if url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
    return create_async_engine(url, echo=False, connect_args=connect_args)


def get_session_factory(engine):
    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


_engine = None
_session_factory = None


def _get_default_engine():
    global _engine
    if _engine is None:
        _engine = get_engine()
    return _engine


def _get_default_session_factory():
    global _session_factory
    if _session_factory is None:
        _session_factory = get_session_factory(_get_default_engine())
    return _session_factory


async def get_db() -> AsyncSession:
    factory = _get_default_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
