from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Float, String, DateTime, ForeignKey
from .base import Base
from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .order_details import OrderDetails

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(index=True)
    amount: Mapped[float]
    shipping_address: Mapped[str]
    order_email: Mapped[str]
    order_date: Mapped[datetime] = mapped_column(default=datetime.utcnow, index=True)
    order_status: Mapped[str] = mapped_column(default="pending", index=True)

    details: Mapped[list["OrderDetails"]] = relationship(back_populates="order")
