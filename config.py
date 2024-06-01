from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRY_MINUTES: int  # Should be an integer

    model_config = SettingsConfigDict(env_file=".env")

class Config:
    DB_CONFIG = "postgresql://{}:{}@{}/{}"

@lru_cache()
def get_settings():
    return Settings()

