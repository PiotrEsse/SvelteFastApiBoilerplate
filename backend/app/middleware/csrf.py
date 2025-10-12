"""Custom middleware that enforces a simple double-submit CSRF protection."""

import secrets
from typing import Iterable, Set

from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse, Response

SAFE_METHODS = {"GET", "HEAD", "OPTIONS", "TRACE"}


class CSRFMiddleware(BaseHTTPMiddleware):
    """Validate CSRF tokens for state-changing requests."""

    def __init__(
        self,
        app,
        *,
        header_name: str,
        cookie_name: str,
        exempt_paths: Iterable[str] | None = None,
    ) -> None:
        super().__init__(app)
        self.header_name = header_name
        self.cookie_name = cookie_name
        self.exempt_paths: Set[str] = {self._normalize(path) for path in (exempt_paths or [])}

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        method = request.method.upper()
        if method in SAFE_METHODS:
            return await call_next(request)

        path = self._normalize(request.url.path)
        if path in self.exempt_paths:
            return await call_next(request)

        csrf_cookie = request.cookies.get(self.cookie_name)
        csrf_header = request.headers.get(self.header_name)
        if not csrf_cookie or not csrf_header:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "CSRF token missing"},
            )
        if not secrets.compare_digest(csrf_cookie, csrf_header):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "CSRF token invalid"},
            )
        return await call_next(request)

    @staticmethod
    def _normalize(path: str) -> str:
        return path if path.startswith("/") else f"/{path}"
