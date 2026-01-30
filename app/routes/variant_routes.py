from fastapi import APIRouter, Depends, Query, status
from app.db import get_db
from sqlalchemy.orm import Session
from ..models.product import Product
from app.models.product_variant import ProductVariant  
from app.schemas.product_variant_schema import ProductVariantRead, ProductVariantCreate
from .route_utilities import validate_model

router = APIRouter(tags=["Products"], prefix="/products/{product_id}/variants")

@router.post("/", status_code=201, response_model=ProductVariantRead)
def create_variant(product_id: int, product_variant: ProductVariantCreate, db: Session = Depends(get_db)):
    validate_model(db, Product, product_id)
    new_variant = ProductVariant(
        product_id= product_id,
        size=product_variant.size,
        shape=product_variant.shape,
        image_url = product_variant.img_url,
        price=product_variant.price,
        stock_quantity=product_variant.stock_quantity
    )
    db.add(new_variant)
    db.commit()
    db.refresh(new_variant)
    return new_variant

@router.get("/", response_model=list[ProductVariantRead])
def get_variants(product_id: int, db: Session = Depends(get_db)):
    return db.query(ProductVariant).filter(ProductVariant.product_id == product_id).all()

@router.get("/{variant_id}", response_model=ProductVariantRead)
def get_variant(product_id: int, variant_id: int, db: Session = Depends(get_db)):
    validate_model(db, Product, product_id)
    variant = validate_model(db, ProductVariant, variant_id)
    return variant

@router.put("/{variant_id}", response_model=ProductVariantRead)
def update_variant(product_id: int, variant_id: int, updated_variant: ProductVariantCreate, db: Session = Depends(get_db)):
    validate_model(db, Product, product_id)
    variant = validate_model(db, ProductVariant, variant_id)
    variant.size = updated_variant.size
    variant.shape = updated_variant.shape
    variant.img_url = updated_variant.img_url
    variant.price = updated_variant.price
    variant.stock_quantity = updated_variant.stock_quantity
    db.commit()
    db.refresh(variant)
    return variant

@router.delete("/{variant_id}", status_code=204)
def delete_variant(product_id: int, variant_id: int, db: Session = Depends(get_db)):
    validate_model(db, Product, product_id)
    variant = validate_model(db, ProductVariant, variant_id)
    db.delete(variant)
    db.commit()
    return None