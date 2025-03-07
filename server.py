from fastapi import FastAPI, Form
import aiosmtplib
from email.mime.text import MIMEText
import os

app = FastAPI()

# Environment variables for security (Set these in your hosting platform)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")  # Default to Gmail
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "your-email@gmail.com")  # Your email
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your-app-password")  # Use an App Password!
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER", "your-email@gmail.com")  # Destination inbox

@app.post("/send-message/")
async def send_message(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    """Handles form submissions and sends an email."""
    
    email_content = f"New Contact Form Submission\n\nName: {name}\nEmail: {email}\nMessage:\n{message}"
    msg = MIMEText(email_content)
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = "New Contact Form Submission"

    try:
        await aiosmtplib.send(
            msg,
            hostname=SMTP_SERVER,
            port=SMTP_PORT,
            username=EMAIL_SENDER,
            password=EMAIL_PASSWORD,
            use_tls=False,
            start_tls=True
        )
        return {"status": "success", "message": "Email sent successfully!"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to send email: {str(e)}"}
