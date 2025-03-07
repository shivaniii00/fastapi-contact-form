from fastapi import FastAPI, Form
import aiosmtplib
from email.mime.text import MIMEText

app = FastAPI()

# Replace with your email settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "shivanichaturvedi892@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "Realmadrid@@35"  # Use an app password for security
EMAIL_RECEIVER = "shivanichaturvedi892@gmail.com"  # Where you want to receive messages

@app.post("/send-message/")
async def send_message(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    email_content = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"
    msg = MIMEText(email_content)
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = "New Contact Form Submission"

    try:
        await aiosmtplib.send(
            msg, hostname=SMTP_SERVER, port=SMTP_PORT, username=EMAIL_SENDER, password=EMAIL_PASSWORD, use_tls=False, start_tls=True
        )
        return {"status": "success", "message": "Email sent successfully!"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to send email: {e}"}
