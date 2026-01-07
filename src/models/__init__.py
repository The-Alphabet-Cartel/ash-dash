"""
============================================================================
Ash-Dash: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================

MISSION - NEVER TO BE VIOLATED:
    Reveal   → Surface crisis alerts and user escalation patterns in real-time
    Enable   → Equip Crisis Response Teams with tools for swift intervention
    Clarify  → Translate detection data into actionable intelligence
    Protect  → Safeguard our LGBTQIA+ community through vigilant oversight

============================================================================
Models Package - SQLAlchemy ORM models and Pydantic schemas
----------------------------------------------------------------------------
FILE VERSION: v5.0-2-2.2-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 2 - Data Layer
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

CONTENTS:
- database.py: Base model class and common mixins
- user.py: User model (Step 2.3)
- session.py: Session model (Step 2.3)
- note.py: Note model (Step 2.3)
- archive.py: Archive model (Step 2.3)

USAGE:
    from src.models import Base, TimestampMixin, UUIDPrimaryKeyMixin
    from src.models import User, Session, Note, Archive  # After Step 2.3
"""

__version__ = "v5.0-2-2.2-1"

# Base class and mixins
from .database import (
    Base,
    TimestampMixin,
    SoftDeleteMixin,
    UUIDPrimaryKeyMixin,
    NAMING_CONVENTION,
)

# Entity models will be imported as created in Step 2.3
# from .user import User
# from .session import Session
# from .note import Note
# from .archive import Archive

__all__ = [
    # Base and mixins
    "Base",
    "TimestampMixin",
    "SoftDeleteMixin",
    "UUIDPrimaryKeyMixin",
    "NAMING_CONVENTION",
    # Entity models (after Step 2.3)
    # "User",
    # "Session",
    # "Note",
    # "Archive",
]
