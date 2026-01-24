from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.product import Product
from sqlalchemy import select

def test_create_product(client: TestClient, db_session: Session):
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

def test_create_product_invalid_data(client: TestClient, db_session: Session):
    # Act
    response = client.post("/products", json={
            "name": "",
            "price": -5.0,
            "description": "",
            "stock": -10
    })
    response_body = response.json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "detail": "Invalid data"
    }

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
    assert response_body == {
        "id": 2,
        "name": "Eterno de Saffron",
        # ingredients=["Saffron", "Oats", "Tapioca", "Vitamin E", "Essential oils"],
        "price": 12.0,
        "description": "Luxurious saffron and oats soap for radiant skin.",
        "stock": 15,
        "category_id": None,
        "category": None
    }

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
        "price": 15.0,
        "description": "Updated Description",
        "stock": 20
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
        "name": "Updated Name",
        "price": 15.0,
        "description": "Updated Description",
        "stock": 20
    })
    response_body = response.json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 2,
        "name": "Updated Name",
        "price": 15.0,
        "description": "Updated Description",
        "stock": 20,
        "category_id": None,
        "category": None
    }

    query = select(Product).where(Product.id == 2)
    updated_product = db_session.scalars(query).first()

    assert updated_product
    assert updated_product.name == "Updated Name"
    assert updated_product.description == "Updated Description"

def test_update_product_invalid_id(client: TestClient, db_session: Session, sample_product_data):
    # Act
    response = client.put("/products/abc", json={
        "name": "Updated Name",
        "price": 15.0,
        "description": "Updated Description",
        "stock": 20
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

def test_patch_product_found(client: TestClient, db_session: Session, sample_product_data):
    # Act
    response = client.patch("/products/3", json={
        "price": 14.0,
        "stock": 8
    })
    response_body = response.json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 3,
        "name": "Serenidad Eterna",
        "price": 14.0,
        "description": "Relaxing lavender and aloe blend for sensitive skin.",
        "stock": 8,
        "category_id": None,
        "category": None
    }

    query = select(Product).where(Product.id == 3)
    patched_product = db_session.scalars(query).first()

    assert patched_product
    assert patched_product.price == 14.0
    assert patched_product.stock == 8

def test_patch_product_not_found(client: TestClient, db_session: Session, sample_product_data):
    # Act
    response = client.patch("/products/999", json={
        "price": 14.0
    })
    response_body = response.json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
        "detail": "Product 999 not found"
    }

def test_patch_product_invalid_id(client: TestClient, db_session: Session, sample_product_data):
    # Act
    response = client.patch("/products/xyz", json={
        "price": 14.0
    })
    response_body = response.json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "detail": "Invalid data"
    }

