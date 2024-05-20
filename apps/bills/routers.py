from fastapi import APIRouter

from .controllers import BillsController

app_name = "bills"
router_v1 = APIRouter(tags=["Bills"])


router_v1.add_api_route(
    path="/bills",
    endpoint=BillsController.get,
    methods=["GET"],
    status_code=200,
    name=f"{app_name}:list",
    summary="Fetches a bill resource",
)

router_v1.add_api_route(
    path="/bills",
    endpoint=BillsController.post,
    methods=["POST"],
    status_code=201,
    name=f"{app_name}:create",
    summary="Creates a new bill resource",
)
