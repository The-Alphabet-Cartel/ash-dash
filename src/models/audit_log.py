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
AuditLog Model - Administrative action logging for accountability
----------------------------------------------------------------------------
FILE VERSION: v5.0-2-2.3-3
LAST MODIFIED: 2026-01-07
PHASE: Phase 2 - Data Layer
CLEAN ARCHITECTURE: Compliant (Rule #14 - SQLAlchemy 2.0 Standards)
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
"""

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Dict, Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import INET, JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.database import Base

if TYPE_CHECKING:
    from src.models.user import User

__version__ = "v5.0-2-2.3-3"

# Common audit actions
AUDIT_ACTIONS = {
    "user.create": "User account created",
    "user.update": "User account updated",
    "user.delete": "User account deleted",
    "user.login": "User logged in",
    "user.logout": "User logged out",
    "user.activate": "User account activated",
    "user.deactivate": "User account deactivated",
    "session.view": "Session viewed",
    "session.assign": "Session assigned to CRT member",
    "session.unassign": "Session unassigned",
    "session.close": "Session closed",
    "note.create": "Note created",
    "note.update": "Note updated",
    "note.delete": "Note deleted",
    "note.lock": "Note locked",
    "note.unlock": "Note unlocked",
    "archive.create": "Session archived",
    "archive.retrieve": "Archive retrieved",
    "archive.delete": "Archive deleted",
    "admin.settings_change": "System settings changed",
    "admin.role_change": "User role changed",
}

# Entity types
ENTITY_TYPES = ("user", "session", "note", "archive", "settings")


class AuditLog(Base):
    """
    Audit log entry for tracking administrative and user actions.
    """

    __tablename__ = "audit_log"

    # Primary key
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    # User who performed action (nullable for system actions)
    user_id: Mapped[Optional[UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )

    # Action details
    action: Mapped[str] = mapped_column(
        String(100),
        index=True,
    )

    entity_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        index=True,
        nullable=True,
    )

    entity_id: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    # Value tracking
    old_values: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )

    new_values: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )

    # Request context
    ip_address: Mapped[Optional[str]] = mapped_column(
        INET,
        nullable=True,
    )

    user_agent: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )

    # Relationships
    user: Mapped[Optional["User"]] = relationship(
        back_populates="audit_logs",
        foreign_keys=[user_id],
    )

    __table_args__ = (
        Index("ix_audit_user", "user_id"),
        Index("ix_audit_action", "action"),
        Index("ix_audit_entity", "entity_type", "entity_id"),
        Index("ix_audit_created", "created_at"),
        {"comment": "Administrative action audit log"},
    )

    @property
    def action_description(self) -> str:
        """Get human-readable description."""
        return AUDIT_ACTIONS.get(self.action, self.action)

    @property
    def has_changes(self) -> bool:
        """Check if this entry records value changes."""
        return self.old_values is not None or self.new_values is not None

    @property
    def is_system_action(self) -> bool:
        """Check if this was a system-generated action."""
        return self.user_id is None

    @classmethod
    def create_entry(
        cls,
        action: str,
        user_id: Optional[UUID] = None,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> "AuditLog":
        """Factory method to create an audit log entry."""
        return cls(
            action=action,
            user_id=user_id,
            entity_type=entity_type,
            entity_id=str(entity_id) if entity_id else None,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent,
        )

    @classmethod
    def log_login(
        cls,
        user_id: UUID,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> "AuditLog":
        """Create a login audit entry."""
        return cls.create_entry(
            action="user.login",
            user_id=user_id,
            entity_type="user",
            entity_id=str(user_id),
            ip_address=ip_address,
            user_agent=user_agent,
        )

    def get_changed_fields(self) -> Dict[str, Dict[str, Any]]:
        """Get dictionary of changed fields."""
        if not self.old_values and not self.new_values:
            return {}
        old = self.old_values or {}
        new = self.new_values or {}
        all_keys = set(old.keys()) | set(new.keys())
        changes = {}
        for key in all_keys:
            old_val = old.get(key)
            new_val = new.get(key)
            if old_val != new_val:
                changes[key] = {"old": old_val, "new": new_val}
        return changes

    def __repr__(self) -> str:
        return f"<AuditLog(id={self.id}, action='{self.action}')>"


__all__ = ["AuditLog", "AUDIT_ACTIONS", "ENTITY_TYPES"]
