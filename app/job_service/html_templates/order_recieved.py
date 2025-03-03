from email.message import EmailMessage
from app.settings.config import auth_settings

from pydantic import EmailStr


def create_order_recieved_email_template(email_to: EmailStr):
    email = EmailMessage()

    email["Subject"] = "Подтверждение почты"
    email["From"] = auth_settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Подтверждение почты</h1>
            Ваш код подтверждения:
        """,
        subtype="html",
    )

    return email
