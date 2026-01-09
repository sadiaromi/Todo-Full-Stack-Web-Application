"""Security configuration for the Todo App"""

import os
from pydantic_settings import BaseSettings

class SecuritySettings(BaseSettings):
    # JWT Settings
    secret_key: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    refresh_token_expire_days: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    # Password hashing
    bcrypt_rounds: int = int(os.getenv("BCRYPT_ROUNDS", "12"))

    # Rate limiting
    rate_limit_requests: int = int(os.getenv("RATE_LIMIT_REQUESTS", "10"))
    rate_limit_window: int = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # in seconds

    # Security headers
    secure_headers_enabled: bool = os.getenv("SECURE_HEADERS_ENABLED", "true").lower() == "true"
    hsts_max_age: int = int(os.getenv("HSTS_MAX_AGE", "31536000"))  # 1 year

    # CORS settings
    allowed_origins: list = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        os.getenv("FRONTEND_URL", ""),
    ]
    # Remove empty string if it exists
    allowed_origins = [origin for origin in allowed_origins if origin]

    class Config:
        env_file = ".env"

security_settings = SecuritySettings()