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
Dependencies Package - FastAPI dependency injection utilities
----------------------------------------------------------------------------
FILE VERSION: v5.0-10-10.1.4-1
LAST MODIFIED: 2026-01-10
PHASE: Phase 10 - Authentication & Authorization
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

This package provides reusable FastAPI dependencies for:
- Authentication and authorization
- Database session management
- Request validation

USAGE:
    from src.api.dependencies import require_member, require_lead, require_admin
    
    @router.get("/protected")
    async def protected_route(user: UserContext = Depends(require_member)):
        return {"user": user.email}
"""

__version__ = "v5.0-10-10.1.4-1"

# Authentication dependencies
from src.api.dependencies.auth import (
    get_current_user,
    get_optional_user,
    get_user_db_id,
    require_member,
    require_lead,
    require_admin,
    require_role,
)

__all__ = [
    # Authentication
    "get_current_user",
    "get_optional_user",
    "get_user_db_id",
    "require_member",
    "require_lead",
    "require_admin",
    "require_role",
]
