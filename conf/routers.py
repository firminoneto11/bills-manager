from fastapi import APIRouter

from apps.bills.routers import router_v1 as bills_router_v1
from apps.core.routers import router_v1 as core_router_v1

router_v1 = APIRouter(prefix="/v1")

router_v1.include_router(core_router_v1)
router_v1.include_router(bills_router_v1)
