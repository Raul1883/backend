from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    CLIENT_URL:str
    DB_URL: str = "sqlite+aiosqlite:///./data/database.db"

    SECRET_KEY: str  # генерируем: openssl rand -hex 32
    REG_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Cookie
    COOKIE_SECURE: bool = False  # True в production (HTTPS)
    COOKIE_HTTPONLY: bool = True
    COOKIE_SAMESITE: str = "lax"


    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    


config = Config()
