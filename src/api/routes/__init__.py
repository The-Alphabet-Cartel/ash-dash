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
API Routes Package - FastAPI route handlers
----------------------------------------------------------------------------
FILE VERSION: v5.0-7-7.4-1
LAST MODIFIED: 2026-01-08
PHASE: Phase 7 - Documentation Wiki
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
"""

__version__ = "v5.0-7-7.4-1"

# Health check routes (Phase 1)
from src.api.routes.health import router as health_router

# Session routes (Phase 2)
from src.api.routes.sessions import router as sessions_router

# User routes (Phase 2)
from src.api.routes.users import router as users_router

# Dashboard routes (Phase 4)
from src.api.routes.dashboard import router as dashboard_router

# Notes routes (Phase 6)
from src.api.routes.notes import router as notes_router

# Wiki routes (Phase 7)
from src.api.routes.wiki import router as wiki_router

__all__ = [
    "health_router",
    "sessions_router",
    "users_router",
    "dashboard_router",
    "notes_router",
    "wiki_router",
]
