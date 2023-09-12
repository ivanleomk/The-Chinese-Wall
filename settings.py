from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    DATABASE_URL: str
    BEARER_TOKEN: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
