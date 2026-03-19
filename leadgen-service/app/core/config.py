from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "LeadGen Service"
    environment: Literal["dev", "test", "prod"] = "dev"
    api_prefix: str = ""
    database_url: str = Field(default="sqlite:///./leadgen.db")
    redis_url: str = Field(default="redis://redis:6379/0")
    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"
    request_timeout_seconds: int = 20
    user_agent: str = "leadgen-service/0.1"
    exports_dir: Path = Path("exports")
    allow_playwright_fallback: bool = True


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    settings = Settings()
    settings.exports_dir.mkdir(parents=True, exist_ok=True)
    return settings
