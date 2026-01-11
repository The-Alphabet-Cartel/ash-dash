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
Redis Manager - Async Redis client for reading Ash-Bot session data
----------------------------------------------------------------------------
FILE VERSION: v5.0-2-2.6-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 2 - Data Layer
CLEAN ARCHITECTURE: Compliant (Rule #1 Factory, Rule #2 DI)
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

RESPONSIBILITIES:
- Connect to Ash-Bot's Redis instance
- Read session data stored by Ash-Bot
- Scan for session keys by pattern
- Parse session JSON data
- Provide health checks and connection management

ASH-BOT REDIS KEY PATTERNS:
- session:{session_id} - Active session data
- session:{session_id}:messages - Session message history
- session:{session_id}:analysis - NLP analysis results
- user:{discord_id}:sessions - User's session history

USAGE:
    redis_manager = await create_redis_manager(
        config_manager=config_manager,
        secrets_manager=secrets_manager,
        logging_manager=logging_manager,
    )
    
    # Get active sessions
    sessions = await redis_manager.get_active_sessions()
    
    # Get specific session
    session_data = await redis_manager.get_session("session_123")
"""

import json
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set

import redis.asyncio as redis
from redis.asyncio import Redis
from redis.exceptions import ConnectionError, TimeoutError, RedisError

__version__ = "v5.0-2-2.6-1"


class RedisManager:
    """
    Async Redis client for reading Ash-Bot session data.

    Provides read-only access to session data stored by Ash-Bot,
    supporting pattern-based key scanning and JSON parsing.

    Attributes:
        _client: Async Redis client instance
        _config: Redis configuration
        _logger: Logging manager
        _connected: Connection status flag
    """

    # Key patterns for Ash-Bot data
    SESSION_KEY_PREFIX = "session:"
    USER_SESSION_KEY_PREFIX = "user:"
    ANALYSIS_KEY_SUFFIX = ":analysis"
    MESSAGES_KEY_SUFFIX = ":messages"

    def __init__(
        self,
        config: Dict[str, Any],
        password: Optional[str],
        logging_manager,
    ):
        """
        Initialize RedisManager (do not call directly, use factory).

        Args:
            config: Redis configuration dictionary
            password: Redis password (from secrets)
            logging_manager: LoggingManager instance
        """
        self._config = config
        self._password = password
        self._logging_manager = logging_manager
        self._logger = logging_manager.get_logger("redis")
        self._client: Optional[Redis] = None
        self._connected = False

    # =========================================================================
    # Connection Management
    # =========================================================================

    async def connect(self) -> None:
        """
        Establish connection to Redis.

        Creates async Redis client with connection pooling.

        Raises:
            ConnectionError: If connection fails
        """
        host = self._config.get("host", "ash-redis")
        port = self._config.get("port", 6379)
        db = self._config.get("db", 0)

        self._logger.info(f"🔌 Connecting to Redis at {host}:{port} db={db}")

        try:
            # Only pass password if it's set and not empty
            connect_kwargs = {
                "host": host,
                "port": port,
                "db": db,
                "decode_responses": True,
                "socket_timeout": 5.0,
                "socket_connect_timeout": 5.0,
                "retry_on_timeout": True,
                "health_check_interval": 30,
            }
            
            # Only add password if provided
            if self._password:
                connect_kwargs["password"] = self._password
            
            self._client = redis.Redis(**connect_kwargs)

            # Test connection
            await self._client.ping()
            self._connected = True
            self._logger.info("✅ Redis connection established")

        except (ConnectionError, TimeoutError) as e:
            self._connected = False
            self._logger.error(f"❌ Redis connection failed: {e}")
            raise

    async def close(self) -> None:
        """Close Redis connection."""
        if self._client:
            await self._client.close()
            self._connected = False
            self._logger.info("🔌 Redis connection closed")

    async def reconnect(self) -> None:
        """Reconnect to Redis."""
        await self.close()
        await self.connect()

    @property
    def is_connected(self) -> bool:
        """Check if connected to Redis."""
        return self._connected

    # =========================================================================
    # Health Check
    # =========================================================================

    async def health_check(self) -> Dict[str, Any]:
        """
        Perform Redis health check.

        Returns:
            Health status dictionary with latency and info
        """
        if not self._client:
            return {
                "healthy": False,
                "error": "Redis client not initialized",
            }

        try:
            start = time.perf_counter()
            await self._client.ping()
            latency_ms = (time.perf_counter() - start) * 1000

            # Get basic info
            info = await self._client.info("server")

            return {
                "healthy": True,
                "latency_ms": round(latency_ms, 2),
                "redis_version": info.get("redis_version"),
                "connected_clients": info.get("connected_clients"),
                "used_memory_human": info.get("used_memory_human"),
            }

        except (ConnectionError, TimeoutError, RedisError) as e:
            self._connected = False
            return {
                "healthy": False,
                "error": str(e),
            }

    # =========================================================================
    # Session Key Operations
    # =========================================================================

    async def scan_session_keys(
        self,
        pattern: Optional[str] = None,
        count: int = 100,
    ) -> List[str]:
        """
        Scan for session keys matching a pattern.

        Args:
            pattern: Key pattern (default: session:*)
            count: Approximate number per scan iteration

        Returns:
            List of matching session keys
        """
        if not self._client:
            return []

        search_pattern = pattern or f"{self.SESSION_KEY_PREFIX}*"
        keys: List[str] = []

        try:
            async for key in self._client.scan_iter(
                match=search_pattern,
                count=count,
            ):
                # Filter out sub-keys (messages, analysis)
                if not key.endswith(self.MESSAGES_KEY_SUFFIX) and \
                   not key.endswith(self.ANALYSIS_KEY_SUFFIX):
                    keys.append(key)

            self._logger.debug(f"Found {len(keys)} session keys")
            return keys

        except RedisError as e:
            self._logger.error(f"Error scanning keys: {e}")
            return []

    async def get_session_ids(self) -> List[str]:
        """
        Get all active session IDs.

        Returns:
            List of session ID strings (without prefix)
        """
        keys = await self.scan_session_keys()
        return [
            key.replace(self.SESSION_KEY_PREFIX, "")
            for key in keys
        ]

    # =========================================================================
    # Session Data Operations
    # =========================================================================

    async def get_session(
        self,
        session_id: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Get session data by ID.

        Args:
            session_id: Session ID (with or without prefix)

        Returns:
            Session data dictionary or None if not found
        """
        if not self._client:
            return None

        # Normalize key
        key = session_id if session_id.startswith(self.SESSION_KEY_PREFIX) \
            else f"{self.SESSION_KEY_PREFIX}{session_id}"

        try:
            data = await self._client.get(key)
            if data:
                return json.loads(data)
            return None

        except json.JSONDecodeError as e:
            self._logger.warning(f"Invalid JSON for session {session_id}: {e}")
            return None
        except RedisError as e:
            self._logger.error(f"Error getting session {session_id}: {e}")
            return None

    async def get_sessions(
        self,
        session_ids: List[str],
    ) -> Dict[str, Optional[Dict[str, Any]]]:
        """
        Get multiple sessions by ID.

        Args:
            session_ids: List of session IDs

        Returns:
            Dict mapping session_id to data (or None if not found)
        """
        if not self._client or not session_ids:
            return {}

        # Normalize keys
        keys = [
            sid if sid.startswith(self.SESSION_KEY_PREFIX)
            else f"{self.SESSION_KEY_PREFIX}{sid}"
            for sid in session_ids
        ]

        try:
            values = await self._client.mget(keys)
            result = {}

            for sid, value in zip(session_ids, values):
                if value:
                    try:
                        result[sid] = json.loads(value)
                    except json.JSONDecodeError:
                        result[sid] = None
                else:
                    result[sid] = None

            return result

        except RedisError as e:
            self._logger.error(f"Error getting sessions: {e}")
            return {}

    async def get_all_active_sessions(self) -> List[Dict[str, Any]]:
        """
        Get all active session data.

        Returns:
            List of session data dictionaries
        """
        session_ids = await self.get_session_ids()
        sessions_data = await self.get_sessions(session_ids)
        return [data for data in sessions_data.values() if data is not None]

    # =========================================================================
    # Session Analysis Data
    # =========================================================================

    async def get_session_analysis(
        self,
        session_id: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Get NLP analysis data for a session.

        Args:
            session_id: Session ID

        Returns:
            Analysis data dictionary or None
        """
        if not self._client:
            return None

        # Build analysis key
        base_id = session_id.replace(self.SESSION_KEY_PREFIX, "")
        key = f"{self.SESSION_KEY_PREFIX}{base_id}{self.ANALYSIS_KEY_SUFFIX}"

        try:
            data = await self._client.get(key)
            if data:
                return json.loads(data)
            return None

        except (json.JSONDecodeError, RedisError) as e:
            self._logger.warning(f"Error getting analysis for {session_id}: {e}")
            return None

    async def get_session_messages(
        self,
        session_id: str,
    ) -> List[Dict[str, Any]]:
        """
        Get message history for a session.

        Args:
            session_id: Session ID

        Returns:
            List of message dictionaries
        """
        if not self._client:
            return []

        # Build messages key
        base_id = session_id.replace(self.SESSION_KEY_PREFIX, "")
        key = f"{self.SESSION_KEY_PREFIX}{base_id}{self.MESSAGES_KEY_SUFFIX}"

        try:
            # Messages might be stored as a list or JSON string
            data = await self._client.get(key)
            if data:
                return json.loads(data)

            # Or as a Redis list
            messages = await self._client.lrange(key, 0, -1)
            return [json.loads(msg) for msg in messages if msg]

        except (json.JSONDecodeError, RedisError) as e:
            self._logger.warning(f"Error getting messages for {session_id}: {e}")
            return []

    # =========================================================================
    # Session with Full Data
    # =========================================================================

    async def get_session_full(
        self,
        session_id: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Get session with analysis and messages.

        Args:
            session_id: Session ID

        Returns:
            Complete session data with analysis and messages
        """
        session = await self.get_session(session_id)
        if not session:
            return None

        # Add analysis if available
        analysis = await self.get_session_analysis(session_id)
        if analysis:
            session["analysis"] = analysis

        # Add messages if available
        messages = await self.get_session_messages(session_id)
        if messages:
            session["messages"] = messages

        return session

    # =========================================================================
    # User Session History
    # =========================================================================

    async def get_user_session_ids(
        self,
        discord_user_id: int,
    ) -> List[str]:
        """
        Get session IDs for a Discord user.

        Args:
            discord_user_id: Discord user snowflake ID

        Returns:
            List of session IDs
        """
        if not self._client:
            return []

        key = f"{self.USER_SESSION_KEY_PREFIX}{discord_user_id}:sessions"

        try:
            # Might be stored as a set or list
            data_type = await self._client.type(key)

            if data_type == "set":
                members = await self._client.smembers(key)
                return list(members)
            elif data_type == "list":
                return await self._client.lrange(key, 0, -1)
            elif data_type == "string":
                data = await self._client.get(key)
                if data:
                    return json.loads(data)

            return []

        except (json.JSONDecodeError, RedisError) as e:
            self._logger.warning(f"Error getting user sessions for {discord_user_id}: {e}")
            return []

    # =========================================================================
    # TTL Operations
    # =========================================================================

    async def get_session_ttl(
        self,
        session_id: str,
    ) -> int:
        """
        Get time-to-live for a session key.

        Args:
            session_id: Session ID

        Returns:
            TTL in seconds (-1 if no expiry, -2 if key doesn't exist)
        """
        if not self._client:
            return -2

        key = session_id if session_id.startswith(self.SESSION_KEY_PREFIX) \
            else f"{self.SESSION_KEY_PREFIX}{session_id}"

        try:
            return await self._client.ttl(key)
        except RedisError:
            return -2

    async def get_sessions_expiring_soon(
        self,
        seconds: int = 300,
    ) -> List[Dict[str, Any]]:
        """
        Get sessions expiring within N seconds.

        Used by sync service to save sessions before they expire.

        Args:
            seconds: TTL threshold in seconds

        Returns:
            List of session data with TTL info
        """
        session_ids = await self.get_session_ids()
        expiring = []

        for session_id in session_ids:
            ttl = await self.get_session_ttl(session_id)
            if 0 < ttl <= seconds:
                session_data = await self.get_session(session_id)
                if session_data:
                    session_data["_ttl"] = ttl
                    session_data["_session_id"] = session_id
                    expiring.append(session_data)

        return expiring

    # =========================================================================
    # Statistics
    # =========================================================================

    async def get_statistics(self) -> Dict[str, Any]:
        """
        Get Redis statistics.

        Returns:
            Statistics dictionary
        """
        if not self._client:
            return {"error": "Not connected"}

        try:
            info = await self._client.info()
            session_keys = await self.scan_session_keys()

            return {
                "connected": True,
                "redis_version": info.get("redis_version"),
                "used_memory_human": info.get("used_memory_human"),
                "connected_clients": info.get("connected_clients"),
                "total_commands_processed": info.get("total_commands_processed"),
                "active_session_count": len(session_keys),
            }

        except RedisError as e:
            return {
                "connected": False,
                "error": str(e),
            }


# =============================================================================
# Factory Function
# =============================================================================


async def create_redis_manager(
    config_manager,
    secrets_manager,
    logging_manager,
) -> RedisManager:
    """
    Factory function to create and connect RedisManager.

    Following Clean Architecture v5.2 Rule #1: Factory Functions.

    Args:
        config_manager: ConfigManager instance
        secrets_manager: SecretsManager instance
        logging_manager: LoggingManager instance

    Returns:
        Connected RedisManager instance

    Raises:
        ConnectionError: If Redis connection fails
    """
    logger = logging_manager.get_logger("src.managers.redis.redis_manager")
    logger.info("🏭 Creating RedisManager")

    # Get Redis configuration
    redis_config = config_manager.get_redis_config()

    # Get Redis password from secrets
    redis_password = secrets_manager.get_redis_token()

    # Create manager
    manager = RedisManager(
        config=redis_config,
        password=redis_password,
        logging_manager=logging_manager,
    )

    # Connect
    await manager.connect()

    return manager


__all__ = [
    "RedisManager",
    "create_redis_manager",
]
