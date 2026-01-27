from pydantic import BaseModel


class OrderDetailsBase(BaseModel):
    product_variant_id: int
    quantity: int
    price: float


class OrderDetailsCreate(OrderDetailsBase):
    pass


class OrderDetailsRead(OrderDetailsBase):
    id: int

    class Config:
        from_attributes = True
