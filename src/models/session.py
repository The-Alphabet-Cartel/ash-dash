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
Session Model - Crisis sessions with metadata from Ash-Bot
----------------------------------------------------------------------------
FILE VERSION: v5.0-2-2.3-3
LAST MODIFIED: 2026-01-07
PHASE: Phase 2 - Data Layer
CLEAN ARCHITECTURE: Compliant (Rule #14 - SQLAlchemy 2.0 Standards)
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
"""

from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.database import Base, TimestampMixin

if TYPE_CHECKING:
    from src.models.user import User
    from src.models.note import Note
    from src.models.archive import Archive

__version__ = "v5.0-2-2.3-3"

# Valid severity levels
SEVERITY_LEVELS = ("critical", "high", "medium", "low", "safe")

# Valid session statuses
SESSION_STATUSES = ("active", "closed", "archived")


class Session(TimestampMixin, Base):
    """
    Crisis session detected by Ash-Bot and analyzed by Ash-NLP.
    """

    __tablename__ = "sessions"

    # Primary key - matches Ash-Bot session ID format
    id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True,
    )

    # Foreign key to CRT responder
    crt_user_id: Mapped[Optional[UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )

    # Discord user information
    discord_user_id: Mapped[int] = mapped_column(
        BigInteger,
        index=True,
    )

    discord_username: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    # Crisis analysis results
    severity: Mapped[str] = mapped_column(
        String(20),
        index=True,
    )

    crisis_score: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(5, 4),
        nullable=True,
    )

    confidence: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(5, 4),
        nullable=True,
    )

    # Session state
    status: Mapped[str] = mapped_column(
        String(20),
        default="active",
        index=True,
    )

    # Timing
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        index=True,
    )

    ended_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    duration_seconds: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )

    # Content
    message_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    ash_summary: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    analysis_data: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )

    # Relationships
    crt_user: Mapped[Optional["User"]] = relationship(
        back_populates="sessions",
        foreign_keys=[crt_user_id],
    )

    notes: Mapped[List["Note"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="Note.created_at",
    )

    archive: Mapped[Optional["Archive"]] = relationship(
        back_populates="session",
        uselist=False,
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index("ix_sessions_discord_user", "discord_user_id"),
        Index("ix_sessions_status", "status"),
        Index("ix_sessions_severity", "severity"),
        Index("ix_sessions_started_at", "started_at"),
        {"comment": "Crisis sessions from Ash-Bot"},
    )

    @property
    def is_active(self) -> bool:
        """Check if session is still active."""
        return self.status == "active"

    @property
    def is_closed(self) -> bool:
        """Check if session has been closed."""
        return self.status == "closed"

    @property
    def is_archived(self) -> bool:
        """Check if session has been archived."""
        return self.status == "archived"

    @property
    def is_critical(self) -> bool:
        """Check if this is a critical severity session."""
        return self.severity == "critical"

    @property
    def is_high_priority(self) -> bool:
        """Check if session requires urgent attention."""
        return self.severity in ("critical", "high")

    @property
    def severity_order(self) -> int:
        """Get numerical severity order for sorting (0=highest)."""
        order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "safe": 4}
        return order.get(self.severity, 5)

    def close(self, summary: Optional[str] = None) -> None:
        """Close the session."""
        self.status = "closed"
        self.ended_at = datetime.now(timezone.utc)
        if self.started_at:
            delta = self.ended_at - self.started_at
            self.duration_seconds = int(delta.total_seconds())
        if summary:
            self.ash_summary = summary

    def assign_to(self, user_id: UUID) -> None:
        """Assign session to a CRT responder."""
        self.crt_user_id = user_id

    def unassign(self) -> None:
        """Remove CRT responder assignment."""
        self.crt_user_id = None

    def mark_archived(self) -> None:
        """Mark session as archived."""
        self.status = "archived"

    def __repr__(self) -> str:
        return f"<Session(id='{self.id}', severity='{self.severity}', status='{self.status}')>"


__all__ = ["Session", "SEVERITY_LEVELS", "SESSION_STATUSES"]
