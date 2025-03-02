from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey

from app.db.models.base import Base


class CartProduct(Base):
    __tablename__ = "cart_product"

    cart_id: Mapped[int] = mapped_column(
        ForeignKey(column="cart.id", ondelete="CASCADE"),
        primary_key=True,
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey(column="product.id", ondelete="CASCADE"),
        primary_key=True,
    )

    quantity: Mapped[int] = mapped_column(default=1)

    cart: Mapped["Cart"] = relationship(
        "Cart",
        back_populates="products",
    )
    product: Mapped["Product"] = relationship(
        "Product",
        lazy="joined",
    )
