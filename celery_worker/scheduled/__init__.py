from celery_worker import celery as app

beat_schedule = {
    "poll_sqs": {
        "task": "celery_worker.tasks.pick_up_sqs_messages",
        "schedule": 30,
        # "args": (topic, queue, region),
        "kwargs": {
            "topic": "test",
            "queue": "test",
            "region": "test",
        },
    },
}

app.conf.beat_schedule = beat_schedule
app.conf.timezone = 'UTC'  # type: ignore
