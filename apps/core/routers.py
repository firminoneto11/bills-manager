from fastapi import APIRouter

from .controllers import HealthCheckController

app_name = "core"
router = APIRouter(prefix="/v1", tags=["Core"])


router.add_api_route(
    path="/health-check",
    endpoint=HealthCheckController.get,
    methods=["GET"],
    status_code=200,
    name=f"{app_name}:get",
    summary="An health check endpoint",
)
