from fastapi import APIRouter, Depends, Query, status
from app.db import get_db
from sqlalchemy.orm import Session
from ..models.product import Product, ProductSchema
from ..models.product_categories import Category
from .route_utilities import validate_model

router = APIRouter(tags=["Products"], prefix="/products/{product_id}/variants")

@router.get("/", response_model=list[ProductVariantSchema])
def create_variant(product_variant: ProductVariantSchema, db: Session = Depends(get_db)):
    new_variant = ProductVariant(
        product_id=product_id,)