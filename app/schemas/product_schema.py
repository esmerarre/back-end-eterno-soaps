from __future__ import annotations
from pydantic import BaseModel
from typing import List
from app.schemas.product_variant_schema import ProductVariantRead

class ProductBase(BaseModel):
    name: str
    description: str
    ingredients: List[str]

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    variants: List[ProductVariantRead] = []
    categories: List[CategoryRead] = []

    class Config:
        from_attributes = True

class ProductCategoryAssign(BaseModel):
    category_ids: List[int]

class ProductCategoryAssignResponse(BaseModel):
    product_id: int
    added_categories: List[str]

class ProductSummary(BaseModel):  # No category reference
    id: int
    name: str
    description: str
    ingredients: List[str]
    variants: List[ProductVariantRead] = []

    class Config:
        from_attributes = True


## Resolve circular imports, do not move import to top ##
from app.schemas.category_schema import CategoryRead
ProductRead.model_rebuild()