from celery import Celery
from src.config import get_settings

setting = get_settings()

celery_app = Celery (
    "neuralsearch",
    broker=setting.REDIS_URL,
    backend=setting.REDIS_URL,
    include=["src.tasks"] # this celary tell where to find the code
)

# saftey setting
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)