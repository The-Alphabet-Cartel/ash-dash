"""
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================

MISSION - NEVER TO BE VIOLATED:
    Reveal   → Surface crisis alerts and user escalation patterns in real-time
    Enable   → Equip Crisis Response Teams with tools for swift intervention
    Clarify  → Translate detection data into actionable intelligence
    Protect  → Safeguard our LGBTQIA+ community through vigilant oversight

============================================================================
Authentication Middleware - Pocket-ID Cookie Parsing and Authorization
----------------------------------------------------------------------------
FILE VERSION: v5.0-1-1.6-1
LAST MODIFIED: 2026-01-06
PHASE: Phase 1 - Foundation & Infrastructure
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

RESPONSIBILITIES:
- Parse Pocket-ID session cookies from incoming requests
- Extract user information (email, groups, etc.)
- Inject user context into request state for downstream handlers
- Block unauthorized requests with appropriate 401/403 responses
- Allow bypass for health endpoints and public paths

POCKET-ID COOKIE FORMAT:
    The Pocket-ID session cookie is a base64-encoded JWT containing:
    {
        "sub": "user-uuid",
        "email": "user@example.com",
        "name": "Display Name",
        "groups": ["crt", "admin"],
        "exp": 1234567890
    }

USAGE:
    # In main.py
    from src.api.middleware.auth_middleware import AuthMiddleware

    app.add_middleware(
        AuthMiddleware,
        cookie_name="pocket_id_session",
        required_groups=["crt", "admin"],
        bypass_paths=["/health", "/docs"]
    )

    # In route handlers
    @router.get("/protected")
    async def protected_route(request: Request):
        user = request.state.user  # User context from middleware
        return {"message": f"Hello, {user.email}"}
"""

import base64
import json
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse

# Module version
__version__ = "v5.0-1-1.6-1"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# User Context Data Class
# =============================================================================

@dataclass
class UserContext:
    """
    User context extracted from Pocket-ID session.

    Contains user identity and authorization information
    for use throughout the request lifecycle.

    Attributes:
        user_id: Unique user identifier (from 'sub' claim)
        email: User's email address
        name: User's display name
        groups: List of group memberships
        is_admin: Whether user is in admin group
        raw_claims: Full JWT claims for advanced usage
    """

    user_id: str
    email: str
    name: str = ""
    groups: List[str] = field(default_factory=list)
    is_admin: bool = False
    raw_claims: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_claims(
        cls,
        claims: Dict[str, Any],
        admin_groups: Optional[List[str]] = None
    ) -> "UserContext":
        """
        Create UserContext from JWT claims.

        Args:
            claims: Decoded JWT claims dictionary
            admin_groups: List of groups that grant admin status

        Returns:
            UserContext instance
        """
        admin_groups = admin_groups or ["admin"]
        user_groups = claims.get("groups", [])

        return cls(
            user_id=claims.get("sub", ""),
            email=claims.get("email", ""),
            name=claims.get("name", ""),
            groups=user_groups,
            is_admin=any(g in admin_groups for g in user_groups),
            raw_claims=claims,
        )

    @classmethod
    def anonymous(cls) -> "UserContext":
        """Create an anonymous (unauthenticated) user context."""
        return cls(
            user_id="anonymous",
            email="",
            name="Anonymous",
            groups=[],
            is_admin=False,
            raw_claims={},
        )


# =============================================================================
# Authentication Middleware
# =============================================================================

class AuthMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware for Pocket-ID authentication.

    Parses session cookies, validates tokens, and injects
    user context into the request state.

    Configuration is loaded from ConfigManager if provided,
    or can be passed directly as constructor arguments.

    Example:
        app.add_middleware(
            AuthMiddleware,
            cookie_name="pocket_id_session",
            required_groups=["crt"],
            bypass_paths=["/health"]
        )
    """

    def __init__(
        self,
        app,
        cookie_name: str = "pocket_id_session",
        required_groups: Optional[List[str]] = None,
        admin_groups: Optional[List[str]] = None,
        bypass_paths: Optional[List[str]] = None,
        config_manager: Optional[Any] = None,
    ):
        """
        Initialize AuthMiddleware.

        Args:
            app: FastAPI application instance
            cookie_name: Name of the session cookie
            required_groups: Groups required for access (any match)
            admin_groups: Groups that grant admin privileges
            bypass_paths: Paths that don't require authentication
            config_manager: Optional ConfigManager for loading settings
        """
        super().__init__(app)

        # Load from config manager if provided
        if config_manager:
            auth_config = config_manager.get_auth_config()
            self.cookie_name = auth_config.get("cookie_name", cookie_name)
            self.required_groups = set(
                auth_config.get("required_groups", required_groups or [])
            )
            self.admin_groups = auth_config.get("admin_groups", admin_groups or ["admin"])
            self.bypass_paths = set(
                auth_config.get("bypass_paths", bypass_paths or [])
            )
        else:
            self.cookie_name = cookie_name
            self.required_groups = set(required_groups or [])
            self.admin_groups = admin_groups or ["admin"]
            self.bypass_paths = set(bypass_paths or [])

        # Add common bypass paths
        self._default_bypass = {
            "/health",
            "/health/",
            "/health/ready",
            "/health/detailed",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/favicon.ico",
        }
        self.bypass_paths.update(self._default_bypass)

        logger.info(f"✅ AuthMiddleware initialized (cookie: {self.cookie_name})")
        logger.debug(f"   Required groups: {self.required_groups}")
        logger.debug(f"   Bypass paths: {len(self.bypass_paths)} configured")

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        """
        Process incoming request for authentication.

        Args:
            request: Incoming HTTP request
            call_next: Next handler in middleware chain

        Returns:
            HTTP response
        """
        path = request.url.path

        # Check if path should bypass authentication
        if self._should_bypass(path):
            # Set anonymous user for bypassed paths
            request.state.user = UserContext.anonymous()
            request.state.authenticated = False
            return await call_next(request)

        # Try to extract and validate token
        try:
            user_context = self._extract_user_context(request)

            if user_context is None:
                logger.warning(f"🔒 No valid session cookie for: {path}")
                return self._unauthorized_response("Authentication required")

            # Check group membership
            if not self._has_required_groups(user_context):
                logger.warning(
                    f"🚫 Access denied for {user_context.email} to {path} "
                    f"(groups: {user_context.groups})"
                )
                return self._forbidden_response("Insufficient permissions")

            # Attach user context to request
            request.state.user = user_context
            request.state.authenticated = True

            logger.debug(f"✅ Authenticated: {user_context.email} -> {path}")

            return await call_next(request)

        except Exception as e:
            logger.error(f"❌ Authentication error: {e}")
            return self._unauthorized_response("Authentication failed")

    def _should_bypass(self, path: str) -> bool:
        """
        Check if path should bypass authentication.

        Args:
            path: Request path

        Returns:
            True if path should bypass auth
        """
        # Exact match
        if path in self.bypass_paths:
            return True

        # Prefix match for paths ending in /
        for bypass_path in self.bypass_paths:
            if bypass_path.endswith("/") and path.startswith(bypass_path):
                return True

        # Check for static file extensions
        static_extensions = {".css", ".js", ".ico", ".png", ".jpg", ".svg"}
        if any(path.endswith(ext) for ext in static_extensions):
            return True

        return False

    def _extract_user_context(self, request: Request) -> Optional[UserContext]:
        """
        Extract user context from session cookie.

        Args:
            request: HTTP request

        Returns:
            UserContext if valid session exists, None otherwise
        """
        # Get cookie value
        cookie_value = request.cookies.get(self.cookie_name)

        if not cookie_value:
            return None

        try:
            # Decode the cookie (base64 + JSON)
            # Note: In production, this should verify JWT signature
            claims = self._decode_session_cookie(cookie_value)

            if not claims:
                return None

            # Check token expiration
            if not self._is_token_valid(claims):
                logger.debug("Session token expired")
                return None

            return UserContext.from_claims(claims, self.admin_groups)

        except Exception as e:
            logger.debug(f"Failed to decode session cookie: {e}")
            return None

    def _decode_session_cookie(self, cookie_value: str) -> Optional[Dict[str, Any]]:
        """
        Decode Pocket-ID session cookie.

        The cookie is expected to be a JWT. For Phase 1, we do simplified
        decoding. Full JWT verification will be added when we have the
        Pocket-ID public key configuration.

        Args:
            cookie_value: Raw cookie string

        Returns:
            Decoded claims dict or None
        """
        try:
            # JWT format: header.payload.signature
            parts = cookie_value.split(".")

            if len(parts) != 3:
                # Not a valid JWT format, try direct base64
                decoded = base64.urlsafe_b64decode(
                    cookie_value + "=" * (4 - len(cookie_value) % 4)
                )
                return json.loads(decoded)

            # Decode JWT payload (middle part)
            payload = parts[1]

            # Add padding if needed
            padding = 4 - len(payload) % 4
            if padding != 4:
                payload += "=" * padding

            decoded = base64.urlsafe_b64decode(payload)
            return json.loads(decoded)

        except (ValueError, json.JSONDecodeError, UnicodeDecodeError) as e:
            logger.debug(f"Cookie decode error: {e}")
            return None

    def _is_token_valid(self, claims: Dict[str, Any]) -> bool:
        """
        Check if token is still valid (not expired).

        Args:
            claims: Decoded JWT claims

        Returns:
            True if token is valid
        """
        exp = claims.get("exp")

        if exp is None:
            # No expiration claim - consider valid
            # (Pocket-ID may handle expiration differently)
            return True

        try:
            return time.time() < float(exp)
        except (TypeError, ValueError):
            return True

    def _has_required_groups(self, user: UserContext) -> bool:
        """
        Check if user has required group membership.

        Args:
            user: User context to check

        Returns:
            True if user has at least one required group
        """
        # If no groups required, allow access
        if not self.required_groups:
            return True

        # Admin always has access
        if user.is_admin:
            return True

        # Check for any matching group
        user_groups = set(user.groups)
        return bool(user_groups & self.required_groups)

    def _unauthorized_response(self, detail: str) -> JSONResponse:
        """Create 401 Unauthorized response."""
        return JSONResponse(
            status_code=401,
            content={
                "status": "error",
                "error": "unauthorized",
                "detail": detail,
            },
        )

    def _forbidden_response(self, detail: str) -> JSONResponse:
        """Create 403 Forbidden response."""
        return JSONResponse(
            status_code=403,
            content={
                "status": "error",
                "error": "forbidden",
                "detail": detail,
            },
        )


# =============================================================================
# Factory Function - Clean Architecture v5.1 Compliance (Rule #1)
# =============================================================================

def create_auth_middleware(
    app,
    config_manager: Optional[Any] = None,
    cookie_name: str = "pocket_id_session",
    required_groups: Optional[List[str]] = None,
    admin_groups: Optional[List[str]] = None,
    bypass_paths: Optional[List[str]] = None,
) -> AuthMiddleware:
    """
    Factory function for AuthMiddleware (Clean Architecture v5.1 Pattern).

    Args:
        app: FastAPI application instance
        config_manager: Optional ConfigManager for loading settings
        cookie_name: Name of the session cookie
        required_groups: Groups required for access
        admin_groups: Groups that grant admin privileges
        bypass_paths: Paths that don't require authentication

    Returns:
        Configured AuthMiddleware instance

    Example:
        >>> from src.managers import create_config_manager
        >>> config = create_config_manager()
        >>> middleware = create_auth_middleware(app, config_manager=config)
    """
    return AuthMiddleware(
        app=app,
        config_manager=config_manager,
        cookie_name=cookie_name,
        required_groups=required_groups,
        admin_groups=admin_groups,
        bypass_paths=bypass_paths,
    )


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "AuthMiddleware",
    "UserContext",
    "create_auth_middleware",
]
