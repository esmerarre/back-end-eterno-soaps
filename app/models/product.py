# product.py
from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, JSON
from .base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .category import Category
    from .product_variant import ProductVariant

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    ingredients: Mapped[list] = mapped_column(JSON)

    category: Mapped["Category"] = relationship(back_populates="products")
    variants: Mapped[list["ProductVariant"]] = relationship(back_populates="product")


from pydantic import BaseModel

class ProductSchema(BaseModel):
    id: int
    name: str
    description: str
    category_id: int
    ingredients: list[str] 

    class Config:
        from_attributes = True
