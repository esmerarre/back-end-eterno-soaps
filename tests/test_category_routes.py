from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.category import Category
from sqlalchemy import select
import pytest

## Category tests ##

def test_create_category(client: TestClient, db_session: Session):
    # Act
    response = client.post("/categories", json={
        "name": "Body",
        "description": "Body soaps"
    })
    response_body = response.json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "name": "Body",
        "description": "Body soaps"
    }
    
    query = select(Category).where(Category.id == 1)
    new_category = db_session.scalars(query).first()

    assert new_category
    assert new_category.name == "Body"
    assert new_category.description == "Body soaps"

def test_get_all_categories_no_categories(client: TestClient):
    response = client.get("/categories/")
    response_body = response.json()

    assert response.status_code == 200
    assert response_body == []

def test_get_all_categories(client: TestClient, db_session: Session, sample_category_data):
    response = client.get("/categories/")
    response_body = response.json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 1,
            "name": "Body",
            "description": "Body soaps"
        },
        {
            "id": 2,
            "name": "Face",
            "description": "Facial soaps"
        },
        {
            "id": 3,
            "name": "None",
            "description": "No specific category"
        }
    ]

def test_get_category_by_id_not_found(client: TestClient, db_session: Session, sample_category_data):
    # Act
    response = client.get("/categories/999")
    response_body = response.json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
        "detail": "Category 999 not found"
    }

def test_get_category_by_id_found(client: TestClient, db_session: Session, sample_category_data):
    # Act
    response = client.get("/categories/2")
    response_body = response.json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 2,
        "name": "Face",
        "description": "Facial soaps"
    }

def test_get_category_by_id_invalid_id(client: TestClient, db_session: Session, sample_category_data):
    # Act
    response = client.get("/categories/abc")
    response_body = response.json()

    # Assert
    assert response.status_code == 422

def test_update_category_not_found(client: TestClient, db_session: Session, sample_category_data):
    # Act
    response = client.put("/categories/999", json={
        "name": "Updated Name",
        "description": "Updated Description"
    })
    response_body = response.json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
        "detail": "Category 999 not found"
    }

def test_update_category_found(client: TestClient, db_session: Session, sample_category_data):
    # Act
    response = client.put("/categories/2", json={
        "name": "Updated Name",
        "description": "Updated Description"
    })
    response_body = response.json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 2,
        "name": "Updated Name",
        "description": "Updated Description"
    }

    query = select(Category).where(Category.id == 2)
    updated_category = db_session.scalars(query).first()

    assert updated_category
    assert updated_category.name == "Updated Name"
    assert updated_category.description == "Updated Description"

def test_update_category_invalid_id(client: TestClient, db_session: Session, sample_category_data):
    # Act
    response = client.put("/categories/abc", json={
        "name": "Updated Name",
        "description": "Updated Description"
    })
    response_body = response.json()

    # Assert
    assert response.status_code == 422

def test_delete_category_not_found(client: TestClient, db_session: Session, sample_category_data):
    # Act
    response = client.delete("/categories/999")
    response_body = response.json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
        "detail": "Category 999 not found"
    }

def test_delete_category_found(client: TestClient, db_session: Session, sample_category_data):
    # Act
    response = client.delete("/categories/1")

    # Assert
    assert response.status_code == 204

    query = select(Category).where(Category.id == 1)
    deleted_category = db_session.scalars(query).first()

    assert deleted_category is None

def test_delete_category_invalid_id(client: TestClient, db_session: Session, sample_category_data):
    # Act
    response = client.delete("/categories/xyz")
    response_body = response.json()

    # Assert
    assert response.status_code == 422

# def test_patch_category_found(client: TestClient, db_session: Session, sample_category_data):
#     # Act
#     response = client.patch("/categories/3", json={
#         "description": "Updated Description"
#     })
    
#     # If PATCH is not implemented, expect 405 Method Not Allowed
#     if response.status_code == 405:
#         return  # Skip test if PATCH not implemented
        
#     response_body = response.json()

#     # Assert
#     assert response.status_code == 200
#     assert response_body["id"] == 3
#     assert response_body["description"] == "Updated Description"

#     query = select(Category).where(Category.id == 3)
#     patched_category = db_session.scalars(query).first()

#     assert patched_category
#     assert patched_category.description == "Updated Description"

# def test_patch_category_not_found(client: TestClient, db_session: Session, sample_category_data):
#     # Act
#     response = client.patch("/categories/999", json={
#         "description": "Updated Description"
#     })
    
#     # If PATCH is not implemented, expect 405 Method Not Allowed
#     if response.status_code == 405:
#         return  # Skip test if PATCH not implemented
        
#     response_body = response.json()

#     # Assert
#     assert response.status_code == 404
#     assert response_body == {
#         "detail": "Category 999 not found"
#     }

# def test_patch_category_invalid_id(client: TestClient, db_session: Session, sample_category_data):
#     # Act
#     response = client.patch("/categories/xyz", json={
#         "description": "Updated Description"
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