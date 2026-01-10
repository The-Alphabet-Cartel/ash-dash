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
Archive Manager - Orchestrates session archiving with encryption
----------------------------------------------------------------------------
FILE VERSION: v5.0-9-9.4-1
LAST MODIFIED: 2026-01-09
PHASE: Phase 9 - Archive System Implementation
CLEAN ARCHITECTURE: Compliant (Rule #1 Factory, Rule #2 DI)
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

RESPONSIBILITIES:
- Orchestrate session archiving workflow (encrypt → upload → store metadata)
- Retrieve and decrypt archived sessions
- Manage retention tiers (standard/permanent)
- Clean up expired archives
- Provide archive listing with filtering

ENCRYPTION FLOW:
    Session + Notes (JSON)
        ↓
    AES-256-GCM Encryption (ArchiveEncryption)
        ↓
    Encrypted Blob
        ↓
    MinIO Upload (MinIOManager)
        ↓
    Metadata → PostgreSQL (ArchiveRepository)

PHASE 9.4 CHANGES:
- Updated to use dedicated queryable columns instead of JSONB
- Improved filtering performance with proper indexes
- Repository methods now use column-based queries

USAGE:
    from src.managers.archive import create_archive_manager
    
    archive_manager = await create_archive_manager(
        config_manager=config,
        secrets_manager=secrets,
        minio_manager=minio,
        database_manager=db,
        logging_manager=logging,
    )
    
    # Archive a session
    archive = await archive_manager.archive_session(
        session_id="sess_12345",
        session_data={...},
        notes=[...],
        archived_by_id=user_uuid,
        archived_by_name="CRT_Member",
        retention_tier="standard",
    )
    
    # Retrieve and decrypt
    data = await archive_manager.retrieve_archive(archive.id)
"""

import hashlib
import io
import json
import logging
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

from dateutil import parser as date_parser

from src.utils.encryption import (
    ArchiveEncryption,
    create_archive_encryption,
    DecryptionError,
    EncryptionError,
)

# Module version
__version__ = "v5.0-9-9.4-1"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# Constants
# =============================================================================

# Retention tier configuration
RETENTION_TIERS = {
    "standard": 365,      # 1 year
    "permanent": 2555,    # ~7 years
}

# Archive package version for forward compatibility
ARCHIVE_PACKAGE_VERSION = "1.0"


# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class ArchivePackage:
    """
    Structure of an archived session package.
    
    This is the JSON structure that gets encrypted and stored.
    """
    version: str
    archived_at: str
    session: Dict[str, Any]
    notes: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    
    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps(asdict(self), indent=2, default=str)
    
    @classmethod
    def from_json(cls, json_str: str) -> "ArchivePackage":
        """Deserialize from JSON string."""
        data = json.loads(json_str)
        return cls(**data)


@dataclass
class ArchiveResult:
    """Result of an archive operation."""
    success: bool
    archive_id: Optional[UUID] = None
    storage_key: Optional[str] = None
    size_bytes: int = 0
    checksum: Optional[str] = None
    error: Optional[str] = None


@dataclass
class ArchiveListFilter:
    """Filters for listing archives."""
    discord_user_id: Optional[int] = None
    severity: Optional[str] = None
    retention_tier: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    archived_by: Optional[UUID] = None


# =============================================================================
# Archive Manager Class
# =============================================================================


class ArchiveManager:
    """
    Manages session archiving operations with encryption.
    
    Coordinates the full archive lifecycle:
    - Archive: Serialize → Encrypt → Upload → Store metadata
    - Retrieve: Fetch metadata → Download → Decrypt → Deserialize
    - Cleanup: Find expired → Delete from MinIO → Remove metadata
    
    Attributes:
        _config: Configuration manager
        _minio: MinIO storage manager
        _encryption: AES-256-GCM encryption handler
        _db: Database manager
        _archive_repo: Archive repository
        _logger: Logging instance
    """
    
    def __init__(
        self,
        config_manager,
        minio_manager,
        encryption: ArchiveEncryption,
        database_manager,
        archive_repository,
        logging_manager,
    ):
        """
        Initialize ArchiveManager.
        
        Args:
            config_manager: Configuration manager instance
            minio_manager: MinIO storage manager instance
            encryption: Archive encryption handler
            database_manager: Database manager instance
            archive_repository: Archive repository instance
            logging_manager: Logging manager instance
        """
        self._config = config_manager
        self._minio = minio_manager
        self._encryption = encryption
        self._db = database_manager
        self._archive_repo = archive_repository
        self._logger = logging_manager.get_logger(__name__)
        
        # Load retention settings from config (with defaults)
        self._retention_days = {
            "standard": config_manager.get(
                "archive", "standard_retention_days", RETENTION_TIERS["standard"]
            ),
            "permanent": config_manager.get(
                "archive", "permanent_retention_days", RETENTION_TIERS["permanent"]
            ),
        }
        
        self._logger.info("✅ ArchiveManager initialized")
    
    # =========================================================================
    # Archive Operations
    # =========================================================================
    
    async def archive_session(
        self,
        session_id: str,
        session_data: Dict[str, Any],
        notes: List[Dict[str, Any]],
        archived_by_id: UUID,
        archived_by_name: str,
        retention_tier: str = "standard",
    ) -> ArchiveResult:
        """
        Archive a completed session with encryption.
        
        Workflow:
        1. Build archive package (session + notes + metadata)
        2. Serialize to JSON
        3. Encrypt with AES-256-GCM
        4. Calculate checksum
        5. Upload to MinIO
        6. Store metadata in PostgreSQL (using dedicated columns)
        
        Args:
            session_id: Crisis session identifier
            session_data: Session metadata and crisis information
            notes: List of session notes
            archived_by_id: UUID of CRT member archiving
            archived_by_name: Display name of CRT member
            retention_tier: "standard" (1 year) or "permanent" (7 years)
            
        Returns:
            ArchiveResult with success status and details
        """
        self._logger.info(f"📦 Archiving session {session_id} ({retention_tier} tier)")
        
        # Validate retention tier
        if retention_tier not in RETENTION_TIERS:
            return ArchiveResult(
                success=False,
                error=f"Invalid retention tier: {retention_tier}. Must be 'standard' or 'permanent'"
            )
        
        try:
            # 1. Build archive package
            archive_package = ArchivePackage(
                version=ARCHIVE_PACKAGE_VERSION,
                archived_at=datetime.now(timezone.utc).isoformat(),
                session=session_data,
                notes=notes,
                metadata={
                    "archived_by_id": str(archived_by_id),
                    "archived_by_name": archived_by_name,
                    "retention_tier": retention_tier,
                    "notes_count": len(notes),
                },
            )
            
            # 2. Serialize to JSON
            json_data = archive_package.to_json()
            plaintext = json_data.encode("utf-8")
            
            self._logger.debug(f"Package size before encryption: {len(plaintext):,} bytes")
            
            # 3. Encrypt
            encrypted = self._encryption.encrypt(plaintext)
            
            self._logger.debug(f"Encrypted size: {len(encrypted):,} bytes")
            
            # 4. Calculate checksum of encrypted data
            checksum = hashlib.sha256(encrypted).hexdigest()
            
            # 5. Generate storage key
            timestamp = int(datetime.now(timezone.utc).timestamp())
            storage_key = f"sessions/{session_id}/archive_{timestamp}.enc"
            
            # 6. Upload to MinIO
            upload_result = await self._minio.upload_archive(
                archive_id=f"{session_id}_{timestamp}",
                data=io.BytesIO(encrypted),
                size=len(encrypted),
                content_type="application/octet-stream",
                metadata={
                    "session_id": session_id,
                    "retention_tier": retention_tier,
                    "checksum": checksum,
                    "encrypted": "true",
                    "archived_by": archived_by_name,
                },
            )
            
            if not upload_result:
                self._logger.error(f"Failed to upload archive to MinIO for session {session_id}")
                return ArchiveResult(
                    success=False,
                    error="Failed to upload archive to storage"
                )
            
            # 7. Calculate retention date
            retention_days = self._retention_days.get(retention_tier, 365)
            
            # 8. Parse session timestamps
            session_started_at = self._parse_datetime(session_data.get("started_at"))
            session_ended_at = self._parse_datetime(session_data.get("ended_at"))
            
            # 9. Store metadata in PostgreSQL with dedicated columns
            async with self._db.session() as db_session:
                archive = await self._archive_repo.create_archive(
                    session=db_session,
                    session_id=session_id,
                    storage_key=upload_result,  # MinIO returns the object path
                    checksum=checksum,
                    size_bytes=len(encrypted),
                    archived_by=archived_by_id,
                    archived_by_name=archived_by_name,
                    storage_bucket="ash-archives",
                    retention_days=retention_days,
                    retention_tier=retention_tier,
                    # Queryable metadata columns
                    discord_user_id=session_data.get("user_id"),
                    discord_user_name=session_data.get("user_name"),
                    severity=session_data.get("severity"),
                    notes_count=len(notes),
                    session_started_at=session_started_at,
                    session_ended_at=session_ended_at,
                    # Legacy JSONB for any additional data
                    extra_data={
                        "package_version": ARCHIVE_PACKAGE_VERSION,
                    },
                )
                await db_session.commit()
            
            self._logger.info(
                f"✅ Archived session {session_id} → {upload_result} "
                f"({len(encrypted):,} bytes, {retention_tier} tier)"
            )
            
            return ArchiveResult(
                success=True,
                archive_id=archive.id,
                storage_key=upload_result,
                size_bytes=len(encrypted),
                checksum=checksum,
            )
            
        except EncryptionError as e:
            self._logger.error(f"❌ Encryption failed for session {session_id}: {e}")
            return ArchiveResult(success=False, error=f"Encryption failed: {e}")
            
        except Exception as e:
            self._logger.exception(f"❌ Failed to archive session {session_id}: {e}")
            return ArchiveResult(success=False, error=str(e))
    
    def _parse_datetime(self, value: Any) -> Optional[datetime]:
        """Parse a datetime from various formats."""
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                return date_parser.parse(value)
            except (ValueError, TypeError):
                return None
        return None
    
    async def retrieve_archive(
        self,
        archive_id: UUID,
    ) -> Optional[ArchivePackage]:
        """
        Retrieve and decrypt an archived session.
        
        Workflow:
        1. Get metadata from PostgreSQL
        2. Download encrypted blob from MinIO
        3. Verify checksum
        4. Decrypt
        5. Deserialize to ArchivePackage
        
        Args:
            archive_id: Archive UUID
            
        Returns:
            ArchivePackage if successful, None otherwise
        """
        self._logger.info(f"📥 Retrieving archive {archive_id}")
        
        try:
            # 1. Get metadata
            async with self._db.session() as db_session:
                archive = await self._archive_repo.get(db_session, archive_id)
                
                if not archive:
                    self._logger.warning(f"Archive not found: {archive_id}")
                    return None
                
                storage_key = archive.storage_key
                storage_bucket = archive.storage_bucket
                expected_checksum = archive.checksum
            
            # 2. Download from MinIO
            encrypted = await self._minio.download_archive(storage_key)
            
            if not encrypted:
                self._logger.error(f"Failed to download archive from MinIO: {storage_key}")
                return None
            
            # 3. Verify checksum
            actual_checksum = hashlib.sha256(encrypted).hexdigest()
            if actual_checksum != expected_checksum:
                self._logger.error(
                    f"Checksum mismatch for archive {archive_id}: "
                    f"expected {expected_checksum}, got {actual_checksum}"
                )
                return None
            
            # 4. Decrypt
            plaintext = self._encryption.decrypt(encrypted)
            
            # 5. Deserialize
            json_str = plaintext.decode("utf-8")
            package = ArchivePackage.from_json(json_str)
            
            self._logger.info(f"✅ Retrieved and decrypted archive {archive_id}")
            
            return package
            
        except DecryptionError as e:
            self._logger.error(f"❌ Decryption failed for archive {archive_id}: {e}")
            return None
            
        except json.JSONDecodeError as e:
            self._logger.error(f"❌ Invalid JSON in archive {archive_id}: {e}")
            return None
            
        except Exception as e:
            self._logger.exception(f"❌ Failed to retrieve archive {archive_id}: {e}")
            return None
    
    async def get_archive_metadata(
        self,
        archive_id: UUID,
    ) -> Optional[Dict[str, Any]]:
        """
        Get archive metadata without decrypting content.
        
        Args:
            archive_id: Archive UUID
            
        Returns:
            Archive metadata dict or None
        """
        async with self._db.session() as db_session:
            archive = await self._archive_repo.get(db_session, archive_id)
            
            if not archive:
                return None
            
            return {
                "id": str(archive.id),
                "session_id": archive.session_id,
                "storage_key": archive.storage_key,
                "storage_bucket": archive.storage_bucket,
                "size_bytes": archive.size_bytes,
                "size_mb": archive.size_mb,
                "checksum": archive.checksum,
                "archived_at": archive.archived_at.isoformat(),
                "archived_by": str(archive.archived_by) if archive.archived_by else None,
                "archived_by_name": archive.archived_by_name,
                "retention_until": archive.retention_until.isoformat() if archive.retention_until else None,
                "retention_tier": archive.retention_tier,
                "is_expired": archive.is_retention_expired,
                "is_permanent": archive.is_permanent,
                "days_until_expiry": archive.days_until_expiry,
                "discord_user_id": archive.discord_user_id,
                "discord_user_name": archive.discord_user_name,
                "severity": archive.severity,
                "notes_count": archive.notes_count,
                "session_started_at": archive.session_started_at.isoformat() if archive.session_started_at else None,
                "session_ended_at": archive.session_ended_at.isoformat() if archive.session_ended_at else None,
            }
    
    # =========================================================================
    # Listing and Filtering
    # =========================================================================
    
    async def list_archives(
        self,
        filters: Optional[ArchiveListFilter] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        List archives with optional filtering.
        
        Uses dedicated columns for efficient filtering.
        
        Args:
            filters: Optional filter criteria
            skip: Number of records to skip (pagination)
            limit: Maximum records to return
            
        Returns:
            Tuple of (list of archive metadata dicts, total count)
        """
        async with self._db.session() as db_session:
            # Extract filter values
            discord_user_id = filters.discord_user_id if filters else None
            severity = filters.severity if filters else None
            retention_tier = filters.retention_tier if filters else None
            archived_by = filters.archived_by if filters else None
            start_date = filters.start_date if filters else None
            end_date = filters.end_date if filters else None
            
            # Get archives using column-based filtering
            archives = await self._archive_repo.get_archives_filtered(
                session=db_session,
                discord_user_id=discord_user_id,
                severity=severity,
                retention_tier=retention_tier,
                archived_by=archived_by,
                start_date=start_date,
                end_date=end_date,
                skip=skip,
                limit=limit,
            )
            
            # Get total count
            total = await self._archive_repo.count_filtered(
                session=db_session,
                discord_user_id=discord_user_id,
                severity=severity,
                retention_tier=retention_tier,
                archived_by=archived_by,
                start_date=start_date,
                end_date=end_date,
            )
            
            # Convert to response dicts
            results = [
                {
                    "id": str(archive.id),
                    "session_id": archive.session_id,
                    "discord_user_id": archive.discord_user_id,
                    "discord_user_name": archive.discord_user_name,
                    "severity": archive.severity,
                    "session_started_at": archive.session_started_at.isoformat() if archive.session_started_at else None,
                    "session_ended_at": archive.session_ended_at.isoformat() if archive.session_ended_at else None,
                    "archived_at": archive.archived_at.isoformat(),
                    "archived_by_name": archive.archived_by_name,
                    "size_bytes": archive.size_bytes,
                    "size_mb": archive.size_mb,
                    "notes_count": archive.notes_count,
                    "retention_tier": archive.retention_tier,
                    "retention_until": archive.retention_until.isoformat() if archive.retention_until else None,
                    "is_expired": archive.is_retention_expired,
                    "is_permanent": archive.is_permanent,
                    "days_until_expiry": archive.days_until_expiry,
                }
                for archive in archives
            ]
            
            return results, total
    
    async def get_archives_for_session(
        self,
        session_id: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Get archive for a specific session.
        
        Args:
            session_id: Crisis session ID
            
        Returns:
            Archive metadata dict or None
        """
        async with self._db.session() as db_session:
            archive = await self._archive_repo.get_by_session(db_session, session_id)
            
            if not archive:
                return None
            
            return {
                "id": str(archive.id),
                "session_id": archive.session_id,
                "discord_user_id": archive.discord_user_id,
                "discord_user_name": archive.discord_user_name,
                "severity": archive.severity,
                "archived_at": archive.archived_at.isoformat(),
                "archived_by_name": archive.archived_by_name,
                "size_bytes": archive.size_bytes,
                "notes_count": archive.notes_count,
                "retention_tier": archive.retention_tier,
                "retention_until": archive.retention_until.isoformat() if archive.retention_until else None,
            }
    
    async def session_has_archive(
        self,
        session_id: str,
    ) -> bool:
        """
        Check if a session has been archived.
        
        Args:
            session_id: Crisis session ID
            
        Returns:
            True if archive exists
        """
        async with self._db.session() as db_session:
            return await self._archive_repo.session_has_archive(db_session, session_id)
    
    async def get_archives_by_discord_user(
        self,
        discord_user_id: int,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        Get all archives for a specific Discord user.
        
        Args:
            discord_user_id: Discord user ID
            skip: Records to skip
            limit: Maximum records
            
        Returns:
            List of archive metadata dicts
        """
        async with self._db.session() as db_session:
            archives = await self._archive_repo.get_by_discord_user(
                db_session,
                discord_user_id,
                skip=skip,
                limit=limit,
            )
            
            return [
                {
                    "id": str(a.id),
                    "session_id": a.session_id,
                    "severity": a.severity,
                    "archived_at": a.archived_at.isoformat(),
                    "archived_by_name": a.archived_by_name,
                    "notes_count": a.notes_count,
                    "retention_tier": a.retention_tier,
                }
                for a in archives
            ]
    
    # =========================================================================
    # Retention Management
    # =========================================================================
    
    async def update_retention_tier(
        self,
        archive_id: UUID,
        new_tier: str,
        updated_by_id: UUID,
        updated_by_name: str,
    ) -> bool:
        """
        Change retention tier for an archive.
        
        Args:
            archive_id: Archive UUID
            new_tier: New retention tier ("standard" or "permanent")
            updated_by_id: UUID of user making change
            updated_by_name: Name of user making change
            
        Returns:
            True if updated successfully
        """
        if new_tier not in RETENTION_TIERS:
            self._logger.error(f"Invalid retention tier: {new_tier}")
            return False
        
        try:
            async with self._db.session() as db_session:
                archive = await self._archive_repo.get(db_session, archive_id)
                
                if not archive:
                    self._logger.warning(f"Archive not found: {archive_id}")
                    return False
                
                old_tier = archive.retention_tier
                new_days = self._retention_days.get(new_tier, 365)
                
                # Update using dedicated method
                await self._archive_repo.set_retention_tier(
                    db_session,
                    archive_id,
                    tier=new_tier,
                    retention_days=new_days,
                )
                
                # Log the change in extra_data
                extra = archive.extra_data or {}
                extra["retention_updated_at"] = datetime.now(timezone.utc).isoformat()
                extra["retention_updated_by"] = updated_by_name
                extra["previous_tier"] = old_tier
                
                await self._archive_repo.update(
                    db_session,
                    archive_id,
                    {"extra_data": extra},
                )
                await db_session.commit()
            
            self._logger.info(
                f"📋 Updated archive {archive_id} retention: "
                f"{old_tier} → {new_tier} by {updated_by_name}"
            )
            return True
            
        except Exception as e:
            self._logger.exception(f"Failed to update retention for archive {archive_id}: {e}")
            return False
    
    async def extend_retention(
        self,
        archive_id: UUID,
        days: int,
        extended_by_name: str,
    ) -> bool:
        """
        Extend an archive's retention by specified days.
        
        Args:
            archive_id: Archive UUID
            days: Days to extend
            extended_by_name: Name of user extending
            
        Returns:
            True if extended successfully
        """
        try:
            async with self._db.session() as db_session:
                archive = await self._archive_repo.extend_retention_by_days(
                    db_session,
                    archive_id,
                    days,
                )
                
                if not archive:
                    return False
                
                # Update extra_data with extension record
                extra = archive.extra_data or {}
                extensions = extra.get("retention_extensions", [])
                extensions.append({
                    "extended_at": datetime.now(timezone.utc).isoformat(),
                    "extended_by": extended_by_name,
                    "days_added": days,
                })
                extra["retention_extensions"] = extensions
                
                await self._archive_repo.update(
                    db_session,
                    archive_id,
                    {"extra_data": extra},
                )
                await db_session.commit()
            
            self._logger.info(
                f"📋 Extended archive {archive_id} retention by {days} days "
                f"by {extended_by_name}"
            )
            return True
            
        except Exception as e:
            self._logger.exception(f"Failed to extend retention for archive {archive_id}: {e}")
            return False
    
    # =========================================================================
    # Cleanup Operations
    # =========================================================================
    
    async def delete_expired_archives(self) -> int:
        """
        Delete archives past their retention date.
        
        Only deletes "standard" tier archives. Permanent archives
        require manual deletion.
        
        Returns:
            Number of archives deleted
        """
        self._logger.info("🗑️ Starting expired archive cleanup")
        deleted_count = 0
        
        try:
            async with self._db.session() as db_session:
                # Get expired standard-tier archives only
                expired = await self._archive_repo.get_expired_standard_tier(
                    db_session,
                    limit=100,
                )
                
                for archive in expired:
                    try:
                        # Delete from MinIO
                        await self._minio.delete_archive(archive.storage_key)
                        
                        # Delete from database
                        await self._archive_repo.delete(db_session, archive.id)
                        
                        deleted_count += 1
                        self._logger.info(f"🗑️ Deleted expired archive: {archive.id}")
                        
                    except Exception as e:
                        self._logger.error(
                            f"Failed to delete archive {archive.id}: {e}"
                        )
                
                await db_session.commit()
            
            if deleted_count > 0:
                self._logger.info(f"🗑️ Cleanup complete: deleted {deleted_count} expired archives")
            else:
                self._logger.debug("No expired archives to delete")
            
            return deleted_count
            
        except Exception as e:
            self._logger.exception(f"Failed during archive cleanup: {e}")
            return deleted_count
    
    async def get_expiring_soon(
        self,
        days: int = 30,
    ) -> List[Dict[str, Any]]:
        """
        Get archives expiring within N days.
        
        Args:
            days: Days until expiration threshold
            
        Returns:
            List of archive metadata dicts
        """
        async with self._db.session() as db_session:
            archives = await self._archive_repo.get_expiring_soon(
                db_session,
                days=days,
            )
            
            return [
                {
                    "id": str(a.id),
                    "session_id": a.session_id,
                    "discord_user_name": a.discord_user_name,
                    "retention_until": a.retention_until.isoformat() if a.retention_until else None,
                    "days_remaining": a.days_until_expiry,
                    "retention_tier": a.retention_tier,
                }
                for a in archives
            ]
    
    # =========================================================================
    # Statistics
    # =========================================================================
    
    async def get_statistics(self) -> Dict[str, Any]:
        """
        Get archive storage statistics.
        
        Returns:
            Dictionary of statistics
        """
        async with self._db.session() as db_session:
            return await self._archive_repo.get_storage_statistics(db_session)


# =============================================================================
# Factory Functions
# =============================================================================


async def create_archive_manager(
    config_manager,
    secrets_manager,
    minio_manager,
    database_manager,
    archive_repository,
    logging_manager,
) -> ArchiveManager:
    """
    Factory function to create ArchiveManager instance.
    
    Following Clean Architecture v5.2 Rule #1: Factory Functions.
    
    Args:
        config_manager: Configuration manager instance
        secrets_manager: Secrets manager instance (for encryption key)
        minio_manager: MinIO storage manager instance
        database_manager: Database manager instance
        archive_repository: Archive repository instance
        logging_manager: Logging manager instance
        
    Returns:
        Configured ArchiveManager instance
        
    Raises:
        InvalidKeyError: If archive master key is not configured
    """
    logger = logging_manager.get_logger(__name__)
    logger.info("🏭 Creating ArchiveManager")
    
    # Create encryption handler
    encryption = create_archive_encryption(secrets_manager)
    
    # Create manager
    manager = ArchiveManager(
        config_manager=config_manager,
        minio_manager=minio_manager,
        encryption=encryption,
        database_manager=database_manager,
        archive_repository=archive_repository,
        logging_manager=logging_manager,
    )
    
    logger.info("✅ ArchiveManager created successfully")
    
    return manager


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "ArchiveManager",
    "ArchivePackage",
    "ArchiveResult",
    "ArchiveListFilter",
    "create_archive_manager",
    "RETENTION_TIERS",
]
