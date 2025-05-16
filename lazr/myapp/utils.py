from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
from django.template.loader import render_to_string

# Load variables from .env
load_dotenv()


def send_email(user_email):
    sender_email = os.getenv("GMAIL_ADDRESS")
    app_password = os.getenv("GMAIL_APP_PASSWORD")
    domain = "https://lazr.onrender.com/"

    if not sender_email or not app_password:
        print("Missing GMAIL_ADDRESS or GMAIL_APP_PASSWORD environment variables.")
        return False  # Return False so the view can handle it

    subject = "You've received crypto on LazrPay!"

    # Render the HTML template with a context including domain
    try:
        html_content = render_to_string("email.html", {"domain": domain})
    except FileNotFoundError:
        print("email.html not found.")
        return False

    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = user_email
    msg["Subject"] = subject

    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        print(f"✅ Email sent successfully to {user_email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False


# Example usage
if __name__ == "__main__":
    recipient = input("Enter recipient's email: ")
    send_email(recipient)
