from typing import TYPE_CHECKING
from unittest.mock import patch

from httpx import ASGITransport, AsyncClient
from pytest import fixture
from uvloop import EventLoopPolicy

from conf.asgi import get_asgi_application
from conf.db import get_db_handler, get_metadata
from shared.models import TimeStampedBaseModel

if TYPE_CHECKING:
    from fastapi import FastAPI
    from sqlalchemy.ext.asyncio import AsyncSession

    from shared.connection_handler import _DBConnectionHandler


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
async def db_session(db_conn: "_DBConnectionHandler"):
    async with db_conn.begin_session() as ses:
        with patch.object(target=ses, attribute="commit", new=ses.flush):
            try:
                yield ses
            finally:
                await ses.rollback()


@fixture
async def client(asgi_app: "FastAPI", db_session: "AsyncSession"):
    transport, dependency = ASGITransport(app=asgi_app), get_db_handler().get_session
    asgi_app.dependency_overrides[dependency] = lambda: db_session
    async with AsyncClient(base_url="http://test", transport=transport) as client:
        yield client
    asgi_app.dependency_overrides[dependency] = dependency
