from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CACHE_TYPE: str = "diskcache"  # or "diskcache"
    REDIS_URL: str = "redis://localhost:6379/0"
    DISKCACHE_DIR: str = "/opt/helpdesk_app/itsm/cache"

    class Config:
        env_file = ".env"

settings = Settings()
