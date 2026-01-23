from __future__ import annotations
from typing import TYPE_CHECKING
from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
  from .product import Product

class Category(Base):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    products: Mapped[list["Product"]] = relationship(back_populates="category")

class CategorySchema(BaseModel):
    id: int
    name: str
    description: str

    class Config:
      from_attributes = True