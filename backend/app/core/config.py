"""
Application configuration via pydantic-settings.

Reads from environment variables and .env file.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized application settings with type validation."""

    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # [ES] Aplicación / [EN] Application
    APP_NAME: str = "cornelio-api"
    APP_ENV: str = "development"
    APP_DEBUG: bool = False
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    APP_SECRET_KEY: str = ""
    APP_ALLOWED_ORIGINS: str = "http://localhost:3000"

    # [ES] Base de datos / [EN] Database
    DATABASE_URL: str = ""
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10

    # [ES] Redis / [EN] Redis
    REDIS_URL: str = ""

    # [ES] JWT / [EN] JWT
    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # [ES] MLX / [EN] MLX
    MLX_MODEL_PATH: str = ""
    MLX_MODEL_CACHE_DIR: str = ""
    MLX_MAX_TOKENS: int = 512
    MLX_TEMPERATURE: float = 0.7
    MLX_DEVICE: str = ""

    # [ES] HuggingFace / [EN] HuggingFace
    HUGGINGFACE_TOKEN: str = ""

    # [ES] Carga de archivos / [EN] File uploads
    MAX_UPLOAD_SIZE_MB: int = 50
    UPLOAD_DIR: str = "uploads"

    # [ES] RAG / Base Vectorial / [EN] RAG / Vector Store
    CHROMA_PERSIST_DIR: str = "chroma_data"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # [ES] Registro de logs / [EN] Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    @property
    def allowed_origins_list(self) -> list[str]:
        """Parse comma-separated CORS origins into a list."""
        return [origin.strip() for origin in self.APP_ALLOWED_ORIGINS.split(",") if origin.strip()]


settings = Settings()
