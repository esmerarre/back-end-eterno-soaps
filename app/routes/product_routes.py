from fastapi import APIRouter, Depends, Query, status
from app.db import get_db
from sqlalchemy.orm import Session
from ..models.product import Product, ProductSchema
from ..models.product_categories import Category
from .route_utilities import validate_model

router = APIRouter(tags=["Products"], prefix="/products")

@router.get("/", status_code=200, response_model=list[ProductSchema])
def get_products(db: Session = Depends(get_db) ):
    return db.query(Product).all()
