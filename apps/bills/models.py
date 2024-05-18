from decimal import Decimal
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.models import TimeStampedBaseModel


class Bills(TimeStampedBaseModel):
    __tablename__ = "bills"

    total: Mapped["Decimal"] = mapped_column(sa.Numeric(precision=10, scale=2))
    sub_bills: Mapped[list["SubBills"]] = relationship(
        back_populates="bill", order_by="SubBills.id"
    )


class SubBills(TimeStampedBaseModel):
    __tablename__ = "sub_bills"

    amount: Mapped["Decimal"] = mapped_column(sa.Numeric(precision=10, scale=2))
    reference: Mapped[Optional[str]] = mapped_column(sa.String(100), unique=True)

    bill_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("bills.id", ondelete="CASCADE")
    )
    bill: Mapped[Bills] = relationship(back_populates="sub_bills")
