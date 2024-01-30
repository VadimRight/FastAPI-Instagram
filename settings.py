from pydantic import BaseSettings, Field, validator

from src.config import DB_NAME, DB_PORT, DB_HOST, DB_PASSWORD, DB_USER


class Settings(BaseSettings):
    env: str = Field("prod", env="ENV")
    app_url: str = Field("http://localhost:8000")
    db_uri: str = Field(
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    github_client_id: str = Field("", env="CLIENT_ID")
    github_client_secret: str = Field("", env="SECRET")
    jwt_secret_key: str = Field("example_key_super_secret", env="SECRET")
    jwt_algorithm: str = Field("HS256", env="JWT_ALGORITHM")

    class Config:
        env_file = '.env'


settings = Settings()