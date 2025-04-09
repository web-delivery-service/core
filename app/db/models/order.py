from typing import List
from sqlalchemy import ForeignKey
import enum
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.db.models.base import Base, IDBaseModel, TimeStampedCreateModel


class StatusEnum(enum.Enum):
    PROCESS = "PROCESS"
    ONTHEWAY = "ONTHEWAY"
    DELIVERED = "DELIVERED"


class Order(Base, IDBaseModel, TimeStampedCreateModel):
    user_id: Mapped[int] = mapped_column(
        ForeignKey(column="user.id", ondelete="CASCADE"),
    )

    status: Mapped[str] = mapped_column(
        PgEnum(StatusEnum, name="status_enum", create_type=False),
        default=StatusEnum.PROCESS,
    )
    cost: Mapped[int]

    user: Mapped["User"] = relationship(
        "User",
        back_populates="orders",
        lazy="joined",
    )

    products: Mapped[List["OrderProduct"]] = relationship(
        "OrderProduct",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="joined",
    )
