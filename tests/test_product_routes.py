from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.product import Product
from sqlalchemy import select

def test_create_product(client: TestClient, db_session: Session, sample_category_data):
    # Act
    response = client.post("/products", json={
        "name": "Cottonwood",
        "description": "A soothing blend of natural herbs for gentle cleansing.",
        "category_id": 1,
        "ingredients": ["Cottonwood Leaves", "Clove", "Cinnamon", "Bay Leaves", "Rosemary"]
    })
    response_body = response.json()

    # Assert
    assert response.status_code == 201
    assert response_body["id"] == 1
    assert response_body["name"] == "Cottonwood"
    assert response_body["description"] == "A soothing blend of natural herbs for gentle cleansing."
    assert response_body["category_id"] == 1
    assert response_body["ingredients"] == ["Cottonwood Leaves", "Clove", "Cinnamon", "Bay Leaves", "Rosemary"]
    
    query = select(Product).where(Product.id == 1)
    new_product = db_session.scalars(query).first()

    assert new_product
    assert new_product.name == "Cottonwood"
    assert new_product.description == "A soothing blend of natural herbs for gentle cleansing."

def test_create_product_invalid_data(client: TestClient, db_session: Session, sample_category_data):
    # Act
    response = client.post("/products", json={
        "name": "",
        "description": "",
        "category_id": 999,  # Non-existent category
        "ingredients": []
    })
    response_body = response.json()

    # Assert
    assert response.status_code in [400, 422]  # Either validation error

def test_get_all_products_no_products(client: TestClient):
    response = client.get("/products/")
    response_body = response.json()

    assert response.status_code == 200
    assert response_body == []


def test_get_all_products(client: TestClient, db_session: Session, sample_product_data):
    response = client.get("/products/")
    response_body = response.json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    
    # Check first product
    assert response_body[0]["name"] == "Cottonwood"
    assert response_body[0]["category_id"] == 1
    assert "ingredients" in response_body[0]
    
    # Check second product
    assert response_body[1]["name"] == "Saffron"
    assert response_body[1]["category_id"] == 2

def test_get_product_by_id_not_found(client: TestClient, db_session: Session, sample_product_data):
    # Act
    response = client.get("/products/999")
    response_body = response.json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
        "detail": "Product 999 not found"
    }

def test_get_product_by_id_found(client: TestClient, db_session: Session, sample_product_data):
    # Act
    response = client.get("/products/2")
    response_body = response.json()

    # Assert
    assert response.status_code == 200
    assert response_body["id"] == 2
    assert response_body["name"] == "Saffron"
    assert response_body["description"] == "Luxurious saffron and oats soap for radiant skin."
    assert response_body["category_id"] == 2
    assert "ingredients" in response_body

def test_get_product_by_id_invalid_id(client: TestClient, db_session: Session, sample_product_data):
    # Act
    response = client.get("/products/abc")
    response_body = response.json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "detail": "Invalid data"
    }


def test_update_product_not_found(client: TestClient, db_session: Session, sample_product_data):
    # Act
    response = client.put("/products/999", json={
        "name": "Updated Name",
        "description": "Updated Description",
        "category_id": 1,
        "ingredients": ["Test"]
    })
    response_body = response.json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
        "detail": "Product 999 not found"
    }

def test_update_product_found(client: TestClient, db_session: Session, sample_product_data):
    # Act
    response = client.put("/products/2", json={
        "name": "Updated Saffron",
        "description": "Updated Description",
        "category_id": 1,
        "ingredients": ["Updated", "Ingredients"]
    })
    response_body = response.json()

    # Assert
    assert response.status_code == 200
    assert response_body["id"] == 2
    assert response_body["name"] == "Updated Saffron"
    assert response_body["description"] == "Updated Description"
    assert response_body["category_id"] == 1

    query = select(Product).where(Product.id == 2)
    updated_product = db_session.scalars(query).first()

    assert updated_product
    assert updated_product.name == "Updated Saffron"
    assert updated_product.description == "Updated Description"

def test_update_product_invalid_id(client: TestClient, db_session: Session, sample_product_data):
    # Act
    response = client.put("/products/abc", json={
        "name": "Updated Name",
        "description": "Updated Description",
        "category_id": 1,
        "ingredients": ["Test"]
    })
    response_body = response.json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "detail": "Invalid data"
    }

def test_delete_product_not_found(client: TestClient, db_session: Session, sample_product_data):
    # Act
    response = client.delete("/products/999")
    response_body = response.json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
        "detail": "Product 999 not found"
    }

def test_delete_product_found(client: TestClient, db_session: Session, sample_product_data):
    # Act
    response = client.delete("/products/1")
    response_body = response.json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "detail": "Product 1 deleted successfully"
    }

    query = select(Product).where(Product.id == 1)
    deleted_product = db_session.scalars(query).first()

    assert deleted_product is None

def test_delete_product_invalid_id(client: TestClient, db_session: Session, sample_product_data):
    # Act
    response = client.delete("/products/xyz")
    response_body = response.json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "detail": "Invalid data"
    }

# def test_patch_product_found(client: TestClient, db_session: Session, sample_product_data):
#     # Act - Note: PATCH not implemented in routes, test may need adjustment
#     response = client.patch("/products/3", json={
#         "description": "Updated description via PATCH"
#     })
    
#     # If PATCH is not implemented, expect 405 Method Not Allowed
#     if response.status_code == 405:
#         return  # Skip test if PATCH not implemented
    
#     response_body = response.json()

#     # Assert
#     assert response.status_code == 200
#     assert response_body["id"] == 3
#     assert response_body["description"] == "Updated description via PATCH"

# def test_patch_product_not_found(client: TestClient, db_session: Session, sample_product_data):
#     # Act
#     response = client.patch("/products/999", json={
#         "description": "Updated"
#     })
    
#     # If PATCH is not implemented, expect 405 Method Not Allowed
#     if response.status_code == 405:
#         return  # Skip test if PATCH not implemented
        
#     response_body = response.json()

#     # Assert
#     assert response.status_code == 404
#     assert response_body == {
#         "detail": "Product 999 not found"
#     }

# def test_patch_product_invalid_id(client: TestClient, db_session: Session, sample_product_data):
#     # Act
#     response = client.patch("/products/xyz", json={
#         "description": "Test"
#     })
    
#     # If PATCH is not implemented, expect 405 Method Not Allowed
#     if response.status_code == 405:
#         return  # Skip test if PATCH not implemented
        
#     response_body = response.json()

#     # Assert
#     assert response.status_code == 400
#     assert response_body == {
#         "detail": "Invalid data"
#     }

