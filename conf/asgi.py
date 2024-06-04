from contextlib import asynccontextmanager

from fastapi import FastAPI

from shared.types import ASGIApp

from .db import get_database
from .middleware import (
    allowed_hosts_middleware_configuration,
    cors_middleware_configuration,
)
from .routers import get_routers
from .settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with get_database():
        yield


def get_asgi_application() -> ASGIApp:
    kwargs = Settings.get_asgi_settings()
    kwargs["docs_url"] = None
    kwargs["openapi_url"] = None
    kwargs["redoc_url"] = None

    application = FastAPI(**kwargs, lifespan=lifespan)

    application.add_middleware(**allowed_hosts_middleware_configuration)
    application.add_middleware(**cors_middleware_configuration)

    # TODO: Check if the middleware is drilled down into the mounted apps

    application.state._mounted_applications = []
    for router in get_routers():
        application.mount(
            path=f"{Settings.API_PREFIX}/{router.version}",
            app=router.app,
            name=router.version,
        )
        application.state._mounted_applications.append(router.app)

    return application


app = get_asgi_application()
