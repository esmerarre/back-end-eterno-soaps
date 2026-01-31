from pydantic import BaseModel
from typing import List
from app.schemas.product_variant_schema import ProductVariantRead

class ProductBase(BaseModel):
    name: str
    description: str
    ingredients: List[str]
    category_id: int

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    variants: List[ProductVariantRead] = []

    class Config:
        from_attributes = True

class ProductCategoryAssign(BaseModel):
    category_ids: List[int]

class ProductCategoryAssignResponse(BaseModel):
    product_id: int
    added_categories: List[str]