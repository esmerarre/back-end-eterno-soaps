from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db

from app.models.product_categories import Category, CategorySchema

router = APIRouter(tags=["Categories"], prefix="/categories")

@router.get("/", response_model=list[CategorySchema])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()