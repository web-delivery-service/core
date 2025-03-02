from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey

from app.db.models.base import Base


class OrderProduct(Base):
    __tablename__ = "order_product"

    order_id: Mapped[int] = mapped_column(
        ForeignKey(column="order.id", ondelete="CASCADE"),
        primary_key=True,
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey(column="product.id", ondelete="CASCADE"),
        primary_key=True,
    )

    quantity: Mapped[int] = mapped_column(default=1)

    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="products",
    )
    product: Mapped["Product"] = relationship(
        "Product",
        lazy="joined",
    )
