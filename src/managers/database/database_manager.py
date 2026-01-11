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
Database Manager - Async PostgreSQL connection and session management
----------------------------------------------------------------------------
FILE VERSION: v5.0-2-2.2-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 2 - Data Layer
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

RESPONSIBILITIES:
- Create and manage async SQLAlchemy engine with connection pooling
- Provide async session factory for request-scoped database sessions
- Build database URL from configuration and Docker secrets
- Health check functionality for readiness probes
- Graceful connection handling with resilient error recovery (Rule #5)

USAGE:
    from src.managers.database.database_manager import create_database_manager

    # Create manager (typically at app startup)
    db_manager = await create_database_manager(
        config_manager=config_manager,
        secrets_manager=secrets_manager,
    )

    # Use async session in routes
    async with db_manager.session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()

    # Health check
    is_healthy = await db_manager.health_check()

    # Cleanup at shutdown
    await db_manager.close()
"""

import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict, Optional
from urllib.parse import quote_plus

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.models.database import Base

# Module version
__version__ = "v5.0-2-2.2-1"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# DATABASE MANAGER
# =============================================================================


class DatabaseManager:
    """
    Async PostgreSQL database manager for Ash-Dash.

    Implements Clean Architecture v5.1 principles:
    - Factory function pattern (create_database_manager)
    - Dependency injection (config_manager, secrets_manager)
    - Resilient error handling with graceful fallbacks (Rule #5)
    - Comprehensive logging for debugging

    Attributes:
        engine: SQLAlchemy async engine with connection pool
        session_factory: Async session maker for creating sessions
        is_connected: Whether the database connection is established
    """

    def __init__(
        self,
        config_manager: Any,
        secrets_manager: Any,
        logging_manager: Optional[Any] = None,
    ):
        """
        Initialize DatabaseManager with dependencies.

        Args:
            config_manager: ConfigManager instance for database configuration
            secrets_manager: SecretsManager instance for password retrieval
            logging_manager: Optional LoggingConfigManager for structured logging

        Note:
            Use create_database_manager() factory function instead of direct
            instantiation. The factory function handles async initialization.
        """
        self._config_manager = config_manager
        self._secrets_manager = secrets_manager
        self._logging_manager = logging_manager

        # Get logger (use structured logger if available)
        if logging_manager:
            self._logger = logging_manager.get_logger("database")
        else:
            self._logger = logger

        # Engine and session factory (initialized in connect())
        self._engine: Optional[AsyncEngine] = None
        self._session_factory: Optional[async_sessionmaker[AsyncSession]] = None

        # Connection state
        self._is_connected: bool = False
        self._connection_error: Optional[str] = None

        self._logger.debug(f"DatabaseManager v{__version__} instantiated")

    # =========================================================================
    # CONNECTION MANAGEMENT
    # =========================================================================

    async def connect(self) -> bool:
        """
        Establish database connection and create engine.

        Creates an async SQLAlchemy engine with connection pooling.
        Verifies connectivity with a test query.

        Returns:
            True if connection successful, False otherwise

        Note:
            This method implements resilient behavior (Rule #5) - it logs
            errors but doesn't crash the system, allowing for retry attempts.
        """
        try:
            # Build database URL
            database_url = self._build_database_url()

            if not database_url:
                self._logger.error("❌ Failed to build database URL")
                self._connection_error = "Invalid database configuration"
                return False

            # Get pool configuration
            db_config = self._config_manager.get_database_config()
            pool_size = db_config.get("pool_size", 5)
            max_overflow = db_config.get("max_overflow", 10)

            self._logger.info(
                f"🔌 Connecting to PostgreSQL (pool_size={pool_size}, "
                f"max_overflow={max_overflow})"
            )

            # Create async engine
            self._engine = create_async_engine(
                database_url,
                pool_size=pool_size,
                max_overflow=max_overflow,
                pool_pre_ping=True,  # Verify connections before use
                pool_recycle=3600,   # Recycle connections after 1 hour
                echo=self._config_manager.is_debug(),  # SQL logging in debug mode
            )

            # Create session factory
            self._session_factory = async_sessionmaker(
                bind=self._engine,
                class_=AsyncSession,
                expire_on_commit=False,  # Keep objects usable after commit
                autoflush=False,
                autocommit=False,
            )

            # Test connection
            async with self._engine.connect() as conn:
                result = await conn.execute(text("SELECT 1"))
                result.scalar()

            self._is_connected = True
            self._connection_error = None
            self._logger.info("✅ PostgreSQL connection established")
            return True

        except SQLAlchemyError as e:
            self._logger.error(f"❌ Database connection failed: {e}")
            self._connection_error = str(e)
            self._is_connected = False
            return False

        except Exception as e:
            self._logger.error(f"❌ Unexpected error connecting to database: {e}")
            self._connection_error = str(e)
            self._is_connected = False
            return False

    async def close(self) -> None:
        """
        Close database connection and cleanup resources.

        Should be called during application shutdown.
        """
        if self._engine:
            self._logger.info("🔌 Closing PostgreSQL connection")
            await self._engine.dispose()
            self._engine = None
            self._session_factory = None
            self._is_connected = False
            self._logger.info("✅ PostgreSQL connection closed")

    def _build_database_url(self) -> Optional[str]:
        """
        Build PostgreSQL connection URL from configuration and secrets.

        Constructs URL in format:
        postgresql+asyncpg://user:password@host:port/database

        Returns:
            Database URL string or None if configuration is invalid
        """
        try:
            db_config = self._config_manager.get_database_config()

            # Check if a full URL is provided (for testing/development)
            url = db_config.get("url", "")
            if url and not url.startswith("${"):
                # URL provided directly, convert to async driver
                if url.startswith("postgresql://"):
                    url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
                self._logger.debug("Using configured database URL")
                return url

            # Build URL from components
            redis_config = self._config_manager.get_redis_config()

            # Get connection parameters (with fallbacks)
            host = db_config.get("host", "ash-dash-db")
            port = db_config.get("port", 5432)
            database = db_config.get("database", "ashdash")
            user = db_config.get("user", "ash")

            # Get password from secrets
            password = self._secrets_manager.get("postgres_token")

            if not password:
                self._logger.warning(
                    "⚠️ No postgres_token secret found, using empty password"
                )
                password = ""

            # URL-encode password to handle special characters
            encoded_password = quote_plus(password)

            # Build URL
            url = (
                f"postgresql+asyncpg://{user}:{encoded_password}"
                f"@{host}:{port}/{database}"
            )

            self._logger.debug(
                f"Built database URL: postgresql+asyncpg://{user}:****@{host}:{port}/{database}"
            )

            return url

        except Exception as e:
            self._logger.error(f"❌ Error building database URL: {e}")
            return None

    # =========================================================================
    # SESSION MANAGEMENT
    # =========================================================================

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Provide an async database session context manager.

        Automatically handles commit on success and rollback on exception.

        Yields:
            AsyncSession for database operations

        Raises:
            RuntimeError: If database is not connected

        Example:
            async with db_manager.session() as session:
                user = User(email="test@example.com")
                session.add(user)
                # Commits automatically on context exit
        """
        if not self._session_factory:
            raise RuntimeError(
                "Database not connected. Call connect() first or use "
                "create_database_manager() factory function."
            )

        session = self._session_factory()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    def get_session_factory(self) -> async_sessionmaker[AsyncSession]:
        """
        Get the session factory for dependency injection.

        Useful for FastAPI Depends() pattern.

        Returns:
            Async session maker instance

        Raises:
            RuntimeError: If database is not connected
        """
        if not self._session_factory:
            raise RuntimeError("Database not connected")
        return self._session_factory

    # =========================================================================
    # SCHEMA MANAGEMENT
    # =========================================================================

    async def create_all_tables(self) -> bool:
        """
        Create all tables defined in models.

        Uses SQLAlchemy's create_all to create tables that don't exist.
        This is mainly for development/testing - production should use
        Alembic migrations.

        Returns:
            True if successful, False otherwise
        """
        if not self._engine:
            self._logger.error("❌ Cannot create tables: database not connected")
            return False

        try:
            self._logger.info("📦 Creating database tables...")
            async with self._engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            self._logger.info("✅ Database tables created")
            return True

        except SQLAlchemyError as e:
            self._logger.error(f"❌ Failed to create tables: {e}")
            return False

    async def drop_all_tables(self) -> bool:
        """
        Drop all tables defined in models.

        ⚠️ DANGER: This will delete all data!
        Only use for testing or development reset.

        Returns:
            True if successful, False otherwise
        """
        if not self._engine:
            self._logger.error("❌ Cannot drop tables: database not connected")
            return False

        try:
            self._logger.warning("⚠️ Dropping all database tables...")
            async with self._engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
            self._logger.info("✅ All database tables dropped")
            return True

        except SQLAlchemyError as e:
            self._logger.error(f"❌ Failed to drop tables: {e}")
            return False

    # =========================================================================
    # HEALTH CHECK
    # =========================================================================

    async def health_check(self) -> Dict[str, Any]:
        """
        Check database connectivity and return health status.

        Used by health endpoints for readiness probes.

        Returns:
            Dictionary with health status information:
            {
                "status": "healthy" | "unhealthy",
                "connected": bool,
                "latency_ms": float | None,
                "error": str | None,
                "pool_size": int,
                "pool_checked_out": int,
            }
        """
        import time

        result = {
            "status": "unhealthy",
            "connected": False,
            "latency_ms": None,
            "error": self._connection_error,
            "pool_size": 0,
            "pool_checked_out": 0,
        }

        if not self._engine:
            result["error"] = "Engine not initialized"
            return result

        try:
            # Get pool stats
            pool = self._engine.pool
            if pool:
                result["pool_size"] = pool.size()
                result["pool_checked_out"] = pool.checkedout()

            # Test query with timing
            start = time.perf_counter()
            async with self._engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            latency = (time.perf_counter() - start) * 1000

            result["status"] = "healthy"
            result["connected"] = True
            result["latency_ms"] = round(latency, 2)
            result["error"] = None

        except Exception as e:
            result["error"] = str(e)
            self._logger.warning(f"⚠️ Database health check failed: {e}")

        return result

    # =========================================================================
    # PROPERTIES
    # =========================================================================

    @property
    def is_connected(self) -> bool:
        """Check if database is connected."""
        return self._is_connected

    @property
    def engine(self) -> Optional[AsyncEngine]:
        """Get the SQLAlchemy async engine."""
        return self._engine

    @property
    def connection_error(self) -> Optional[str]:
        """Get the last connection error message."""
        return self._connection_error

    def __repr__(self) -> str:
        """String representation for debugging."""
        status = "connected" if self._is_connected else "disconnected"
        return f"DatabaseManager(status={status})"


# =============================================================================
# FACTORY FUNCTION - Clean Architecture v5.1 Compliance (Rule #1)
# =============================================================================


async def create_database_manager(
    config_manager: Any,
    secrets_manager: Any,
    logging_manager: Optional[Any] = None,
    auto_connect: bool = True,
) -> DatabaseManager:
    """
    Factory function for DatabaseManager (Clean Architecture v5.1 Pattern).

    This is the ONLY way to create a DatabaseManager instance.
    Direct instantiation should be avoided in production code.

    Args:
        config_manager: ConfigManager instance for database configuration
        secrets_manager: SecretsManager instance for password retrieval
        logging_manager: Optional LoggingConfigManager for structured logging
        auto_connect: Whether to establish connection immediately (default: True)

    Returns:
        Configured DatabaseManager instance with active connection

    Example:
        >>> db_manager = await create_database_manager(
        ...     config_manager=config,
        ...     secrets_manager=secrets,
        ... )
        >>> async with db_manager.session() as session:
        ...     # Use session
        ...     pass
    """
    logger.info("🏭 Creating DatabaseManager")

    manager = DatabaseManager(
        config_manager=config_manager,
        secrets_manager=secrets_manager,
        logging_manager=logging_manager,
    )

    if auto_connect:
        connected = await manager.connect()
        if not connected:
            logger.warning(
                "⚠️ DatabaseManager created but connection failed. "
                "System will attempt to reconnect on first use."
            )

    return manager


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = ["DatabaseManager", "create_database_manager"]
