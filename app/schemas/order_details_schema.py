from pydantic import BaseModel
from datetime import datetime

class OrderDetailsSchema(BaseModel):
    product_id: int
    price: float
    quantity: int
    date: datetime

    class Config:
        from_attributes = True
