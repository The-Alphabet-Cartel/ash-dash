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
FILE VERSION: v5.0-8-8.1-1
LAST MODIFIED: 2026-01-09
PHASE: Phase 8 - Archive Infrastructure
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

ARCHIVE INFRASTRUCTURE:
- MinIOManager: S3-compatible storage client for Syn VM (10.20.30.202)
- Three storage buckets:
  - ash-archives: Encrypted crisis session archives
  - ash-documents: Document backups
  - ash-exports: PDF exports and reports

PHASE 9 DELIVERABLES (Future):
- Client-side encryption (AES-256-GCM) before storage
- Archive metadata management
- Retrieval and decryption workflows
- Retention policy enforcement
- Archive search and browsing UI

USAGE:
    from src.managers.archive import create_minio_manager
    
    # Create and connect
    minio = await create_minio_manager(
        config_manager=config,
        secrets_manager=secrets,
        logging_manager=logging,
    )
    
    # Upload encrypted archive
    await minio.upload_archive("session_123.enc", encrypted_data)
    
    # List archives
    archives = await minio.list_archives(prefix="2026/01/")
"""

__version__ = "v5.0-8-8.1-1"

from src.managers.archive.minio_manager import (
    MinIOManager,
    create_minio_manager,
)

__all__ = [
    "MinIOManager",
    "create_minio_manager",
]
