"""Routes for the auth service"""

from auth_service.db.schemas import UserCreate
from auth_service.db.schemas import UserLogin
from auth_service.services.auth import AuthService
from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

auth_router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = AuthService()


@auth_router.post("/register")
async def register(user: UserCreate):
    """This route registers a new user.

    ### Args:
    - **user** (`UserCreate`): The user to register.

    ### Returns:
    - **dict**: The registered user.
    """
    return await auth_service.register_user(user)


@auth_router.post("/login")
def login(user: UserLogin):
    """This route logs in a user.

    ### Args:
    - **user** (`UserLogin`): The user to log in.

    ### Returns:
    - **dict**: The access token.
    """
    return auth_service.authenticate_user(user)


@auth_router.get("/verify")
async def verify_email(token: str):
    """This route verifies a user's email.

    ### Args:
    - **token** (`str`): The verification token.

    ### Returns:
    - **dict**: The verification status.
    """

    return await auth_service.verify_user_email(token)


@auth_router.get("/logout")
async def logout(
    access_token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    """This route logs out a user.

    ### Returns:
    - **dict**: The logout status.
    """
    return await auth_service.logout_user(access_token)
