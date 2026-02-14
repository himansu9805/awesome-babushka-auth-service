"""Token core functionalities."""

import uuid
from datetime import datetime, timedelta, timezone

from commons import MongoConnect
from jose import jwt

from auth_service.core.config import settings
from auth_service.db.enums import TokenType


class TokenUtils:
    """Utility class for token operations."""

    @staticmethod
    def create_token(
        data: dict,
        token_type: TokenType,
        token_family: str | None = None,
    ) -> tuple[TokenType, str, dict]:
        """
        Create token of specified type.

        **Access Tokens:** These tokens are short-lived and are used to authenticate
        user requests. They typically have a short expiration time (e.g., 15 minutes
        to 1 hour) and are included in the Authorization header of HTTP requests.

        **Refresh Tokens:** These tokens are long-lived and are used to obtain new
        access tokens without requiring the user to re-authenticate. They usually
        have a longer expiration time (e.g., days to weeks) and are securely stored
        on the client side.

        Args:
            data (dict): The data to encode in the token.
            token_type (TokenType): The type of token to create.
            token_family (str | None): The token family identifier for refresh tokens.

        Returns:
            tuple[TokenType, str, dict]: The token type, the encoded token, and metadata.
        """
        username = data.get("username")
        if username is None:
            raise ValueError("username is required to create a token")
        to_encode = data.copy()
        now = datetime.now(timezone.utc)
        jti = str(uuid.uuid4())

        # Set expiration based on token type
        if token_type == TokenType.REFRESH:
            expire_minutes = settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES
        elif token_type == TokenType.BEARER:
            expire_minutes = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        else:
            raise ValueError("Invalid token type")

        expire = now + timedelta(minutes=expire_minutes)
        to_encode.update(
            {
                "iss": settings.JWT_ISSUER,
                "sub": str(username),
                "aud": settings.JWT_AUDIENCE,
                "iat": int(now.timestamp()),
                "exp": int(expire.timestamp()),
                "jti": jti,
                "token_type": token_type.value,
            }
        )
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_PRIVATE_KEY, algorithm=settings.JWT_ALGORITHM
        )
        metadata = {
            "jti": jti,
            "token_family": token_family,
            "expires_at": expire,
            "username": str(username),
        }

        return token_type, encoded_jwt, metadata

    @staticmethod
    def create_access_token(data: dict) -> str:
        """Create an access token.

        Args:
            data (dict): The data to encode in the token.

        Returns:
            str: The encoded access token.
        """
        _, access_token, _ = TokenUtils.create_token(data, TokenType.BEARER)
        return access_token

    @staticmethod
    def create_refresh_token(data: dict) -> tuple[str, dict]:
        """Create a refresh token.

        Args:
            data (dict): The data to encode in the token.

        Returns:
            tuple[str, dict]: The encoded refresh token and metadata.
        """
        _, refresh_token, metadata = TokenUtils.create_token(data, TokenType.REFRESH)
        return refresh_token, metadata

    @staticmethod
    def decode_token(token: str, expected_type: TokenType) -> dict:
        """Validate and decode a token.

        Args:
            token (str): The token to decode.
            expected_type (TokenType): The expected type of the token.

        Returns:
            dict: The decoded token data.

        Raises:
            jwt.InvalidTokenError: If the token is invalid or does not
                match the expected type.
            ValueError: If the token type does not match the expected type.
        """
        payload = jwt.decode(
            token,
            settings.JWT_PUBLIC_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            audience=settings.JWT_AUDIENCE,
            issuer=settings.JWT_ISSUER,
        )

        if payload.get("token_type") != expected_type.value:
            raise ValueError(
                f"Invalid token type. Expected {expected_type.value}, "
                f"got {payload.get('token_type')}"
            )

        return payload
