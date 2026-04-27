from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "API Raizes do Nordeste"
    app_version: str = "0.1.0"
    environment: str = "development"
    database_url: str = "sqlite:///./raizes_do_nordeste.db"
    secret_key: str = "altere-esta-chave-no-ambiente-local"
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
