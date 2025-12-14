from celery import Celery
from src.config import get_settings

setting = get_settings()

celery_app = Celery (
    "neuralsearch",
    broker=setting.REDIS_URL,
    backend=setting.REDIS_URL,
    # Auto-discover tasks from the specified module.
    include=["src.tasks"]
)

# Configuration to enhance security and interoperability.
# Standardizes on the JSON serializer, which is safer than the default (pickle).
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)