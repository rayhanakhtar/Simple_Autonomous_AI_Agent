"""Application configuration loaded from environment variables."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Central configuration for the autonomous agent application."""

    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
    OUTPUT_DIRECTORY: str = os.getenv("OUTPUT_DIRECTORY", "output")
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "2"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def validate(cls) -> None:
        """Ensure required configuration values are present."""
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set. Check your .env file.")


config = Config()
