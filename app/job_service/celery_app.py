from celery import Celery

from app.settings.config import settings


celery_worker = Celery(
    "jobs",
    broker=settings.JOBS_BROKER_URI,
    include=["app.job_service.jobs"],
)
