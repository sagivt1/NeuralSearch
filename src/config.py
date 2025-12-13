from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "neuralsearch API"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Load settings from a .env file.
    # `extra="ignore"` prevents errors if extra env vars are present.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Cache the settings object to avoid re-reading the .env file on every call.
# This is a performance optimization.
@lru_cache()
def get_settings():
    return Settings()