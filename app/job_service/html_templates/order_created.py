from email.message import EmailMessage
from app.settings.config import settings, auth_settings

from pydantic import EmailStr


def create_order_created_email_template(
        email_to: EmailStr, 
        name: str, 
        cost: int, 
        address: str
):
    email = EmailMessage()

    email["Subject"] = "Новый заказ"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Поступил новый заказ</h1>
            <p>Заказ от <b>{name}</b>, на сумму <b>{cost} руб.</b></p>
            
            <p>Адрес доставки: {address}</p>

            <a style="color: green; text-decoration: none;" href="{auth_settings.ADMIN_PANEL_URL}">АДМИН ПАНЕЛЬ</a>
        """,
        subtype="html",
    )

    return email
