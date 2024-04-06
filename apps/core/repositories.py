from dataclasses import dataclass
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from .models import Bills

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class BillsRepository:
    db_session: "AsyncSession"

    async def create(self, instance: Bills):
        self.db_session.add(instance)
        await self.db_session.commit()
        return instance

    async def fetch_all(self):
        result = await self.db_session.scalars(
            select(Bills).options(joinedload(Bills.sub_bills))
        )
        return result.unique().all()
