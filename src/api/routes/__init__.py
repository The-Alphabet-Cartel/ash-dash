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
FILE VERSION: v5.0-1-1.5-1
LAST MODIFIED: 2026-01-06
PHASE: Phase 1 - Foundation & Infrastructure
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
"""

__version__ = "v5.0-1-1.5-1"

# Health check routes
from src.api.routes.health import router as health_router

# Future routes (added in subsequent phases)
# from .dashboard import router as dashboard_router
# from .sessions import router as sessions_router
# from .notes import router as notes_router
# from .wiki import router as wiki_router
# from .archives import router as archives_router
# from .admin import router as admin_router

__all__ = [
    "health_router",
]
