import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Settings(BaseModel):
    """Application settings loaded from environment variables and the .env file."""

    PROJECT_NAME: str = Field(default="VisionGuide AI Backend")
    API_VERSION: str = Field(default="v1")
    FIREBASE_SERVICE_ACCOUNT_PATH: str = Field(default=str(BASE_DIR / "serviceAccountKey.json"))
    FIREBASE_WEB_API_KEY: str = Field(default="")
    FIREBASE_PROJECT_ID: str = Field(default="")
    ALLOWED_ORIGINS: list[str] = Field(default_factory=lambda: ["*"])

    @classmethod
    def from_env(cls) -> "Settings":
        """Build settings from the process environment and .env values."""
        raw_values: dict[str, Any] = {
            "PROJECT_NAME": os.getenv("PROJECT_NAME", "VisionGuide AI Backend"),
            "API_VERSION": os.getenv("API_VERSION", "v1"),
            "FIREBASE_SERVICE_ACCOUNT_PATH": os.getenv(
                "FIREBASE_SERVICE_ACCOUNT_PATH",
                str(BASE_DIR / "serviceAccountKey.json"),
            ),
            "FIREBASE_WEB_API_KEY": os.getenv("FIREBASE_WEB_API_KEY", ""),
            "FIREBASE_PROJECT_ID": os.getenv("FIREBASE_PROJECT_ID", ""),
            "ALLOWED_ORIGINS": [
                item.strip()
                for item in os.getenv("ALLOWED_ORIGINS", "*").split(",")
                if item.strip()
            ],
        }
        return cls(**raw_values)


settings = Settings.from_env()
