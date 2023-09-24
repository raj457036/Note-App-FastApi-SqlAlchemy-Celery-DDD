import logging

from celery_worker import celery
from src.core.settings import Settings
from src.infra.integration.queue.sqs import SQSMessageQueueService

logger = logging.getLogger(__name__)


@celery.task
def pick_up_sqs_messages(*, queue_name: str, endpoint: str):
    logger.info("Picking up messages from SQS")
    settings = Settings.cached()
    queue = SQSMessageQueueService(
        queue_name=queue_name,
        endpoint=endpoint,
    )

    messages = queue.get_messages()
    logger.info([message.body for message in messages])
    logger.info(f"Got {len(messages)} messages from SQS")
    logger.info("Done picking up messages from SQS")
