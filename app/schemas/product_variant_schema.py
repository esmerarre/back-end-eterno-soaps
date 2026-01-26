from pydantic import BaseModel
from typing import Optional

class ProductVariantSchema(BaseModel):
    id: int
    product_id: int
    size: str
    shape: Optional[str]
    price: float
    stock_quantity: int

    class Config:
        from_attributes = True
