# status gives us constants for HTTP status codes; HTTPException is used to create custom error responses; Request is used to handle incoming requests
from fastapi import FastAPI


@app.get("/")  # Root endpoint
@app.get("/products")  # Products endpoint
def read_root():
    return {"Hello": "World"}


@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")