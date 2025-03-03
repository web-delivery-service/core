import smtplib
from pydantic import EmailStr

from app.job_service.celery_app import celery_worker
from app.job_service.html_templates.order_recieved import (
    create_order_recieved_email_template,
)

from app.settings.config import settings


@celery_worker.task
def send_otp_to_email(email: EmailStr):

    msg_content = create_order_recieved_email_template(
        email_to=email,
    )

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg_content)
