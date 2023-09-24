import logging
import re
from typing import Any

import boto3
from pydantic import BaseModel, model_validator
from typing_extensions import override

from src.domain.integration.queue import MessageQueueService

logger = logging.getLogger(__name__)


class SQSMessage(BaseModel):
    message_id: str
    body: str
    receipt_handle: str
    attributes: dict | None = None
    message_attributes: dict | None = None

    @model_validator(mode='before')
    @classmethod
    def pascal_case_to_snake_case(cls, data: dict[str, Any]) -> Any:
        pattern = re.compile(r'(?<!^)(?=[A-Z])')
        _data: dict[str, Any] = {}
        for key, value in data.items():
            _key = pattern.sub('_', key).lower()
            _data[_key] = value
        return _data


class SQSMessageQueueService(MessageQueueService[SQSMessage]):
    def __init__(
            self,
            queue_name: str,
            endpoint: str,
            region: str = "us-east-1",
    ):
        self._queue_name = queue_name
        self._region = region
        self._sqs = boto3.client(
            "sqs", region_name=self._region, endpoint_url=endpoint)
        self._queue_url = self._sqs.get_queue_url(
            QueueName=self._queue_name)["QueueUrl"]

    @override
    def get_messages(
        self,
        *,
        max_msgs: int = 10,
        wait_time: int = 10,
        visibility_timeout: int = 60,
        **kwargs
    ) -> list[SQSMessage]:
        assert max_msgs > 0, "max_msgs must be greater than 0"
        assert wait_time > 0, "wait_time must be greater than 0"
        assert visibility_timeout > 0, "visibility_timeout must be greater than 0"

        try:
            messages = self._sqs.receive_message(
                QueueUrl=self._queue_url,
                MaxNumberOfMessages=max_msgs,
                WaitTimeSeconds=wait_time,
                VisibilityTimeout=visibility_timeout,
            ).get("Messages", [])
            logger.debug(messages)
            return [SQSMessage(**message) for message in messages]
        except Exception as e:
            logger.error(e)
            return []

    @override
    def delete_message(self, receipt_handle: str, **kwargs) -> None:
        assert receipt_handle is not None, "receipt_handle is required"

        self._sqs.delete_message(
            QueueUrl=self._queue_url,
            ReceiptHandle=receipt_handle,
        )
