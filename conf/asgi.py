from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db import get_db_handler
from .middleware import (
    allowed_hosts_middleware_configuration,
    cors_middleware_configuration,
)
from .routers import app_v1, app_v2
from .settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await (conn := get_db_handler()).connect()
    yield
    await conn.disconnect()


def get_asgi_application():
    application = FastAPI(
        title=Settings.APP_NAME,
        description=Settings.APP_DESCRIPTION,
        version=Settings.APP_VERSION,
        debug=Settings.DEBUG,
        docs_url=Settings.DOCS_URL,
        openapi_url=Settings.OPENAPI_URL,
        redoc_url=Settings.REDOC_URL,
        root_path=Settings.API_PREFIX,
        lifespan=lifespan,
    )

    application.add_middleware(**allowed_hosts_middleware_configuration)
    application.add_middleware(**cors_middleware_configuration)

    application.mount(path="/v1", app=app_v1, name="v1")
    application.mount(path="/v2", app=app_v2, name="v2")

    return application


app = get_asgi_application()
