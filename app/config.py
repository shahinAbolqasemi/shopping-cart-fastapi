from pydantic import BaseSettings
from typing import Optional
from functools import lru_cache
from pathlib import Path


@lru_cache
def get_env_path() -> Path:
    env_path = Path(__file__).parent.parent / ".env"
    return env_path


class Settings(BaseSettings):
    """
    Settings for the application.
    """

    cart_path_prefix: Optional[str] = ""
    # Authentication
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # Database
    # TODO: Add database settings

    # Logging
    LOG_LEVEL: str = "DEBUG"

    class Config:
        env_file = get_env_path()


@lru_cache()
def get_settings():
    return Settings()
