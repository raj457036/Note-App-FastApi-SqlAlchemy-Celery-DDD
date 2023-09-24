import os

from celery import Celery

from setup_infra import setup_infra

setup_infra()

# Initialize Celery
celery = Celery(
    "tasks",
    # Use the appropriate broker URL
    broker="redis://{REDIS_HOST}:{REDIS_PORT}/0".format_map(os.environ),
    include=[
        "celery_worker.tasks",
        "celery_worker.scheduled"
    ],
)
