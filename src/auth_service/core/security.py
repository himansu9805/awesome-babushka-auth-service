"""Security utilities"""

from datetime import datetime
from datetime import timedelta
from datetime import timezone

from auth_service.core.config import settings
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password.

    Args:
        plain_password (str): The plain password.
        hashed_password (str): The hashed password.

    Returns:
        bool: Whether the passwords match.
    """
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    """Hash a password.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def create_access_token(data: dict) -> str:
    """Create an access token.

    Args:
        data (dict): The data to encode in the token.

    Returns:
        str: The encoded token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create a refresh token.

    Args:
        data (dict): The data to encode in the token.

    Returns:
        str: The encoded token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_token(token: HTTPAuthorizationCredentials) -> dict:
    """Decode a token.

    Args:
        token (str): The token to decode.

    Returns:
        dict: The decoded token data.
    """
    try:
        payload = jwt.decode(
            token.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.JWTError:
        return {"error": "Invalid token"}
    except Exception:
        return {"error": "An unknown error occurred while decoding the token"}
