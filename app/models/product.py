from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .base import Base
from typing import Optional
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from .product_categories import Category

class Product(Base):
    __tablename__ = "product"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("category.id"))
    category: Mapped[Optional["Category"]] = relationship(back_populates="products")