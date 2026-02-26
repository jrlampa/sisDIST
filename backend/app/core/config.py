from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "sisDIST"
    app_version: str = "1.0.0"
    environment: str = "development"
    secret_key: str = "dev-secret-change-in-production"
    database_url: str = "postgresql+asyncpg://sisdist:sisdist_pass@localhost:5432/sisdist"
    redis_url: str = "redis://localhost:6379/0"

    # External APIs
    overpass_url: str = "https://overpass-api.de/api/interpreter"
    opentopodata_url: str = "https://api.opentopodata.org/v1/srtm90m"

    # CORS
    allowed_origins: list[str] = ["http://localhost:5173", "http://localhost:80", "http://localhost"]

    # Cache TTL seconds
    osm_cache_ttl: int = 3600
    elevation_cache_ttl: int = 86400

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
