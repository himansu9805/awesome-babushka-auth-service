"""Service for handling user endpoint related operations."""

import re
import logging

from commons.database import MongoConnect
from fastapi import status
from fastapi.exceptions import HTTPException

from auth_service.core.config import settings
from auth_service.db.models import BasicUserInfo

logger = logging.getLogger(__file__)


class UserService:
    """User service class."""

    def __init__(self):
        """Initialize the UserService class."""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        self.mongo_connection = MongoConnect(
            settings.MONGO_URI, settings.DB_NAME
        )

    def __del__(self):
        """Cleanup the connections."""
        self.mongo_connection.close()

    def get_user(self, username: str) -> BasicUserInfo:
        """Get basic information for a given username.

        Args:
            username (str): Username for basic information

        Returns:
            BasicUserInfo: Basic information for the username, if available
        """
        user_details = self.mongo_connection.get_collection(
            settings.USER_COLLECTION
        ).find_one({"username": re.escape(username)})
        if not user_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User does not exists",
            )
        return BasicUserInfo(**user_details)
