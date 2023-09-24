from functools import cache, lru_cache

from pydantic import HttpUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="NOTER_APP_",
        frozen=True,
    )

    # database
    pg_user: str = "postgres"
    pg_password: SecretStr = SecretStr("postgres")
    pg_host: str = "localhost"
    pg_db: str = "postgres"
    pg_port: int = 5432

    # s3
    s3_endpoint: HttpUrl | None = None
    s3_bucket_name: str | None = None

    # sqs
    sqs_endpoint: HttpUrl | None = None
    sqs_queue_name: str | None = None

    # sns
    sns_endpoint: HttpUrl | None = None
    sns_topic: str | None = None

    @classmethod
    @cache
    def cached(cls, **kwargs) -> "Settings":
        return cls(**kwargs)
