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
Database Base Model - SQLAlchemy declarative base and common model utilities
----------------------------------------------------------------------------
FILE VERSION: v5.0-2-2.2-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 2 - Data Layer
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

RESPONSIBILITIES:
- Define the SQLAlchemy declarative Base class
- Provide common model mixins (timestamps, soft delete)
- Establish naming conventions for database objects
- Support async operations with asyncpg

USAGE:
    from src.models.database import Base, TimestampMixin

    class User(TimestampMixin, Base):
        __tablename__ = "users"
        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        email = Column(String(255), unique=True, nullable=False)
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict

from sqlalchemy import Column, DateTime, MetaData, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, declared_attr

# Module version
__version__ = "v5.0-2-2.2-1"


# =============================================================================
# NAMING CONVENTIONS
# =============================================================================
# Consistent naming for database objects improves maintainability
# and ensures Alembic migrations generate predictable constraint names

NAMING_CONVENTION: Dict[str, str] = {
    "ix": "ix_%(column_0_label)s",              # Index
    "uq": "uq_%(table_name)s_%(column_0_name)s",  # Unique constraint
    "ck": "ck_%(table_name)s_%(constraint_name)s",  # Check constraint
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",  # Foreign key
    "pk": "pk_%(table_name)s",                  # Primary key
}


# =============================================================================
# DECLARATIVE BASE
# =============================================================================

class Base(DeclarativeBase):
    """
    SQLAlchemy declarative base class for all Ash-Dash models.

    Features:
    - Consistent naming conventions for all database objects
    - PostgreSQL-optimized metadata
    - Automatic table name generation from class name

    All models should inherit from this Base class.
    """

    # Apply naming conventions to all tables
    metadata = MetaData(naming_convention=NAMING_CONVENTION)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Generate table name from class name.

        Converts CamelCase to snake_case and pluralizes.
        Example: UserSession -> user_sessions

        Can be overridden by explicitly setting __tablename__ on the model.
        """
        # Convert CamelCase to snake_case
        name = cls.__name__
        result = []
        for i, char in enumerate(name):
            if char.isupper() and i > 0:
                result.append("_")
            result.append(char.lower())
        table_name = "".join(result)

        # Simple pluralization (add 's' if not ending in 's')
        if not table_name.endswith("s"):
            table_name += "s"

        return table_name

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
        # Try to get a meaningful identifier
        if hasattr(self, "id"):
            return f"<{class_name}(id={self.id})>"
        return f"<{class_name}()>"


# =============================================================================
# COMMON MIXINS
# =============================================================================

class TimestampMixin:
    """
    Mixin providing created_at and updated_at timestamp columns.

    Automatically sets created_at on insert and updates updated_at on changes.

    Usage:
        class MyModel(TimestampMixin, Base):
            __tablename__ = "my_table"
            id = Column(Integer, primary_key=True)
    """

    @declared_attr
    def created_at(cls) -> Column:
        """Timestamp when the record was created."""
        return Column(
            DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc),
            nullable=False,
        )

    @declared_attr
    def updated_at(cls) -> Column:
        """Timestamp when the record was last updated."""
        return Column(
            DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc),
            onupdate=lambda: datetime.now(timezone.utc),
            nullable=False,
        )


class SoftDeleteMixin:
    """
    Mixin providing soft delete functionality.

    Records are marked as deleted rather than being removed from the database.
    This preserves data integrity and allows for recovery.

    Usage:
        class MyModel(SoftDeleteMixin, Base):
            __tablename__ = "my_table"
            id = Column(Integer, primary_key=True)

        # To soft delete:
        record.deleted_at = datetime.now(timezone.utc)
        record.deleted_by = user_id

        # To query non-deleted records:
        session.query(MyModel).filter(MyModel.deleted_at.is_(None))
    """

    @declared_attr
    def deleted_at(cls) -> Column:
        """Timestamp when the record was soft deleted (None if active)."""
        return Column(
            DateTime(timezone=True),
            nullable=True,
            default=None,
        )

    @declared_attr
    def deleted_by(cls) -> Column:
        """UUID of the user who deleted the record."""
        return Column(
            UUID(as_uuid=True),
            nullable=True,
            default=None,
        )

    @property
    def is_deleted(self) -> bool:
        """Check if the record has been soft deleted."""
        return self.deleted_at is not None


class UUIDPrimaryKeyMixin:
    """
    Mixin providing a UUID primary key column.

    Uses PostgreSQL's native UUID type with auto-generation.

    Usage:
        class MyModel(UUIDPrimaryKeyMixin, Base):
            __tablename__ = "my_table"
            name = Column(String(100))
    """

    @declared_attr
    def id(cls) -> Column:
        """UUID primary key, auto-generated."""
        return Column(
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
        )


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "Base",
    "TimestampMixin",
    "SoftDeleteMixin",
    "UUIDPrimaryKeyMixin",
    "NAMING_CONVENTION",
]
