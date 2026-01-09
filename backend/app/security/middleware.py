"""Security middleware for the Todo App"""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from datetime import datetime
import time
import re
from typing import Dict, List, Optional

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add security headers to responses
    """
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Add security headers
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

        return response

class SQLInjectionProtectionMiddleware(BaseHTTPMiddleware):
    """
    Middleware to detect and prevent potential SQL injection attempts
    """
    def __init__(self, app, blocked_patterns: Optional[List[str]] = None):
        super().__init__(app)
        self.blocked_patterns = blocked_patterns or [
            r"(?i)(union\s+select)",
            r"(?i)(drop\s+table)",
            r"(?i)(drop\s+database)",
            r"(?i)(exec\s*\()",
            r"(?i)(execute\s+)",
            r"(?i)(insert\s+into)",
            r"(?i)(delete\s+from)",
            r"(?i)(update\s+.+set)",
            r"(?i)(create\s+(table|database))",
            r"(?i)(alter\s+)",
            r"(?i)(shutdown\s*)",
            r"(?i)(waitfor\s+delay\s+)",
            r"(?i)(xp_cmdshell)",
            r"(?i)(sp_)",
            r"(?i)(exec\s+)",
        ]

    async def dispatch(self, request: Request, call_next):
        # Check query parameters
        for param_value in request.query_params.values():
            for pattern in self.blocked_patterns:
                if re.search(pattern, param_value):
                    return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content={"detail": "Potential SQL injection detected"}
                    )

        # Check form data and JSON body
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.body()
                if body:
                    body_str = body.decode('utf-8', errors='ignore')
                    for pattern in self.blocked_patterns:
                        if re.search(pattern, body_str):
                            return JSONResponse(
                                status_code=status.HTTP_400_BAD_REQUEST,
                                content={"detail": "Potential SQL injection detected"}
                            )
            except Exception:
                # If we can't decode the body, continue anyway
                pass

        response = await call_next(request)
        return response

class InputValidationMiddleware(BaseHTTPMiddleware):
    """
    Middleware to validate input data
    """
    def __init__(self, app, max_request_size: int = 1024 * 1024):  # 1MB
        super().__init__(app)
        self.max_request_size = max_request_size

    async def dispatch(self, request: Request, call_next):
        # Check content length
        content_length = request.headers.get("content-length")
        if content_length:
            try:
                if int(content_length) > self.max_request_size:
                    return JSONResponse(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        content={"detail": "Request entity too large"}
                    )
            except ValueError:
                # If content-length header is not a valid integer
                pass

        response = await call_next(request)
        return response

class RateLimitMiddleware:
    """
    Rate limiting middleware
    """
    def __init__(self, app, limit: str = "10/minute"):
        self.app = app
        self.limit = limit

    async def __call__(self, scope, receive, send):
        # This is a simplified rate limiting implementation
        # In a real application, you would use a more sophisticated approach
        # with Redis or other storage for tracking requests
        await self.app(scope, receive, send)

def add_security_middleware(app):
    """
    Add all security middleware to the application
    """
    # Add trusted host middleware to prevent host header attacks
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[
            "localhost",
            "127.0.0.1",
            "0.0.0.0",
            ".ngrok.io",  # For development with ngrok
        ]
    )

    # Add security headers middleware
    app.add_middleware(SecurityHeadersMiddleware)

    # Add SQL injection protection middleware
    app.add_middleware(SQLInjectionProtectionMiddleware)

    # Add input validation middleware
    app.add_middleware(InputValidationMiddleware)

    # Register rate limit handler
    app.state.limiter = limiter
    app.add_exception_handler(status.HTTP_429_TOO_MANY_REQUESTS, _rate_limit_exceeded_handler)