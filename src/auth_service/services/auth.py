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
from auth_service.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from auth_service.db.models import Token, User
from auth_service.db.schemas import UserCreate, UserLogin
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
        self.mongo_connection = MongoConnect(
            settings.MONGO_URI, settings.DB_NAME
        )

    def __del__(self):
        """Close the MongoDB connection."""
        self.mongo_connection.close()

    async def register_user(self, user: UserCreate) -> JSONResponse:
        """Register a new user.

        Args:
            user (UserCreate): User details for registration.

        Returns:
            GenericResponse: Response message indicating success or failure.
        """
        try:
            hashed_password = pwd_context.hash(user.password)
            verification_token = uuid4().hex
            db_user = User(
                username=user.username,
                email=user.email,
                password=hashed_password,
            )
            self.mongo_connection.get_collection(
                settings.USER_COLLECTION
            ).insert_one(db_user.model_dump())
            db_token = Token(
                email=user.email,
                token=verification_token,
            )
            self.mongo_connection.get_collection(
                settings.TOKEN_COLLECTION
            ).insert_one(db_token.model_dump())
        except DuplicateKeyError:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"error": "User already exists"},
            )
        except Exception:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Unable to register user"},
            )
        if settings.ENABLE_EMAIL:
            await send_verification_email(
                email=user.email, token=verification_token
            )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "User registered successfully"},
        )

    def authenticate_user(
        self,
        user_request: UserLogin,
    ) -> JSONResponse:
        """Authenticate a user.

        Args:
            user (UserLogin): User credentials for authentication.

        Returns:
            JSONResponse: Access token and token type if
                authentication is successful.
            JSONResponse: Error message if authentication fails.
        """
        username = user_request.username
        if not username:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "Username is required"},
            )
        user_details = self.mongo_connection.get_collection(
            settings.USER_COLLECTION
        ).find_one({"username": user_request.username})
        if not user_details:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"error": "User does not exist"},
            )
        user_details = User(**user_details)
        if not pwd_context.verify(
            user_request.password, user_details.password
        ):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": "Invalid credentials"},
            )
        token_data = user_details.model_dump(
            exclude={
                "password",
                "created_at",
                "updated_at",
            }
        )
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        if not access_token or not refresh_token:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Internal server error"},
            )
        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content=token_data,
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
        )
        return response

    async def verify_user_email(self, token: str) -> JSONResponse:
        """Verify a user's email.

        Args:
            token (str): Verification token.

        Returns:
            JSONResponse: Verification status message.
        """
        db_token = self.mongo_connection.get_collection(
            settings.TOKEN_COLLECTION
        ).find_one({"token": token})
        if not db_token:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"error": "Token not found"},
            )
        db_user = self.mongo_connection.get_collection(
            settings.USER_COLLECTION
        ).find_one({"email": db_token["email"]})
        if not db_user:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"error": "User not found"},
            )
        self.mongo_connection.get_collection(
            settings.TOKEN_COLLECTION
        ).delete_one({"token": token})
        self.mongo_connection.get_collection(
            settings.USER_COLLECTION
        ).update_one(
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

    async def logout_user(
        self,
        access_token: HTTPAuthorizationCredentials,
    ) -> JSONResponse:
        """Logout a user.

        Returns:
            JSONResponse: Logout status message.
        """
        decoded_token = decode_token(access_token)
        if "error" in decoded_token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": decoded_token["error"]},
            )
        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "User logged out successfully"},
        )
        response.delete_cookie(key="access_token")
        response.delete_cookie(key="refresh_token")
        return response
