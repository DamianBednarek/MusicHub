from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    PROJECT_NAME: str = "MusicHub"
    SECRET_KEY: str = "development"
    DEFAULT_TOKEN_EXPIRATION_TIME = 30
    SQL_USER: str = os.getenv("SQL_USER", "postgres")
    SQL_PASSWORD: str = os.getenv("SQL_PASSWORD", "postgres")
    SQL_DB_NAME: str = os.getenv("SQL_NAME", "postgres")
    DATABASE_URL: str = (
        f"postgresql://{SQL_USER}:{SQL_PASSWORD}@localhost/{SQL_DB_NAME}"
    )


settings = Settings()
