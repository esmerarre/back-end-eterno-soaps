from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.product import Product


def test_assign_categories_to_product(client: TestClient, db_session: Session, sample_category_data, sample_product_data):
    response = client.post("/products/1/categories", json={
        "category_ids": [1, 2]
    })
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["product_id"] == 1
    assert set(response_body["added_categories"]) == {"Body", "Face"}

    query = select(Product).where(Product.id == 1)
    product = db_session.scalars(query).first()

    assert product
    assert {category.name for category in product.categories} == {"Body", "Face"}


def test_get_product_categories(client: TestClient, db_session: Session, sample_category_data, sample_product_data):
    client.post("/products/1/categories", json={
        "category_ids": [1, 2]
    })

    response = client.get("/products/1/categories")
    response_body = response.json()

    assert response.status_code == 200
    assert len(response_body) == 2
    assert {category["name"] for category in response_body} == {"Body", "Face"}


def test_delete_product_category(client: TestClient, db_session: Session, sample_category_data, sample_product_data):
    client.post("/products/1/categories", json={
        "category_ids": [1, 2]
    })

    response = client.delete("/products/1/categories/1")
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["id"] == 1
    assert {category["name"] for category in response_body["categories"]} == {"Face"}


def test_assign_categories_product_not_found(client: TestClient, db_session: Session, sample_category_data):
    response = client.post("/products/999/categories", json={
        "category_ids": [1]
    })
    response_body = response.json()

    assert response.status_code == 404
    assert response_body == {
        "detail": "Product 999 not found"
    }

