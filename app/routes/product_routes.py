from fastapi import APIRouter, Depends, Query, status
from app.db import get_db
from sqlalchemy.orm import Session

# Models = database tables
from app.models.product import Product
from app.models.product_variant import ProductVariant  

# Schemas = request/response models
from app.schemas.product_schema import ProductRead, ProductCreate, ProductBase
from app.schemas.product_variant_schema import ProductVariantRead, ProductVariantCreate, ProductVariantBase

from .route_utilities import validate_model


router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/")
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()  # query all products
    return products