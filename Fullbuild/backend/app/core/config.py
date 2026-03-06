from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Startup Builder OS"
    database_url: str = Field(default="postgresql+psycopg://postgres:postgres@postgres:5432/fullbuild")
    redis_url: str = Field(default="redis://redis:6379/0")
    secret_key: str = Field(default="dev-secret")
    jwt_algorithm: str = "HS256"
    jwt_exp_minutes: int = 1440
    openai_api_base: str = "https://api.openai.com/v1"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    storage_root: str = "/data"
    environment: str = "dev"


settings = Settings()
