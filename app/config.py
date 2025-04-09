from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str  # will be loaded from .env

    class Config:
        env_file = ".env"

settings = Settings()
