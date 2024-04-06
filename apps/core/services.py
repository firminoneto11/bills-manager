from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from fastapi import HTTPException

from .models import Bills, SubBills

if TYPE_CHECKING:
    from .repositories import BillsRepository
    from .schemas import BillSchemaInput

    class QueryParams(TypedDict):
        reference: str | None
        total_from: float | None
        total_to: float | None


@dataclass
class BillsService:
    repository: "BillsRepository"

    async def get_bills(self, query_params: "QueryParams"):
        return await self.repository.fetch_all(params=query_params)

    async def create_bill(self, data: "BillSchemaInput"):
        sub_bills = [SubBills(**sb.model_dump()) for sb in data.sub_bills]
        bill = Bills(**data.model_dump(exclude="sub_bills"), sub_bills=sub_bills)

        if bill.total != sum(sb.amount for sb in sub_bills):
            raise HTTPException(
                status_code=400,
                detail="The bill's amount doesn't match the sum of its sub bills",
            )

        return await self.repository.create(instance=bill)
