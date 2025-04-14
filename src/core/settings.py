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
    prefix: str = ""

class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()


settings = Settings()