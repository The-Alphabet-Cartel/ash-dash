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
Services Package - Background services and workers
----------------------------------------------------------------------------
FILE VERSION: v5.0-10-10.4-1
LAST MODIFIED: 2026-01-10
PHASE: Phase 10 - Authentication & Authorization
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
"""

__version__ = "v5.0-10-10.1.5-1"

from src.services.sync_service import (
    SyncService,
    create_sync_service,
)

from src.services.user_sync_service import (
    UserSyncService,
    create_user_sync_service,
)

from src.services.oidc_service import (
    OIDCService,
    create_oidc_service,
    OIDCTokenError,
    OIDCAuthError,
)

__all__ = [
    "__version__",
    # Session sync service
    "SyncService",
    "create_sync_service",
    # User sync service (Phase 10)
    "UserSyncService",
    "create_user_sync_service",
    # OIDC service (Phase 10)
    "OIDCService",
    "create_oidc_service",
    "OIDCTokenError",
    "OIDCAuthError",
]
