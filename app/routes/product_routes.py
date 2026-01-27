from fastapi import APIRouter, Depends, Query, status
from app.db import get_db
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.category import Category
from app.schemas.product_schema import ProductRead, ProductCreate, ProductBase
from app.schemas.category_schema import CategoryRead, CategoryCreate, CategoryBase
from .route_utilities import validate_model

router = APIRouter(tags=["Products"], prefix="/products")

@router.post("/", status_code=201, response_model=ProductRead)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    validate_model(db, Category, product.category_id)
    new_product = Product(
        name=product.name,
        description=product.description,
        ingredients=product.ingredients,
        category_id=product.category_id,
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
    validate_model(db, Category, updated_product.category_id)
    product.name = updated_product.name
    product.description = updated_product.description
    product.ingredients = updated_product.ingredients
    product.category_id = updated_product.category_id
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

@router.post("/{product_id}/categories", response_model=ProductRead) ## check CategoryCreate, assuming that category create will be format of category data.
def post_product_category(product_id: int, category_data: CategoryCreate, db: Session = Depends(get_db)):
    product = validate_model(db, Product, product_id)
    category = validate_model(db, Category, category_data.category_id)
    product.categories.append(category) ## NEEDS REVIEW, pending updating to many-to-many relationship
    db.commit()
    db.refresh(product)
    return product

@router.get("/{product_id}/categories", response_model=list[CategoryRead])
def get_product_categories(product_id: int, db: Session = Depends(get_db)):
    product = validate_model(db, Product, product_id)
    return product.categories  ## NEEDS REVIEW, pending updating to many-to-many relationship

@router.delete("/{product_id}/categories/{category_id}", response_model=ProductRead)
def delete_product_category(product_id: int, category_id: int, db: Session = Depends(get_db)):
    product = validate_model(db, Product, product_id)
    category = validate_model(db, Category, category_id)
    product.categories.remove(category)  ## NEEDS REVIEW, pending updating to many-to-many relationship
    db.commit()
    db.refresh(product)
    return product

