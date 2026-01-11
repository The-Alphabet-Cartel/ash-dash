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
Database Managers Package - PostgreSQL and Redis data access
----------------------------------------------------------------------------
FILE VERSION: v5.0-2-2.2-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 2 - Data Layer
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

CONTENTS:
- DatabaseManager: PostgreSQL connection and session management
- RedisManager: Redis client for reading Ash-Bot data (Step 2.6)

USAGE:
    from src.managers.database import create_database_manager

    db_manager = await create_database_manager(
        config_manager=config,
        secrets_manager=secrets,
    )
"""

__version__ = "v5.0-2-2.2-1"

from .database_manager import DatabaseManager, create_database_manager

# Redis manager will be added in Step 2.6
# from .redis_manager import RedisManager, create_redis_manager

__all__ = [
    "DatabaseManager",
    "create_database_manager",
]
