"""Service for handling authentication."""

from commons.database import MongoConnect
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials
from passlib.context import CryptContext

from auth_service.core.config import settings
from auth_service.core.security import create_access_token, decode_token
from auth_service.db.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenService:
    """Token service class."""

    def __init__(self):
        """Initialize the TokenService class."""

        self.mongo_connection = MongoConnect(
            settings.MONGO_URI, settings.DB_NAME
        )

    def __del__(self):
        """Close the MongoDB connection."""
        self.mongo_connection.close()

    async def validate_token(
        self,
        access_token: HTTPAuthorizationCredentials,
    ) -> dict:
        """Validate a token.

        Args:
            access_token (HTTPAuthorizationCredentials): Access token.

        Returns:
            dict: Validation status and user details.

        Raises:
            HTTPException: If the token is invalid or user does not exist.
        """
        decoded_token = decode_token(access_token)
        if "error" in decoded_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=decoded_token["error"],
            )
        user_details = self.mongo_connection.get_collection(
            settings.USER_COLLECTION
        ).find_one({"username": decoded_token["username"]})
        if not user_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User does not exist",
            )
        user_details = User(**user_details)
        return {
            "valid": True,
            "user": user_details.model_dump(
                exclude={
                    "password",
                    "created_at",
                    "updated_at",
                }
            ),
        }

    async def refresh_access_token(
        self,
        refresh_token: HTTPAuthorizationCredentials,
    ) -> JSONResponse:
        """Refresh a token.

        Args:
            refresh_token (HTTPAuthorizationCredentials): Refresh token.

        Returns:
            JSONResponse: New access token.
        """
        decoded_token = decode_token(refresh_token)
        if "error" in decoded_token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": decoded_token["error"]},
            )
        user_details = self.mongo_connection.get_collection(
            settings.USER_COLLECTION
        ).find_one({"username": decoded_token["username"]})
        if not user_details:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"error": "User does not exist"},
            )
        user_details = User(**user_details)
        token_data = user_details.model_dump(
            exclude={
                "password",
                "created_at",
                "updated_at",
            }
        )
        access_token = create_access_token(token_data)
        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "access_token": access_token,
                "token_type": "bearer",
            },
        )
        response.set_cookie(key="access_token", value=access_token)
        return response
