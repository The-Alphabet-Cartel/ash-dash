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
Database Base Model - SQLAlchemy 2.0 declarative base and common mixins
----------------------------------------------------------------------------
FILE VERSION: v5.0-2-2.3-3
LAST MODIFIED: 2026-01-07
PHASE: Phase 2 - Data Layer
CLEAN ARCHITECTURE: Compliant (Rule #14 - SQLAlchemy 2.0 Standards)
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

RESPONSIBILITIES:
- Define the SQLAlchemy 2.0 declarative Base class
- Provide common model mixins (timestamps, soft delete)
- Establish naming conventions for database objects
- Support async operations with asyncpg

USAGE:
    from src.models.database import Base, TimestampMixin
    from sqlalchemy.orm import Mapped, mapped_column

    class User(TimestampMixin, Base):
        __tablename__ = "users"
        id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
        email: Mapped[str] = mapped_column(String(255), unique=True)
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import UUID

from sqlalchemy import DateTime, MetaData, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

# Module version
__version__ = "v5.0-2-2.3-3"


# =============================================================================
# NAMING CONVENTIONS
# =============================================================================
# Consistent naming for database objects improves maintainability
# and ensures Alembic migrations generate predictable constraint names

NAMING_CONVENTION: Dict[str, str] = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


# =============================================================================
# DECLARATIVE BASE
# =============================================================================


class Base(DeclarativeBase):
    """
    SQLAlchemy 2.0 declarative base class for all Ash-Dash models.

    Features:
    - SQLAlchemy 2.0 Mapped[] type annotations (Rule #14)
    - Consistent naming conventions for all database objects
    - PostgreSQL-optimized metadata
    - Helper methods for serialization

    All models should inherit from this Base class.
    """

    # Apply naming conventions to all tables
    metadata = MetaData(naming_convention=NAMING_CONVENTION)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model instance to dictionary.

        Useful for API responses and debugging.
        Handles UUID and datetime serialization.

        Returns:
            Dictionary representation of the model
        """
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)

            # Handle special types for JSON serialization
            if isinstance(value, uuid.UUID):
                value = str(value)
            elif isinstance(value, datetime):
                value = value.isoformat()

            result[column.name] = value

        return result

    def __repr__(self) -> str:
        """String representation for debugging."""
        class_name = self.__class__.__name__
        if hasattr(self, "id"):
            return f"<{class_name}(id={self.id})>"
        return f"<{class_name}()>"


# =============================================================================
# COMMON MIXINS - SQLAlchemy 2.0 Style
# =============================================================================


class TimestampMixin:
    """
    Mixin providing created_at and updated_at timestamp columns.

    Uses SQLAlchemy 2.0 Mapped[] annotations per Rule #14.

    Usage:
        class MyModel(TimestampMixin, Base):
            __tablename__ = "my_table"
            id: Mapped[UUID] = mapped_column(primary_key=True)
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class SoftDeleteMixin:
    """
    Mixin providing soft delete functionality.

    Uses SQLAlchemy 2.0 Mapped[] annotations per Rule #14.

    Usage:
        class MyModel(SoftDeleteMixin, Base):
            __tablename__ = "my_table"
            id: Mapped[UUID] = mapped_column(primary_key=True)

        # To soft delete:
        record.deleted_at = datetime.now(timezone.utc)
    """

    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )

    deleted_by: Mapped[Optional[UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True,
        default=None,
    )

    @property
    def is_deleted(self) -> bool:
        """Check if the record has been soft deleted."""
        return self.deleted_at is not None


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "Base",
    "TimestampMixin",
    "SoftDeleteMixin",
    "NAMING_CONVENTION",
]
