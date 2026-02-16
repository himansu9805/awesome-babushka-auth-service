"""Routes for the auth service"""

from fastapi import (
    APIRouter,
    Depends,
    status,
    Request,
    HTTPException,
    Response,
)
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth_service.db.enums import TokenType
from auth_service.db.schemas import UserCreate, LoginRequest
from auth_service.services.auth import AuthService
from auth_service.services.token import (
    TokenService,
    TokenRefreshError,
    TokenReuseDetected,
)
from auth_service.core.config import settings

auth_router = APIRouter(prefix="/auth", tags=["authentication"])
auth_service = AuthService()
token_service = TokenService()

security = HTTPBearer()


@auth_router.post("/register")
async def register(user: UserCreate):
    """
    Register endpoint to create a user and sent account activation email.

    ### Args:
    - **user** (`UserCreate`): The user to register.

    ### Returns:
    - **dict**: The registered user.
    """
    try:
        response = await auth_service.register_user(user)
        if response:
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "message": "User registered successfully. "
                    "Please verify your email."
                },
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to register user",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}",
        )


@auth_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
)
async def login(
    credentials: LoginRequest, request: Request, response: Response
):
    """
    Login endpoint to authenticate a user and provide access tokens.

    ### Args:
    - **credentials** (`LoginRequest`): The user's login credentials.
    - **request** (`Request`): The incoming HTTP request.
    - **response** (`Response`): The outgoing HTTP response.

    ### Returns:
    - **dict**: The access token.
    """
    user = auth_service.authenticate_user(credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    device_info = request.headers.get("User-Agent", "unknown")
    ip_address = request.client.host if request.client else "unknown"

    token_pair = await token_service.create_token_pair(
        user_data=user,
        device_info=device_info,
        ip_address=ip_address,
    )

    response.set_cookie(
        key="refresh_token",
        value=token_pair.refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES * 60,
    )
    return {"access_token": token_pair.access_token}


@auth_router.get(
    "/refresh",
    status_code=status.HTTP_200_OK,
)
async def refresh_token(
    request: Request,
    response: Response,
):
    """
    Refresh access token using refresh token.

    ### Returns:
    - **dict**: New access and refresh tokens.

    ### Raises:
    - **HTTPException**: If token is invalid or reused.
    """
    refresh_token = request.cookies.get("refresh_token", "")
    device_info = request.headers.get("User-Agent", "unknown")
    ip_address = request.client.host if request.client else "unknown"

    try:
        new_tokens = await token_service.refresh_access_token(
            refresh_token, device_info=device_info, ip_address=ip_address
        )
        response.set_cookie(
            key="refresh_token",
            value=new_tokens.refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        )
        response.status_code = status.HTTP_200_OK
        return {"access_token": new_tokens.access_token}
    except TokenReuseDetected as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except TokenRefreshError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@auth_router.get("/logout", status_code=status.HTTP_200_OK)
async def logout(request: Request, response: Response):
    """Logout a user by revoking their access token.

    ### Returns:
    - **JSONResponse**: Logout status message.
    """
    try:
        refresh_token = request.cookies.get("refresh_token", "")
        payload = await token_service.decode_token(
            refresh_token,
            expected_type=TokenType.REFRESH,
        )

        jti = payload.get("jti", None)
        if not jti:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token",
            )
        if token_service.revoke_token(jti):
            response.delete_cookie(
                key="refresh_token",
                httponly=True,
                secure=False,
                samesite="lax",
            )
            response.status_code = status.HTTP_200_OK
            return {"message": "Successfully logged out"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token already revoked or invalid",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid token: {str(e)}",
        )
