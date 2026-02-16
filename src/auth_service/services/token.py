"""Service for handling authentication."""

from dataclasses import dataclass
from commons.database import MongoConnect
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from passlib.context import CryptContext
from pymongo import ASCENDING
from datetime import datetime, timezone
from jose.exceptions import JWTError

from auth_service.core.config import settings
from auth_service.core.token import TokenUtils
from auth_service.db.enums import TokenType
from auth_service.db.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class TokenPair:
    """Dataclass for token pair."""

    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class TokenRefreshError(Exception):
    """Raised when token refresh fails."""

    pass


class TokenReuseDetected(TokenRefreshError):
    """Raised when refresh token reuse is detected."""

    pass


class TokenService:
    """Token service class."""

    def __init__(self):
        """Initialize the TokenService class."""

        self.mongo_connection = MongoConnect(
            settings.MONGO_URI, settings.DB_NAME
        )
        self._create_indexes()

    def __del__(self):
        """Close the MongoDB connection."""
        self.mongo_connection.close()

    def _create_indexes(self):
        """Create necessary indexes in the database.

        - Unique index on `jti` to ensure each token is unique.
        - Index on `username` for efficient querying of tokens by user.
        - Index on `token_family` to facilitate family revocation of tokens.
        - TTL index on `expires_at` to automatically delete expired tokens.
        - Compound index on `username` and `is_revoked` for faster queries
            related to token revocation.
        """
        refresh_tokens = self.mongo_connection.db.refresh_tokens
        refresh_tokens.create_index([("jti", ASCENDING)], unique=True)
        refresh_tokens.create_index([("username", ASCENDING)])
        refresh_tokens.create_index([("token_family", ASCENDING)])
        refresh_tokens.create_index(
            [("expires_at", ASCENDING)], expireAfterSeconds=0
        )
        refresh_tokens.create_index(
            [("username", ASCENDING), ("is_revoked", ASCENDING)]
        )

    async def decode_token(
        self,
        token: str,
        expected_type: TokenType,
    ) -> dict:
        """Decode and validate a token.

        Args:
            token (str): The token to decode.
            expected_type (TokenType): The expected type of the token.

        Returns:
            dict: The decoded token data.

        Raises:
            ValueError: If the token is invalid.
        """
        try:
            decoded_token = TokenUtils.decode_token(
                token=token,
                expected_type=expected_type,
            )
            return decoded_token
        except JWTError as e:
            raise ValueError(f"Invalid token: {str(e)}")

    async def validate_token(
        self,
        auth_credentials: HTTPAuthorizationCredentials,
        expected_type: TokenType,
    ) -> dict:
        """Validate a token.

        Args:
            auth_credentials (HTTPAuthorizationCredentials): Auth credentials.

        Returns:
            dict: Validation status and user details.

        Raises:
            HTTPException: If the token is invalid or user does not exist.
        """
        decoded_token = TokenUtils.decode_token(
            token=auth_credentials.credentials, expected_type=expected_type
        )
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

    async def create_token_pair(
        self,
        user_data: dict,
        device_info: str | None = None,
        ip_address: str | None = None,
    ) -> TokenPair:
        """Create a pair of access and refresh tokens.

        Args:
            user_data (dict): The user data to encode in the tokens.
            device_info (str | None): Device information.
            ip_address (str | None): IP address.

        Returns:
            TokenPair: The access and refresh tokens.
        """
        access_token = TokenUtils.create_access_token(user_data)
        refresh_token, metadata = TokenUtils.create_refresh_token(user_data)
        token_doc = {
            "jti": metadata["jti"],
            "username": metadata["username"],
            "token_family": metadata["token_family"],
            "expires_at": metadata["expires_at"],
            "created_at": datetime.now(timezone.utc),
            "is_revoked": False,
            "used_at": None,
            "device_info": device_info,
            "ip_address": ip_address,
        }

        # Insert refresh token document
        self.mongo_connection.db.refresh_tokens.insert_one(token_doc)

        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def refresh_access_token(
        self,
        refresh_token: str,
        device_info: str | None = None,
        ip_address: str | None = None,
    ) -> TokenPair:
        """Refresh access token using refresh token with rotation.

        Args:
            refresh_token (str): The refresh token.
            device_info (str | None): Device information.
            ip_address (str | None): IP address.

        Returns:
            TokenPair: New access and refresh tokens.
        """
        try:
            payload = TokenUtils.decode_token(refresh_token, TokenType.REFRESH)
        except JWTError:
            raise TokenRefreshError("Refresh token has expired or is invalid")

        if payload.get("token_type") != TokenType.REFRESH.value:
            raise TokenRefreshError("Invalid token type for refresh")

        jti = payload.get("jti")
        token_family = payload.get("token_family")
        username = payload.get("sub")

        db_token = self.mongo_connection.db.refresh_tokens.find_one(
            {"jti": jti}
        )
        if not db_token:
            raise TokenRefreshError("Refresh token not found")

        if db_token.get("used_at") is not None or db_token.get("is_revoked"):
            await self.revoke_token_family(token_family)
            raise TokenReuseDetected(
                "Refresh token reuse detected. All tokens in this family have "
                "been revoked. Please login again."
            )

        expires_at = db_token["expires_at"]
        if isinstance(expires_at, datetime) and expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        if datetime.now(timezone.utc) > expires_at:
            self.mongo_connection.db.refresh_tokens.update_one(
                {"jti": jti}, {"$set": {"is_revoked": True}}
            )
            raise TokenRefreshError("Refresh token has expired")

        self.mongo_connection.db.refresh_tokens.update_one(
            {"jti": jti},
            {
                "$set": {
                    "used_at": datetime.now(timezone.utc),
                    "device_id": device_info,
                    "ip_address": ip_address,
                }
            },
        )

        user_data = {"username": username}
        token_pair = await self.create_token_pair(
            user_data=user_data,
            device_info=device_info,
            ip_address=ip_address,
        )

        # Revoke the old refresh token
        self.mongo_connection.db.refresh_tokens.update_one(
            {"jti": jti}, {"$set": {"is_revoked": True}}
        )

        return token_pair

    async def revoke_token(self, jti: str) -> bool:
        """Revoke a refresh token by its JTI.

        Args:
            jti (str): The JTI of the token to revoke.

        Returns:
            bool: True if the token was successfully revoked, False otherwise.
        """
        result = self.mongo_connection.db.refresh_token.update_one(
            {"jti": jti}, {"$set": {"is_revoked": True}}
        )
        return result.modified_count > 0

    async def revoke_token_family(self, token_family: str) -> int:
        """Revoke all tokens in a token family.

        Args:
            token_family (str): The token family identifier.

        Returns:
            int: The number of tokens revoked.
        """
        result = self.mongo_connection.db.refresh_tokens.update_many(
            {"token_family": token_family, "is_revoked": False},
            {"$set": {"is_revoked": True}},
        )
        return result.modified_count

    async def revoke_all_user_tokens(self, username: str) -> int:
        """Revoke all refresh tokens for a specific user.

        Args:
            username (str): The user ID whose tokens are to be revoked.

        Returns:
            int: The number of tokens revoked.
        """
        result = self.mongo_connection.db.refresh_tokens.update_many(
            {"username": username, "is_revoked": False},
            {"$set": {"is_revoked": True}},
        )
        return result.modified_count
