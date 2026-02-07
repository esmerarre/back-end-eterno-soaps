from __future__ import annotations
from pydantic import BaseModel
from typing import List

class CategoryBase(BaseModel):
    name: str
    description: str

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int

    class Config:
        from_attributes = True

class CategoryWithProducts(CategoryBase):
    id: int
    products: List["ProductSummary"] = []

    class Config:
        from_attributes = True

## Resolve circular imports, do not move import to top ##
from app.schemas.product_schema import ProductSummary
CategoryWithProducts.model_rebuild()