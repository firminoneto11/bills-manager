from dataclasses import dataclass

from fastapi import FastAPI

from apps.bills.routers import router as bills_router
from apps.core.routers import router as core_router
from conf import Settings


@dataclass
class ApplicationMount:
    path: str
    app: FastAPI
    name: str


def get_routers():
    # V1 Routes
    _app_v1 = FastAPI(**Settings.get_asgi_settings())

    _app_v1.include_router(core_router)
    _app_v1.include_router(bills_router)

    # V2 Routes
    _app_v2 = FastAPI(**Settings.get_asgi_settings())

    _app_v2.include_router(core_router)

    # Returning routers
    return [
        ApplicationMount(path=f"{Settings.API_PREFIX}/v1", app=_app_v1, name="v1"),
        ApplicationMount(path=f"{Settings.API_PREFIX}/v2", app=_app_v2, name="v2"),
    ]
