from pydantic import BaseModel, Field
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Any


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080


class ApiV1Prefix(BaseModel):
    booking: str = "/booking"


class ApiPrefix(BaseModel):
    prefix: str = "/api"

class Settings(BaseSettings):
    # model_config = SettingsConfigDict(
    #     env_file=".env",
    #     case_sensitive=False,
    #     env_nested_delimiter="__",
    #     env_prefix="CONFIG__",
    #     extra='ignore'
    # )
    # secret_key: str
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()


settings = Settings()