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
Base Repository - Abstract base class for all repositories
----------------------------------------------------------------------------
FILE VERSION: v5.0-2-2.5-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 2 - Data Layer
CLEAN ARCHITECTURE: Compliant (Rule #1 Factory, Rule #2 DI, Rule #14 SQLAlchemy 2.0)
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

RESPONSIBILITIES:
- Provide common CRUD operations for all entities
- Abstract database session management
- Implement pagination and filtering patterns
- Handle async SQLAlchemy operations

USAGE:
    class UserRepository(BaseRepository[User, UUID]):
        def __init__(self, db_manager, logging_manager):
            super().__init__(User, db_manager, logging_manager)
"""

from abc import ABC
from typing import Any, Dict, Generic, List, Optional, Sequence, Type, TypeVar
from uuid import UUID

from sqlalchemy import func, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.database import Base

__version__ = "v5.0-2-2.5-1"

# Type variables for generic repository
ModelType = TypeVar("ModelType", bound=Base)
PrimaryKeyType = TypeVar("PrimaryKeyType", UUID, str, int)


class BaseRepository(Generic[ModelType, PrimaryKeyType], ABC):
    """
    Abstract base repository providing common CRUD operations.

    Generic Parameters:
        ModelType: The SQLAlchemy model class
        PrimaryKeyType: The type of the primary key (UUID, str, or int)

    All repositories should inherit from this class and can override
    methods to add entity-specific behavior.
    """

    def __init__(
        self,
        model: Type[ModelType],
        db_manager,
        logging_manager,
    ):
        """
        Initialize the base repository.

        Args:
            model: The SQLAlchemy model class
            db_manager: DatabaseManager instance for session access
            logging_manager: LoggingManager for structured logging
        """
        self._model = model
        self._db_manager = db_manager
        self._logger = logging_manager.get_logger(
            f"repository.{model.__tablename__}"
        )

    @property
    def model(self) -> Type[ModelType]:
        """Get the model class."""
        return self._model

    # =========================================================================
    # CREATE Operations
    # =========================================================================

    async def create(
        self,
        session: AsyncSession,
        obj_in: Dict[str, Any],
    ) -> ModelType:
        """
        Create a new record.

        Args:
            session: Database session
            obj_in: Dictionary of field values

        Returns:
            The created model instance
        """
        db_obj = self._model(**obj_in)
        session.add(db_obj)
        await session.flush()
        await session.refresh(db_obj)
        self._logger.debug(f"Created {self._model.__name__} with id={db_obj.id}")
        return db_obj

    async def create_many(
        self,
        session: AsyncSession,
        objects_in: List[Dict[str, Any]],
    ) -> List[ModelType]:
        """
        Create multiple records.

        Args:
            session: Database session
            objects_in: List of dictionaries with field values

        Returns:
            List of created model instances
        """
        db_objects = [self._model(**obj) for obj in objects_in]
        session.add_all(db_objects)
        await session.flush()
        for obj in db_objects:
            await session.refresh(obj)
        self._logger.debug(f"Created {len(db_objects)} {self._model.__name__} records")
        return db_objects

    # =========================================================================
    # READ Operations
    # =========================================================================

    async def get(
        self,
        session: AsyncSession,
        id: PrimaryKeyType,
        load_relationships: Optional[List[str]] = None,
    ) -> Optional[ModelType]:
        """
        Get a single record by primary key.

        Args:
            session: Database session
            id: Primary key value
            load_relationships: List of relationship names to eagerly load

        Returns:
            Model instance or None if not found
        """
        query = select(self._model).where(self._model.id == id)
        
        if load_relationships:
            for rel_name in load_relationships:
                if hasattr(self._model, rel_name):
                    query = query.options(selectinload(getattr(self._model, rel_name)))
        
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_ids(
        self,
        session: AsyncSession,
        ids: List[PrimaryKeyType],
    ) -> List[ModelType]:
        """
        Get multiple records by their primary keys.

        Args:
            session: Database session
            ids: List of primary key values

        Returns:
            List of found model instances
        """
        if not ids:
            return []
        query = select(self._model).where(self._model.id.in_(ids))
        result = await session.execute(query)
        return list(result.scalars().all())

    async def get_by_field(
        self,
        session: AsyncSession,
        field_name: str,
        value: Any,
    ) -> Optional[ModelType]:
        """
        Get a single record by a field value.

        Args:
            session: Database session
            field_name: Name of the field to filter by
            value: Value to match

        Returns:
            Model instance or None if not found
        """
        if not hasattr(self._model, field_name):
            raise ValueError(f"Model {self._model.__name__} has no field '{field_name}'")
        
        field = getattr(self._model, field_name)
        query = select(self._model).where(field == value)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        order_by: Optional[str] = None,
        descending: bool = False,
    ) -> List[ModelType]:
        """
        Get all records with pagination.

        Args:
            session: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            order_by: Field name to order by
            descending: If True, order descending

        Returns:
            List of model instances
        """
        query = select(self._model)
        
        if order_by and hasattr(self._model, order_by):
            order_field = getattr(self._model, order_by)
            query = query.order_by(order_field.desc() if descending else order_field)
        
        query = query.offset(skip).limit(limit)
        result = await session.execute(query)
        return list(result.scalars().all())

    async def get_filtered(
        self,
        session: AsyncSession,
        filters: Dict[str, Any],
        skip: int = 0,
        limit: int = 100,
        order_by: Optional[str] = None,
        descending: bool = False,
    ) -> List[ModelType]:
        """
        Get records matching filter criteria.

        Args:
            session: Database session
            filters: Dictionary of field_name: value pairs
            skip: Number of records to skip
            limit: Maximum number of records to return
            order_by: Field name to order by
            descending: If True, order descending

        Returns:
            List of matching model instances
        """
        query = select(self._model)
        
        for field_name, value in filters.items():
            if hasattr(self._model, field_name):
                field = getattr(self._model, field_name)
                if value is None:
                    query = query.where(field.is_(None))
                elif isinstance(value, list):
                    query = query.where(field.in_(value))
                else:
                    query = query.where(field == value)
        
        if order_by and hasattr(self._model, order_by):
            order_field = getattr(self._model, order_by)
            query = query.order_by(order_field.desc() if descending else order_field)
        
        query = query.offset(skip).limit(limit)
        result = await session.execute(query)
        return list(result.scalars().all())

    async def count(
        self,
        session: AsyncSession,
        filters: Optional[Dict[str, Any]] = None,
    ) -> int:
        """
        Count records, optionally filtered.

        Args:
            session: Database session
            filters: Optional dictionary of field_name: value pairs

        Returns:
            Number of matching records
        """
        query = select(func.count()).select_from(self._model)
        
        if filters:
            for field_name, value in filters.items():
                if hasattr(self._model, field_name):
                    field = getattr(self._model, field_name)
                    if value is None:
                        query = query.where(field.is_(None))
                    elif isinstance(value, list):
                        query = query.where(field.in_(value))
                    else:
                        query = query.where(field == value)
        
        result = await session.execute(query)
        return result.scalar() or 0

    async def exists(
        self,
        session: AsyncSession,
        id: PrimaryKeyType,
    ) -> bool:
        """
        Check if a record exists.

        Args:
            session: Database session
            id: Primary key value

        Returns:
            True if record exists
        """
        query = select(func.count()).select_from(self._model).where(self._model.id == id)
        result = await session.execute(query)
        return (result.scalar() or 0) > 0

    # =========================================================================
    # UPDATE Operations
    # =========================================================================

    async def update(
        self,
        session: AsyncSession,
        id: PrimaryKeyType,
        obj_in: Dict[str, Any],
    ) -> Optional[ModelType]:
        """
        Update a record by primary key.

        Args:
            session: Database session
            id: Primary key value
            obj_in: Dictionary of field values to update

        Returns:
            Updated model instance or None if not found
        """
        db_obj = await self.get(session, id)
        if not db_obj:
            return None
        
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        await session.flush()
        await session.refresh(db_obj)
        self._logger.debug(f"Updated {self._model.__name__} id={id}")
        return db_obj

    async def update_many(
        self,
        session: AsyncSession,
        filters: Dict[str, Any],
        values: Dict[str, Any],
    ) -> int:
        """
        Update multiple records matching filters.

        Args:
            session: Database session
            filters: Dictionary of field_name: value pairs for filtering
            values: Dictionary of field_name: value pairs to update

        Returns:
            Number of updated records
        """
        query = update(self._model)
        
        for field_name, value in filters.items():
            if hasattr(self._model, field_name):
                field = getattr(self._model, field_name)
                query = query.where(field == value)
        
        query = query.values(**values)
        result = await session.execute(query)
        self._logger.debug(f"Updated {result.rowcount} {self._model.__name__} records")
        return result.rowcount

    # =========================================================================
    # DELETE Operations
    # =========================================================================

    async def delete(
        self,
        session: AsyncSession,
        id: PrimaryKeyType,
    ) -> bool:
        """
        Delete a record by primary key.

        Args:
            session: Database session
            id: Primary key value

        Returns:
            True if record was deleted
        """
        db_obj = await self.get(session, id)
        if not db_obj:
            return False
        
        await session.delete(db_obj)
        await session.flush()
        self._logger.debug(f"Deleted {self._model.__name__} id={id}")
        return True

    async def delete_many(
        self,
        session: AsyncSession,
        filters: Dict[str, Any],
    ) -> int:
        """
        Delete multiple records matching filters.

        Args:
            session: Database session
            filters: Dictionary of field_name: value pairs

        Returns:
            Number of deleted records
        """
        query = delete(self._model)
        
        for field_name, value in filters.items():
            if hasattr(self._model, field_name):
                field = getattr(self._model, field_name)
                query = query.where(field == value)
        
        result = await session.execute(query)
        self._logger.debug(f"Deleted {result.rowcount} {self._model.__name__} records")
        return result.rowcount


__all__ = ["BaseRepository", "ModelType", "PrimaryKeyType"]
