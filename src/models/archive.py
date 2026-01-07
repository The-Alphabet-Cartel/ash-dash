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
Archive Model - Long-term encrypted storage references in MinIO
----------------------------------------------------------------------------
FILE VERSION: v5.0-2-2.3-3
LAST MODIFIED: 2026-01-07
PHASE: Phase 2 - Data Layer
CLEAN ARCHITECTURE: Compliant (Rule #14 - SQLAlchemy 2.0 Standards)
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

NOTE: Column named 'extra_data' instead of 'metadata' because 'metadata'
      is a reserved SQLAlchemy attribute on Base class (Rule #14).
"""

from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Any, Dict, Optional
from uuid import UUID, uuid4

from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, Index, LargeBinary, String
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.database import Base

if TYPE_CHECKING:
    from src.models.session import Session
    from src.models.user import User

__version__ = "v5.0-2-2.3-3"

# Default MinIO bucket
DEFAULT_BUCKET = "ash-archives"

# SHA-256 checksum length
CHECKSUM_LENGTH = 64


class Archive(Base):
    """
    Long-term encrypted storage reference for archived sessions.
    """

    __tablename__ = "archives"

    # Primary key
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    # Foreign key to session (unique - one archive per session)
    session_id: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("sessions.id", ondelete="CASCADE"),
        unique=True,
        index=True,
    )

    # Storage location
    storage_key: Mapped[str] = mapped_column(String(500))

    storage_bucket: Mapped[str] = mapped_column(
        String(100),
        default=DEFAULT_BUCKET,
    )

    # Encryption
    encryption_iv: Mapped[Optional[bytes]] = mapped_column(
        LargeBinary,
        nullable=True,
    )

    # Integrity
    checksum: Mapped[str] = mapped_column(String(64))

    size_bytes: Mapped[int] = mapped_column(BigInteger)

    # Timestamps
    archived_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )

    archived_by: Mapped[Optional[UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )

    retention_until: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        index=True,
        nullable=True,
    )

    # Additional data (named 'extra_data' to avoid SQLAlchemy reserved 'metadata')
    extra_data: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        default=dict,
        nullable=True,
    )

    # Relationships
    session: Mapped["Session"] = relationship(
        back_populates="archive",
    )

    archived_by_user: Mapped[Optional["User"]] = relationship(
        back_populates="archives",
        foreign_keys=[archived_by],
    )

    __table_args__ = (
        CheckConstraint(
            f"LENGTH(checksum) = {CHECKSUM_LENGTH}",
            name="ck_archives_valid_checksum",
        ),
        Index("ix_archives_session", "session_id"),
        Index("ix_archives_date", "archived_at"),
        {"comment": "Encrypted session archives in MinIO"},
    )

    @property
    def storage_uri(self) -> str:
        """Get the full MinIO URI."""
        return f"s3://{self.storage_bucket}/{self.storage_key}"

    @property
    def size_mb(self) -> float:
        """Get size in megabytes."""
        return self.size_bytes / (1024 * 1024)

    @property
    def is_retention_expired(self) -> bool:
        """Check if retention period has expired."""
        if not self.retention_until:
            return False
        return datetime.now(timezone.utc) > self.retention_until

    @property
    def is_encrypted(self) -> bool:
        """Check if archive has encryption IV."""
        return self.encryption_iv is not None

    def verify_checksum(self, calculated_checksum: str) -> bool:
        """Verify archive integrity."""
        return self.checksum.lower() == calculated_checksum.lower()

    def extend_retention(self, days: int) -> None:
        """Extend retention period by specified days."""
        base = self.retention_until or datetime.now(timezone.utc)
        self.retention_until = base + timedelta(days=days)

    def __repr__(self) -> str:
        size = f"{self.size_mb:.2f}MB" if self.size_bytes else "unknown"
        return f"<Archive(id={self.id}, session='{self.session_id}', size={size})>"


__all__ = ["Archive", "DEFAULT_BUCKET", "CHECKSUM_LENGTH"]
