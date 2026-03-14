from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    PROJECT_NAME: str = "Mini AI Sales Prediction API"
    API_V1_STR: str = "/api"

    # Enable CORS for all origins in development
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    # Logging
    LOG_LEVEL: str = "INFO"

    # Database Configuration
    DATABASE_URL: str

    # JWT Settings
    SECRET_KEY: str = "super-rahasia"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


settings = Settings()
