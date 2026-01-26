from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.schemas.order_details import OrderDetailsRead


class OrderBase(BaseModel):
    shipping_address: str
    order_email: str


class OrderCreate(OrderBase):
    pass


class OrderRead(OrderBase):
    id: int
    order_status: str
    amount: float
    order_date: datetime
    details: List[OrderDetailsRead]

    class Config:
        from_attributes = True
