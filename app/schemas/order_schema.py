from pydantic import BaseModel
from datetime import datetime
from .order_details_schema import OrderDetailsSchema

class OrderSchema(BaseModel):
    id: int
    customer_id: int
    amount: float
    shipping_address: str
    order_email: str
    order_date: datetime
    order_status: str
    details: list[OrderDetailsSchema]

    class Config:
        from_attributes = True
