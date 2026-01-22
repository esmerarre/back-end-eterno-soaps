from sqlalchemy.orm import Mapped, mapped_column, relationship
#from sqlalchemy import ForeignKey
from .base import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from .product import Product

class Category(Base):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    products: Mapped[list["Product"]] = relationship(back_populates="category")