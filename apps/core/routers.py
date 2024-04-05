from fastapi import APIRouter

from .controllers import BillsController

app_name, resource_name = "core", "bills"
router = APIRouter(prefix="/v1", tags=["Core"])


router.add_api_route(
    path="/bills",
    endpoint=BillsController.get,
    methods=["GET"],
    status_code=200,
    name=f"{app_name}:{resource_name}:list",
)

router.add_api_route(
    path="/bills",
    endpoint=BillsController.post,
    methods=["POST"],
    status_code=201,
    name=f"{app_name}:{resource_name}:create",
)
