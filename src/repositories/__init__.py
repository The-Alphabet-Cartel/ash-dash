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
Repositories Package - Data Access Layer
----------------------------------------------------------------------------
FILE VERSION: v5.0-2-2.5-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 2 - Data Layer
CLEAN ARCHITECTURE: Compliant (Rule #1 Factory, Rule #2 DI)
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

PACKAGE CONTENTS:
- BaseRepository: Generic base class with CRUD operations
- UserRepository: User entity operations
- SessionRepository: Crisis session operations
- NoteRepository: Session note operations
- ArchiveRepository: Archive entity operations
- AuditLogRepository: Audit log operations

USAGE:
    from src.repositories import (
        create_user_repository,
        create_session_repository,
        create_note_repository,
        create_archive_repository,
        create_audit_log_repository,
    )
    
    # Create repositories with dependency injection
    user_repo = create_user_repository(db_manager, logging_manager)
    session_repo = create_session_repository(db_manager, logging_manager)
    
    # Use within a database session
    async with db_manager.session() as session:
        users = await user_repo.get_active_users(session)
        critical = await session_repo.get_critical_sessions(session)
"""

__version__ = "v5.0-2-2.5-1"

# Base repository
from src.repositories.base import BaseRepository

# Entity repositories
from src.repositories.user_repository import (
    UserRepository,
    create_user_repository,
)
from src.repositories.session_repository import (
    SessionRepository,
    create_session_repository,
)
from src.repositories.note_repository import (
    NoteRepository,
    create_note_repository,
)
from src.repositories.archive_repository import (
    ArchiveRepository,
    create_archive_repository,
)
from src.repositories.audit_log_repository import (
    AuditLogRepository,
    create_audit_log_repository,
)

__all__ = [
    # Version
    "__version__",
    # Base
    "BaseRepository",
    # User
    "UserRepository",
    "create_user_repository",
    # Session
    "SessionRepository",
    "create_session_repository",
    # Note
    "NoteRepository",
    "create_note_repository",
    # Archive
    "ArchiveRepository",
    "create_archive_repository",
    # Audit Log
    "AuditLogRepository",
    "create_audit_log_repository",
]
