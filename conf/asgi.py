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
    kwargs = Settings.get_asgi_settings()
    kwargs["docs_url"] = None
    kwargs["openapi_url"] = None
    kwargs["redoc_url"] = None

    application = FastAPI(**kwargs, lifespan=lifespan)

    application.add_middleware(**allowed_hosts_middleware_configuration)
    application.add_middleware(**cors_middleware_configuration)

    application.mount(path=f"{Settings.API_PREFIX}/v1", app=app_v1, name="v1")
    application.mount(path=f"{Settings.API_PREFIX}/v2", app=app_v2, name="v2")

    return application


app = get_asgi_application()
