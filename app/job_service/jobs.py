import smtplib
from pydantic import EmailStr

from app.job_service.celery_app import celery_worker
from app.job_service.html_templates.order_recieved import (
    create_order_recieved_email_template,
)
from app.job_service.html_templates.order_process import (
    create_order_proccess_email_template,
)
from app.job_service.html_templates.order_created import (
    create_order_created_email_template,
)

from app.settings.config import settings, auth_settings


@celery_worker.task
def send_order_recieved_email(email: EmailStr, name: str):
    msg_content = create_order_recieved_email_template(
        email_to=email,
        name=name,
    )
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg_content)


@celery_worker.task
def send_order_proccess_email(email: EmailStr, name: str):
    msg_content = create_order_proccess_email_template(
        email_to=email,
        name=name,
    )
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg_content)


@celery_worker.task
def send_order_created_email(name: str, cost: int, address: str):
    msg_content = create_order_created_email_template(
        email_to=auth_settings.ADMIN_EMAIL,
        name=name,
        cost=cost,
        address=address
    )
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg_content)
