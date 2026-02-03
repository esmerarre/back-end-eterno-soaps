from pydantic import BaseModel, computed_field
from typing import Optional
from app.routes.route_utilities import generate_signed_url


class ProductVariantBase(BaseModel):
    size: str
    shape: Optional[str]
    img_key: Optional[str]
    price: float
    stock_quantity: int


class ProductVariantCreate(ProductVariantBase):
    pass


class ProductVariantRead(ProductVariantBase):
    id: int
    product_id: int

    @computed_field
    @property
    def image_url(self) -> Optional[str]:
        """Generate signed URL from S3 key"""
        if self.img_key:
            return generate_signed_url(self.img_key)
        return None

    class Config:
        from_attributes = True