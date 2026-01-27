from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.product_categories import Category, 
from ..schemas.category_schema import CategoryCreate, CategoryRead
from .route_utilities import validate_model

router = APIRouter(tags=["Categories"], prefix="/categories")

@router.post("/", response_model=CategoryRead, status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    new_category = Category(
        name=category.name,
        description=category.description
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get("/", response_model=list[CategoryRead])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = validate_model(db, Category, category_id)
    return db.query(category).filter(Category.id==category_id).first() # .filter() returns query object, therefore need to use .first() to get the actual data

@router.put("/{category_id}/", response_model=CategoryRead)
def update_category(category_id: int, updated_category: CategoryRead, db: Session = Depends(get_db)):
    category = validate_model(db, Category, category_id)
    category.name = updated_category.name
    category.description = updated_category.description
    db.commit()
    db.refresh(category)
    return category

@router.delete("/{category_id}/", response_model=CategoryRead)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = validate_model(db, Category, category_id)
    db.delete(category)
    db.commit()
    return category