from __future__ import annotations
from pydantic import BaseModel, computed_field
from typing import List, Optional
from app.schemas.product_variant_schema import ProductVariantRead
from app.routes.route_utilities import generate_signed_url

class ProductBase(BaseModel):
    name: str
    description: str
    ingredients: List[str]
    img_key: Optional[str]

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    variants: List[ProductVariantRead] = []
    categories: List[CategoryRead] = []

    @computed_field
    @property
    def image_url(self) -> Optional[str]:
        """Generate signed URL from S3 key"""
        if self.img_key:
            return generate_signed_url(self.img_key)
        return None

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