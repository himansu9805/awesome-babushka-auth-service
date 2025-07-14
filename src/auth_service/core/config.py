"""Configuration settings for the auth service"""

import os


class Settings:
    """Configuration settings for the auth service"""

    def __init__(self):
        # pylint: disable=invalid-name

        # ------------- MongoDB Config -------------
        self.MONGO_URI: str = os.getenv(
            "MONGO_URI",
            "mongodb://172.17.0.1:27017/?directConnection=true&"
            "serverSelectionTimeoutMS=2000&appName=mongosh+2.3.9",
        )
        self.DB_NAME: str = os.getenv("DB_NAME", "test")
        self.USER_COLLECTION: str = os.getenv("USER_COLLECTION", "users")
        self.TOKEN_COLLECTION: str = os.getenv("TOKEN_COLLECTION", "tokens")
        # ------------- MongoDB Config -------------

        # ------------- JWT Config -------------
        self.SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "secret_key")
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
            os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")
        )
        self.ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
        # ------------- JWT Config -------------

        # ------------- Email Config -------------
        self.ENABLE_EMAIL: bool = (
            os.getenv("ENABLE_EMAIL", "false").lower() == "true"
        )
        self.NO_REPLY_EMAIL: str = os.getenv(
            "NO_REPLY_EMAIL", "noreply@awesomebabushka.com"
        )
        self.SMTP_HOST: str = os.getenv("SMTP_HOST", "172.18.0.1")
        self.SMTP_PORT: int = int(os.getenv("SMTP_PORT", "1025"))
        self.HOST_NAME: str = "localhost:8000"
        # ------------- Email Config -------------


settings = Settings()
