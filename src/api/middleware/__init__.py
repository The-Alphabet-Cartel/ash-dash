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
API Middleware Package - Request/Response middleware handlers
----------------------------------------------------------------------------
FILE VERSION: v5.0-1-1.6-1
LAST MODIFIED: 2026-01-06
PHASE: Phase 1 - Foundation & Infrastructure
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
"""

__version__ = "v5.0-1-1.6-1"

# Authentication Middleware
from src.api.middleware.auth_middleware import (
    AuthMiddleware,
    UserContext,
    create_auth_middleware,
)

__all__ = [
    "AuthMiddleware",
    "UserContext",
    "create_auth_middleware",
]
