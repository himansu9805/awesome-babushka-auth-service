""" Database models for the auth service """

from datetime import datetime
from datetime import timedelta
from datetime import timezone

from auth_service.db.database import Base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String


class User(Base):
    """User model"""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    verified = Column(Integer, nullable=False, default=0)
    active = Column(Integer, nullable=False, default=1)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now(timezone.utc),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now(timezone.utc),
    )


class VerificationToken(Base):
    """Verification token model"""

    __tablename__ = "verification_tokens"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, index=True)
    token = Column(String, nullable=False)
    expires_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now(timezone.utc) + timedelta(days=1),
    )
