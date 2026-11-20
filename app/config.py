
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    APP_NAME: str = "Enterprise Knowledge Assistant"

    API_KEY: str = "my-secret-api-key"

    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = "meta-llama/llama-3.3-70b-instruct:free"
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    DATA_DIR: str = str(BASE_DIR / "data" / "policies")
    INDEX_DIR: str = str(BASE_DIR / "data" / "processed")

    SCORE_THRESHOLD: float = 0.35
    CONTEXT_TOKEN_BUDGET: int = 3000
    DEFAULT_TOP_K: int = 4

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()


def get_settings():
    return settings
