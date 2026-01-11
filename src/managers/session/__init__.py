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
Session Managers Package - Authentication Session Management
----------------------------------------------------------------------------
FILE VERSION: v5.0-10-10.4-1
LAST MODIFIED: 2026-01-10
PHASE: Phase 10 - Authentication & Authorization
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

COMPONENTS:
- SessionManager: OIDC authentication session storage in Redis
- UserSession: Session data model with tokens and user info

NOTE: This package handles OIDC authentication sessions, not crisis
sessions from Discord. Crisis session management is in the data layer.
"""

__version__ = "v5.0-10-10.4-1"

from src.managers.session.session_manager import (
    SessionManager,
    UserSession,
    create_session_manager,
    SessionError,
    SessionNotFoundError,
)

__all__ = [
    "SessionManager",
    "UserSession",
    "create_session_manager",
    "SessionError",
    "SessionNotFoundError",
]
