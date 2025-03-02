from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
import enum
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

from app.db.models.base import Base, IDBaseModel


class RoleEnum(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class User(Base, IDBaseModel):
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]

    role: Mapped[str] = mapped_column(
        PgEnum(RoleEnum, name="role_enum", create_type=False),
        default=RoleEnum.USER,
    )
    name: Mapped[Optional[str]]
    address: Mapped[Optional[str]]

    cart: Mapped["Cart"] = relationship(
        "Cart",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    orders: Mapped[List["Order"]] = relationship(
        "Order",
        back_populates="user",
    )
