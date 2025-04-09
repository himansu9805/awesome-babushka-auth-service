"""Database models for the auth service"""

from datetime import datetime
from datetime import timedelta
from datetime import timezone

from pydantic import BaseModel
from pydantic.fields import Field


class User(BaseModel):
    """User model"""

    username: str = Field(..., examples=["johndoe", "janedoe"])
    email: str = Field(
        ..., examples=["john.doe@example.com", "jane.doe@example.com"]
    )
    password: str = Field(..., examples=["password123", "password456"])
    verified: bool = Field(False, examples=[True, False])
    active: bool = Field(True, examples=[True, False])
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        examples=[datetime.now(timezone.utc)],
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        examples=[datetime.now(timezone.utc)],
    )


class Token(BaseModel):
    """Verification token model"""

    email: str = Field(
        ..., examples=["john.doe@example.com", "jane.doe@example.com"]
    )
    token: str = Field(..., examples=["verification_token"])
    expires_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc) + timedelta(days=1),
        examples=[datetime.now(timezone.utc) + timedelta(days=1)],
    )
