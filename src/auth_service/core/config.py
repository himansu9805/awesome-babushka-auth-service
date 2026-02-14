"""Configuration settings for the auth service"""

import os


class Settings:
    """Configuration settings for the auth service"""

    def __init__(self):
        # pylint: disable=invalid-name

        # ------------- MongoDB Config -------------
        self.MONGO_URI: str = os.getenv(
            "MONGO_URI",
            "mongodb://172.29.62.30:27017/?directConnection=true&"
            "serverSelectionTimeoutMS=2000&appName=mongosh+2.3.9",
        )
        self.DB_NAME: str = os.getenv("DB_NAME", "test")
        self.USER_COLLECTION: str = os.getenv("USER_COLLECTION", "users")
        self.ACTIVATION_KEY_COLLECTION: str = os.getenv(
            "ACTIVATION_KEY_COLLECTION", "activation_keys"
        )
        # ------------- MongoDB Config -------------

        # ------------- JWT Config -------------
        with open(
            "/home/himansu/workspace/awesome-babushka-auth-service/.keys/private.pem"
        ) as key_file:
            self.JWT_PRIVATE_KEY: str = key_file.read()
        with open(
            "/home/himansu/workspace/awesome-babushka-auth-service/.keys/public.pem"
        ) as key_file:
            self.JWT_PUBLIC_KEY: str = key_file.read()
        self.JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
            os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")
        )
        self.JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = int(
            os.getenv("JWT_REFRESH_TOKEN_EXPIRE_MINUTES", "43200")
        )
        self.JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "RS256")
        self.JWT_ISSUER: str = os.getenv("JWT_ISSUER", "awesome-babushka-auth-service")
        self.JWT_AUDIENCE: str = os.getenv("JWT_AUDIENCE", "awesome-babushka-users")
        # ------------- JWT Config -------------

        # ------------- Email Config -------------
        self.ENABLE_EMAIL: bool = os.getenv("ENABLE_EMAIL", "false").lower() == "true"
        self.NO_REPLY_EMAIL: str = os.getenv("NO_REPLY_EMAIL", "noreply@awesomebabushka.com")
        self.SMTP_HOST: str = os.getenv("SMTP_HOST", "172.18.0.1")
        self.SMTP_PORT: int = int(os.getenv("SMTP_PORT", "1025"))
        self.HOST_NAME: str = "localhost:8000"
        # ------------- Email Config -------------


settings = Settings()
