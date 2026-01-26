from fastapi import APIRouter, Depends, Query, status
from app.db import get_db
from sqlalchemy.orm import Session
from ..models.product import Product, ProductSchema
from ..models.product_categories import Category
from .route_utilities import validate_model

router = APIRouter(tags=["Products"], prefix="/products")

@router.post("/", status_code=201, response_model=ProductSchema)
def create_product(product: ProductSchema, db: Session = Depends(get_db)):
    new_product = Product(
        name=product.name,
        description=product.description,
        ingredients=product.ingredients,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/", response_model=list[ProductSchema])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.get("/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.id==product_id).first() # .filter() returns query object, therefore need to use .first() to get the actual data

@router.put("/{product_id}", response_model=ProductSchema)
def update_product(product_id: int, updated_product: ProductSchema, db: Session = Depends(get_db)):
    # product = validate_model(db, Product, product_id)
    product.name = updated_product.name
    product.description = updated_product.description
    product.ingredients = updated_product.ingredients
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}", response_model=ProductSchema)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    # product = validate_model(db, Product, product_id)
    db.delete(product)
    db.commit()
    return product

