import asyncio
from typing import AsyncGenerator
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import NullPool
from src.database import get_session
from src.models.models import metadata
from src.config import DB_HOST_TEST, DB_NAME_TEST, DB_PASSWORD_TEST, DB_PORT_TEST, DB_USER_TEST
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from src.main import app
from httpx import AsyncClient


DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASSWORD_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"


engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool, echo=True, pool_pre_ping=True)
async_session = async_sessionmaker(engine_test, expire_on_commit=False)
metadata.bind = engine_test

async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
