from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.category import Category
from app.schemas.category_schema import CategoryRead, CategoryCreate, CategoryWithProducts
from .route_utilities import validate_model
from typing import List

router = APIRouter(tags=["Categories"], prefix="/categories")

@router.post("/", response_model=List[CategoryRead], status_code=201)
def create_category(categories: list[CategoryCreate], db: Session = Depends(get_db)):
    db_new_categories = [Category(**category.model_dump()) for category in categories]
    db.add_all(db_new_categories)
    db.commit()
    return db_new_categories

@router.get("/", response_model=list[CategoryRead])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.get("/{category_id}", response_model=CategoryWithProducts)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = validate_model(db, Category, category_id)
    return category

@router.put("/{category_id}", response_model=CategoryRead)
def update_category(category_id: int, updated_category: CategoryCreate, db: Session = Depends(get_db)):
    category = validate_model(db, Category, category_id)
    category.name = updated_category.name
    category.description = updated_category.description
    db.commit()
    db.refresh(category)
    return category

@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = validate_model(db, Category, category_id)
    db.delete(category)
    db.commit()
    return None