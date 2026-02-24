"""Routes for user endpoint."""

from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
)
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth_service.db.enums import TokenType
from auth_service.services.user import UserService
from auth_service.services.token import TokenService
from auth_service.db.schemas import UserUpdate

user_router = APIRouter(prefix="/user", tags=["user"])
user_service = UserService()
token_service = TokenService()

security = HTTPBearer()


@user_router.get("/me")
async def get_user_profile(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Get user information based on the access token.

    ### Args:
    - **credentials** (`HTTPAuthorizationCredentials`): The bearer token
        credentials.

    ### Returns:
    - **BasicUserInfo**: User information.
    """
    try:
        bearer_token = credentials.credentials
        payload = await token_service.decode_token(
            bearer_token, expected_type=TokenType.BEARER
        )
        username = payload.get("username")
        if not username:
            raise ValueError("unable to extract username from token")
        return user_service.get_user(username=username)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid token: {str(e)}",
        )


@user_router.patch("/me")
async def update_user_profile(
    update_request: UserUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Update user profile information.

    ### Args:
    - **update_request** (`UserUpdate`): Update request
    - **credentials** (`HTTPAuthorizationCredentials`): The bearer token
        credentials.

    ### Returns:
    - **BasicUserInfo**: User information.
    """
    try:
        bearer_token = credentials.credentials
        payload = await token_service.decode_token(
            bearer_token, expected_type=TokenType.BEARER
        )
        username = payload.get("username")
        if not username:
            raise ValueError("unable to extract username from token")
        return user_service.update_user(
            username=username,
            update_request=update_request,
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid token: {str(e)}",
        )
