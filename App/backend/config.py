# backend/config.py
from functools import lru_cache
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or .env file.
    """
    YAHOO_CONSUMER_KEY: str
    YAHOO_CONSUMER_SECRET: str
    YAHOO_REDIRECT_URI: str
    YAHOO_LEAGUE_ID: str
    YAHOO_GAME_CODE: str
    # Access token and refresh token are managed by YFPy, but can be loaded if present
    YAHOO_ACCESS_TOKEN: str = ""
    YAHOO_REFRESH_TOKEN: str = ""


    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Using lru_cache to ensure settings are loaded only once.
# Source: FastAPI Settings and Environment Variables, 'Creating the Settings Only Once with lru_cache'
@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached instance of the Settings object.
    """
    return Settings()
