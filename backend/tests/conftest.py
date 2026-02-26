"""
Test configuration — must mock geoalchemy2 BEFORE any app imports.
Uses SQLite in-memory database so PostGIS is NOT required.
"""
import sys
from unittest.mock import MagicMock
from sqlalchemy import String

# ── Mock geoalchemy2 before any app code imports it ──────────────────────────
mock_geo = MagicMock()
mock_geo.Geometry = lambda *args, **kwargs: String()
mock_geo.types = MagicMock()
mock_geo.types.Geometry = lambda *args, **kwargs: String()
mock_geo.shape = MagicMock()

sys.modules["geoalchemy2"] = mock_geo
sys.modules["geoalchemy2.types"] = mock_geo.types
sys.modules["geoalchemy2.shape"] = mock_geo.shape

# ── Now safe to import app modules ──────────────────────────────────────────
import pytest
import pytest_asyncio
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from httpx import AsyncClient, ASGITransport

from app.core.database import Base
from app.main import app as fastapi_app


TEST_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop_policy():
    return asyncio.DefaultEventLoopPolicy()


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest_asyncio.fixture(scope="function")
async def db_engine():
    engine = create_async_engine(TEST_DB_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine):
    factory = async_sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)
    async with factory() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def client(db_engine):
    """HTTP test client with overridden DB dependency."""
    from app.core.database import get_db
    factory = async_sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_db():
        async with factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    fastapi_app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    fastapi_app.dependency_overrides.clear()
