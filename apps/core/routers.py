from fastapi import APIRouter

from .controllers import HealthCheckController

app_name = "core"
router_v1 = APIRouter(tags=["Core"])


router_v1.add_api_route(
    path="/health-check",
    endpoint=HealthCheckController.get,
    methods=["GET"],
    status_code=200,
    name=f"{app_name}:get",
    summary="An health check endpoint",
)
