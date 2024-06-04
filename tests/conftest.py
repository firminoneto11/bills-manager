from typing import TYPE_CHECKING
from unittest.mock import patch

from httpx import ASGITransport, AsyncClient
from pytest import fixture
from uvloop import EventLoopPolicy

from conf.asgi import get_asgi_application
from conf.db import get_database, get_metadata, get_session
from shared.models import TimeStampedBaseModel

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from shared.database import Database
    from shared.types import ASGIApp


@fixture(scope="session", autouse=True)
def asgi_app():
    return get_asgi_application()


@fixture(scope="session", autouse=True)
async def database():
    get_metadata()

    async with get_database() as db:
        await db.migrate(TimeStampedBaseModel, True)
        yield db


@fixture(scope="session")
def event_loop_policy():
    return EventLoopPolicy()


@fixture
async def db_session(database: "Database"):
    async with database.begin_session() as session:
        with patch.object(target=session, attribute="commit", new=session.flush):
            try:
                yield session
            finally:
                await session.rollback()


@fixture
async def httpx_client(asgi_app: "ASGIApp", db_session: "AsyncSession"):
    asgi_app.dependency_overrides[get_session] = lambda: db_session
    for mount in asgi_app.state._mounted_applications:
        mount.dependency_overrides[get_session] = lambda: db_session

    transport = ASGITransport(app=asgi_app)
    async with AsyncClient(base_url="http://test", transport=transport) as client:
        yield (client, asgi_app)

    asgi_app.dependency_overrides.clear()
    for mount in asgi_app.state._mounted_applications:
        mount.dependency_overrides.clear()
