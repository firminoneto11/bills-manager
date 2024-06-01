from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from sqlalchemy import select
from sqlalchemy.orm import contains_eager

from .models import Bills, SubBills

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    class QueryParams(TypedDict):
        reference: str | None
        total_from: float | None
        total_to: float | None


@dataclass
class BillsRepository:
    db_session: "AsyncSession"

    async def create(self, instance: Bills):
        self.db_session.add(instance)
        await self.db_session.commit()
        return instance

    async def fetch_all(self, params: "QueryParams"):
        stmt = (
            select(Bills)
            .join(Bills.sub_bills)
            .options(contains_eager(Bills.sub_bills))
            .order_by(Bills.id)
        )

        if total_from := params.get("total_from"):
            stmt = stmt.filter(Bills.total == total_from)

        if ref := params.get("reference"):
            stmt = stmt.filter(SubBills.reference.ilike(f"%{ref}%"))

        if total_to := params.get("total_to"):
            stmt = stmt.filter(SubBills.amount == total_to)

        return (await self.db_session.scalars(stmt)).unique().all()
