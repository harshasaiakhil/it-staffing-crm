from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./crm.db"
    JWT_SECRET: str = "secretkey"
    JWT_ALGORITHM: str = "HS256"


settings = Settings()
