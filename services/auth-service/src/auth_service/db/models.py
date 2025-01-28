""" Database models for the auth service """

from auth_service.db.database import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String


class User(Base):
    """User model"""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
