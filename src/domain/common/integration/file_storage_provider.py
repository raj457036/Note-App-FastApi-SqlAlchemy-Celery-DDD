from abc import ABC, abstractmethod
from typing import Generic, TypeVar

SignedURLReturnType = TypeVar("SignedURLReturnType")


class FileStorageProvider(ABC, Generic[SignedURLReturnType]):
    """An storage provider like AWS S3 or Google Cloud Storage"""

    @abstractmethod
    def get_presigned_upload_url(self, *args, **kwargs) -> SignedURLReturnType:
        """Returns a presigned url to upload a file"""
        raise NotImplementedError

    @abstractmethod
    def get_presigned_download_url(self, *args, **kwargs) -> SignedURLReturnType:
        """Returns a presigned url to download a file"""
        raise NotImplementedError

    @abstractmethod
    def delete(self, *args, **kwargs) -> None:
        """Deletes a file"""
        raise NotImplementedError
