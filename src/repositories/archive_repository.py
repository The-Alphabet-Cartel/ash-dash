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
Archive Repository - Data access layer for Session Archive entities
----------------------------------------------------------------------------
FILE VERSION: v5.0-2-2.5-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 2 - Data Layer
CLEAN ARCHITECTURE: Compliant (Rule #1 Factory, Rule #2 DI)
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
"""

from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.archive import Archive
from src.repositories.base import BaseRepository

__version__ = "v5.0-2-2.5-1"


class ArchiveRepository(BaseRepository[Archive, UUID]):
    """
    Repository for Archive entity operations.

    Provides CRUD operations plus archive-specific queries like
    finding by session, checking retention, and storage statistics.
    """

    def __init__(self, db_manager, logging_manager):
        """
        Initialize ArchiveRepository.

        Args:
            db_manager: DatabaseManager instance
            logging_manager: LoggingManager instance
        """
        super().__init__(Archive, db_manager, logging_manager)

    # =========================================================================
    # Archive Queries
    # =========================================================================

    async def get_by_session(
        self,
        session: AsyncSession,
        session_id: str,
    ) -> Optional[Archive]:
        """
        Get archive for a session (one-to-one relationship).

        Args:
            session: Database session
            session_id: Crisis session ID

        Returns:
            Archive or None if not found
        """
        return await self.get_by_field(session, "session_id", session_id)

    async def get_by_storage_key(
        self,
        session: AsyncSession,
        storage_key: str,
    ) -> Optional[Archive]:
        """
        Get archive by its MinIO storage key.

        Args:
            session: Database session
            storage_key: MinIO object key

        Returns:
            Archive or None if not found
        """
        return await self.get_by_field(session, "storage_key", storage_key)

    async def session_has_archive(
        self,
        session: AsyncSession,
        session_id: str,
    ) -> bool:
        """
        Check if a session has been archived.

        Args:
            session: Database session
            session_id: Crisis session ID

        Returns:
            True if archive exists
        """
        archive = await self.get_by_session(session, session_id)
        return archive is not None

    async def get_by_archived_by(
        self,
        session: AsyncSession,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Archive]:
        """
        Get archives created by a specific user.

        Args:
            session: Database session
            user_id: User who created the archives
            skip: Records to skip
            limit: Maximum records

        Returns:
            List of archives
        """
        return await self.get_filtered(
            session,
            filters={"archived_by": user_id},
            skip=skip,
            limit=limit,
            order_by="archived_at",
            descending=True,
        )

    # =========================================================================
    # Retention Management
    # =========================================================================

    async def get_expired_archives(
        self,
        session: AsyncSession,
        limit: int = 100,
    ) -> List[Archive]:
        """
        Get archives past their retention date.

        Args:
            session: Database session
            limit: Maximum records

        Returns:
            List of expired archives
        """
        now = datetime.now(timezone.utc)
        query = (
            select(Archive)
            .where(
                and_(
                    Archive.retention_until.isnot(None),
                    Archive.retention_until < now,
                )
            )
            .order_by(Archive.retention_until.asc())
            .limit(limit)
        )
        result = await session.execute(query)
        return list(result.scalars().all())

    async def get_expiring_soon(
        self,
        session: AsyncSession,
        days: int = 30,
    ) -> List[Archive]:
        """
        Get archives expiring within N days.

        Args:
            session: Database session
            days: Days until expiration

        Returns:
            List of archives expiring soon
        """
        now = datetime.now(timezone.utc)
        cutoff = now + timedelta(days=days)
        
        query = (
            select(Archive)
            .where(
                and_(
                    Archive.retention_until.isnot(None),
                    Archive.retention_until >= now,
                    Archive.retention_until <= cutoff,
                )
            )
            .order_by(Archive.retention_until.asc())
        )
        result = await session.execute(query)
        return list(result.scalars().all())

    async def extend_retention(
        self,
        session: AsyncSession,
        archive_id: UUID,
        new_date: datetime,
    ) -> Optional[Archive]:
        """
        Extend an archive's retention date.

        Args:
            session: Database session
            archive_id: Archive UUID
            new_date: New retention date

        Returns:
            Updated archive or None if not found
        """
        return await self.update(session, archive_id, {"retention_until": new_date})

    async def extend_retention_by_days(
        self,
        session: AsyncSession,
        archive_id: UUID,
        days: int,
    ) -> Optional[Archive]:
        """
        Extend an archive's retention by N days from now.

        Args:
            session: Database session
            archive_id: Archive UUID
            days: Days to extend

        Returns:
            Updated archive or None if not found
        """
        new_date = datetime.now(timezone.utc) + timedelta(days=days)
        return await self.extend_retention(session, archive_id, new_date)

    # =========================================================================
    # Archive Creation
    # =========================================================================

    async def create_archive(
        self,
        session: AsyncSession,
        session_id: str,
        storage_key: str,
        checksum: str,
        size_bytes: int,
        archived_by: Optional[UUID] = None,
        storage_bucket: str = "ash-archives",
        encryption_iv: Optional[bytes] = None,
        retention_days: int = 365,
        extra_data: Optional[Dict[str, Any]] = None,
    ) -> Archive:
        """
        Create a new archive record.

        Args:
            session: Database session
            session_id: Crisis session ID
            storage_key: MinIO object key
            checksum: SHA-256 checksum of data
            size_bytes: Size in bytes
            archived_by: User who created the archive
            storage_bucket: MinIO bucket name
            encryption_iv: AES initialization vector
            retention_days: Days to retain
            extra_data: Additional metadata

        Returns:
            Created archive
        """
        retention_until = datetime.now(timezone.utc) + timedelta(days=retention_days)
        
        archive_data = {
            "session_id": session_id,
            "storage_key": storage_key,
            "storage_bucket": storage_bucket,
            "encryption_iv": encryption_iv,
            "checksum": checksum,
            "size_bytes": size_bytes,
            "archived_by": archived_by,
            "retention_until": retention_until,
            "extra_data": extra_data or {},
        }
        
        return await self.create(session, archive_data)

    # =========================================================================
    # Archive Verification
    # =========================================================================

    async def verify_checksum(
        self,
        session: AsyncSession,
        archive_id: UUID,
        provided_checksum: str,
    ) -> bool:
        """
        Verify an archive's checksum matches.

        Args:
            session: Database session
            archive_id: Archive UUID
            provided_checksum: Checksum to verify

        Returns:
            True if checksums match
        """
        archive = await self.get(session, archive_id)
        if not archive:
            return False
        
        return archive.checksum == provided_checksum

    # =========================================================================
    # Storage Statistics
    # =========================================================================

    async def get_storage_statistics(
        self,
        session: AsyncSession,
    ) -> Dict[str, Any]:
        """
        Get storage statistics for all archives.

        Args:
            session: Database session

        Returns:
            Dictionary of statistics
        """
        # Total count and size
        total_query = select(
            func.count(Archive.id),
            func.sum(Archive.size_bytes),
        )
        total_result = await session.execute(total_query)
        total_row = total_result.one()
        total_count = total_row[0] or 0
        total_bytes = total_row[1] or 0
        
        # Count by bucket
        bucket_query = (
            select(
                Archive.storage_bucket,
                func.count(Archive.id),
                func.sum(Archive.size_bytes),
            )
            .group_by(Archive.storage_bucket)
        )
        bucket_result = await session.execute(bucket_query)
        buckets = {
            row[0]: {"count": row[1], "size_bytes": row[2] or 0}
            for row in bucket_result.all()
        }
        
        # Encrypted count
        encrypted_query = select(func.count(Archive.id)).where(
            Archive.encryption_iv.isnot(None)
        )
        encrypted_result = await session.execute(encrypted_query)
        encrypted_count = encrypted_result.scalar() or 0
        
        return {
            "total_archives": total_count,
            "total_size_bytes": total_bytes,
            "total_size_mb": round(total_bytes / (1024 * 1024), 2),
            "total_size_gb": round(total_bytes / (1024 * 1024 * 1024), 4),
            "encrypted_count": encrypted_count,
            "by_bucket": buckets,
        }

    async def get_archives_in_date_range(
        self,
        session: AsyncSession,
        start_date: datetime,
        end_date: datetime,
    ) -> List[Archive]:
        """
        Get archives created within a date range.

        Args:
            session: Database session
            start_date: Range start (inclusive)
            end_date: Range end (inclusive)

        Returns:
            List of archives
        """
        query = (
            select(Archive)
            .where(
                and_(
                    Archive.archived_at >= start_date,
                    Archive.archived_at <= end_date,
                )
            )
            .order_by(Archive.archived_at.desc())
        )
        result = await session.execute(query)
        return list(result.scalars().all())


def create_archive_repository(db_manager, logging_manager) -> ArchiveRepository:
    """
    Factory function for ArchiveRepository.

    Args:
        db_manager: DatabaseManager instance
        logging_manager: LoggingManager instance

    Returns:
        Configured ArchiveRepository instance
    """
    return ArchiveRepository(db_manager, logging_manager)


__all__ = ["ArchiveRepository", "create_archive_repository"]
