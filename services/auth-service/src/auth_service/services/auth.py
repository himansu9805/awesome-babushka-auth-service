""" Service for handling authentication. """

from auth_service.core.security import create_access_token
from auth_service.db.database import SessionLocal
from auth_service.db.models import User
from auth_service.db.schemas import UserCreate
from auth_service.db.schemas import UserLogin
from fastapi.responses import JSONResponse
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def register_user(user: UserCreate):
    """Register a new user."""
    db = SessionLocal()
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username, email=user.email, password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {
        "message": "User registered successfully",
    }


def authenticate_user(user: UserLogin):
    """Authenticate a user."""
    db = SessionLocal()
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        return JSONResponse(
            status_code=401, content={"error": "Invalid credentials"}
        )
    if not pwd_context.verify(user.password, db_user.password):
        return JSONResponse(
            status_code=401, content={"error": "Invalid credentials"}
        )
    access_token = create_access_token(data={"sub": db_user.username})
    if not access_token:
        return JSONResponse(
            status_code=500, content={"error": "Internal server error"}
        )
    return JSONResponse(
        status_code=200,
        content={"access_token": access_token, "token_type": "bearer"},
    )
