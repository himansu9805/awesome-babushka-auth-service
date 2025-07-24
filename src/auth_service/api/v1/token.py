"""Routers for token management."""

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth_service.services.token import TokenService

token_router = APIRouter(prefix="/token", tags=["token"])
token_service = TokenService()


@token_router.get("/validate")
async def validate_token(
    access_token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    """This route validates a user's token.

    ### Args:
    - **access_token** (`HTTPAuthorizationCredentials`): The access token.

    ### Returns:
    - **JSONResponse**: The validation status.
    """
    result = await token_service.validate_token(access_token)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=result,
    )


@token_router.get("/refresh")
async def refresh_access_token(
    refresh_token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    """This route refreshes a user's access token.

    ### Args:
    - **refresh_token** (`HTTPAuthorizationCredentials`): The refresh token.

    ### Returns:
    - **dict**: The new access token.
    """
    return await token_service.refresh_access_token(refresh_token)
