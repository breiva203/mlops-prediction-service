from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application configuration.
    Loaded from environment variables or .env file.
    """

    # =========================
    # Application Metadata
    # =========================
    app_name: str = "MLOps Prediction Service"
    version: str = "1.0.0"
    debug: bool = False

    # =========================
    # Model Configuration
    # =========================
    model_name: str = "dummy-model"
    model_version: str = "1.0"

    # =========================
    # Infrastructure (Future Ready)
    # =========================
    # database_url: str | None = None
    # redis_url: str | None = None
    # log_level: str = "INFO"

    # ✅ Modern Pydantic v2 configuration
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignore unknown env variables safely
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Load settings once and cache them.
    Prevents re-reading environment variables repeatedly.
    """
    return Settings()