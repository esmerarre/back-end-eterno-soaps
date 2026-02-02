from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from app.models.base import Base

class Admin(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
