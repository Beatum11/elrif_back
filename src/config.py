from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv

class Settings(BaseSettings):
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    JWT_SECRET: str
    REFRESH_SECRET: str
    JWT_ALGO: str
    REDIS_HOST: str
    REDIS_PORT: int


    model_config = SettingsConfigDict(
        env_file=find_dotenv(), 
        extra='ignore'
    )

settings = Settings()