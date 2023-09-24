import boto3
from botocore.exceptions import ClientError

from src.core.settings import Settings


def setup_infra():
    settings = Settings.cached()
    s3_client = boto3.client("s3", endpoint_url=str(settings.s3_endpoint))
    sns_client = boto3.client("sns", endpoint_url=str(settings.sns_endpoint))
    sqs_client = boto3.client("sqs", endpoint_url=str(settings.sqs_endpoint))

    try:
        s3_client.head_bucket(
            Bucket=settings.s3_bucket_name
        )
    except ClientError:
        s3_client.create_bucket(
            Bucket=settings.s3_bucket_name
        )

    topic: dict[str, str] = sns_client.create_topic(
        Name=settings.sns_topic,
    )

    try:
        queue_url = sqs_client.get_queue_url(
            QueueName=settings.sqs_queue_name
        )["QueueUrl"]
    except ClientError:
        queue = sqs_client.create_queue(
            QueueName=settings.sqs_queue_name,
        )
        queue_url = queue["QueueUrl"]

    # bucket_arn: str = f"arn:aws:s3:::{settings.s3_bucket_name}"
    topic_arn: str = topic["TopicArn"]

    s3_client.put_bucket_notification_configuration(
        Bucket=settings.s3_bucket_name,
        NotificationConfiguration={
            "TopicConfigurations": [
                {
                    "TopicArn": topic_arn,
                    "Events": ["s3:ObjectCreated:*", "s3:ObjectRemoved:*"],
                }
            ]
        }
    )

    queue_arn = sqs_client.get_queue_attributes(
        QueueUrl=queue_url,
        AttributeNames=["QueueArn"]
    )["Attributes"]["QueueArn"]

    sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol="sqs",
        Endpoint=queue_arn,
    )
