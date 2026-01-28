from fastapi import FastAPI
from app.routes.product_routes import router as product_router
from app.routes.category_routes import router as category_router
from app.routes.variant_routes import router as variant_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",   # Vite frontend
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # or ["*"] for development
    allow_credentials=True,
    allow_methods=["*"],        # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],
)


app.include_router(product_router)
app.include_router(category_router)
app.include_router(variant_router)








