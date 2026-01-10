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
FILE VERSION: v5.0-9-9.4-1
LAST MODIFIED: 2026-01-09
PHASE: Phase 9 - Archive System Implementation
CLEAN ARCHITECTURE: Compliant (Rule #14 - SQLAlchemy 2.0 Standards)
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

NOTE: Column named 'extra_data' instead of 'metadata' because 'metadata'
      is a reserved SQLAlchemy attribute on Base class (Rule #14).

PHASE 9 ADDITIONS:
- Added dedicated columns for queryable fields (performance optimization)
- discord_user_id, discord_user_name: The Discord user whose session was archived
- severity: Crisis severity level for filtering
- retention_tier: "standard" (1 year) or "permanent" (7 years)
- notes_count: Number of notes included in archive
- archived_by_name: Display name of CRT member who archived
- session_started_at, session_ended_at: Original session timestamps
"""

from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Any, Dict, Optional
from uuid import UUID, uuid4

from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, Index, Integer, LargeBinary, String
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.database import Base

if TYPE_CHECKING:
    from src.models.session import Session
    from src.models.user import User

__version__ = "v5.0-9-9.4-1"

# Default MinIO bucket
DEFAULT_BUCKET = "ash-archives"

# SHA-256 checksum length
CHECKSUM_LENGTH = 64

# Valid retention tiers
RETENTION_TIERS = ("standard", "permanent")


class Archive(Base):
    """
    Long-term encrypted storage reference for archived sessions.
    
    Contains both storage metadata (where the encrypted blob is stored)
    and queryable session metadata for efficient filtering/searching.
    """

    __tablename__ = "archives"

    # =========================================================================
    # Primary Key
    # =========================================================================
    
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    # =========================================================================
    # Session Reference
    # =========================================================================
    
    # Foreign key to session (unique - one archive per session)
    session_id: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("sessions.id", ondelete="CASCADE"),
        unique=True,
        index=True,
    )

    # =========================================================================
    # Storage Location (MinIO)
    # =========================================================================
    
    storage_key: Mapped[str] = mapped_column(String(500))

    storage_bucket: Mapped[str] = mapped_column(
        String(100),
        default=DEFAULT_BUCKET,
    )

    # =========================================================================
    # Encryption & Integrity
    # =========================================================================
    
    # Legacy field - kept for backward compatibility but not used with new
    # AES-256-GCM encryption (salt/IV are embedded in the encrypted blob)
    encryption_iv: Mapped[Optional[bytes]] = mapped_column(
        LargeBinary,
        nullable=True,
    )

    # SHA-256 checksum of the encrypted blob
    checksum: Mapped[str] = mapped_column(String(64))

    # Size of encrypted blob in bytes
    size_bytes: Mapped[int] = mapped_column(BigInteger)

    # =========================================================================
    # Archive Timestamps
    # =========================================================================
    
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

    # =========================================================================
    # Retention Management
    # =========================================================================
    
    retention_until: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        index=True,
        nullable=True,
    )
    
    # Retention tier: "standard" (1 year) or "permanent" (7 years)
    retention_tier: Mapped[str] = mapped_column(
        String(20),
        default="standard",
        index=True,
    )

    # =========================================================================
    # Queryable Session Metadata (Phase 9)
    # =========================================================================
    # These columns enable efficient filtering without decrypting archives
    
    # Discord user whose session was archived
    discord_user_id: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        nullable=True,
        index=True,
    )
    
    discord_user_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    
    # Crisis severity level
    severity: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        index=True,
    )
    
    # Number of notes included in archive
    notes_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    
    # Display name of CRT member who archived (denormalized for display)
    archived_by_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    
    # Original session timestamps
    session_started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    session_ended_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # =========================================================================
    # Flexible Storage (for future extensibility)
    # =========================================================================
    
    # Additional data (named 'extra_data' to avoid SQLAlchemy reserved 'metadata')
    extra_data: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        default=dict,
        nullable=True,
    )

    # =========================================================================
    # Relationships
    # =========================================================================
    
    session: Mapped["Session"] = relationship(
        back_populates="archive",
    )

    archived_by_user: Mapped[Optional["User"]] = relationship(
        back_populates="archives",
        foreign_keys=[archived_by],
    )

    # =========================================================================
    # Table Configuration
    # =========================================================================
    
    __table_args__ = (
        # Checksum validation
        CheckConstraint(
            f"LENGTH(checksum) = {CHECKSUM_LENGTH}",
            name="ck_archives_valid_checksum",
        ),
        # Retention tier validation
        CheckConstraint(
            "retention_tier IN ('standard', 'permanent')",
            name="ck_archives_valid_retention_tier",
        ),
        # Indexes for common queries
        Index("ix_archives_session", "session_id"),
        Index("ix_archives_date", "archived_at"),
        Index("ix_archives_discord_user", "discord_user_id"),
        Index("ix_archives_severity", "severity"),
        Index("ix_archives_retention", "retention_tier", "retention_until"),
        # Composite index for common filter combinations
        Index(
            "ix_archives_filter_combo",
            "severity",
            "retention_tier",
            "archived_at",
        ),
        {"comment": "Encrypted session archives in MinIO with queryable metadata"},
    )

    # =========================================================================
    # Properties
    # =========================================================================

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
        """Check if archive has encryption IV (legacy check)."""
        return self.encryption_iv is not None
    
    @property
    def is_permanent(self) -> bool:
        """Check if archive has permanent retention."""
        return self.retention_tier == "permanent"
    
    @property
    def days_until_expiry(self) -> Optional[int]:
        """Get days until retention expires, or None if permanent/no date."""
        if not self.retention_until:
            return None
        delta = self.retention_until - datetime.now(timezone.utc)
        return max(0, delta.days)

    # =========================================================================
    # Methods
    # =========================================================================

    def verify_checksum(self, calculated_checksum: str) -> bool:
        """Verify archive integrity."""
        return self.checksum.lower() == calculated_checksum.lower()

    def extend_retention(self, days: int) -> None:
        """Extend retention period by specified days."""
        base = self.retention_until or datetime.now(timezone.utc)
        self.retention_until = base + timedelta(days=days)
    
    def set_permanent(self) -> None:
        """Set archive to permanent retention."""
        self.retention_tier = "permanent"
        # Set retention_until far in the future (but still have a date for queries)
        self.retention_until = datetime.now(timezone.utc) + timedelta(days=2555)

    def __repr__(self) -> str:
        size = f"{self.size_mb:.2f}MB" if self.size_bytes else "unknown"
        return f"<Archive(id={self.id}, session='{self.session_id}', size={size}, tier={self.retention_tier})>"


__all__ = ["Archive", "DEFAULT_BUCKET", "CHECKSUM_LENGTH", "RETENTION_TIERS"]
