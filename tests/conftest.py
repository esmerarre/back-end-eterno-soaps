import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from main import app
from app.db import get_db
from app.models.base import Base
from app.models.product import Product
from app.models.category import Category
from app.models.product_variant import ProductVariant
import os

TEST_DATABASE_URI = os.getenv("SQLALCHEMY_TEST_DATABASE_URI")

# Safety check so you don’t nuke prod/dev by accident
assert "test" in TEST_DATABASE_URI.lower()

@pytest.fixture(scope="session")
def engine():
    """
    Create a SQLAlchemy engine connected to the local Postgres test database.
    Engine is shared across all tests.
    """
    engine = create_engine(TEST_DATABASE_URI)
    yield engine
    engine.dispose()

@pytest.fixture(scope="function")
def db_session(engine):
    """
    Creates a fresh database session per test.
    Tables are created before the test and dropped after.
    """

    # Create all tables
    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
    )

    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()

        # Clean up DB so tests are isolated
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session: Session):
    """
    FastAPI TestClient that uses the test database session
    instead of the real one. Needed for request validation, 
    checking HTTP status codes, etc.
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    # Override FastAPI dependency
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # Remove overrides after test
    app.dependency_overrides.clear()


## Sample data ##

@pytest.fixture(scope='function')
def sample_product_data(db_session: Session, sample_category_data):
    """Creates sample products that depend on categories being present"""
    products: list[Product] = [
        Product(
            name="Cottonwood",
            description="A soothing blend of natural herbs for gentle cleansing.",
            category_id=1,
            ingredients=["Cottonwood Leaves", "Clove", "Cinnamon", "Bay Leaves", "Rosemary"]
        ),
        Product(
            name="Saffron",
            description="Luxurious saffron and oats soap for radiant skin.",
            category_id=2,
            ingredients=["Saffron", "Oats", "Tapioca", "Vitamin E", "Essential oils"]
        ),
        Product(
            name="Aloe Vera",
            description="Relaxing lavender and aloe blend for sensitive skin.",
            category_id=2,
            ingredients=["Lavender", "Turmeric", "Aloe Vera", "Calendula"]
        )
    ]

    db_session.add_all(products)
    db_session.commit()

@pytest.fixture(scope='function')
def sample_category_data(db_session: Session):
    categories: list[Category] = [
        Category(
            name="Body",
            description="Body soaps"
        ),
        Category(
            name="Face",
            description="Facial soaps"
        ),
        Category(
            name="None",
            description="No specific category"
        )
    ]

    db_session.add_all(categories)
    db_session.commit()

@pytest.fixture(scope='function')
def sample_variant_data(db_session: Session, sample_product_data):
    
    variants: list[ProductVariant] = [
        ProductVariant(
            product_id=1,
            size="Small",
            shape="Round",
            img_url="https://example.com/images/cottonwood-small.jpg",
            price=8.99,
            stock_quantity=100
        ),
        ProductVariant(
            product_id=1,
            size="Large",
            shape="Round",
            img_url="https://example.com/images/cottonwood-large.jpg",
            price=12.99,
            stock_quantity=50
        ),
        ProductVariant(
            product_id=2,
            size="Medium",
            shape="Square",
            img_url="https://example.com/images/saffron-medium.jpg",
            price=10.99,
            stock_quantity=75
        )
    ]

    db_session.add_all(variants)
    db_session.commit()
