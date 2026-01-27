from fastapi import FastAPI
from app.routes.product_routes import router as product_router
from app.routes.category_routes import router as category_router

app = FastAPI()

app.include_router(product_router)
app.include_router(category_router)
