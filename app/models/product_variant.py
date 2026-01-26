from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .product import Product

class ProductVariant(Base):
    __tablename__ = "product_variants"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    size: Mapped[str] = mapped_column(index=True) 
    shape: Mapped[str | None] = mapped_column(String, nullable=True)
    price: Mapped[float]
    stock_quantity: Mapped[int]

    product: Mapped["Product"] = relationship(back_populates="variants")


