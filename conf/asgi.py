from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db import get_db_handler
from .middleware import (
    allowed_hosts_middleware_configuration,
    cors_middleware_configuration,
)
from .routers import routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    await (conn := get_db_handler()).connect(echo_sql=True)
    yield
    await conn.disconnect()


def get_asgi_application():
    app = FastAPI(lifespan=lifespan)

    app.add_middleware(**allowed_hosts_middleware_configuration)
    app.add_middleware(**cors_middleware_configuration)

    [app.include_router(router=router, prefix="/api") for router in routers]

    return app


application = get_asgi_application()
