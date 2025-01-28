""" Configuration settings for the auth service """

import os


class Settings:
    """Configuration settings for the auth service"""

    def __init__(self):
        self.SECRET_KEY: str = os.getenv(
            "JWT_SECRET_KEY", "secret_key"
        )  # noqa
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
            os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")
        )  # noqa
        self.ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")  # noqa


settings = Settings()
