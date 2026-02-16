"""Database models for the auth service"""

from datetime import datetime, timedelta, timezone

from bson import ObjectId
from pydantic import BaseModel
from pydantic.fields import Field


class BasicUserInfo(BaseModel):
    """Base User Info model."""

    username: str = Field(..., examples=["johndoe", "janedoe"])
    email: str = Field(
        ..., examples=["john.doe@example.com", "jane.doe@example.com"]
    )
    verified: bool = Field(False, examples=[True, False])
    active: bool = Field(True, examples=[True, False])


class User(BasicUserInfo):
    """User model"""

    password: str = Field(..., examples=["password123", "password456"])
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        examples=[datetime.now(timezone.utc)],
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        examples=[datetime.now(timezone.utc)],
    )


class ActivationKey(BaseModel):
    """Model for activation keys"""

    email: str = Field(..., examples=["john.doe@example.com"])
    token: str = Field(..., examples=["activation_token_123"])
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        examples=[datetime.now(timezone.utc)],
    )
    expires_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
        + timedelta(hours=1),
        examples=[datetime.now(timezone.utc) + timedelta(hours=1)],
    )


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic models"""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class RefreshToken(BaseModel):
    """Model for refresh tokens"""

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    jti: str = Field(..., examples=["unique_token_id"])
    username: str = Field(..., examples=["user123", "user456"])
    email: str = Field(
        ..., examples=["john.doe@example.com", "jane.doe@example.com"]
    )
    token_family: str = Field(
        ..., examples=["email_verification", "password_reset"]
    )
    is_revoked: bool = Field(False, examples=[True, False])
    expires_at: datetime = Field(
        ..., examples=[datetime.now(timezone.utc) + timedelta(hours=1)]
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        examples=[datetime.now(timezone.utc)],
    )
    used_at: datetime | None = Field(
        default=None, examples=[datetime.now(timezone.utc), None]
    )
    device_id: str | None = Field(default=None, examples=["device123", None])
    ip_address: str | None = Field(
        default=None, examples=["192.168.1.1", None]
    )

    class Config:
        """Pydantic configuration"""

        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
