from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.admin import Admin
from app.schemas.admin_schema import AdminCreate, AdminLogin, AdminOut, Token
from app.services.auth_service import (
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
)

router = APIRouter(prefix="/admins", tags=["admins"])
# Reads bearer token from Authorization header: "Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admins/login")


def get_current_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Admin:
    # 1) Decode and validate JWT.
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    # 2) Read admin identity from the subject claim.
    username: str | None = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    # 3) Ensure admin still exists in DB.
    admin = db.query(Admin).filter(Admin.username == username).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin not found",
        )
    return admin

@router.get("/", response_model=list[AdminOut])
def get_all_admins(
    db: Session = Depends(get_db),
    # This dependency protects the route.
    _: Admin = Depends(get_current_admin),
):
    return db.query(Admin).all()

@router.get("/{username}", response_model=AdminOut)
def get_admin(
    username: str,
    db: Session = Depends(get_db),
    # This dependency protects the route.
    _: Admin = Depends(get_current_admin),
):
    admin = db.query(Admin).filter(Admin.username == username).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin

@router.post("/login", response_model=Token)
def admin_login(admin: AdminLogin, db: Session = Depends(get_db)):
    # 1) Find admin by username.
    existing_admin = db.query(Admin).filter(Admin.username == admin.username).first()
    # 2) Verify plaintext password against stored hash.
    if not existing_admin or not verify_password(admin.password, existing_admin.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 3) Issue signed JWT with username in "sub" claim.
    access_token = create_access_token(data={"sub": existing_admin.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/", response_model=AdminOut)
def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    # Avoid duplicate usernames.
    existing_admin = db.query(Admin).filter(Admin.username == admin.username).first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash password before saving.
    new_admin = Admin(
        username=admin.username,
        hashed_password=get_password_hash(admin.password),
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin


