from email.message import EmailMessage
from app.settings.config import settings

from pydantic import EmailStr


def create_order_proccess_email_template(email_to: EmailStr, name: str):
    email = EmailMessage()

    email["Subject"] = "Заказ в обработке"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Ваш заказ готовится</h1>
            <p>Здравствуйте {name}, мы приняли ваш заказ</p>

            <p>Наш курьер свяжется с вами в ближайшее время</p>
        """,
        subtype="html",
    )

    return email
