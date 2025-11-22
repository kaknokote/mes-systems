"""Application configuration loaded from environment variables."""
from functools import lru_cache
from pathlib import Path
import os

from dotenv import load_dotenv

# Load variables from .env if present
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")


class Settings:
    APP_NAME: str = "FastAPI CRUD API with AI"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
