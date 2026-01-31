from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, JSON
from .category import Category
from .product_categories import association_table
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .category import Category
    from .product_variant import ProductVariant

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str]
    ingredients: Mapped[list] = mapped_column(JSON)

    # Relationships
    categories: Mapped[list["Category"]] = relationship(secondary=association_table, back_populates="products")
    variants: Mapped[list["ProductVariant"]] = relationship(back_populates="product")
