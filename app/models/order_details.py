from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime
from datetime import datetime
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .order import Order
    from .product_variant import ProductVariant

class OrderDetails(Base):
    __tablename__ = "order_details"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_variant_id: Mapped[int] = mapped_column(ForeignKey("product_variants.id"))

    quantity: Mapped[int]
    price: Mapped[float]  # snapshot at time of purchase
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    order: Mapped["Order"] = relationship(back_populates="details")
    product_variant: Mapped["ProductVariant"] = relationship()
