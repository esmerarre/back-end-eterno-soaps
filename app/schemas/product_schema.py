from pydantic import BaseModel
from typing import List
from app.schemas.product_variant import ProductVariantRead



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
