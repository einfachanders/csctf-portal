import os
from pathlib import Path
from typing import Any, Annotated, Literal
from pydantic import AnyUrl, BeforeValidator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        if v == "":
            return []
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    FASTAPI_PROJECT_NAME: str
    FASTAPI_ENVIRONMENT: Literal["development", "staging", "production"] = "development"

    # http/https
    FASTAPI_PROTOCOL: str = "http"
    FASTAPI_DOMAIN: str
    FASTAPI_PORT: int
    # Base path under which the api is reachable
    FASTAPI_BASE_URI: str = "/api"
    # Allowed Cross Origin Request origins
    FASTAPI_BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []
    # 128 bit secret to sign cookies
    # NOTE: can be regenerated for each livetime since
    # the cookies are very short-lived and not renewed
    FASTAPI_JWS_SECRET: str = os.urandom(64).hex()
    FASTAPI_SESSION_TIMEOUT: int = 60 * 60 * 4 # 4 hours

    FASTAPI_CSCTF_USER: str
    FASTAPI_CSCTF_USER_PASSWORD: str

    FASTAPI_SESSION_COOKIE_NAME: str = "csctf_session"

    @computed_field
    @property
    def FASTAPI_HOST(self) -> str:
        return f"{self.FASTAPI_PROTOCOL}://{self.FASTAPI_DOMAIN}:{self.FASTAPI_PORT}"

    # Path to the applications root folder, used for path construction
    # this will point to the app/ directory
    BACKEND_DIR: Path = Path().resolve()

settings = Settings()