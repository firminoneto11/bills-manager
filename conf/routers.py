from fastapi import FastAPI

from apps.bills.routers import router as bills_router
from apps.core.routers import router as core_router
from conf import Settings

app_v1, app_v2 = (
    FastAPI(**Settings.get_asgi_settings()),
    FastAPI(**Settings.get_asgi_settings()),
)


app_v1.include_router(core_router)
app_v1.include_router(bills_router)

app_v2.include_router(core_router)
