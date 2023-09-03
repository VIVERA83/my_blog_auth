from typing import Any, Generator

from core.components import Application
from core.settings import PostgresSettings
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from store.database.postgres import Base

from tests.app.core.app import setup_app_test
from tests.auth_service.fixtures.data import *

settings = PostgresSettings()
settings.postgres_db = "test"


@pytest.fixture(autouse=True)
async def clear_db() -> Generator[Application, Any, None]:
    _db = Base
    _engine = create_async_engine(
        settings.dsn(True),
        echo=False,
        future=True,
    )
    session = AsyncSession(_engine, expire_on_commit=False)
    async with _engine.begin() as conn:
        await conn.run_sync(_db.metadata.drop_all)
        await conn.run_sync(_db.metadata.create_all)
    yield session
    async with _engine.begin() as conn:
        conn.run_sync(_db.metadata.drop_all)


@pytest.fixture(autouse=True)
def db():
    _db = Base
    _engine = create_async_engine(
        settings.dsn(True),
        echo=False,
        future=True,
    )
    session = AsyncSession(_engine, expire_on_commit=False)
    yield session
    _engine.sync_engine.dispose()


@pytest.fixture(scope="session")
def app() -> Generator[Application, Any, None]:
    """Create app."""
    _app = setup_app_test()
    yield _app


@pytest.fixture(scope="function")
def client(app: FastAPI) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    with TestClient(app) as client:
        yield client
