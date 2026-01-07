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
Alembic Environment - Async SQLAlchemy migration configuration
----------------------------------------------------------------------------
FILE VERSION: v5.0-2-2.4-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 2 - Data Layer
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
"""

import asyncio
import os
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parents[1]))

# Import our models and Base
from src.models.database import Base
from src.models import User, Session, Note, Archive, AuditLog  # noqa: F401

# This is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for autogenerate support
target_metadata = Base.metadata


def get_database_url() -> str:
    """
    Build database URL from environment variables or secrets.
    
    Priority:
    1. DATABASE_URL environment variable (for CI/CD)
    2. Individual components from environment/secrets
    """
    # Check for complete URL first (useful for CI/CD)
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        # Ensure it uses asyncpg driver
        if database_url.startswith("postgresql://"):
            database_url = database_url.replace(
                "postgresql://", "postgresql+asyncpg://", 1
            )
        return database_url
    
    # Build from components
    host = os.environ.get("DATABASE_HOST", "ash-dash-db")
    port = os.environ.get("DATABASE_PORT", "5432")
    database = os.environ.get("DATABASE_NAME", "ashdash")
    user = os.environ.get("DATABASE_USER", "ash")
    
    # Try to read password from Docker secret first
    password = None
    secret_path = Path("/run/secrets/postgres_token")
    if secret_path.exists():
        password = secret_path.read_text().strip()
    
    # Fall back to environment variable
    if not password:
        password = os.environ.get("DATABASE_PASSWORD", "")
    
    if not password:
        raise ValueError(
            "Database password not found. Set DATABASE_PASSWORD environment "
            "variable or create /run/secrets/postgres_token"
        )
    
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine,
    though an Engine is acceptable here as well. By skipping the Engine
    creation we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Run migrations with the given connection."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,  # Detect column type changes
        compare_server_default=True,  # Detect default value changes
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Run migrations in 'online' mode with async engine.

    Creates an async Engine and associates a connection with the context.
    """
    # Build configuration with our database URL
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = get_database_url()
    
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


# Determine which mode to run
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
