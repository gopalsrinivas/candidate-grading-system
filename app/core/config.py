from pydantic_settings import BaseSettings
from .logging_config import logger


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    DEBUG: bool
    ALLOWED_HOSTS: str
    CORS_ORIGINS: str
    ENVIRONMENT: str

    class Config:
        env_file = ".env"


settings = Settings()
