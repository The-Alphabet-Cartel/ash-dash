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
Session Manager - Redis-Based Server-Side Session Storage
----------------------------------------------------------------------------
FILE VERSION: v5.0-10-10.4-2
LAST MODIFIED: 2026-01-10
PHASE: Phase 10 - Authentication & Authorization
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

RESPONSIBILITIES:
- Create sessions after successful OIDC authentication
- Store sessions in Redis with automatic expiry
- Retrieve sessions by session ID (from cookie)
- Update sessions when tokens are refreshed
- Destroy sessions on logout
- Compute user roles from PocketID groups

REDIS DATABASE ISOLATION:
    Ash-Dash uses a SEPARATE Redis database from Ash-Bot:
    - DB 0: Ash-Bot crisis session data (Discord crisis sessions)
    - DB 1: Ash-Dash auth sessions (OIDC authentication sessions)

    This is configured via DASH_REDIS_SESSION_DB environment variable.

SESSION STORAGE:
    Key format: ash_session:{session_id}
    Value: JSON-serialized UserSession data
    TTL: Configured session lifetime (default 24 hours)

SESSION COOKIE:
    Name: ash_session_id (configurable)
    Value: Secure random session ID
    Flags: HttpOnly, Secure, SameSite=Lax

USAGE:
    session_manager = await create_session_manager(
        config_manager=config_manager,
        secrets_manager=secrets_manager,
        oidc_config=oidc_config_manager,
        logging_manager=logging_manager,
    )

    # Create session after login
    session_id = await session_manager.create_session(user_data, tokens)

    # Get session
    session = await session_manager.get_session(session_id)

    # Destroy session
    await session_manager.destroy_session(session_id)
"""

import json
import logging
import os
import secrets
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID

import redis.asyncio as aioredis
from redis.asyncio import Redis
from redis.exceptions import RedisError, ConnectionError, TimeoutError

__version__ = "v5.0-10-10.4-2"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# User Session Data Class
# =============================================================================

@dataclass
class UserSession:
    """
    User session data stored in Redis.

    Contains user identity, tokens, and computed role information.

    Attributes:
        session_id: Unique session identifier
        user_id: PocketID user ID (from 'sub' claim)
        email: User's email address
        name: User's display name
        groups: List of PocketID group memberships
        role: Computed CRT role (member/lead/admin)
        access_token: OAuth2 access token
        refresh_token: OAuth2 refresh token
        id_token: OIDC ID token
        token_expires_at: Access token expiration timestamp
        created_at: Session creation timestamp
        last_activity: Last request timestamp
        db_user_id: Database user UUID (set after user sync)
    """

    session_id: str
    user_id: str
    email: str
    name: str = ""
    groups: List[str] = field(default_factory=list)
    role: Optional[str] = None
    access_token: str = ""
    refresh_token: str = ""
    id_token: str = ""
    token_expires_at: float = 0.0
    created_at: float = field(default_factory=time.time)
    last_activity: float = field(default_factory=time.time)
    db_user_id: Optional[str] = None

    # =========================================================================
    # Role Properties
    # =========================================================================

    @property
    def is_crt_member(self) -> bool:
        """Check if user has any CRT role."""
        return self.role is not None

    @property
    def is_lead(self) -> bool:
        """Check if user is Lead or Admin."""
        return self.role in ("lead", "admin")

    @property
    def is_admin(self) -> bool:
        """Check if user is Admin."""
        return self.role == "admin"

    # =========================================================================
    # Token Properties
    # =========================================================================

    @property
    def is_token_expired(self) -> bool:
        """Check if access token is expired."""
        return time.time() >= self.token_expires_at

    @property
    def token_expires_in(self) -> int:
        """Get seconds until token expiration."""
        return max(0, int(self.token_expires_at - time.time()))

    def should_refresh_token(self, threshold_seconds: int = 300) -> bool:
        """
        Check if token should be refreshed.

        Args:
            threshold_seconds: Refresh if expires within this many seconds

        Returns:
            True if token should be refreshed
        """
        return self.token_expires_in <= threshold_seconds

    # =========================================================================
    # Serialization
    # =========================================================================

    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary for storage."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert session to JSON string for Redis storage."""
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserSession":
        """Create session from dictionary."""
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> "UserSession":
        """Create session from JSON string."""
        return cls.from_dict(json.loads(json_str))

    def to_user_context_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary suitable for user context.

        Returns dictionary without sensitive token data.
        """
        return {
            "id": self.db_user_id,
            "pocket_id": self.user_id,
            "email": self.email,
            "name": self.name,
            "role": self.role,
            "groups": self.groups,
            "is_crt_member": self.is_crt_member,
            "is_lead": self.is_lead,
            "is_admin": self.is_admin,
        }


# =============================================================================
# Session Manager
# =============================================================================

class SessionManager:
    """
    Manages user sessions in Redis.

    Sessions are created after successful OIDC authentication and
    stored in Redis with automatic expiry.

    Session lifecycle:
    1. Created on successful OIDC callback
    2. Updated on token refresh
    3. Validated on each request
    4. Destroyed on logout or expiry

    IMPORTANT: SessionManager uses a SEPARATE Redis database from
    the main Ash-Bot data to isolate authentication sessions:
    - DB 0: Ash-Bot crisis session data
    - DB 1: Ash-Dash authentication sessions (default)

    Attributes:
        _client: Redis client for session DB
        _config: OIDC config manager
        _logger: Logger instance
        _lifetime: Session lifetime in seconds
        _connected: Connection status
    """

    # Redis key prefix for sessions
    SESSION_PREFIX = "ash_session:"

    def __init__(
        self,
        redis_config: Dict[str, Any],
        redis_password: Optional[str],
        oidc_config,
        logging_manager,
    ):
        """
        Initialize SessionManager (do not call directly, use factory).

        Args:
            redis_config: Redis connection configuration
            redis_password: Redis password (from secrets)
            oidc_config: OIDCConfigManager instance
            logging_manager: LoggingManager instance
        """
        self._redis_config = redis_config
        self._redis_password = redis_password
        self._config = oidc_config
        self._logging_manager = logging_manager
        self._logger = logging_manager.get_logger("session")
        self._lifetime = oidc_config.session_lifetime
        self._client: Optional[Redis] = None
        self._connected = False

    # =========================================================================
    # Cookie Configuration
    # =========================================================================

    @property
    def cookie_name(self) -> str:
        """Get session cookie name."""
        return self._config.cookie_name

    @property
    def cookie_secure(self) -> bool:
        """Check if cookie should be secure."""
        return self._config.cookie_secure

    @property
    def cookie_httponly(self) -> bool:
        """Check if cookie should be HTTP-only."""
        return self._config.cookie_httponly

    @property
    def cookie_samesite(self) -> str:
        """Get cookie SameSite setting."""
        return self._config.cookie_samesite

    @property
    def session_lifetime(self) -> int:
        """Get session lifetime in seconds."""
        return self._lifetime

    @property
    def is_connected(self) -> bool:
        """Check if connected to Redis."""
        return self._connected

    # =========================================================================
    # Connection Management
    # =========================================================================

    async def connect(self) -> None:
        """
        Establish connection to Redis session database.

        Uses a separate database from Ash-Bot data (default: DB 1).

        Raises:
            ConnectionError: If connection fails
        """
        host = self._redis_config.get("host", "ash-redis")
        port = self._redis_config.get("port", 6379)
        db = self._redis_config.get("session_db", 1)

        self._logger.info(f"🔌 Connecting to Redis session store at {host}:{port} db={db}")

        try:
            connect_kwargs = {
                "host": host,
                "port": port,
                "db": db,
                "decode_responses": True,
                "socket_timeout": 5.0,
                "socket_connect_timeout": 5.0,
                "retry_on_timeout": True,
            }

            if self._redis_password:
                connect_kwargs["password"] = self._redis_password

            self._client = aioredis.Redis(**connect_kwargs)

            # Test connection
            await self._client.ping()
            self._connected = True
            self._logger.info("✅ Redis session store connected")

        except (ConnectionError, TimeoutError) as e:
            self._connected = False
            self._logger.error(f"❌ Redis session store connection failed: {e}")
            raise

    async def close(self) -> None:
        """Close Redis connection."""
        if self._client:
            await self._client.close()
            self._connected = False
            self._logger.info("🔌 Redis session store disconnected")

    # =========================================================================
    # Session Creation
    # =========================================================================

    async def create_session(
        self,
        user_data: Dict[str, Any],
        tokens: Dict[str, Any],
        db_user_id: Optional[str] = None,
    ) -> str:
        """
        Create new session after successful authentication.

        Args:
            user_data: User info from ID token/userinfo
            tokens: Token set from OIDC exchange
            db_user_id: Optional database user UUID

        Returns:
            Session ID to set in cookie
        """
        # Generate secure session ID
        session_id = secrets.token_urlsafe(32)

        # Extract user info
        groups = user_data.get("groups", [])

        # Compute role from groups
        role = self._compute_role(groups)

        # Calculate token expiration
        expires_in = tokens.get("expires_in", 3600)
        token_expires_at = time.time() + expires_in

        # Create session object
        session = UserSession(
            session_id=session_id,
            user_id=user_data.get("sub", ""),
            email=user_data.get("email", ""),
            name=user_data.get("name", user_data.get("preferred_username", "")),
            groups=groups,
            role=role,
            access_token=tokens.get("access_token", ""),
            refresh_token=tokens.get("refresh_token", ""),
            id_token=tokens.get("id_token", ""),
            token_expires_at=token_expires_at,
            db_user_id=db_user_id,
        )

        # Store in Redis
        await self._store_session(session)

        self._logger.info(
            f"✅ Session created for {session.email} "
            f"(role: {role or 'none'}, session: {session_id[:8]}...)"
        )

        return session_id

    async def _store_session(self, session: UserSession) -> None:
        """
        Store session in Redis.

        Args:
            session: UserSession to store
        """
        if not self._client:
            raise SessionError("Redis session store not connected")

        key = f"{self.SESSION_PREFIX}{session.session_id}"

        try:
            await self._client.setex(
                key,
                self._lifetime,
                session.to_json(),
            )
        except RedisError as e:
            self._logger.error(f"Failed to store session: {e}")
            raise SessionError(f"Failed to store session: {e}")

    # =========================================================================
    # Session Retrieval
    # =========================================================================

    async def get_session(
        self,
        session_id: str,
    ) -> Optional[UserSession]:
        """
        Retrieve session by ID.

        Args:
            session_id: Session ID from cookie

        Returns:
            UserSession if valid, None if expired/invalid
        """
        if not session_id or not self._client:
            return None

        key = f"{self.SESSION_PREFIX}{session_id}"

        try:
            data = await self._client.get(key)
            if not data:
                return None

            session = UserSession.from_json(data)
            return session

        except (json.JSONDecodeError, TypeError) as e:
            self._logger.warning(f"Invalid session data for {session_id[:8]}...: {e}")
            return None
        except RedisError as e:
            self._logger.error(f"Redis error getting session: {e}")
            return None

    # =========================================================================
    # Session Update
    # =========================================================================

    async def update_session(
        self,
        session_id: str,
        tokens: Dict[str, Any],
    ) -> bool:
        """
        Update session with refreshed tokens.

        Args:
            session_id: Session ID
            tokens: New token set

        Returns:
            True if updated, False if session not found
        """
        session = await self.get_session(session_id)
        if not session:
            return False

        # Update tokens
        session.access_token = tokens.get("access_token", session.access_token)
        session.id_token = tokens.get("id_token", session.id_token)

        # Update refresh token if provided (some flows don't return new one)
        if tokens.get("refresh_token"):
            session.refresh_token = tokens["refresh_token"]

        # Update expiration
        expires_in = tokens.get("expires_in", 3600)
        session.token_expires_at = time.time() + expires_in

        # Store updated session
        await self._store_session(session)

        self._logger.debug(f"Session tokens updated for {session_id[:8]}...")
        return True

    async def update_db_user_id(
        self,
        session_id: str,
        db_user_id: str,
    ) -> bool:
        """
        Update session with database user ID.

        Called after user sync to link session to database user.

        Args:
            session_id: Session ID
            db_user_id: Database user UUID string

        Returns:
            True if updated, False if session not found
        """
        session = await self.get_session(session_id)
        if not session:
            return False

        session.db_user_id = db_user_id
        await self._store_session(session)

        return True

    async def touch_session(
        self,
        session_id: str,
    ) -> bool:
        """
        Update last activity timestamp.

        Called on each request to track session activity.

        Args:
            session_id: Session ID

        Returns:
            True if updated
        """
        session = await self.get_session(session_id)
        if not session:
            return False

        session.last_activity = time.time()
        await self._store_session(session)

        return True

    # =========================================================================
    # Session Destruction
    # =========================================================================

    async def destroy_session(
        self,
        session_id: str,
    ) -> bool:
        """
        Destroy session on logout.

        Args:
            session_id: Session ID to destroy

        Returns:
            True if destroyed, False if not found
        """
        if not session_id or not self._client:
            return False

        key = f"{self.SESSION_PREFIX}{session_id}"

        try:
            result = await self._client.delete(key)
            if result:
                self._logger.info(f"Session destroyed: {session_id[:8]}...")
            return result > 0

        except RedisError as e:
            self._logger.error(f"Failed to destroy session: {e}")
            return False

    # =========================================================================
    # Role Computation
    # =========================================================================

    def _compute_role(self, groups: List[str]) -> Optional[str]:
        """
        Compute user role from PocketID groups.

        Group hierarchy:
        - admin_group -> admin
        - lead_group -> lead
        - member_group -> member

        Args:
            groups: List of group names from PocketID

        Returns:
            Role string (admin, lead, member) or None
        """
        if self._config.admin_group in groups:
            return "admin"
        if self._config.lead_group in groups:
            return "lead"
        if self._config.member_group in groups:
            return "member"
        return None

    # =========================================================================
    # Health Check
    # =========================================================================

    async def health_check(self) -> Dict[str, Any]:
        """
        Check session manager health.

        Returns:
            Health status dictionary
        """
        if not self._client:
            return {
                "healthy": False,
                "error": "Not connected",
            }

        try:
            # Count active sessions
            pattern = f"{self.SESSION_PREFIX}*"
            keys = []
            async for key in self._client.scan_iter(match=pattern, count=100):
                keys.append(key)
                if len(keys) >= 1000:  # Limit scan
                    break

            return {
                "healthy": True,
                "active_sessions": len(keys),
                "session_lifetime_seconds": self._lifetime,
            }

        except RedisError as e:
            return {
                "healthy": False,
                "error": str(e),
            }


# =============================================================================
# Exceptions
# =============================================================================

class SessionError(Exception):
    """Raised when session operations fail."""
    pass


class SessionNotFoundError(SessionError):
    """Raised when session is not found."""
    pass


# =============================================================================
# Factory Function
# =============================================================================

async def create_session_manager(
    config_manager,
    secrets_manager,
    oidc_config,
    logging_manager,
) -> SessionManager:
    """
    Factory function to create and connect SessionManager.

    Following Clean Architecture v5.2 Rule #1: Factory Functions.

    SessionManager uses a SEPARATE Redis database from Ash-Bot:
    - DB 0: Ash-Bot crisis session data
    - DB 1: Ash-Dash authentication sessions (configurable via DASH_REDIS_SESSION_DB)

    Args:
        config_manager: ConfigManager instance
        secrets_manager: SecretsManager instance
        oidc_config: OIDCConfigManager instance
        logging_manager: LoggingManager instance

    Returns:
        Connected SessionManager instance

    Raises:
        ConnectionError: If Redis connection fails
    """
    logger = logging_manager.get_logger("session")
    logger.info("🏭 Creating SessionManager")

    # Get Redis configuration
    redis_config = config_manager.get_redis_config()

    # Get session-specific DB number (default: 1)
    session_db = int(os.environ.get("DASH_REDIS_SESSION_DB", "1"))
    redis_config["session_db"] = session_db

    # Get Redis password
    redis_password = secrets_manager.get_redis_token()

    # Create manager
    manager = SessionManager(
        redis_config=redis_config,
        redis_password=redis_password,
        oidc_config=oidc_config,
        logging_manager=logging_manager,
    )

    # Connect to Redis
    await manager.connect()

    logger.info(
        f"✅ SessionManager initialized "
        f"(lifetime: {manager.session_lifetime}s, cookie: {manager.cookie_name}, db: {session_db})"
    )

    return manager


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "SessionManager",
    "UserSession",
    "create_session_manager",
    "SessionError",
    "SessionNotFoundError",
]
