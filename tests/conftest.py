import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from app.main import app
from app.db import get_db
from app.models.base import Base
from app.models.product import Product
from app.models.product_categories import Category
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
def sample_product_data(db_session: Session):
    products: list[Product] = [
        Product(
            name="Eternas Caricias",
            # ingredients=["Cottonwood Leaves", "Clove", "Cinnamon", "Bay Leaves", "Rosemary"],
            price=10.0,
            description="A soothing blend of natural herbs for gentle cleansing.",
            stock=10
        ),
        Product(
            name="Eterno de Saffron",
            # ingredients=["Saffron", "Oats", "Tapioca", "Vitamin E", "Essential oils"],
            price=12.0,
            description="Luxurious saffron and oats soap for radiant skin.",
            stock=15
        ),
        Product(
            name="Serenidad Eterna",
            # ingredients=["Lavender", "Turmeric", "Aloe Vera", "Calendula"],
            price=11.0,
            description="Relaxing lavender and aloe blend for sensitive skin.",
            stock=4
        )
    ]

    db_session.add_all(products)
    db_session.commit()

@pytest.fixture(scope='function')
def sample_category_data(db_session: Session):
    categories: list[Category] = [
        Category(
            name="Essential Oils",
            description="Herbal infused soaps for natural care."
        ),
        Category(
            name="Mosturizing",
            description="Hydrating soaps for dry skin."
        ),
        Category(
            name="Sensitive",
            description="Gentle soaps for sensitive skin."
        ),
        Category(
            name="Exfoliating",
            description="Soaps with natural exfoliants for smooth skin."
        )
    ]

    db_session.add_all(categories)
    db_session.commit()
