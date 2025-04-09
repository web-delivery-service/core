from email.message import EmailMessage
from app.settings.config import settings

from pydantic import EmailStr


def create_order_recieved_email_template(email_to: EmailStr, name: str):
    email = EmailMessage()

    email["Subject"] = "Заказ доставлен"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Курьер прибыл</h1>
            <p>Здравствуйте {name}, курьер прибыл</p>

            <br>ПРИЯТНОГО АППЕТИТА!<br>
        """,
        subtype="html",
    )

    return email
