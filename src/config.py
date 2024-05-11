from pydantic_settings import BaseSettings ,SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str 

    model_config = SettingsConfigDict(
        env_file=".env",
        extra ="ignore"
    )



Config = Settings()