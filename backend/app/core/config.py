"""Application configuration settings."""

from functools import lru_cache
from typing import List, Sequence

from pydantic import BaseSettings, Field

try:  # pragma: no cover - compatibility shim
    from pydantic import field_validator as _field_validator
except ImportError:  # pragma: no cover
    _field_validator = None
    from pydantic import validator as _field_validator  # type: ignore


class Settings(BaseSettings):
    """Settings pulled from environment variables with sensible defaults."""

    app_name: str = "SvelteFastAPI"
    api_prefix: str = "/api"
    secret_key: str = Field("change-me", env="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    access_token_cookie_name: str = "access_token"
    refresh_token_cookie_name: str = "refresh_token"
    csrf_cookie_name: str = "csrf_token"
    csrf_header_name: str = "X-CSRF-Token"
    csrf_exempt_paths: Sequence[str] = (
        "/auth/login",
        "/auth/register",
        "/auth/refresh",
        "/auth/logout",
    )
    backend_cors_origins: List[str] = Field(
        default_factory=lambda: ["http://localhost:5173"]
    )
    allow_cors_credentials: bool = True
    allow_cors_methods: Sequence[str] = ("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS")
    allow_cors_headers: Sequence[str] = (
        "Authorization",
        "Content-Type",
        "X-CSRF-Token",
    )
    cookie_domain: str | None = Field(default=None, env="COOKIE_DOMAIN")
    cookie_secure: bool = Field(default=False, env="COOKIE_SECURE")
    cookie_samesite: str = Field(default="lax", env="COOKIE_SAMESITE")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    if _field_validator is not None:  # pragma: no branch - decorator assignment

        @_field_validator("backend_cors_origins", pre=True)  # type: ignore[misc]
        def assemble_cors_origins(  # type: ignore[override]
            cls, value: str | Sequence[str]
        ) -> List[str]:
            if isinstance(value, str) and not value.startswith("["):
                return [url.strip() for url in value.split(",") if url]
            return list(value)


@lru_cache()
def get_settings() -> Settings:
    """Return the cached settings instance."""

    return Settings()
