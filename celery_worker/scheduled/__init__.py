from celery_worker import celery as app
from src.core.settings import Settings

settings = Settings.cached()
beat_schedule = {
    "poll_sqs": {
        "task": "celery_worker.tasks.pick_up_sqs_messages",
        "schedule": 20,
        "kwargs": {
            "queue_name": settings.sqs_queue_name,
            "endpoint": str(settings.sqs_endpoint),
        },
    },
}

app.conf.beat_schedule = beat_schedule
app.conf.timezone = 'UTC'  # type: ignore
