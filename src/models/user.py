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
User Model - CRT members and administrators linked to Pocket-ID
----------------------------------------------------------------------------
FILE VERSION: v5.0-10-10.1.6-1
LAST MODIFIED: 2026-01-10
PHASE: Phase 10 - Authentication & Authorization
CLEAN ARCHITECTURE: Compliant (Rule #14 - SQLAlchemy 2.0 Standards)
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
"""

from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, Index, String
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.database import Base, TimestampMixin

if TYPE_CHECKING:
    from src.models.session import Session
    from src.models.note import Note
    from src.models.archive import Archive
    from src.models.audit_log import AuditLog

__version__ = "v5.0-10-10.1.6-1"


class User(TimestampMixin, Base):
    """
    CRT (Crisis Response Team) member or administrator.
    
    Users are linked to Pocket-ID for authentication and authorization.
    """

    __tablename__ = "users"

    # Primary key
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    # User information
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
    )

    display_name: Mapped[str] = mapped_column(String(100))

    pocket_id_sub: Mapped[Optional[str]] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=True,
    )

    # Authorization
    groups: Mapped[list] = mapped_column(
        JSONB,
        default=list,
    )

    role: Mapped[str] = mapped_column(
        String(20),
        default="member",  # member, lead, admin
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    last_login: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relationships
    sessions: Mapped[List["Session"]] = relationship(
        back_populates="crt_user",
        foreign_keys="Session.crt_user_id",
    )

    notes: Mapped[List["Note"]] = relationship(
        back_populates="author",
        foreign_keys="Note.author_id",
    )

    archives: Mapped[List["Archive"]] = relationship(
        back_populates="archived_by_user",
        foreign_keys="Archive.archived_by",
    )

    audit_logs: Mapped[List["AuditLog"]] = relationship(
        back_populates="user",
        foreign_keys="AuditLog.user_id",
    )

    __table_args__ = (
        Index("ix_users_email", "email"),
        Index("ix_users_pocket_id", "pocket_id_sub"),
        {"comment": "CRT members and administrators"},
    )

    @property
    def is_admin(self) -> bool:
        """Check if user has admin privileges (role=admin)."""
        return self.role == "admin"

    @property
    def is_lead(self) -> bool:
        """Check if user is Lead or Admin."""
        return self.role in ("lead", "admin")

    @property
    def is_crt_member(self) -> bool:
        """Check if user has any CRT role (member, lead, or admin)."""
        return self.role in ("member", "lead", "admin")

    def has_group(self, group_name: str) -> bool:
        """Check if user belongs to a specific Pocket-ID group."""
        return group_name in (self.groups or [])

    def record_login(self) -> None:
        """Update last_login timestamp to now."""
        self.last_login = datetime.now(timezone.utc)

    def deactivate(self) -> None:
        """Deactivate the user account."""
        self.is_active = False

    def activate(self) -> None:
        """Activate the user account."""
        self.is_active = True

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"


__all__ = ["User"]
