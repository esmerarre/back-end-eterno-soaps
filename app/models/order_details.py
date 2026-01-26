from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Float, DateTime
from .base import Base
from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .product import Product
    from .order import Order

class OrderDetails(Base):
    __tablename__ = "order_details"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    price: Mapped[float]
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    quantity: Mapped[int]

    # Relationships
    order: Mapped["Order"] = relationship(back_populates="details")
    product: Mapped["Product"] = relationship()
