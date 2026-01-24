from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.product_categories import Category
from sqlalchemy import select

def test_create_product_with_category(client: TestClient, db_session: Session, sample_category_data):
    # Act
    response = client.post("/products", json={
            "name": "Eternas Caricias",
            # ingredients=["Cottonwood Leaves", "Clove", "Cinnamon", "Bay Leaves", "Rosemary"],
            "price": 10.0,
            "description": "A soothing blend of natural herbs for gentle cleansing.",
            "stock": 10,
            "category_id": 2
    })
    response_body = response.json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
            "id": 1,
            "name": "Eternas Caricias",
            # ingredients=["Cottonwood Leaves", "Clove", "Cinnamon", "Bay Leaves", "Rosemary"],
            "price": 10.0,
            "description": "A soothing blend of natural herbs for gentle cleansing.",
            "stock": 10,
            "category_id": 2,
            "category": {
                "id": 2,
                "name": "Mosturizing",
                "description": "Hydrating soaps for dry skin."
            }
    }
    
    query = select(Product).where(Product.id == 1)
    new_product = db_session.scalars(query).first()

    assert new_product
    assert new_product.name == "Eternas Caricias"
    assert new_product.category_id == 2

def test_post_product_ids_to_category(client: TestClient, db_session: Session, sample_category_data, sample_product_data):
    # Act
    response = client.post("/categories/2/products", json={
        "product_ids": [1, 3]
    })
    response_body = response.json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 2,
        "product_ids": [1, 3]
    }

    # Check that Category was updated in the db
    query = select(Category).where(Category.id == 2)
    category = db_session.scalars(query).first()
    assert len(category.products) == 2


#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_products_for_specific_category_no_category(client: TestClient, db_session: Session, sample_product_data):
    # Act
    response = client.get("/categories/1/products")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Category 1 not found"}

def test_get_products_for_specific_category_no_products(client: TestClient, db_session: Session, sample_category_data):
    # Act
    response = client.get("/categories/1/products")
    response_body = response.json()

    # Assert
    assert response.status_code == 200
    assert "products" in response_body
    assert len(response_body["products"]) == 0
    assert response_body == {
        "id": 1,
        "name": "Essential Oils",
        "description": "Herbal infused soaps for natural care.",
        "products": []
    }

def test_get_products_for_specific_category_with_products(client: TestClient, db_session: Session, sample_category_data, sample_product_data):
    # Assigning some products to the category
    category = db_session.get(Category, 2)
    product1 = db_session.get(Product, 1)
    product2 = db_session.get(Product, 3)
    category.products.append(product1)
    category.products.append(product2)
    db_session.commit()

    # Act
    response = client.get("/categories/2/products")
    response_body = response.json()

    # Assert
    assert response.status_code == 200
    assert "products" in response_body
    assert len(response_body["products"]) == 2
    assert response_body == {
        "id": 2,
        "name": "Mosturizing",
        "description": "Hydrating soaps for dry skin.",
        "products": [
            {
                "id": 1,
                "name": "Eternas Caricias",
                # ingredients=["Cottonwood Leaves", "Clove", "Cinnamon", "Bay Leaves", "Rosemary"],
                "price": 10.0,
                "description": "A soothing blend of natural herbs for gentle cleansing.",
                "stock": 10,
                "category_id": 2,
                "category": {
                    "id": 2,
                    "name": "Mosturizing",
                    "description": "Hydrating soaps for dry skin."
                }
            },
            {
                "id": 3,
                "name": "Serenidad Eterna",
                # ingredients=["Lavender", "Turmeric", "Aloe Vera", "Calendula"],
                "price": 11.0,
                "description": "Relaxing lavender and aloe blend for sensitive skin.",
                "stock": 4,
                "category_id": 2,
                "category": {
                    "id": 2,
                    "name": "Mosturizing",
                    "description": "Hydrating soaps for dry skin."
                }
            }
        ]
    }

