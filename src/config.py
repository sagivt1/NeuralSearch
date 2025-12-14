from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    APP_NAME: str = "neuralsearch API"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Pydantic settings configuration.
    # Loads from a .env file and ignores extra environment variables.
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"),
        extra="ignore",
        env_file_encoding="utf-8"
    )

# Cache settings to avoid re-reading the .env file on every request.
@lru_cache()
def get_settings():
    return Settings()
