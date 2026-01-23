from fastapi import FastAPI
from app.routes import product_routes, category_routes

app = FastAPI()

app.include_router(product_routes.router)
app.include_router(category_routes.router)
