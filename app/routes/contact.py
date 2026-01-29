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

from fastapi import APIRouter, HTTPException
from app.schemas.contact_schema import ContactForm
from app.services.gmail import log_contact_message

router = APIRouter(prefix="/contact", tags=["Contact"])

@router.post("/")
def submit_contact(form: ContactForm):
    try:
        log_contact_message(
            name=form.name,
            email=form.email,
            message=form.message,
        )
        return {"status": "received"}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to process contact form")
