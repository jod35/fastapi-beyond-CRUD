from pydantic_settings import BaseSettings ,SettingsConfigDict



class Settings(BaseSettings):
    DATABASE_URL: str ="aiosqlite+sqlite:///db.sqlite3" 

    model_config = SettingsConfigDict(
        env_file=".env",
        extra ="ignore"
    )



Config = Settings()