import asyncio
import logging
from functools import lru_cache
from typing import Optional

import aiohttp
from pydantic import ValidationError, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_prefix="ETL_CLIENT_")

    source_schema: str = "http"
    source_host: str = "localhost"
    source_port: int = 8000
    source_timeout: int = 2
    source_api_key: str = "ADU8S67Ddy!d7f?"
    source_timezone: str = "UTC"
    previous_days_count: int = 7
    concurrency: int = 5
    destination_dir: str = "output"
    retry_interval: int = 1
    log_level: str = "INFO"

    @model_validator(mode="after")
    def validate_source(self) -> "Settings":
        """Validate entire settings object."""
        source_timezone = asyncio.get_event_loop().run_until_complete(self.get_source_timezone())
        if source_timezone is not None:
            self.source_timezone = source_timezone
        return self

    async def get_source_timezone(self) -> Optional[str]:
        """Check is source is available and get its timezone."""
        url = f"{self.source_schema}://{self.source_host}:{self.source_port}/status"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        raise ValueError("Data source is unavailable.")
                    headers = resp.headers
            except aiohttp.ClientError:
                raise ValueError("Data source is unavailable.")
        if source_date := headers.get("Date"):
            return source_date.split(" ")[-1]
        return None


@lru_cache
def get_settings() -> Settings:
    return Settings()
