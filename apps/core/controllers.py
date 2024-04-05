from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from conf.db import get_db_handler

from .services import BillsService

DbHandlerDep = Annotated[AsyncSession, Depends(get_db_handler().begin_session)]


class BillsController:
    @staticmethod
    async def get(db_handler: DbHandlerDep):
        svc = BillsService()
        return await svc.get_bills()

    @staticmethod
    async def post(db_handler: DbHandlerDep):
        svc = BillsService()
        return await svc.create_bill()
