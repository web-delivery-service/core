from typing import List
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.db.models.base import Base, IDBaseModel


class Category(Base, IDBaseModel):
    title: Mapped[str] = mapped_column(unique=True)

    products: Mapped[List["Product"]] = relationship(
        "Product",
        back_populates="category",
        cascade="all, delete-orphan",
        lazy="select",
    )
