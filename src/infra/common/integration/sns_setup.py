import json
import logging

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class SNSSetupFactory:
    def __init__(self, s3_endpoint: str | None = None,  sns_endpoint: str | None = None) -> None:
        self.s3 = boto3.client('s3', endpoint_url=s3_endpoint)
        self.sns = boto3.client('sns', endpoint_url=sns_endpoint)

    def create_topic(self, *, topic_name: str) -> str | None:
        try:
            # Attempt to create the SNS topic
            response = self.sns.create_topic(Name=topic_name)
            topic_arn = response['TopicArn']
            print("Topic ARN:", topic_arn)
            return topic_arn
        except ClientError as e:
            # If the topic already exists, retrieve its ARN
            if e.response['Error']['Code'] == 'TopicNameAlreadyExists':
                response = self.sns.list_topics()
                for topic in response['Topics']:
                    if topic['TopicArn'].endswith(topic_name):
                        topic_arn = topic['TopicArn']
                        print("Topic ARN (Already Exists):", topic_arn)
                        return topic_arn
            else:
                # Handle other errors as needed
                print("Error:", e)

    def subscribe_sns_with_endpoint(self, *, topic: str, endpoint: str) -> None:

        # Create Topic if not exists
        topic_arn = self.create_topic(topic_name=topic)

        try:
            # Subscribe the http endpoint to the SNS topic
            self.sns.subscribe(
                TopicArn=topic_arn,
                Protocol='http',
                Endpoint=endpoint,
                Attributes={
                    "DeliveryPolicy": json.dumps({
                        "healthyRetryPolicy": {
                            "minDelayTarget": 1,
                            "maxDelayTarget": 60,
                            "numRetries": 50,
                            "numNoDelayRetries": 3,
                            "numMinDelayRetries": 2,
                            "numMaxDelayRetries": 35,
                            "backoffFunction": "exponential"
                        },
                        "throttlePolicy": {
                            "maxReceivesPerSecond": 10
                        },
                        "requestPolicy": {
                            "headerContentType": "application/json"
                        }
                    })
                }
            )
        except ClientError as e:
            logger.error(e)
            return None

    def configure_s3(self, *,  bucket_name: str | None, topic: str | None) -> None:
        assert bucket_name is not None, 'Bucket name is required'
        assert topic is not None, 'Topic is required'

        # Get the ARN of the S3 bucket
        response = self.s3.list_buckets()
        bucket_arn: str | None = None
        for bucket in response['Buckets']:
            if bucket['Name'] == bucket_name:
                bucket_arn = f'arn:aws:s3:::{bucket["Name"]}'

        if bucket_arn is None:
            # create bucket
            self.s3.create_bucket(Bucket=bucket_name)
            bucket_arn = f'arn:aws:s3:::{bucket_name}'

        # Create Topic if not exists
        topic_arn = self.create_topic(topic_name=topic)

        if topic_arn is None:
            raise Exception('Topic not created')

        # Add the S3 bucket notification configuration
        self.s3.put_bucket_notification_configuration(
            Bucket=bucket_name,
            NotificationConfiguration={
                'TopicConfigurations': [
                    {
                        'TopicArn': topic_arn,
                        'Events': [
                            's3:ObjectCreated:*',
                            's3:ObjectRemoved:*'
                        ]
                    }
                ]
            }
        )
