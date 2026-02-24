"""Models for the auth service"""

from typing import Optional

from pydantic import BaseModel
from pydantic.fields import Field


class UserCreate(BaseModel):
    """User creation model"""

    firstname: str = Field(..., title="User's first name", examples=["John"])
    lastname: str = Field(..., title="User's last name", examples=["Doe"])
    username: str = Field(..., examples=["johndoe", "janedoe"])
    email: str = Field(
        ..., examples=["john.doe@example.com", "jane.doe@example.com"]
    )
    password: str = Field(..., examples=["password123", "password456"])


class LoginRequest(BaseModel):
    """User login model"""

    username: str = Field(..., examples=["johndoe", "janedoe"])
    password: str = Field(..., examples=["password123", "password456"])


class Token(BaseModel):
    """Token model"""

    access_token: str = Field(..., examples=["access_token"])
    token_type: str = Field(..., examples=["bearer"])


class GenericResponse(BaseModel):
    """Generic response model"""

    message: Optional[str] = Field(
        ..., examples=["User registered successfully"]
    )
    error: Optional[str] = Field(..., examples=["Invalid credentials"])


class LoginResponse(BaseModel):
    """Login response model"""

    access_token: str = Field(..., examples=["access_token"])
    token_type: str = Field(..., examples=["bearer"])
    message: Optional[str] = Field(..., examples=["Login successful"])
    error: Optional[str] = Field(..., examples=["Invalid credentials"])


class BasicUserInfo(BaseModel):
    """Base User Info model."""

    firstname: str = Field(..., title="User's first name", examples=["John"])
    lastname: str = Field(..., title="User's last name", examples=["Doe"])
    username: str = Field(..., examples=["johndoe", "janedoe"])
    email: str = Field(
        ..., examples=["john.doe@example.com", "jane.doe@example.com"]
    )
    bio: str = Field("", examples=["This is John Doe, an imaginary person :)"])
    verified: bool = Field(False, examples=[True, False])
    active: bool = Field(True, examples=[True, False])


class UserUpdate(BaseModel):
    """User Update request model."""

    firstname: str | None = Field(
        None, title="User's first name", examples=["John"]
    )
    lastname: str | None = Field(
        None, title="User's last name", examples=["Doe"]
    )
    username: str | None = Field(None, examples=["johndoe", "janedoe"])
    bio: str | None = Field(
        None, examples=["This is John Doe, an imaginary person :)"]
    )
