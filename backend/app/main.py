"""Application entrypoint for the FastAPI app."""

from typing import Set

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app.api.routes.auth import router as auth_router
from backend.app.api.routes.todos import router as todos_router
from backend.app.core.config import get_settings
from backend.app.dependencies.auth import AuthenticationError
from backend.app.middleware.csrf import CSRFMiddleware


def _build_csrf_exempt_paths(settings) -> Set[str]:
    def normalize(path: str) -> str:
        return path if path.startswith("/") else f"/{path}"

    base_paths = {normalize(path) for path in settings.csrf_exempt_paths}
    prefixed_paths = {f"{settings.api_prefix}{path}" for path in base_paths}
    return base_paths | prefixed_paths


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.backend_cors_origins,
        allow_credentials=settings.allow_cors_credentials,
        allow_methods=list(settings.allow_cors_methods),
        allow_headers=list(settings.allow_cors_headers),
        expose_headers=[settings.csrf_header_name],
    )

    app.add_middleware(
        CSRFMiddleware,
        header_name=settings.csrf_header_name,
        cookie_name=settings.csrf_cookie_name,
        exempt_paths=_build_csrf_exempt_paths(settings),
    )

    @app.exception_handler(AuthenticationError)
    async def authentication_exception_handler(
        request: Request, exc: AuthenticationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers={"WWW-Authenticate": "Bearer"},
        )

    app.include_router(auth_router, prefix=settings.api_prefix)
    app.include_router(todos_router, prefix=settings.api_prefix)

    return app


app = create_app()
