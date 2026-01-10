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
FILE VERSION: v5.0-10-10.1.7-1
LAST MODIFIED: 2026-01-10
PHASE: Phase 10 - Authentication & Authorization
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

RESPONSIBILITIES:
- Parse Pocket-ID session cookies from incoming requests
- Extract user information (email, groups, etc.)
- Compute user role from Pocket-ID groups (Member/Lead/Admin)
- Inject user context into request state for downstream handlers
- Block unauthorized requests with appropriate 401/403 responses
- Allow bypass for health endpoints and public paths

POCKET-ID COOKIE FORMAT:
    The Pocket-ID session cookie is a JWT containing:
    {
        "sub": "user-uuid",
        "email": "user@example.com",
        "name": "Display Name",
        "groups": ["cartel_crt", "cartel_crt_lead"],
        "exp": 1234567890
    }

ROLE MAPPING (from Pocket-ID groups):
    cartel_crt_admin  → Admin  (full access)
    cartel_crt_lead   → Lead   (member + reopen, unlock, retention)
    cartel_crt        → Member (base CRT access)

USAGE:
    # In main.py
    from src.api.middleware.auth_middleware import AuthMiddleware

    app.add_middleware(
        AuthMiddleware,
        cookie_name="pocket_id_session",
        required_groups=["cartel_crt", "cartel_crt_lead", "cartel_crt_admin"],
        bypass_paths=["/health", "/docs"]
    )

    # In route handlers
    @router.get("/protected")
    async def protected_route(request: Request):
        user = request.state.user  # User context from middleware
        if user.is_lead:
            # Lead or Admin access
            pass
"""

import base64
import json
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set
from uuid import UUID

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse

# Import role enumeration
from src.models.enums import (
    UserRole,
    ROLE_HIERARCHY,
    get_role_from_groups,
    role_meets_requirement,
)

# Module version
__version__ = "v5.0-10-10.1.7-1"

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
        user_id: Unique user identifier (from 'sub' claim - Pocket-ID UUID)
        email: User's email address
        name: User's display name
        groups: List of Pocket-ID group memberships
        role: Computed CRT role (Member/Lead/Admin) or None if not CRT
        raw_claims: Full JWT claims for advanced usage
        db_user_id: Database user UUID (set after user sync)
    """

    user_id: str
    email: str
    name: str = ""
    groups: List[str] = field(default_factory=list)
    role: Optional[UserRole] = None
    raw_claims: Dict[str, Any] = field(default_factory=dict)
    db_user_id: Optional[UUID] = None

    # -------------------------------------------------------------------------
    # Role-Based Properties
    # -------------------------------------------------------------------------

    @property
    def is_crt_member(self) -> bool:
        """
        Check if user has any CRT role (Member, Lead, or Admin).
        
        Returns True if user is part of the Crisis Response Team.
        """
        return self.role is not None

    @property
    def is_lead(self) -> bool:
        """
        Check if user is Lead or Admin.
        
        Leads have elevated permissions including:
        - Reopen closed sessions
        - Unlock locked notes
        - Change archive retention tier
        - View CRT roster and audit logs
        """
        return self.role in (UserRole.LEAD, UserRole.ADMIN)

    @property
    def is_admin(self) -> bool:
        """
        Check if user is Admin.
        
        Admins have full permissions including:
        - Edit any note (not just their own)
        - Delete notes
        - Delete archives
        - Execute cleanup jobs
        - View system health
        """
        return self.role == UserRole.ADMIN

    def has_permission(self, required_role: UserRole) -> bool:
        """
        Check if user meets or exceeds the required role level.
        
        Uses the role hierarchy: Member < Lead < Admin
        
        Args:
            required_role: The minimum role required for access
            
        Returns:
            True if user's role >= required_role
            
        Examples:
            >>> user.role = UserRole.LEAD
            >>> user.has_permission(UserRole.MEMBER)  # True
            >>> user.has_permission(UserRole.LEAD)    # True
            >>> user.has_permission(UserRole.ADMIN)   # False
        """
        return role_meets_requirement(self.role, required_role)

    # -------------------------------------------------------------------------
    # Factory Methods
    # -------------------------------------------------------------------------

    @classmethod
    def from_claims(cls, claims: Dict[str, Any]) -> "UserContext":
        """
        Create UserContext from JWT claims.

        Automatically computes the user's role from their Pocket-ID groups.

        Args:
            claims: Decoded JWT claims dictionary

        Returns:
            UserContext instance with computed role
        """
        user_groups = claims.get("groups", [])
        
        # Compute role from Pocket-ID groups
        role = get_role_from_groups(user_groups)

        return cls(
            user_id=claims.get("sub", ""),
            email=claims.get("email", ""),
            name=claims.get("name", ""),
            groups=user_groups,
            role=role,
            raw_claims=claims,
            db_user_id=None,  # Set later by user sync
        )

    @classmethod
    def anonymous(cls) -> "UserContext":
        """
        Create an anonymous (unauthenticated) user context.
        
        Used for bypassed paths like /health endpoints.
        """
        return cls(
            user_id="anonymous",
            email="",
            name="Anonymous",
            groups=[],
            role=None,
            raw_claims={},
            db_user_id=None,
        )

    # -------------------------------------------------------------------------
    # Utility Methods
    # -------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert UserContext to dictionary for API responses.
        
        Returns:
            Dictionary representation of user context
        """
        return {
            "id": str(self.db_user_id) if self.db_user_id else None,
            "pocket_id": self.user_id,
            "email": self.email,
            "name": self.name,
            "role": self.role.value if self.role else None,
            "groups": self.groups,
            "is_crt_member": self.is_crt_member,
            "is_lead": self.is_lead,
            "is_admin": self.is_admin,
        }

    def __repr__(self) -> str:
        role_str = self.role.value if self.role else "none"
        return f"<UserContext(email='{self.email}', role='{role_str}')>"


# =============================================================================
# Authentication Middleware
# =============================================================================

class AuthMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware for Pocket-ID authentication.

    Parses session cookies, validates tokens, computes user roles,
    and injects user context into the request state.

    Configuration is loaded from ConfigManager if provided,
    or can be passed directly as constructor arguments.
    
    The middleware can be disabled by:
    - Setting enabled=False in constructor
    - Setting DASH_AUTH_ENABLED=false in environment
    - Setting enabled=false in config
    
    When disabled, all requests pass through with an anonymous user context.

    Example:
        app.add_middleware(
            AuthMiddleware,
            cookie_name="pocket_id_session",
            required_groups=["cartel_crt", "cartel_crt_lead", "cartel_crt_admin"],
            bypass_paths=["/health"]
        )
    """

    def __init__(
        self,
        app,
        cookie_name: str = "pocket_id_session",
        required_groups: Optional[List[str]] = None,
        bypass_paths: Optional[List[str]] = None,
        config_manager: Optional[Any] = None,
        enabled: Optional[bool] = None,
    ):
        """
        Initialize AuthMiddleware.

        Args:
            app: FastAPI application instance
            cookie_name: Name of the session cookie
            required_groups: CRT groups required for access (any match)
            bypass_paths: Paths that don't require authentication
            config_manager: Optional ConfigManager for loading settings
            enabled: Override to enable/disable auth (None = check config/env)
        """
        super().__init__(app)
        
        # Determine if auth is enabled
        # Priority: constructor arg > config > env var > default (True)
        if enabled is not None:
            self._enabled = enabled
        elif config_manager:
            auth_config = config_manager.get_auth_config()
            self._enabled = auth_config.get("enabled", True)
        else:
            # Check environment variable
            import os
            env_enabled = os.environ.get("DASH_AUTH_ENABLED", "true").lower()
            self._enabled = env_enabled not in ("false", "0", "no", "off")

        # Load from config manager if provided
        if config_manager:
            auth_config = config_manager.get_auth_config()
            self.cookie_name = auth_config.get("cookie_name", cookie_name)
            self.required_groups = set(
                auth_config.get("required_groups", required_groups or [])
            )
            self.bypass_paths = set(
                auth_config.get("bypass_paths", bypass_paths or [])
            )
        else:
            self.cookie_name = cookie_name
            self.required_groups = set(required_groups or [])
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

        # Log initialization status
        if self._enabled:
            logger.info(f"✅ AuthMiddleware initialized (cookie: {self.cookie_name})")
            logger.debug(f"   Required groups: {self.required_groups}")
            logger.debug(f"   Bypass paths: {len(self.bypass_paths)} configured")
        else:
            logger.warning("⚠️  AuthMiddleware DISABLED - all requests will pass through!")
            logger.warning("   Set DASH_AUTH_ENABLED=true for production!")
    
    @property
    def enabled(self) -> bool:
        """Check if authentication is enabled."""
        return self._enabled

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
        
        # If auth is disabled, pass all requests through with anonymous user
        if not self._enabled:
            request.state.user = UserContext.anonymous()
            request.state.authenticated = False
            return await call_next(request)

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

            # Check CRT membership (user must have a role)
            if not user_context.is_crt_member:
                logger.warning(
                    f"🚫 Access denied for {user_context.email} to {path} - "
                    f"Not a CRT member (groups: {user_context.groups})"
                )
                return self._forbidden_response(
                    "Access denied: CRT membership required"
                )

            # Attach user context to request
            request.state.user = user_context
            request.state.authenticated = True

            logger.debug(
                f"✅ Authenticated: {user_context.email} "
                f"(role: {user_context.role.value if user_context.role else 'none'}) "
                f"-> {path}"
            )

            return await call_next(request)

        except Exception as e:
            logger.error(f"❌ Authentication error: {e}", exc_info=True)
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
        static_extensions = {".css", ".js", ".ico", ".png", ".jpg", ".svg", ".woff", ".woff2"}
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
            # Decode the cookie (JWT format)
            claims = self._decode_session_cookie(cookie_value)

            if not claims:
                return None

            # Check token expiration
            if not self._is_token_valid(claims):
                logger.debug("Session token expired")
                return None

            return UserContext.from_claims(claims)

        except Exception as e:
            logger.debug(f"Failed to decode session cookie: {e}")
            return None

    def _decode_session_cookie(self, cookie_value: str) -> Optional[Dict[str, Any]]:
        """
        Decode Pocket-ID session cookie.

        The cookie is expected to be a JWT. We decode the payload
        to extract claims. Full JWT signature verification should
        be added when Pocket-ID JWKS is configured.

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
# Factory Function - Clean Architecture v5.2 Compliance (Rule #1)
# =============================================================================

def create_auth_middleware(
    app,
    config_manager: Optional[Any] = None,
    cookie_name: str = "pocket_id_session",
    required_groups: Optional[List[str]] = None,
    bypass_paths: Optional[List[str]] = None,
) -> AuthMiddleware:
    """
    Factory function for AuthMiddleware (Clean Architecture Pattern).

    Args:
        app: FastAPI application instance
        config_manager: Optional ConfigManager for loading settings
        cookie_name: Name of the session cookie
        required_groups: CRT groups required for access
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
