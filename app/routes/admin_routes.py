from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.admin import Admin
from app.schemas.admin_schema import AdminCreate, AdminOut

router = APIRouter(prefix="/admins", tags=["admins"])

@router.post("/login", response_model=AdminOut)
def admin_login(admin: AdminCreate, db: Session = Depends(get_db)):
    # Very simple login for now: just check username exists
    existing_admin = db.query(Admin).filter(Admin.username == admin.username).first()
    if not existing_admin:
        raise HTTPException(status_code=401, detail="Admin not found")
    return existing_admin

@router.post("/", response_model=AdminOut)
def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    new_admin = Admin(username=admin.username)
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin
