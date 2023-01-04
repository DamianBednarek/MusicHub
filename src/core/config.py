import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "MusicHub"

    # website link
    LINK: str = "http://localhost:8000/"
    # Storage link
    STORAGE_LINK: str = "https://musichubstorage.s3.eu-central-1.amazonaws.com"

    # JWT
    DEFAULT_TOKEN_EXPIRATION_TIME: int = 30
    SECRET_KEY: str = os.getenv("JWT_KEY")
    ALGORITHM: str = "HS256"

    # Database connection
    SQL_USER: str = os.getenv("SQL_USER", "postgres")
    SQL_PASSWORD: str = os.getenv("SQL_PASSWORD", "postgres")
    SQL_DB_NAME: str = os.getenv("SQL_NAME", "postgres")
    DATABASE_URL: str = (
        f"postgresql://{SQL_USER}:{SQL_PASSWORD}@localhost/{SQL_DB_NAME}"
    )

    # Email provider
    EMAIL_USERNAME: str = os.getenv("EMAIL_USERNAME", "apikey")
    EMAIL_PASSWORD: str = os.getenv("DJANGO_EMAIL_KEY")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "musichub.itechart@gmail.com")
    EMAIL_PORT: int = os.getenv("EMAIL_PORT", 587)
    EMAIL_SERVER: str = os.getenv("EMAIL_SERVER", "smtp.sendgrid.com")
    MAIL_STARTTLS: bool = os.getenv("MAIL_STARTTLS", False)
    MAIL_SSL_TLS: bool = os.getenv("MAIL_SSL_TLS", False)

    # Boto3
    AWS_ACCESS_KEY_ID: str = os.getenv("DJANGO_AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("DJANGO_AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME: str = "musichubstorage"

    # Google OAuth2
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET")
    SESSION_KEY: str = os.getenv("SESSION_KEY")

    # ANTIVIRUS
    ANTIVIRUS_API_KEY: str = os.getenv("ANTIVIRUS_API_KEY")


settings = Settings()
