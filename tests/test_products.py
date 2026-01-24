from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.product import Product
from sqlalchemy import select
import pytest

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


def test_get_all_products_no_products(client: TestClient):
    response = client.get("/products/")
    response_body = response.json()

    assert response.status_code == 200
    assert response_body == []


def test_get_all_products(client: TestClient, db_session: Session, sample_product_data):
    response = client.get("/products/")
    response_body = response.json()

    # Assert
    print(response_body)
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 1,
            "name": "Eternas Caricias",
            # ingredients=["Cottonwood Leaves", "Clove", "Cinnamon", "Bay Leaves", "Rosemary"],
            "price": 10.0,
            "description": "A soothing blend of natural herbs for gentle cleansing.",
            "stock": 10,
            "category_id": None, 
            "category": None
        },
        {
            "id": 2,
            "name": "Eterno de Saffron",
            # ingredients=["Saffron", "Oats", "Tapioca", "Vitamin E", "Essential oils"],
            "price": 12.0,
            "description": "Luxurious saffron and oats soap for radiant skin.",
            "stock": 15,
            "category_id": None, 
            "category": None
        },
        {
            "id": 3,
            "name": "Serenidad Eterna",
            # ingredients=["Lavender", "Turmeric", "Aloe Vera", "Calendula"],
            "price": 11.0,
            "description": "Relaxing lavender and aloe blend for sensitive skin.",
            "stock": 4,
            "category_id": None, 
            "category": None
        }
    ]



#@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_task(client: TestClient, db_session: Session):
    # Act
    response = client.post("/products", json={
            "name": "Eternas Caricias",
            # ingredients=["Cottonwood Leaves", "Clove", "Cinnamon", "Bay Leaves", "Rosemary"],
            "price": 10.0,
            "description": "A soothing blend of natural herbs for gentle cleansing.",
            "stock": 10
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
            "id": 1,
            "name": "Eternas Caricias",
            # ingredients=["Cottonwood Leaves", "Clove", "Cinnamon", "Bay Leaves", "Rosemary"],
            "price": 10.0,
            "description": "A soothing blend of natural herbs for gentle cleansing.",
            "stock": 10,
            "category_id": None,
            "category": None
    }
    
    query = select(Product).where(Product.id == 1)
    new_product = db_session.scalars(query)

    assert new_product
    assert new_product.name == "Eternas Caricias"
    assert new_product.description == "A soothing blend of natural herbs for gentle cleansing."

def test_get_product_by_id_not_found(client: TestClient, db_session: Session, sample_product_data):
    # Act
    response = client.get("/products/999")
    response_body = response.json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
        "detail": "Product 999 not found"
    }