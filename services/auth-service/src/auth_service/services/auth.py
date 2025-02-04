""" Service for handling authentication. """

from uuid import uuid4

from auth_service.core.security import create_access_token
from auth_service.db.database import SessionLocal
from auth_service.db.models import User
from auth_service.db.models import VerificationToken
from auth_service.db.schemas import UserCreate
from auth_service.db.schemas import UserLogin
from auth_service.services.email_agent import send_verification_email
from fastapi.responses import JSONResponse
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def register_user(user: UserCreate):
    """Register a new user."""
    db = SessionLocal()
    hashed_password = pwd_context.hash(user.password)
    verification_token = uuid4().hex
    db_user = User(
        username=user.username, email=user.email, password=hashed_password
    )
    db.add(db_user)
    db_token = VerificationToken(
        email=user.email,
        token=verification_token,
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_user)
    db.refresh(db_token)
    await send_verification_email(email=user.email, token=verification_token)
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


async def verify_user_email(token: str):
    """Verify a user's email."""
    db = SessionLocal()
    db_token = (
        db.query(VerificationToken)
        .filter(VerificationToken.token == token)
        .first()
    )
    if not db_token:
        return JSONResponse(
            status_code=404, content={"error": "Token not found"}
        )
    db_user = db.query(User).filter(User.email == db_token.email).first()
    if not db_user:
        return JSONResponse(
            status_code=404, content={"error": "User not found"}
        )
    db.delete(db_token)
    db_user.verified = 1
    db.commit()
    return JSONResponse(
        status_code=200,
        content={"message": "Email verified successfully"},
    )
