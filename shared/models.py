from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from .utils import generate_uuid, utcnow


class TimeStampedBaseModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
        primary_key=True,
        autoincrement=True,
        sort_order=-2,
    )

    uuid: Mapped[str] = mapped_column(
        sa.String(36), unique=True, default=generate_uuid, sort_order=-1
    )

    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), default=utcnow, sort_order=9998
    )

    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), default=utcnow, onupdate=utcnow, sort_order=9999
    )
