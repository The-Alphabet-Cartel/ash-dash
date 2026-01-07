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
Session Sync Service - Background worker for Redis → PostgreSQL sync
----------------------------------------------------------------------------
FILE VERSION: v5.0-2-2.7-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 2 - Data Layer
CLEAN ARCHITECTURE: Compliant (Rule #1 Factory, Rule #2 DI)
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

RESPONSIBILITIES:
- Periodically scan Redis for active sessions
- Save sessions to PostgreSQL before Redis TTL expiration
- Transform Redis data format to PostgreSQL model format
- Track sync statistics and health
- Handle graceful shutdown

SYNC STRATEGY:
1. Scan all active session keys in Redis
2. Check each session's TTL
3. For sessions with TTL < threshold OR first-time seen: sync to PostgreSQL
4. Update existing sessions with latest data
5. Mark sessions as closed when they disappear from Redis

USAGE:
    sync_service = await create_sync_service(
        redis_manager=redis_manager,
        database_manager=database_manager,
        logging_manager=logging_manager,
        config_manager=config_manager,
    )
    
    # Start background sync
    await sync_service.start()
    
    # Stop gracefully
    await sync_service.stop()
"""

import asyncio
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set
from uuid import UUID

from src.repositories import (
    create_session_repository,
    create_audit_log_repository,
)

__version__ = "v5.0-2-2.7-1"


class SyncService:
    """
    Background service for syncing Redis sessions to PostgreSQL.

    Runs periodically to:
    - Discover new sessions in Redis
    - Update existing sessions with latest data
    - Save sessions before TTL expiration
    - Mark sessions as closed when removed from Redis

    Attributes:
        _redis_manager: RedisManager for reading session data
        _database_manager: DatabaseManager for PostgreSQL access
        _session_repo: SessionRepository for CRUD operations
        _audit_repo: AuditLogRepository for logging sync actions
        _logger: Structured logger
        _running: Flag indicating if sync loop is active
        _task: Background asyncio task
        _sync_interval: Seconds between sync cycles
        _ttl_threshold: Sync sessions with TTL below this (seconds)
        _known_sessions: Set of session IDs we've seen
        _stats: Sync statistics
    """

    def __init__(
        self,
        redis_manager,
        database_manager,
        logging_manager,
        sync_interval: int = 30,
        ttl_threshold: int = 300,
    ):
        """
        Initialize SyncService (use factory function instead).

        Args:
            redis_manager: RedisManager instance
            database_manager: DatabaseManager instance
            logging_manager: LoggingManager instance
            sync_interval: Seconds between sync cycles (default: 30)
            ttl_threshold: Sync when TTL below this (default: 300 = 5 min)
        """
        self._redis_manager = redis_manager
        self._database_manager = database_manager
        self._logging_manager = logging_manager
        self._logger = logging_manager.get_logger("sync_service")

        # Create repositories
        self._session_repo = create_session_repository(
            database_manager, logging_manager
        )
        self._audit_repo = create_audit_log_repository(
            database_manager, logging_manager
        )

        # Configuration
        self._sync_interval = sync_interval
        self._ttl_threshold = ttl_threshold

        # State
        self._running = False
        self._task: Optional[asyncio.Task] = None
        self._known_sessions: Set[str] = set()

        # Statistics
        self._stats = {
            "cycles_completed": 0,
            "sessions_created": 0,
            "sessions_updated": 0,
            "sessions_closed": 0,
            "last_sync": None,
            "last_error": None,
            "errors_count": 0,
        }

    # =========================================================================
    # Lifecycle Management
    # =========================================================================

    async def start(self) -> None:
        """
        Start the background sync service.

        Creates an asyncio task that runs the sync loop.
        """
        if self._running:
            self._logger.warning("Sync service already running")
            return

        self._running = True
        self._task = asyncio.create_task(self._sync_loop())
        self._logger.info(
            f"🔄 Sync service started (interval={self._sync_interval}s, "
            f"ttl_threshold={self._ttl_threshold}s)"
        )

    async def stop(self) -> None:
        """
        Stop the background sync service gracefully.

        Cancels the background task and waits for cleanup.
        """
        if not self._running:
            return

        self._running = False

        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

        self._logger.info("🛑 Sync service stopped")

    @property
    def is_running(self) -> bool:
        """Check if sync service is running."""
        return self._running

    @property
    def stats(self) -> Dict[str, Any]:
        """Get sync statistics."""
        return self._stats.copy()

    # =========================================================================
    # Main Sync Loop
    # =========================================================================

    async def _sync_loop(self) -> None:
        """
        Main sync loop - runs until stopped.

        Performs sync cycle, then sleeps for sync_interval.
        """
        self._logger.info("🔄 Sync loop started")

        # Initial sync to populate known sessions
        await self._perform_sync()

        while self._running:
            try:
                await asyncio.sleep(self._sync_interval)

                if self._running:
                    await self._perform_sync()

            except asyncio.CancelledError:
                break
            except Exception as e:
                self._stats["errors_count"] += 1
                self._stats["last_error"] = str(e)
                self._logger.error(f"Sync loop error: {e}")
                # Continue running despite errors
                await asyncio.sleep(self._sync_interval)

    async def _perform_sync(self) -> None:
        """
        Perform a single sync cycle.

        Steps:
        1. Get all session IDs from Redis
        2. Identify new, existing, and removed sessions
        3. Sync new and updated sessions to PostgreSQL
        4. Mark removed sessions as closed
        """
        try:
            sync_start = datetime.now(timezone.utc)

            # Get current sessions from Redis
            redis_session_ids = set(await self._redis_manager.get_session_ids())

            # Identify changes
            new_sessions = redis_session_ids - self._known_sessions
            removed_sessions = self._known_sessions - redis_session_ids
            existing_sessions = redis_session_ids & self._known_sessions

            # Process new sessions
            for session_id in new_sessions:
                await self._sync_new_session(session_id)

            # Process existing sessions (check for updates)
            for session_id in existing_sessions:
                await self._sync_existing_session(session_id)

            # Process removed sessions (mark as closed)
            for session_id in removed_sessions:
                await self._close_session(session_id)

            # Update known sessions
            self._known_sessions = redis_session_ids

            # Update stats
            self._stats["cycles_completed"] += 1
            self._stats["last_sync"] = sync_start.isoformat()

            self._logger.debug(
                f"Sync cycle complete: {len(new_sessions)} new, "
                f"{len(existing_sessions)} existing, {len(removed_sessions)} closed"
            )

        except Exception as e:
            self._stats["errors_count"] += 1
            self._stats["last_error"] = str(e)
            self._logger.error(f"Sync cycle failed: {e}")

    # =========================================================================
    # Session Sync Operations
    # =========================================================================

    async def _sync_new_session(self, session_id: str) -> None:
        """
        Sync a new session from Redis to PostgreSQL.

        Args:
            session_id: Redis session ID
        """
        try:
            # Get session data from Redis
            redis_data = await self._redis_manager.get_session(session_id)
            if not redis_data:
                return

            # Transform to PostgreSQL format
            session_data = self._transform_redis_to_postgres(session_id, redis_data)

            # Check if session already exists in PostgreSQL
            async with self._database_manager.session() as db_session:
                existing = await self._session_repo.get(db_session, session_id)

                if existing:
                    # Update existing session
                    await self._session_repo.update(
                        db_session, session_id, session_data
                    )
                    await db_session.commit()
                    self._stats["sessions_updated"] += 1
                else:
                    # Create new session
                    session_data["id"] = session_id
                    await self._session_repo.create(db_session, session_data)
                    await db_session.commit()
                    self._stats["sessions_created"] += 1

                self._logger.debug(f"Synced new session: {session_id}")

        except Exception as e:
            self._logger.error(f"Failed to sync new session {session_id}: {e}")

    async def _sync_existing_session(self, session_id: str) -> None:
        """
        Update an existing session with latest Redis data.

        Only syncs if TTL is below threshold or data has changed significantly.

        Args:
            session_id: Redis session ID
        """
        try:
            # Check TTL
            ttl = await self._redis_manager.get_session_ttl(session_id)

            # Only sync if TTL is low (about to expire) or periodic refresh
            if ttl > self._ttl_threshold and self._stats["cycles_completed"] % 10 != 0:
                return

            # Get session data from Redis
            redis_data = await self._redis_manager.get_session(session_id)
            if not redis_data:
                return

            # Transform and update
            session_data = self._transform_redis_to_postgres(session_id, redis_data)

            async with self._database_manager.session() as db_session:
                await self._session_repo.update(db_session, session_id, session_data)
                await db_session.commit()

            self._stats["sessions_updated"] += 1
            self._logger.debug(f"Updated session: {session_id} (TTL={ttl})")

        except Exception as e:
            self._logger.error(f"Failed to update session {session_id}: {e}")

    async def _close_session(self, session_id: str) -> None:
        """
        Mark a session as closed when it disappears from Redis.

        Args:
            session_id: Session ID that was removed from Redis
        """
        try:
            async with self._database_manager.session() as db_session:
                session = await self._session_repo.get(db_session, session_id)

                if session and session.status == "active":
                    await self._session_repo.close_session(db_session, session_id)
                    await db_session.commit()
                    self._stats["sessions_closed"] += 1
                    self._logger.info(f"Closed session: {session_id}")

        except Exception as e:
            self._logger.error(f"Failed to close session {session_id}: {e}")

    # =========================================================================
    # Data Transformation
    # =========================================================================

    def _transform_redis_to_postgres(
        self,
        session_id: str,
        redis_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Transform Redis session data to PostgreSQL model format.

        Args:
            session_id: Session ID
            redis_data: Raw Redis session data

        Returns:
            Dictionary suitable for SessionRepository

        Note:
            This mapping depends on Ash-Bot's Redis data format.
            Adjust field names as needed to match Ash-Bot's schema.
        """
        # Extract fields from Redis data (adjust based on Ash-Bot format)
        return {
            # Discord user info
            "discord_user_id": redis_data.get("discord_user_id")
                or redis_data.get("user_id"),
            "discord_username": redis_data.get("discord_username")
                or redis_data.get("username"),
            "discord_display_name": redis_data.get("discord_display_name")
                or redis_data.get("display_name"),

            # Channel info
            "channel_id": redis_data.get("channel_id"),
            "guild_id": redis_data.get("guild_id"),

            # Session status
            "status": redis_data.get("status", "active"),
            "severity": redis_data.get("severity", "medium"),

            # Crisis analysis
            "crisis_score": redis_data.get("crisis_score")
                or redis_data.get("score"),
            "detected_topics": redis_data.get("detected_topics")
                or redis_data.get("topics", []),

            # Timestamps
            "started_at": self._parse_timestamp(
                redis_data.get("started_at") or redis_data.get("created_at")
            ),

            # Message tracking
            "message_count": redis_data.get("message_count", 0),

            # NLP summary (if available)
            "ash_summary": redis_data.get("summary")
                or redis_data.get("ash_summary"),
        }

    def _parse_timestamp(
        self,
        value: Any,
    ) -> Optional[datetime]:
        """
        Parse a timestamp from various formats.

        Args:
            value: Timestamp value (string, int, float, or None)

        Returns:
            datetime object or None
        """
        if value is None:
            return None

        if isinstance(value, datetime):
            return value

        if isinstance(value, (int, float)):
            # Unix timestamp
            return datetime.fromtimestamp(value, tz=timezone.utc)

        if isinstance(value, str):
            # ISO format string
            try:
                # Handle various ISO formats
                if value.endswith("Z"):
                    value = value[:-1] + "+00:00"
                return datetime.fromisoformat(value)
            except ValueError:
                pass

            # Unix timestamp as string
            try:
                return datetime.fromtimestamp(float(value), tz=timezone.utc)
            except ValueError:
                pass

        return None

    # =========================================================================
    # Manual Sync Operations
    # =========================================================================

    async def sync_session(self, session_id: str) -> bool:
        """
        Manually sync a specific session.

        Args:
            session_id: Session ID to sync

        Returns:
            True if sync succeeded
        """
        try:
            await self._sync_new_session(session_id)
            return True
        except Exception as e:
            self._logger.error(f"Manual sync failed for {session_id}: {e}")
            return False

    async def sync_all(self) -> Dict[str, int]:
        """
        Force sync all current Redis sessions.

        Returns:
            Dictionary with sync counts
        """
        session_ids = await self._redis_manager.get_session_ids()

        synced = 0
        failed = 0

        for session_id in session_ids:
            try:
                await self._sync_new_session(session_id)
                synced += 1
            except Exception:
                failed += 1

        return {"synced": synced, "failed": failed}


# =============================================================================
# Factory Function
# =============================================================================


async def create_sync_service(
    redis_manager,
    database_manager,
    logging_manager,
    config_manager,
) -> SyncService:
    """
    Factory function to create SyncService.

    Following Clean Architecture v5.2 Rule #1: Factory Functions.

    Args:
        redis_manager: RedisManager instance
        database_manager: DatabaseManager instance
        logging_manager: LoggingManager instance
        config_manager: ConfigManager instance

    Returns:
        Configured SyncService instance (not started)
    """
    logger = logging_manager.get_logger("src.services.sync_service")
    logger.info("🏭 Creating SyncService")

    # Get sync configuration
    polling_config = config_manager.get_polling_config()
    sync_interval = polling_config.get("sessions_interval_seconds", 30)

    return SyncService(
        redis_manager=redis_manager,
        database_manager=database_manager,
        logging_manager=logging_manager,
        sync_interval=sync_interval,
        ttl_threshold=300,  # 5 minutes
    )


__all__ = [
    "SyncService",
    "create_sync_service",
]
