from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .product import Product

class Category(Base):
    __tablename__ = "categories"  # plural is conventional
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)  # filterable
    description: Mapped[str]

    # Relationship: one category → many products
    products: Mapped[list["Product"]] = relationship(back_populates="category")
