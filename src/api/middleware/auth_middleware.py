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
Authentication Middleware - Session-Based Authorization
----------------------------------------------------------------------------
FILE VERSION: v5.0-11-11.4-2
LAST MODIFIED: 2026-01-11
PHASE: Phase 10 - Authentication & Authorization
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

RESPONSIBILITIES:
- Read session ID from cookie
- Validate session against Redis session store
- Check CRT membership from session role
- Inject user context into request state
- Handle token refresh when needed
- Return 401/403 for unauthorized requests
- Allow bypass for health endpoints and public paths

SESSION-BASED AUTH:
    Unlike the previous JWT-cookie approach, this middleware reads
    sessions from Redis. The session was created during the OIDC
    callback and contains all user claims and tokens.

ROLE MAPPING (from session):
    admin  → Admin  (full access)
    lead   → Lead   (member + reopen, unlock, retention)
    member → Member (base CRT access)

USAGE:
    # In main.py
    from src.api.middleware.auth_middleware import AuthMiddleware

    app.add_middleware(
        AuthMiddleware,
        bypass_paths=["/health", "/docs", "/auth/"]
    )

    # In route handlers
    @router.get("/protected")
    async def protected_route(request: Request):
        user = request.state.user  # User context from middleware
        if user.is_lead:
            # Lead or Admin access
            pass
"""

import asyncio
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set
from uuid import UUID

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse, RedirectResponse

# Import role enumeration
from src.models.enums import (
    UserRole,
    ROLE_HIERARCHY,
    role_meets_requirement,
)

# Module version
__version__ = "v5.0-11-11.4-2"

# Initialize logger
logger = logging.getLogger(__name__)

# =============================================================================
# Token Refresh Lock Manager
# =============================================================================

class TokenRefreshLockManager:
    """
    Manages per-session locks for token refresh operations.
    
    Prevents race conditions where multiple concurrent requests
    try to refresh the same session's tokens simultaneously.
    With rotating refresh tokens, only the first refresh succeeds
    and subsequent attempts fail because the token was invalidated.
    
    This manager ensures only one refresh happens per session at a time.
    Other requests wait for the refresh to complete and then use the
    newly refreshed session.
    """
    
    def __init__(self):
        """Initialize the lock manager."""
        self._locks: Dict[str, asyncio.Lock] = {}
        self._lock_guard = asyncio.Lock()  # Guards access to _locks dict
    
    async def get_lock(self, session_id: str) -> asyncio.Lock:
        """
        Get or create a lock for a specific session.
        
        Args:
            session_id: The session ID to get a lock for
            
        Returns:
            asyncio.Lock for this session
        """
        async with self._lock_guard:
            if session_id not in self._locks:
                self._locks[session_id] = asyncio.Lock()
            return self._locks[session_id]
    
    async def cleanup_lock(self, session_id: str) -> None:
        """
        Remove a lock when no longer needed.
        
        Called after successful operations to prevent memory buildup.
        Only removes if the lock is not currently held.
        
        Args:
            session_id: The session ID to clean up
        """
        async with self._lock_guard:
            lock = self._locks.get(session_id)
            if lock and not lock.locked():
                del self._locks[session_id]


# Global lock manager instance
_refresh_lock_manager = TokenRefreshLockManager()


# =============================================================================
# User Context Data Class
# =============================================================================

@dataclass
class UserContext:
    """
    User context extracted from session.

    Contains user identity and authorization information
    for use throughout the request lifecycle.

    Attributes:
        user_id: PocketID user ID (from 'sub' claim)
        email: User's email address
        name: User's display name
        groups: List of PocketID group memberships
        role: Computed CRT role (Member/Lead/Admin) or None if not CRT
        db_user_id: Database user UUID
        session_id: Session ID for reference
    """

    user_id: str
    email: str
    name: str = ""
    groups: List[str] = field(default_factory=list)
    role: Optional[UserRole] = None
    db_user_id: Optional[UUID] = None
    session_id: Optional[str] = None

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
    def from_session(cls, session) -> "UserContext":
        """
        Create UserContext from a UserSession object.

        Args:
            session: UserSession from session manager

        Returns:
            UserContext instance
        """
        # Map string role to UserRole enum
        role = None
        if session.role == "admin":
            role = UserRole.ADMIN
        elif session.role == "lead":
            role = UserRole.LEAD
        elif session.role == "member":
            role = UserRole.MEMBER

        return cls(
            user_id=session.user_id,
            email=session.email,
            name=session.name,
            groups=session.groups,
            role=role,
            db_user_id=UUID(session.db_user_id) if session.db_user_id else None,
            session_id=session.session_id,
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
            db_user_id=None,
            session_id=None,
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
    FastAPI middleware for session-based authentication.

    Reads session ID from cookie, validates against Redis session store,
    and injects user context into the request state.

    The middleware can be disabled by:
    - Setting enabled=False in constructor
    - Setting DASH_AUTH_ENABLED=false in environment

    When disabled, all requests pass through with an anonymous user context.

    Example:
        app.add_middleware(
            AuthMiddleware,
            bypass_paths=["/health", "/auth/"]
        )
    """

    def __init__(
        self,
        app,
        bypass_paths: Optional[List[str]] = None,
        config_manager: Optional[Any] = None,
        enabled: Optional[bool] = None,
    ):
        """
        Initialize AuthMiddleware.

        Args:
            app: FastAPI application instance
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
            env_enabled = os.environ.get("DASH_OIDC_ENABLED", "true").lower()
            self._enabled = env_enabled not in ("false", "0", "no", "off")

        # Configure bypass paths
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
            "/favicon.svg",
            # OIDC flow endpoints must bypass auth
            "/auth/login",
            "/auth/callback",
            "/auth/logout",
        }
        self.bypass_paths.update(self._default_bypass)

        # Log initialization status
        if self._enabled:
            logger.info("✅ AuthMiddleware initialized (session-based)")
            logger.debug(f"   Bypass paths: {len(self.bypass_paths)} configured")
        else:
            logger.warning("⚠️  AuthMiddleware DISABLED - all requests will pass through!")
            logger.warning("   Set DASH_OIDC_ENABLED=true for production!")

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

        # Get session manager from app state
        session_manager = getattr(request.app.state, "session_manager", None)

        if not session_manager:
            logger.error("SessionManager not available in app state")
            return self._unauthorized_response("Authentication service unavailable")

        if not session_manager.is_connected:
            logger.error("SessionManager not connected to Redis")
            return self._unauthorized_response("Authentication service unavailable")

        # Get session ID from cookie
        session_id = request.cookies.get(session_manager.cookie_name)

        if not session_id:
            logger.debug(f"🔒 No session cookie for: {path}")
            return self._unauthorized_response(request, "Authentication required")

        try:
            # Get session from Redis
            session = await session_manager.get_session(session_id)

            if session is None:
                logger.debug(f"🔒 Invalid or expired session for: {path}")
                return self._unauthorized_response(request, "Session expired")

            # Check CRT membership (user must have a role)
            if not session.is_crt_member:
                logger.warning(
                    f"🚫 Access denied for {session.email} to {path} - "
                    f"Not a CRT member (groups: {session.groups})"
                )
                return self._forbidden_response(
                    "Access denied: CRT membership required"
                )

            # Check if token needs refresh
            oidc_config = getattr(request.app.state, "oidc_config", None)
            if oidc_config and session.should_refresh_token(
                oidc_config.token_refresh_threshold
            ):
                await self._refresh_session_tokens(request, session)

            # Create user context from session
            user_context = UserContext.from_session(session)

            # Attach user context to request
            request.state.user = user_context
            request.state.authenticated = True
            request.state.session = session

            logger.debug(
                f"✅ Authenticated: {user_context.email} "
                f"(role: {user_context.role.value if user_context.role else 'none'}) "
                f"-> {path}"
            )

            return await call_next(request)

        except Exception as e:
            logger.error(f"❌ Authentication error: {e}", exc_info=True)
            return self._unauthorized_response(request, "Authentication failed")

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

        # Check for /assets/ path (static files)
        if path.startswith("/assets/"):
            return True

        return False

    async def _refresh_session_tokens(
        self,
        request: Request,
        session,
    ) -> None:
        """
        Refresh tokens for a session that is near expiry.
        
        Uses a per-session mutex to prevent race conditions where
        multiple concurrent requests try to refresh the same token.
        With rotating refresh tokens, only the first refresh succeeds;
        subsequent attempts fail because the old token is invalidated.
        
        This method:
        1. Acquires a lock for this specific session
        2. Re-checks if refresh is still needed (another request may have completed it)
        3. Performs the refresh if still needed
        4. Releases the lock

        Args:
            request: FastAPI request
            session: Current session
        """
        oidc_service = getattr(request.app.state, "oidc_service", None)
        session_manager = request.app.state.session_manager
        oidc_config = getattr(request.app.state, "oidc_config", None)

        if not oidc_service or not session.refresh_token:
            return

        # Get the lock for this session
        lock = await _refresh_lock_manager.get_lock(session.session_id)
        
        try:
            # Acquire lock - other requests for this session will wait here
            async with lock:
                # Re-fetch session to check if another request already refreshed
                current_session = await session_manager.get_session(session.session_id)
                
                if current_session is None:
                    # Session was invalidated while waiting
                    logger.debug(f"Session {session.session_id[:8]}... invalidated during refresh wait")
                    return
                
                # Check if refresh is still needed
                # Another request may have refreshed while we were waiting for the lock
                if oidc_config and not current_session.should_refresh_token(
                    oidc_config.token_refresh_threshold
                ):
                    logger.debug(
                        f"Token already refreshed by another request for {session.email}"
                    )
                    return
                
                # Still needs refresh - proceed
                logger.debug(f"Refreshing tokens for {session.email}")
                
                # Refresh tokens
                new_tokens = await oidc_service.refresh_tokens(
                    current_session.refresh_token
                )

                # Update session with new tokens
                await session_manager.update_session(session.session_id, new_tokens)

                logger.info(f"✅ Tokens refreshed for {session.email}")

        except Exception as e:
            # Log but don't fail the request - session still valid until expiry
            logger.warning(f"⚠️ Token refresh failed for {session.session_id[:8]}...: {e}")
        
        finally:
            # Clean up lock if no longer held (prevents memory buildup)
            await _refresh_lock_manager.cleanup_lock(session.session_id)

    def _is_api_request(self, request: Request) -> bool:
        """
        Check if request is an API call vs a browser page request.
        
        API requests should get JSON responses.
        Browser requests should get redirects.
        
        Args:
            request: FastAPI request
            
        Returns:
            True if this is an API request
        """
        path = request.url.path
        
        # API paths always get JSON
        if path.startswith("/api/"):
            return True
        
        # Check Accept header for JSON preference
        accept = request.headers.get("accept", "")
        if "application/json" in accept and "text/html" not in accept:
            return True
        
        # Check for XHR/fetch requests
        if request.headers.get("x-requested-with", "").lower() == "xmlhttprequest":
            return True
        
        return False

    def _unauthorized_response(self, request: Request, detail: str) -> Response:
        """
        Create 401 Unauthorized response.
        
        For API requests: returns JSON error.
        For browser requests: redirects to login page.
        
        Args:
            request: FastAPI request
            detail: Error message
            
        Returns:
            JSONResponse or RedirectResponse
        """
        if self._is_api_request(request):
            return JSONResponse(
                status_code=401,
                content={
                    "status": "error",
                    "error": "unauthorized",
                    "detail": detail,
                },
            )
        
        # Browser request - redirect to login with return path
        from urllib.parse import quote
        current_path = request.url.path
        if request.url.query:
            current_path += f"?{request.url.query}"
        
        login_url = f"/auth/login?redirect={quote(current_path)}"
        return RedirectResponse(url=login_url, status_code=302)

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
    bypass_paths: Optional[List[str]] = None,
) -> AuthMiddleware:
    """
    Factory function for AuthMiddleware (Clean Architecture Pattern).

    Args:
        app: FastAPI application instance
        config_manager: Optional ConfigManager for loading settings
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
