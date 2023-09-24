
import logging
from dataclasses import dataclass
from typing import Any

import boto3
from botocore.exceptions import ClientError
from typing_extensions import override

from src.domain.common.integration.file_storage_provider import \
    FileStorageProvider

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class S3SignedUrlResponse:
    """A response from S3 presigned url"""
    url: str
    fields: dict[str, str]


class S3StorageProvider(FileStorageProvider[S3SignedUrlResponse | None]):
    """An S3 storage provider"""

    def __init__(self, endpoint: str | None = None, bucket_name: str | None = None) -> None:
        super().__init__()
        self.bucket_name = bucket_name
        self.client = boto3.client('s3', endpoint_url=endpoint)

    @override
    def get_presigned_upload_url(
        self,
        object_name: str,
        bucket_name: str | None = None,
        fields: dict[str, str] | None = None,
        conditions: list[dict | str] | None = None,
        expiration: int = 3600,
    ) -> S3SignedUrlResponse | None:
        """Returns a presigned url to upload a file"""
        try:
            # list buckets and print
            response = self.client.list_buckets()
            print('Existing buckets:', response['Buckets'])

            _response = self.client.generate_presigned_post(
                bucket_name or self.bucket_name,
                object_name,
                Fields=fields,
                Conditions=conditions,
                ExpiresIn=expiration,
            )
            response = S3SignedUrlResponse(**_response)
        except ClientError as e:
            logger.error(e)
            return None

        # The response contains the presigned URL and required fields
        return response

    @override
    def get_presigned_download_url(self, *args, **kwargs):
        """Returns a presigned url to download a file"""
        raise NotImplementedError

    @override
    def delete(self, *args, **kwargs):
        """Deletes a file"""
        raise NotImplementedError
