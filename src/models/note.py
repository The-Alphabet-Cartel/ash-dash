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
Note Model - Session documentation written by CRT members
----------------------------------------------------------------------------
FILE VERSION: v5.0-2-2.3-3
LAST MODIFIED: 2026-01-07
PHASE: Phase 2 - Data Layer
CLEAN ARCHITECTURE: Compliant (Rule #14 - SQLAlchemy 2.0 Standards)
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
"""

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.database import Base, TimestampMixin

if TYPE_CHECKING:
    from src.models.session import Session
    from src.models.user import User

__version__ = "v5.0-2-2.3-3"


class Note(TimestampMixin, Base):
    """
    Documentation note written by CRT members during crisis sessions.
    """

    __tablename__ = "notes"

    # Primary key
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    # Foreign keys
    session_id: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("sessions.id", ondelete="CASCADE"),
        index=True,
    )

    author_id: Mapped[Optional[UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )

    # Content
    content: Mapped[str] = mapped_column(Text)

    content_html: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Versioning
    version: Mapped[int] = mapped_column(
        Integer,
        default=1,
    )

    is_locked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    # Relationships
    session: Mapped["Session"] = relationship(
        back_populates="notes",
    )

    author: Mapped[Optional["User"]] = relationship(
        back_populates="notes",
        foreign_keys=[author_id],
    )

    __table_args__ = (
        CheckConstraint(
            "LENGTH(content) > 0",
            name="ck_notes_content_not_empty",
        ),
        Index("ix_notes_session", "session_id"),
        Index("ix_notes_author", "author_id"),
        {"comment": "Session documentation notes"},
    )

    @property
    def is_editable(self) -> bool:
        """Check if note can be edited (not locked)."""
        return not self.is_locked

    @property
    def word_count(self) -> int:
        """Get approximate word count of content."""
        if not self.content:
            return 0
        return len(self.content.split())

    def update_content(
        self,
        new_content: str,
        html_content: Optional[str] = None,
    ) -> bool:
        """Update note content if not locked."""
        if self.is_locked:
            return False
        self.content = new_content
        self.content_html = html_content
        self.version += 1
        self.updated_at = datetime.now(timezone.utc)
        return True

    def lock(self) -> None:
        """Lock the note to prevent further edits."""
        self.is_locked = True

    def unlock(self) -> None:
        """Unlock the note (admin only)."""
        self.is_locked = False

    def __repr__(self) -> str:
        return f"<Note(id={self.id}, session_id='{self.session_id}', v{self.version})>"


__all__ = ["Note"]
