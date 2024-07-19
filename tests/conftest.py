from asyncio import get_event_loop_policy

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from pytest_asyncio import is_async_test
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.postgres_init import Base, get_session
from app.main import app


def pytest_collection_modifyitems(items):
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


engine = create_async_engine(settings.POSTGRES_TEST_URL)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine


async def get_test_session() -> AsyncSession:
    async with async_session() as session:
        yield session


app.dependency_overrides[get_session] = get_test_session


@pytest_asyncio.fixture(scope="session")
async def create_test_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
