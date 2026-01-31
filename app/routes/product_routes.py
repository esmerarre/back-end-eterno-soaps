from fastapi import APIRouter, Depends, Query, status
from app.db import get_db
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.category import Category
from app.models.product_categories import association_table
from app.schemas.product_schema import ProductRead, ProductCreate, ProductCategoryAssign, ProductCategoryAssignResponse
from app.schemas.category_schema import CategoryRead, CategoryCreate
from .route_utilities import validate_model

router = APIRouter(tags=["Products"], prefix="/products")

@router.post("/", status_code=201, response_model=ProductRead)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(
        name=product.name,
        description=product.description,
        ingredients=product.ingredients,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/", response_model=list[ProductRead])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = validate_model(db, Product, product_id)
    return product

@router.put("/{product_id}", response_model=ProductRead)
def update_product(product_id: int, updated_product: ProductCreate, db: Session = Depends(get_db)):
    product = validate_model(db, Product, product_id)
    product.name = updated_product.name
    product.description = updated_product.description
    product.ingredients = updated_product.ingredients
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = validate_model(db, Product, product_id)
    db.delete(product)
    db.commit()
    return None

##Category routes for products ##

@router.post("/{product_id}/categories", response_model=ProductCategoryAssignResponse)
def post_product_category(product_id: int, category_data: ProductCategoryAssign, db: Session = Depends(get_db)):
    product = validate_model(db, Product, product_id)
    categories = db.query(Category).filter(Category.id.in_(category_data.category_ids)).all()
    for category in categories:
        product.categories.append(category) 
    db.commit()
    db.refresh(product)
    return {
            "product_id": product.id,
            "added_categories": [c.name for c in categories]
        }

@router.get("/{product_id}/categories", response_model=list[CategoryRead])
def get_product_categories(product_id: int, db: Session = Depends(get_db)):
    product = validate_model(db, Product, product_id)
    return product.categories  

@router.delete("/{product_id}/categories/{category_id}", response_model=ProductRead)
def delete_product_category(product_id: int, category_id: int, db: Session = Depends(get_db)):
    product = validate_model(db, Product, product_id)
    category = validate_model(db, Category, category_id) ## this will validate if category exists, but not if it's associated with product
    product.categories.remove(category)  
    db.commit()
    db.refresh(product)
    return product