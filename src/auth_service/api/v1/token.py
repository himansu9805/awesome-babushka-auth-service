"""Routers for token management."""

from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth_service.db.enums import TokenType
from auth_service.services.token import TokenService

token_router = APIRouter(prefix="/token", tags=["token"])
token_service = TokenService()

security = HTTPBearer()


@token_router.get("/validate")
async def validate_token(
    access_token: HTTPAuthorizationCredentials = Depends(security),
):
    """This route validates a user's token.

    ### Args:
    - **access_token** (`HTTPAuthorizationCredentials`): The access token.

    ### Returns:
    - **JSONResponse**: The validation status.
    """
    result = await token_service.validate_token(access_token, expected_type=TokenType.BEARER)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=result,
    )


@token_router.get("/refresh")
async def refresh_access_token(
    request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """This route refreshes a user's access token.

    ### Args:
    - **refresh_token** (`HTTPAuthorizationCredentials`): The refresh token.

    ### Returns:
    - **dict**: The new access token.
    """
    refresh_token = credentials.credentials

    device_info = request.headers.get("User-Agent", "unknown")
    ip_address = request.client.host if request.client else "unknown"
    return await token_service.refresh_access_token(
        refresh_token, device_info=device_info, ip_address=ip_address
    )
 