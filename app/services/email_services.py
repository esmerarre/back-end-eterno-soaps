import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")
TO_EMAIL = os.getenv("TO_EMAIL")

def send_contact_email(name: str, email: str, message: str):
    email_message = Mail(
        from_email=FROM_EMAIL,
        to_emails=TO_EMAIL,
        subject="New Contact Form Submission",
        html_content=f"""
        <strong>Name:</strong> {name}<br>
        <strong>Email:</strong> {email}<br><br>
        <strong>Message:</strong><br>
        {message}
        """
    )
    


    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(email_message)
    except Exception as e:
        print("❌ Error sending email:", e)
        raise
  
