from typing import TYPE_CHECKING
from unittest.mock import patch

from httpx import ASGITransport, AsyncClient
from pytest import fixture
from uvloop import EventLoopPolicy

from conf import Settings
from conf.asgi import get_asgi_application
from conf.db import get_db_handler, get_metadata, get_session
from shared.models import TimeStampedBaseModel

if TYPE_CHECKING:
    from fastapi import FastAPI
    from sqlalchemy.ext.asyncio import AsyncSession

    from shared.connection_handler import DBConnectionHandler


@fixture(scope="session", autouse=True)
def asgi_app():
    return get_asgi_application()


@fixture(scope="session", autouse=True)
async def db_conn():
    get_metadata()

    await (conn := get_db_handler()).connect()
    await conn.migrate(TimeStampedBaseModel, True)

    yield conn

    await conn.disconnect()


@fixture(scope="session")
def event_loop_policy():
    return EventLoopPolicy()


@fixture
async def db_session(db_conn: "DBConnectionHandler"):
    async with db_conn.begin_session() as ses:
        with patch.object(target=ses, attribute="commit", new=ses.flush):
            try:
                yield ses
            finally:
                await ses.rollback()


@fixture
async def client(asgi_app: "FastAPI", db_session: "AsyncSession"):
    transport = ASGITransport(app=asgi_app)
    asgi_app.dependency_overrides[get_session] = lambda: db_session
    base_url = f"http://test{Settings.API_PREFIX}"
    async with AsyncClient(base_url=base_url, transport=transport) as client:
        yield client
    asgi_app.dependency_overrides[get_session] = get_session
