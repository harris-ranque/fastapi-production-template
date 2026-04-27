import secrets

from pydantic import ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    # Application
    app_name: str = "FastAPI Production Template"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = True
    log_level: str = "INFO"

    # Database
    database_url: str | None = None

    # Security
    secret_key: str = "" # Will be generated if empty
    cors_origins: list[str] = [] # Empty by default for security

    # Sentry
    sentry_dsn: str | None = None

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Generate a random secret key if not provided
        if not self.secret_key:
            self.secret_key = secrets.token_urlsafe(32)
    
settings = Settings()