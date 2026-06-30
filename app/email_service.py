import smtplib
from email.mime.text import MIMEText

EMAIL = "your_email@gmail.com"
PASSWORD = "your_app_password"


def send_email(subject: str, body: str, to_email: str):

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)