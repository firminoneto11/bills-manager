from typing import Optional

from pydantic import BaseModel, ConfigDict


class SubBillSchemaInput(BaseModel):
    amount: float
    reference: Optional[str]


class BillSchemaInput(BaseModel):
    total: float
    sub_bills: list[SubBillSchemaInput]


class SubBillSchemaOutput(BaseModel):
    id: int
    amount: float
    reference: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class BillSchemaOutput(BaseModel):
    id: int
    total: float
    sub_bills: list[SubBillSchemaOutput]

    model_config = ConfigDict(from_attributes=True)
