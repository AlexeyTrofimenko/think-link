from collections.abc import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.database import get_session
from app.db.models import Base
from app.main import app


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    sync_url = "sqlite:///./tests/test.db"
    async_url = "sqlite+aiosqlite:///./tests/test.db"

    sync_engine = create_engine(sync_url, connect_args={"check_same_thread": False})
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)

    async_engine = create_async_engine(async_url, connect_args={"check_same_thread": False})
    async_session = async_sessionmaker(async_engine, expire_on_commit=False, autoflush=False)

    async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    try:
        with TestClient(app) as c:
            yield c
    finally:
        app.dependency_overrides.clear()
        sync_engine.dispose()
