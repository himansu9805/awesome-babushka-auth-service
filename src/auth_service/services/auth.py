"""Service for handling authentication."""

import logging
from datetime import datetime, timezone
from uuid import uuid4

from commons.database import MongoConnect
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials
from passlib.context import CryptContext
from pymongo.errors import DuplicateKeyError

from auth_service.core.config import settings
from auth_service.core.token import TokenUtils
from auth_service.db.models import User, ActivationKey
from auth_service.db.schemas import UserCreate, LoginRequest
from auth_service.services.email_agent import send_verification_email

logger = logging.getLogger(__file__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Authentication service class."""

    def __init__(self):
        """Initialize the AuthService class."""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        self.mongo_connection = MongoConnect(settings.MONGO_URI, settings.DB_NAME)

    def __del__(self):
        """Close the MongoDB connection."""
        self.mongo_connection.close()

    async def register_user(self, user: UserCreate) -> bool:
        """Register a new user.

        Args:
            user (UserCreate): User details for registration.

        Returns:
            bool: Registration success status.
        """
        try:
            hashed_password = pwd_context.hash(user.password)
            verification_token = uuid4().hex
            db_user = User(
                username=user.username,
                email=user.email,
                password=hashed_password,
                verified=False,
                active=True,
            )
            self.mongo_connection.get_collection(settings.USER_COLLECTION).insert_one(
                db_user.model_dump()
            )
            db_token = ActivationKey(
                email=user.email,
                token=verification_token,
            )
            self.mongo_connection.get_collection(settings.ACTIVATION_KEY_COLLECTION).insert_one(
                db_token.model_dump()
            )
        except DuplicateKeyError:
            raise ValueError("Username or email already exists")
        except Exception:
            raise ValueError("Failed to register user")
        if settings.ENABLE_EMAIL:
            await send_verification_email(email=user.email, token=verification_token)
        return True

    def authenticate_user(
        self,
        credentials: LoginRequest,
    ) -> dict:
        """Authenticate a user.

        This method verifies the provided user credentials against the stored user data.

        Args:
            credentials (LoginRequest): User credentials for authentication.

        Returns:
            dict: User details if authentication is successful.

        Raises:
            ValueError: If the username is missing, user does not exist,
                or credentials are invalid.
        """
        username = credentials.username
        if not username:
            raise ValueError("Username is required")
        user_details = self.mongo_connection.get_collection(settings.USER_COLLECTION).find_one(
            {"username": credentials.username}
        )
        if not user_details:
            raise ValueError("User does not exist")
        user_details = User(**user_details)
        if not pwd_context.verify(credentials.password, user_details.password):
            raise ValueError("Invalid credentials")
        token_data = user_details.model_dump(
            exclude={
                "password",
                "created_at",
                "updated_at",
            }
        )
        return token_data

    async def verify_user_email(self, token: str) -> JSONResponse:
        """Verify a user's email.

        Args:
            token (str): Verification token.

        Returns:
            JSONResponse: Verification status message.
        """
        db_token = self.mongo_connection.get_collection(
            settings.ACTIVATION_KEY_COLLECTION
        ).find_one({"token": token})
        if not db_token:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"error": "Token not found"},
            )
        db_user = self.mongo_connection.get_collection(settings.USER_COLLECTION).find_one(
            {"email": db_token["email"]}
        )
        if not db_user:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"error": "User not found"},
            )
        self.mongo_connection.get_collection(settings.ACTIVATION_KEY_COLLECTION).delete_one(
            {"token": token}
        )
        self.mongo_connection.get_collection(settings.USER_COLLECTION).update_one(
            {"email": db_token["email"]},
            {
                "$set": {
                    "verified": True,
                    "updated_at": datetime.now(timezone.utc),
                }
            },
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Email verified successfully"},
        )
