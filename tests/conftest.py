import pytest
from sqlalchemy import NullPool

from src.config import DB_HOST_TEST, DB_NAME_TEST, DB_PASSWORD_TEST, DB_PORT_TEST, DB_USER_TEST
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASSWORD_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"


engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool, echo=True, pool_pre_ping=True)
async_session = async_sessionmaker(engine_test, expire_on_commit=False)
metadata.bind = engine_test
