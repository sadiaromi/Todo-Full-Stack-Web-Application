from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str = "sqlite:///todo_app.db"
    jwt_secret: str = "your-super-secret-jwt-key-here-make-it-long-and-random"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    debug_mode: bool = True
    better_auth_secret: str = "your-better-auth-secret"
    better_auth_url: str = "http://localhost:3000"
    api_prefix: str = "/api"

    class Config:
        env_file = ".env"


settings = Settings()