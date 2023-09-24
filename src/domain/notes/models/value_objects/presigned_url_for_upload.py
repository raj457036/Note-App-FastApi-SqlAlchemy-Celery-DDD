from dataclasses import dataclass


@dataclass(
    frozen=True,
)
class PresignedURLForUploadVO:
    url: str
    expiry: int
    extra_fields: dict[str, str] | None = None
