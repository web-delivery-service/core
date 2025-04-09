from typing import List
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey

from app.db.models.base import Base, IDBaseModel


class Cart(Base, IDBaseModel):
    user_id: Mapped[int] = mapped_column(
        ForeignKey(column="user.id", ondelete="CASCADE"), unique=True
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="cart",
        single_parent=True,
    )

    products: Mapped[List["CartProduct"]] = relationship(
        "CartProduct",
        back_populates="cart",
        cascade="all, delete-orphan",
        lazy="select",
    )
