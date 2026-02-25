from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    CLIENT_URL:str
    DB_URL: str = "sqlite+aiosqlite:///./database.db"

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


config = Config()
