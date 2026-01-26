# category.py
from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .product import Product

class Category(Base):
    __tablename__ = "category"  # make consistent with Postgres table
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]

    products: Mapped[list["Product"]] = relationship(back_populates="category")


# Optional: Pydantic model for FastAPI
from pydantic import BaseModel

class CategorySchema(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True
