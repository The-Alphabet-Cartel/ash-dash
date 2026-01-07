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
Redis Manager Package
----------------------------------------------------------------------------
FILE VERSION: v5.0-2-2.6-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 2 - Data Layer
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
"""

__version__ = "v5.0-2-2.6-1"

from src.managers.redis.redis_manager import (
    RedisManager,
    create_redis_manager,
)

__all__ = [
    "__version__",
    "RedisManager",
    "create_redis_manager",
]
