# from fastapi import APIRouter, HTTPException
# from app.schemas.contact_schema import ContactForm
# from app.services.gmail import send_contact_email

# router = APIRouter(prefix="/contact", tags=["Contact"])

# @router.post("/")
# def submit_contact(form: ContactForm):
#     try:
#         print("Received contact form:")
#         print(f"Name: {form.name}")
#         print(f"Email: {form.email}")
#         print(f"Message: {form.message}")

#         send_contact_email(
#             name=form.name,
#             email=form.email,
#             message=form.message,
#         )
#         return {"status": "sent"}
#     except Exception as e:
#         print("Email error:", e)  # ✅ print the exact exception
#         raise HTTPException(status_code=500, detail=str(e))

# backend/app/routes/contact.py
from fastapi import APIRouter, Request
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class ContactForm(BaseModel):
    name: str
    email: str
    message: str

@router.post("/contact")
async def submit_contact(form: ContactForm):
    print("\n📨 NEW CONTACT FORM SUBMISSION")
    print("-" * 32)
    print(f"Time: {datetime.now()}")
    print(f"Name: {form.name}")
    print(f"Email: {form.email}")
    print("Message:")
    print(form.message)
    print("-" * 32)
    return {"message": "Form received!"}
