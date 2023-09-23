from hashlib import sha256
from uuid import UUID

from pydantic import BaseModel, SecretStr


class User(BaseModel):
    id: UUID
    name: str
    email: str
    password_hash: SecretStr
    is_active: bool

    class Config:
        from_attributes = True
        json_encoders = {
            UUID: lambda uuid: str(uuid)
        }

    @staticmethod
    def hash_password(password: str) -> str:
        salt = "salt"
        return sha256((salt+password).encode()).hexdigest()
