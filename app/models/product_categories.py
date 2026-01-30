from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from .base import Base

association_table = Table(
    "product_categories",
    Base.metadata,
    Column("product_id", ForeignKey("products.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
)