from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from conf.db import get_db_handler

from .repositories import BillsRepository
from .schemas import BillSchemaInput, BillSchemaOutput
from .services import BillsService

DbSessionDep = Annotated[AsyncSession, Depends(get_db_handler().get_session)]


class BillsController:
    @staticmethod
    async def get(db_session: DbSessionDep) -> list[BillSchemaOutput]:
        svc = BillsService(BillsRepository(db_session))
        return await svc.get_bills()

    @staticmethod
    async def post(db_session: DbSessionDep, data: BillSchemaInput) -> BillSchemaOutput:
        svc = BillsService(BillsRepository(db_session))
        return await svc.create_bill(data)
