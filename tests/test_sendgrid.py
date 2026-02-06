import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

message = Mail(
    from_email=os.getenv("FROM_EMAIL"),
    to_emails=os.getenv("TO_EMAIL"),
    subject="SendGrid Test",
    html_content="If you see this, SendGrid works 🎉"
)

sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
response = sg.send(message)

print(response.status_code)
