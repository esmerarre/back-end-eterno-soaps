from fastapi import FastAPI
from app.routes.product_routes import router as product_router
from app.routes.category_routes import router as category_router
from app.routes.variant_routes import router as variant_router
from app.routes.contact import router as contact_router
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # allow POST, GET, OPTIONS, etc.
    allow_headers=["*"],
)

app.include_router(product_router)
app.include_router(category_router)
app.include_router(variant_router)
app.include_router(contact_router)
