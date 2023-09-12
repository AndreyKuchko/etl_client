from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_prefix="ETL_CLIENT_")

    source_schema: str = "http"
    source_host: str = "localhost"
    source_port: int = 8000
    source_timeout: int = 2
    source_api_key: str = "ADU8S67Ddy!d7f?"
    previous_days_count: int = 7
    concurrency: int = 5
    destination_dir: str = "output"
    default_server_timezone: str = "Europe/Berlin"
    retry_interval: int = 1
    log_level: str = "INFO"


settings = Settings()
