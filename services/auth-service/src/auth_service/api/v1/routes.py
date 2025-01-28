""" Routes for the auth service """

from auth_service.db.schemas import UserCreate
from auth_service.db.schemas import UserLogin
from auth_service.services.auth import authenticate_user
from auth_service.services.auth import register_user
from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register")
def register(user: UserCreate):
    """This route registers a new user.

    ### Args:
    - **user** (`UserCreate`): The user to register.

    ### Returns:
    - **dict**: The registered user.
    """
    return register_user(user)


@auth_router.post("/login")
def login(user: UserLogin):
    """This route logs in a user.

    ### Args:
    - **user** (`UserLogin`): The user to log in.

    ### Returns:
    - **dict**: The access token.
    """
    return authenticate_user(user)
