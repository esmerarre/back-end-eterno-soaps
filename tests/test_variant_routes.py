from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.product_variant import ProductVariant
from sqlalchemy import select

def test_create_variant(client: TestClient, db_session: Session, sample_product_data):
    # Act
    response = client.post("/products/1/variants", json={
        "product_id": 1,
        "size": "Extra Large",
        "shape": "Oval",
        "img_url": "https://example.com/images/cottonwood-xl.jpg",
        "price": 15.99,
        "stock_quantity": 25
    })
    response_body = response.json()

    # Assert
    assert response.status_code == 201
    assert response_body["id"] == 1
    assert response_body["product_id"] == 1
    assert response_body["size"] == "Extra Large"
    assert response_body["shape"] == "Oval"
    assert response_body["img_url"] == "https://example.com/images/cottonwood-xl.jpg"
    assert response_body["price"] == 15.99
    assert response_body["stock_quantity"] == 25
    
    query = select(ProductVariant).where(ProductVariant.id == 1)
    new_variant = db_session.scalars(query).first()

    assert new_variant
    assert new_variant.product_id == 1
    assert new_variant.size == "Extra Large"
    assert new_variant.img_url == "https://example.com/images/cottonwood-xl.jpg"
    assert new_variant.price == 15.99

def test_create_variant_invalid_product(client: TestClient, db_session: Session, sample_product_data):
    # Act
    response = client.post("/products/999/variants", json={
        "product_id": 999,
        "size": "Large",
        "shape": "Round",
        "img_url": "https://example.com/images/invalid.jpg",
        "price": 12.99,
        "stock_quantity": 50
    })
    response_body = response.json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
        "detail": "Product 999 not found"
    }

def test_get_all_variants_no_variants(client: TestClient, db_session: Session, sample_product_data):
    response = client.get("/products/1/variants/")
    response_body = response.json()

    assert response.status_code == 200
    assert response_body == []


def test_get_all_variants(client: TestClient, db_session: Session, sample_variant_data):
    response = client.get("/products/1/variants/")
    response_body = response.json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    
    # Check first variant
    assert response_body[0]["product_id"] == 1
    assert response_body[0]["size"] == "Small"
    assert response_body[0]["img_url"] == "https://example.com/images/cottonwood-small.jpg"
    assert response_body[0]["price"] == 8.99
    
    # Check second variant
    assert response_body[1]["product_id"] == 1
    assert response_body[1]["size"] == "Large"
    assert response_body[1]["img_url"] == "https://example.com/images/cottonwood-large.jpg"
    assert response_body[1]["price"] == 12.99

def test_get_variant_by_id_not_found(client: TestClient, db_session: Session, sample_variant_data):
    # Act
    response = client.get("/products/1/variants/999")
    response_body = response.json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
        "detail": "ProductVariant 999 not found"
    }

def test_get_variant_by_id_found(client: TestClient, db_session: Session, sample_variant_data):
    # Act
    response = client.get("/products/1/variants/1")
    response_body = response.json()

    # Assert
    assert response.status_code == 200
    assert response_body["id"] == 1
    assert response_body["product_id"] == 1
    assert response_body["size"] == "Small"
    assert response_body["shape"] == "Round"
    assert response_body["img_url"] == "https://example.com/images/cottonwood-small.jpg"
    assert response_body["price"] == 8.99
    assert response_body["stock_quantity"] == 100

def test_get_variant_by_id_invalid_id(client: TestClient, db_session: Session, sample_variant_data):
    # Act
    response = client.get("/products/1/variants/abc")
    response_body = response.json()

    # Assert
    assert response.status_code == 422


def test_update_variant_not_found(client: TestClient, db_session: Session, sample_variant_data):
    # Act
    response = client.put("/products/1/variants/999", json={
        "product_id": 1,
        "size": "Updated Size",
        "shape": "Square",
        "img_url": "https://example.com/images/updated-square.jpg",
        "price": 15.99,
        "stock_quantity": 25
    })
    response_body = response.json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
        "detail": "ProductVariant 999 not found"
    }

def test_update_variant_found(client: TestClient, db_session: Session, sample_variant_data):
    # Act
    response = client.put("/products/1/variants/2", json={
        "product_id": 1,
        "size": "Updated Large",
        "shape": "Oval",
        "img_url": "https://example.com/images/updated-large.jpg",
        "price": 14.99,
        "stock_quantity": 30
    })
    response_body = response.json()

    # Assert
    assert response.status_code == 200
    assert response_body["id"] == 2
    assert response_body["size"] == "Updated Large"
    assert response_body["shape"] == "Oval"
    assert response_body["img_url"] == "https://example.com/images/updated-large.jpg"
    assert response_body["price"] == 14.99
    assert response_body["stock_quantity"] == 30

    query = select(ProductVariant).where(ProductVariant.id == 2)
    updated_variant = db_session.scalars(query).first()

    assert updated_variant
    assert updated_variant.size == "Updated Large"
    assert updated_variant.shape == "Oval"
    assert updated_variant.img_url == "https://example.com/images/updated-large.jpg"
    assert updated_variant.price == 14.99

def test_update_variant_invalid_id(client: TestClient, db_session: Session, sample_variant_data):
    # Act
    response = client.put("/products/1/variants/abc", json={
        "product_id": 1,
        "size": "Updated Size",
        "shape": "Square",
        "img_url": "https://example.com/images/updated-square.jpg",
        "price": 15.99,
        "stock_quantity": 25
    })
    response_body = response.json()

    # Assert
    assert response.status_code == 422

def test_delete_variant_not_found(client: TestClient, db_session: Session, sample_variant_data):
    # Act
    response = client.delete("/products/1/variants/999")
    response_body = response.json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
        "detail": "ProductVariant 999 not found"
    }

def test_delete_variant_found(client: TestClient, db_session: Session, sample_variant_data):
    # Act
    response = client.delete("/products/1/variants/1")

    # Assert
    assert response.status_code == 204

    query = select(ProductVariant).where(ProductVariant.id == 1)
    deleted_variant = db_session.scalars(query).first()

    assert deleted_variant is None

def test_delete_variant_invalid_id(client: TestClient, db_session: Session, sample_variant_data):
    # Act
    response = client.delete("/products/1/variants/xyz")
    response_body = response.json()

    # Assert
    assert response.status_code == 422
