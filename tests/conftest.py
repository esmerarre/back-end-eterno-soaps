import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from app.main import app
from app.db import get_db
from app.models.base import Base
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