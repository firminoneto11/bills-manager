from dataclasses import dataclass
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from .models import Bills, SubBills

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class BillsRepository:
    db_session: "AsyncSession"

    async def create(self, instance: Bills):
        self.db_session.add(instance)
        await self.db_session.commit()
        return instance

    async def fetch_all(self, params: dict):
        stmt = select(Bills).options(joinedload(Bills.sub_bills))

        if ref := params.get("reference"):
            stmt = stmt.where(SubBills.reference.ilike(ref))

        if total_from := params.get("total_from"):
            stmt = stmt.where(Bills.total == total_from)

        if total_to := params.get("total_to"):
            stmt = stmt.where(SubBills.amount == total_to)

        return (await self.db_session.scalars(stmt)).unique().all()
