from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    SESSION_EXPIRE_MINUTES: int = 30
    SESSION_COOKIE_NAME: str
    API_ACTIVE_VERSION: int

    class Config:
        env_file = ".env"

settings = Settings()
