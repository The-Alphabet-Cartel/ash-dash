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
Archive Managers Package - Encrypted long-term session storage
----------------------------------------------------------------------------
FILE VERSION: v5.0-9-9.6-1
LAST MODIFIED: 2026-01-09
PHASE: Phase 9 - Archive System Implementation (Step 9.6)
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

ARCHIVE INFRASTRUCTURE:
- MinIOManager: S3-compatible storage client for Syn VM (10.20.30.202)
- ArchiveManager: Orchestrates encryption, storage, and metadata
- Three storage buckets:
  - ash-archives: Encrypted crisis session archives
  - ash-documents: Document backups
  - ash-exports: PDF exports and reports

ENCRYPTION:
- AES-256-GCM client-side encryption before storage
- PBKDF2 key derivation with unique salt per archive
- Double encryption: application layer + ZFS storage layer

USAGE:
    from src.managers.archive import (
        create_minio_manager,
        create_archive_manager,
    )
    
    # Create MinIO connection
    minio = await create_minio_manager(
        config_manager=config,
        secrets_manager=secrets,
        logging_manager=logging,
    )
    
    # Create Archive Manager (handles encryption + storage)
    archive_mgr = await create_archive_manager(
        config_manager=config,
        secrets_manager=secrets,
        minio_manager=minio,
        database_manager=db,
        archive_repository=archive_repo,
        logging_manager=logging,
    )
    
    # Archive a session (encrypts + uploads + stores metadata)
    result = await archive_mgr.archive_session(
        session_id="sess_123",
        session_data={...},
        notes=[...],
        archived_by_id=user_uuid,
        archived_by_name="CRT_Member",
    )
    
    # Retrieve and decrypt
    package = await archive_mgr.retrieve_archive(archive_id)
"""

__version__ = "v5.0-9-9.6-1"

# MinIO Storage Manager
from src.managers.archive.minio_manager import (
    MinIOManager,
    create_minio_manager,
)

# Archive Manager (orchestration)
from src.managers.archive.archive_manager import (
    ArchiveManager,
    ArchivePackage,
    ArchiveResult,
    ArchiveListFilter,
    create_archive_manager,
    RETENTION_TIERS,
)

__all__ = [
    # MinIO
    "MinIOManager",
    "create_minio_manager",
    # Archive Manager
    "ArchiveManager",
    "ArchivePackage",
    "ArchiveResult",
    "ArchiveListFilter",
    "create_archive_manager",
    "RETENTION_TIERS",
]
