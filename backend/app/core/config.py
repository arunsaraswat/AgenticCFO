"""Application configuration management."""
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Attributes:
        app_name: Name of the application
        debug: Debug mode flag
        database_url: PostgreSQL database connection string
        secret_key: Secret key for JWT encoding
        algorithm: Algorithm used for JWT encoding
        access_token_expire_minutes: JWT token expiration time
        cors_origins: List of allowed CORS origins
    """

    app_name: str = Field(default="AgenticCFO", env="APP_NAME")
    debug: bool = Field(default=False, env="DEBUG")
    database_url: str = Field(..., env="DATABASE_URL")
    test_database_url: str = Field(default="", env="TEST_DATABASE_URL")
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    cors_origins: str = Field(default="http://localhost:5173", env="CORS_ORIGINS")

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins string into list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()
