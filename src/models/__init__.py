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
Models Package - SQLAlchemy 2.0 ORM models
----------------------------------------------------------------------------
FILE VERSION: v5.0-10-10.1.1-1
LAST MODIFIED: 2026-01-10
PHASE: Phase 10 - Authentication & Authorization
CLEAN ARCHITECTURE: Compliant (Rule #14 - SQLAlchemy 2.0 Standards)
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

All models use SQLAlchemy 2.0 Mapped[] type annotations per Rule #14.
"""

__version__ = "v5.0-10-10.1.1-1"

# Base class and mixins
from src.models.database import (
    Base,
    TimestampMixin,
    SoftDeleteMixin,
    NAMING_CONVENTION,
)

# Enumerations
from src.models.enums import (
    UserRole,
    POCKET_ID_GROUP_MAP,
    ROLE_HIERARCHY,
    get_role_from_groups,
    role_meets_requirement,
    get_role_permissions,
)

# Entity models
from src.models.user import User
from src.models.session import Session, SEVERITY_LEVELS, SESSION_STATUSES
from src.models.note import Note
from src.models.archive import Archive, DEFAULT_BUCKET, CHECKSUM_LENGTH
from src.models.audit_log import AuditLog, AUDIT_ACTIONS, ENTITY_TYPES

__all__ = [
    # Base and mixins
    "Base",
    "TimestampMixin",
    "SoftDeleteMixin",
    "NAMING_CONVENTION",
    # Enumerations
    "UserRole",
    "POCKET_ID_GROUP_MAP",
    "ROLE_HIERARCHY",
    "get_role_from_groups",
    "role_meets_requirement",
    "get_role_permissions",
    # Entity models
    "User",
    "Session",
    "Note",
    "Archive",
    "AuditLog",
    # Constants
    "SEVERITY_LEVELS",
    "SESSION_STATUSES",
    "DEFAULT_BUCKET",
    "CHECKSUM_LENGTH",
    "AUDIT_ACTIONS",
    "ENTITY_TYPES",
]
