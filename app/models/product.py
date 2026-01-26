from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .product_categories import CategorySchema

if TYPE_CHECKING:
  from .product_categories import Category

class Product(Base):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    price: Mapped[float]
    description: Mapped[str]
    size: Mapped[str]
    ingredients: Mapped[list[str]]
    stock: Mapped[int]
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("category.id"))
    category: Mapped[Optional["Category"]] = relationship(back_populates="products")

class ProductSchema(BaseModel):
    id: int
    name: str
    price: float
    description: str
    size: str
    ingredients: list[str]
    stock: int
    category_id: Optional[int] = None
    category: Optional[CategorySchema] = None

    class Config:
      from_attributes = True