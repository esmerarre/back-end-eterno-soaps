# backend/routes/checkout.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import stripe
import os
from dotenv import load_dotenv

load_dotenv()  # this reads .env and sets environment variables

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")



router = APIRouter()

class CheckoutItem(BaseModel):
    id: int
    name: str
    price: float
    quantity: int

class CheckoutRequest(BaseModel):
    items: list[CheckoutItem]

@router.post("/checkout")
async def create_checkout_session(request: CheckoutRequest):
    line_items = [
        {
            "price_data": {
                "currency": "usd",
                "product_data": {"name": item.name},
                "unit_amount": int(item.price * 100),  # Stripe expects cents
            },
            "quantity": item.quantity,
        }
        for item in request.items
    ]

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url="http://localhost:5173/success",
            cancel_url="http://localhost:5173/cancel",
        )
        return JSONResponse({"url": session.url})
    except stripe.error.StripeError as e:
        return JSONResponse({"error": str(e)}, status_code=500)