import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Career Assessment & Password Manager"
    API_V1_STR: str = "/api"
    DB_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecret")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION: int = 60 * 60 * 24   # 24 hours
    CORS_ORIGINS: list = ["http://localhost:5173"]
    RATE_LIMIT: str = "5/minute"

settings = Settings()