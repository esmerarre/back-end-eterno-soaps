# import base64
# from email.message import EmailMessage
# from google.oauth2.credentials import Credentials
# from googleapiclient.discovery import build
# import os

# def send_contact_email(name: str, email: str, message: str):
#     creds = Credentials(
#         token=None,
#         refresh_token=os.getenv("GMAIL_REFRESH_TOKEN"),
#         client_id=os.getenv("GMAIL_CLIENT_ID"),
#         client_secret=os.getenv("GMAIL_CLIENT_SECRET"),
#         token_uri="https://oauth2.googleapis.com/token",
#         scopes=["https://www.googleapis.com/auth/gmail.send"],
#     )

#     service = build("gmail", "v1", credentials=creds)

#     email_msg = EmailMessage()
#     email_msg.set_content(
#         f"From: {name}\nEmail: {email}\n\n{message}"
#     )

#     email_msg["To"] = os.getenv("GMAIL_SENDER")
#     email_msg["From"] = os.getenv("GMAIL_SENDER")
#     email_msg["Subject"] = "New Contact Form Submission"

#     encoded_message = base64.urlsafe_b64encode(
#         email_msg.as_bytes()
#     ).decode()

#     service.users().messages().send(
#         userId="me",
#         body={"raw": encoded_message},
#     ).execute()
from datetime import datetime

def log_contact_message(name: str, email: str, message: str):
    timestamp = datetime.utcnow().isoformat()

    print("\n📨 NEW CONTACT FORM SUBMISSION")
    print("--------------------------------")
    print(f"Time: {timestamp}")
    print(f"Name: {name}")
    print(f"Email: {email}")
    print("Message:")
    print(message)

