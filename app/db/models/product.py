from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text

from app.db.models.base import Base, IDBaseModel


class Product(Base, IDBaseModel):
    category_id: Mapped[int] = mapped_column(
        ForeignKey(column="category.id", ondelete="CASCADE")
    )

    title: Mapped[str] = mapped_column(unique=True)
    quantity: Mapped[int] = mapped_column(default=1)
    cost: Mapped[int]
    info: Mapped[Optional[str]] = mapped_column(Text)
    image_id: Mapped[Optional[str]]

    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="products",
        lazy="joined",
    )

    carts: Mapped[List["CartProduct"]] = relationship(
        "CartProduct",
        back_populates="product",
    )
