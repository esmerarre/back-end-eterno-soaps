from fastapi import APIRouter
from pydantic import BaseModel
import stripe
import os
from dotenv import load_dotenv
load_dotenv()

# Stripe secret key (use environment variable)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

router = APIRouter(tags=["Checkout"], prefix="/api")

# Pydantic model for items
class CartItem(BaseModel):
    id: int
    name: str
    price: float
    quantity: int

class CheckoutRequest(BaseModel):
    items: list[CartItem]

# Checkout session route
@router.post("/checkout")
def create_checkout_session(data: CheckoutRequest):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": item.name},
                        "unit_amount": int(item.price * 100),
                    },
                    "quantity": item.quantity,
                }
                for item in data.items
            ],
            mode="payment",
            success_url="http://localhost:5173/success",
            cancel_url="http://localhost:5173/cancel",
        )
        return {"url": session.url}
    except Exception as e:
        return {"error": str(e)}
