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
User Sync Service - Synchronizes Pocket-ID users to local database
----------------------------------------------------------------------------
FILE VERSION: v5.0-10-10.1.5-1
LAST MODIFIED: 2026-01-10
PHASE: Phase 10 - Authentication & Authorization
CLEAN ARCHITECTURE: Compliant (Rule #1 Factory, Rule #2 DI)
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

This service handles user synchronization between Pocket-ID and the local
database. It is called by the authentication middleware on each authenticated
request to ensure user records exist and stay up-to-date.

RESPONSIBILITIES:
- Create new user records on first login
- Update user info when Pocket-ID claims change
- Update last_login timestamp on each request
- Compute and store role from Pocket-ID groups

USAGE:
    # In auth middleware or route handler
    from src.services.user_sync_service import create_user_sync_service
    
    user_sync = create_user_sync_service(db_manager, logging_manager)
    
    async with db_manager.session() as db:
        user = await user_sync.sync_user(
            pocket_id_sub=claims["sub"],
            email=claims["email"],
            name=claims["name"],
            groups=claims["groups"],
            db=db,
        )
"""

from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.models.enums import UserRole, get_role_from_groups
from src.repositories.user_repository import create_user_repository

__version__ = "v5.0-10-10.1.5-1"


class UserSyncService:
    """
    Service for synchronizing Pocket-ID users to the local database.
    
    This service is called on each authenticated request to ensure
    user records exist and stay current with Pocket-ID claims.
    
    Attributes:
        _db_manager: DatabaseManager for connections
        _logging_manager: LoggingManager for logging
        _logger: Logger instance
        _repo: UserRepository for database operations
    """
    
    def __init__(self, db_manager, logging_manager):
        """
        Initialize UserSyncService.
        
        Args:
            db_manager: DatabaseManager instance
            logging_manager: LoggingManager instance
        """
        self._db_manager = db_manager
        self._logging_manager = logging_manager
        self._logger = logging_manager.get_logger("user_sync")
        self._repo = create_user_repository(db_manager, logging_manager)
    
    async def sync_user(
        self,
        pocket_id_sub: str,
        email: str,
        name: str,
        groups: list[str],
        db: AsyncSession,
    ) -> Optional[User]:
        """
        Create or update user from Pocket-ID claims.
        
        Called by auth middleware on each authenticated request.
        Creates a new user if one doesn't exist, or updates the
        existing user if their information has changed.
        
        Args:
            pocket_id_sub: Pocket-ID subject (unique user ID)
            email: User's email address
            name: User's display name
            groups: List of Pocket-ID groups
            db: Database session
            
        Returns:
            User model instance, or None if user is not a CRT member
            
        Note:
            Users without CRT group membership are not synced to the
            database. They will receive a 403 Forbidden response from
            the auth middleware.
        """
        # Compute role from Pocket-ID groups
        role = get_role_from_groups(groups)
        
        if role is None:
            # User is not a CRT member - don't sync to database
            self._logger.debug(
                f"User {email} has no CRT groups ({groups}), skipping sync"
            )
            return None
        
        # Look for existing user by Pocket-ID subject
        user = await self._repo.get_by_pocket_id(db, pocket_id_sub)
        
        if user:
            # Update existing user if anything changed
            user = await self._update_existing_user(
                db=db,
                user=user,
                email=email,
                name=name,
                groups=groups,
                role=role,
            )
        else:
            # Check if user exists by email (may have been created before SSO)
            user = await self._repo.get_by_email(db, email)
            
            if user:
                # Link existing email user to Pocket-ID
                user = await self._link_pocket_id(
                    db=db,
                    user=user,
                    pocket_id_sub=pocket_id_sub,
                    name=name,
                    groups=groups,
                    role=role,
                )
            else:
                # Create new user
                user = await self._create_new_user(
                    db=db,
                    pocket_id_sub=pocket_id_sub,
                    email=email,
                    name=name,
                    groups=groups,
                    role=role,
                )
        
        return user
    
    async def _update_existing_user(
        self,
        db: AsyncSession,
        user: User,
        email: str,
        name: str,
        groups: list[str],
        role: UserRole,
    ) -> User:
        """
        Update an existing user with new Pocket-ID claims.
        
        Only updates fields that have changed to minimize database writes.
        Always updates last_login timestamp.
        
        Args:
            db: Database session
            user: Existing user record
            email: Email from Pocket-ID
            name: Name from Pocket-ID
            groups: Groups from Pocket-ID
            role: Computed role
            
        Returns:
            Updated user record
        """
        # Check what changed
        changes = {}
        
        if user.email != email:
            changes["email"] = email
            
        if user.display_name != name:
            changes["display_name"] = name
            
        if set(user.groups or []) != set(groups):
            changes["groups"] = groups
            
        if user.role != role.value:
            changes["role"] = role.value
            
        # Reactivate if previously deactivated
        if not user.is_active:
            changes["is_active"] = True
            self._logger.info(f"Reactivated user: {email}")
        
        # Always update last_login and updated_at
        now = datetime.now(timezone.utc)
        changes["last_login"] = now
        changes["updated_at"] = now
        
        # Apply changes
        for key, value in changes.items():
            setattr(user, key, value)
        
        await db.commit()
        await db.refresh(user)
        
        # Log significant changes
        significant_changes = {k: v for k, v in changes.items() 
                              if k not in ("last_login", "updated_at")}
        if significant_changes:
            self._logger.info(
                f"Updated CRT user: {email} (role: {role.value}) - "
                f"changed: {list(significant_changes.keys())}"
            )
        
        return user
    
    async def _link_pocket_id(
        self,
        db: AsyncSession,
        user: User,
        pocket_id_sub: str,
        name: str,
        groups: list[str],
        role: UserRole,
    ) -> User:
        """
        Link a Pocket-ID to an existing email user.
        
        This handles the case where a user record was created before
        SSO was enabled (e.g., manually created admin accounts).
        
        Args:
            db: Database session
            user: Existing user record
            pocket_id_sub: Pocket-ID subject
            name: Name from Pocket-ID
            groups: Groups from Pocket-ID
            role: Computed role
            
        Returns:
            Updated user record
        """
        now = datetime.now(timezone.utc)
        
        user.pocket_id_sub = pocket_id_sub
        user.display_name = name
        user.groups = groups
        user.role = role.value
        user.is_active = True
        user.last_login = now
        user.updated_at = now
        
        await db.commit()
        await db.refresh(user)
        
        self._logger.info(
            f"Linked Pocket-ID to existing user: {user.email} (role: {role.value})"
        )
        
        return user
    
    async def _create_new_user(
        self,
        db: AsyncSession,
        pocket_id_sub: str,
        email: str,
        name: str,
        groups: list[str],
        role: UserRole,
    ) -> User:
        """
        Create a new user from Pocket-ID claims.
        
        Args:
            db: Database session
            pocket_id_sub: Pocket-ID subject
            email: User's email
            name: User's display name
            groups: Pocket-ID groups
            role: Computed role
            
        Returns:
            New user record
        """
        now = datetime.now(timezone.utc)
        
        user = User(
            pocket_id_sub=pocket_id_sub,
            email=email,
            display_name=name or email.split("@")[0],  # Fallback to email prefix
            groups=groups,
            role=role.value,
            is_active=True,
            last_login=now,
        )
        
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        self._logger.info(
            f"✅ Created new CRT user: {email} (role: {role.value})"
        )
        
        return user
    
    async def get_user_by_pocket_id(
        self,
        db: AsyncSession,
        pocket_id_sub: str,
    ) -> Optional[User]:
        """
        Get a user by their Pocket-ID subject.
        
        Args:
            db: Database session
            pocket_id_sub: Pocket-ID subject
            
        Returns:
            User or None if not found
        """
        return await self._repo.get_by_pocket_id(db, pocket_id_sub)
    
    async def deactivate_user(
        self,
        db: AsyncSession,
        pocket_id_sub: str,
    ) -> bool:
        """
        Deactivate a user (e.g., when removed from CRT groups).
        
        Args:
            db: Database session
            pocket_id_sub: Pocket-ID subject
            
        Returns:
            True if user was deactivated, False if not found
        """
        user = await self._repo.get_by_pocket_id(db, pocket_id_sub)
        
        if user:
            user.is_active = False
            user.updated_at = datetime.now(timezone.utc)
            await db.commit()
            
            self._logger.info(f"Deactivated user: {user.email}")
            return True
        
        return False
    
    async def get_all_active_users(
        self,
        db: AsyncSession,
    ) -> list[User]:
        """
        Get all active CRT users.
        
        Args:
            db: Database session
            
        Returns:
            List of active users
        """
        return await self._repo.get_active_users(db, limit=1000)


def create_user_sync_service(db_manager, logging_manager) -> UserSyncService:
    """
    Factory function for UserSyncService.
    
    Args:
        db_manager: DatabaseManager instance
        logging_manager: LoggingManager instance
        
    Returns:
        Configured UserSyncService instance
    """
    return UserSyncService(db_manager, logging_manager)


__all__ = [
    "UserSyncService",
    "create_user_sync_service",
]
