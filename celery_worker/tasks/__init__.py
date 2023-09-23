import logging
from time import sleep

from celery_worker import celery

logger = logging.getLogger(__name__)


@celery.task
def pick_up_sqs_messages(*, topic: str, queue: str, region: str):
    logger.info("Picking up messages from SQS")
    sleep(10)
    logger.info("Done picking up messages from SQS")
