from pydantic import BaseModel
from typing import Optional


class ProductVariantBase(BaseModel):
    size: str
    shape: Optional[str]
    img_url: Optional[str]
    price: float
    stock_quantity: int


class ProductVariantCreate(ProductVariantBase):
    product_id: int


class ProductVariantRead(ProductVariantBase):
    id: int
    product_id: int

    class Config:
        from_attributes = True
