""" Models for the auth service """

from pydantic import BaseModel
from pydantic.fields import Field


class UserCreate(BaseModel):
    """User creation model"""

    username: str = Field(..., examples=["johndoe", "janedoe"])
    email: str = Field(
        ..., examples=["john.doe@example.com", "jane.doe@example.com"]
    )
    password: str = Field(..., examples=["password123", "password456"])


class UserLogin(BaseModel):
    """User login model"""

    username: str = Field(..., examples=["johndoe", "janedoe"])
    password: str = Field(..., examples=["password123", "password456"])


class Token(BaseModel):
    """Token model"""

    access_token: str = Field(..., examples=["access_token"])
    token_type: str = Field(..., examples=["bearer"])
