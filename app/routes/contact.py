from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.schemas.contact_schema import ContactForm
from app.services.email_services import send_contact_email

router = APIRouter()

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

    try:
        send_contact_email(
            name=form.name,
            email=form.email,
            message=form.message
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to send email")

    return {"message": "Form received and email sent!"}


