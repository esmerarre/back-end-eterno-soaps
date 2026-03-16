from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from app.models.base import Base

class Admin(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    # Store only the password hash (never the raw password).
    # This is what gets checked at login.
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
