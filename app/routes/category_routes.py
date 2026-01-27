from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.category import Category
from app.schemas.category_schema import CategoryRead, CategoryCreate, CategoryBase




router = APIRouter(tags=["Categories"], prefix="/categories")

@router.get("/", response_model=list[CategoryRead])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()