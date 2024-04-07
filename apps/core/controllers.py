from conf.db import DbSessionDep

from .repositories import BillsRepository
from .schemas import BillSchemaInput, BillSchemaOutput
from .services import BillsService


class BillsController:
    @staticmethod
    async def get(
        db_session: DbSessionDep,
        reference: str | None = None,
        total_from: float | None = None,
        total_to: float | None = None,
    ) -> list[BillSchemaOutput]:
        svc = BillsService(BillsRepository(db_session))
        query_params = {
            "reference": reference,
            "total_from": total_from,
            "total_to": total_to,
        }
        return await svc.get_bills(query_params)

    @staticmethod
    async def post(db_session: DbSessionDep, data: BillSchemaInput) -> BillSchemaOutput:
        svc = BillsService(BillsRepository(db_session))
        return await svc.create_bill(data)
