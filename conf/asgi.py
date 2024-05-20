from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db import get_db_handler
from .middleware import (
    allowed_hosts_middleware_configuration,
    cors_middleware_configuration,
)
from .routers import router_v1
from .settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await (conn := get_db_handler()).connect()
    yield
    await conn.disconnect()


def get_asgi_application():
    app = FastAPI(
        title=Settings.APP_NAME,
        description=Settings.APP_DESCRIPTION,
        version=Settings.APP_VERSION,
        lifespan=lifespan,
        debug=Settings.DEBUG,
        docs_url=Settings.DOCS_URL,
        redoc_url=Settings.REDOC_URL,
        openapi_url=Settings.OPENAPI_URL,
    )

    app.add_middleware(**allowed_hosts_middleware_configuration)
    app.add_middleware(**cors_middleware_configuration)

    app.include_router(router_v1, prefix=Settings.API_PREFIX)

    return app


application = get_asgi_application()
