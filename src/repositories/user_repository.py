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
User Repository - Data access layer for User entities
----------------------------------------------------------------------------
FILE VERSION: v5.0-2-2.5-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 2 - Data Layer
CLEAN ARCHITECTURE: Compliant (Rule #1 Factory, Rule #2 DI)
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.repositories.base import BaseRepository

__version__ = "v5.0-2-2.5-1"


class UserRepository(BaseRepository[User, UUID]):
    """
    Repository for User entity operations.

    Provides CRUD operations plus user-specific queries like
    finding by email, Pocket-ID, role, and group membership.
    """

    def __init__(self, db_manager, logging_manager):
        """
        Initialize UserRepository.

        Args:
            db_manager: DatabaseManager instance
            logging_manager: LoggingManager instance
        """
        super().__init__(User, db_manager, logging_manager)

    # =========================================================================
    # User-Specific Queries
    # =========================================================================

    async def get_by_email(
        self,
        session: AsyncSession,
        email: str,
    ) -> Optional[User]:
        """
        Find a user by email address.

        Args:
            session: Database session
            email: Email address to search for

        Returns:
            User or None if not found
        """
        return await self.get_by_field(session, "email", email)

    async def get_by_pocket_id(
        self,
        session: AsyncSession,
        pocket_id_sub: str,
    ) -> Optional[User]:
        """
        Find a user by Pocket-ID subject identifier.

        Args:
            session: Database session
            pocket_id_sub: Pocket-ID subject identifier

        Returns:
            User or None if not found
        """
        return await self.get_by_field(session, "pocket_id_sub", pocket_id_sub)

    async def get_by_email_or_pocket_id(
        self,
        session: AsyncSession,
        email: str,
        pocket_id_sub: str,
    ) -> Optional[User]:
        """
        Find a user by email OR Pocket-ID.

        Useful for SSO login flows where we might match on either.

        Args:
            session: Database session
            email: Email address
            pocket_id_sub: Pocket-ID subject identifier

        Returns:
            User or None if not found
        """
        query = select(User).where(
            or_(
                User.email == email,
                User.pocket_id_sub == pocket_id_sub,
            )
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def get_active_users(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ) -> List[User]:
        """
        Get all active users.

        Args:
            session: Database session
            skip: Number of records to skip
            limit: Maximum number of records

        Returns:
            List of active users
        """
        return await self.get_filtered(
            session,
            filters={"is_active": True},
            skip=skip,
            limit=limit,
            order_by="display_name",
        )

    async def get_by_role(
        self,
        session: AsyncSession,
        role: str,
        active_only: bool = True,
    ) -> List[User]:
        """
        Get users by role.

        Args:
            session: Database session
            role: Role to filter by (e.g., "admin", "crt_member")
            active_only: If True, only return active users

        Returns:
            List of users with the specified role
        """
        filters = {"role": role}
        if active_only:
            filters["is_active"] = True
        
        return await self.get_filtered(
            session,
            filters=filters,
            order_by="display_name",
            limit=1000,
        )

    async def get_admins(
        self,
        session: AsyncSession,
        active_only: bool = True,
    ) -> List[User]:
        """
        Get all admin users.

        Args:
            session: Database session
            active_only: If True, only return active admins

        Returns:
            List of admin users
        """
        return await self.get_by_role(session, "admin", active_only)

    async def get_crt_members(
        self,
        session: AsyncSession,
        active_only: bool = True,
    ) -> List[User]:
        """
        Get all CRT members.

        Args:
            session: Database session
            active_only: If True, only return active members

        Returns:
            List of CRT members
        """
        return await self.get_by_role(session, "crt_member", active_only)

    async def search_users(
        self,
        session: AsyncSession,
        query: str,
        active_only: bool = True,
        limit: int = 20,
    ) -> List[User]:
        """
        Search users by name or email.

        Args:
            session: Database session
            query: Search string
            active_only: If True, only return active users
            limit: Maximum results

        Returns:
            List of matching users
        """
        search_pattern = f"%{query}%"
        stmt = select(User).where(
            or_(
                User.display_name.ilike(search_pattern),
                User.email.ilike(search_pattern),
            )
        )
        
        if active_only:
            stmt = stmt.where(User.is_active == True)
        
        stmt = stmt.order_by(User.display_name).limit(limit)
        result = await session.execute(stmt)
        return list(result.scalars().all())

    # =========================================================================
    # User Actions
    # =========================================================================

    async def record_login(
        self,
        session: AsyncSession,
        user_id: UUID,
    ) -> Optional[User]:
        """
        Record a user login by updating last_login timestamp.

        Args:
            session: Database session
            user_id: User ID

        Returns:
            Updated user or None if not found
        """
        return await self.update(
            session,
            user_id,
            {"last_login": datetime.now(timezone.utc)},
        )

    async def deactivate_user(
        self,
        session: AsyncSession,
        user_id: UUID,
    ) -> Optional[User]:
        """
        Deactivate a user account.

        Args:
            session: Database session
            user_id: User ID

        Returns:
            Updated user or None if not found
        """
        return await self.update(session, user_id, {"is_active": False})

    async def activate_user(
        self,
        session: AsyncSession,
        user_id: UUID,
    ) -> Optional[User]:
        """
        Activate a user account.

        Args:
            session: Database session
            user_id: User ID

        Returns:
            Updated user or None if not found
        """
        return await self.update(session, user_id, {"is_active": True})

    async def update_role(
        self,
        session: AsyncSession,
        user_id: UUID,
        new_role: str,
    ) -> Optional[User]:
        """
        Update a user's role.

        Args:
            session: Database session
            user_id: User ID
            new_role: New role value

        Returns:
            Updated user or None if not found
        """
        if new_role not in ("admin", "crt_member"):
            raise ValueError(f"Invalid role: {new_role}")
        
        return await self.update(session, user_id, {"role": new_role})

    async def update_groups(
        self,
        session: AsyncSession,
        user_id: UUID,
        groups: List[str],
    ) -> Optional[User]:
        """
        Update a user's group memberships.

        Args:
            session: Database session
            user_id: User ID
            groups: List of group names

        Returns:
            Updated user or None if not found
        """
        return await self.update(session, user_id, {"groups": groups})

    async def link_pocket_id(
        self,
        session: AsyncSession,
        user_id: UUID,
        pocket_id_sub: str,
    ) -> Optional[User]:
        """
        Link a Pocket-ID to a user account.

        Args:
            session: Database session
            user_id: User ID
            pocket_id_sub: Pocket-ID subject identifier

        Returns:
            Updated user or None if not found
        """
        return await self.update(session, user_id, {"pocket_id_sub": pocket_id_sub})


def create_user_repository(db_manager, logging_manager) -> UserRepository:
    """
    Factory function for UserRepository.

    Args:
        db_manager: DatabaseManager instance
        logging_manager: LoggingManager instance

    Returns:
        Configured UserRepository instance
    """
    return UserRepository(db_manager, logging_manager)


__all__ = ["UserRepository", "create_user_repository"]
