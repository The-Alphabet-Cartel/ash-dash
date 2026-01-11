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
Audit Log Repository - Data access layer for Audit Log entities
----------------------------------------------------------------------------
FILE VERSION: v5.0-2-2.5-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 2 - Data Layer
CLEAN ARCHITECTURE: Compliant (Rule #1 Factory, Rule #2 DI)
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
"""

from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.audit_log import AuditLog, AUDIT_ACTIONS, ENTITY_TYPES
from src.repositories.base import BaseRepository

__version__ = "v5.0-2-2.5-1"


class AuditLogRepository(BaseRepository[AuditLog, UUID]):
    """
    Repository for AuditLog entity operations.

    Provides query operations for audit logs. Note that audit logs
    are typically append-only - updates and deletes are not common.
    """

    def __init__(self, db_manager, logging_manager):
        """
        Initialize AuditLogRepository.

        Args:
            db_manager: DatabaseManager instance
            logging_manager: LoggingManager instance
        """
        super().__init__(AuditLog, db_manager, logging_manager)

    # =========================================================================
    # Audit Log Creation
    # =========================================================================

    async def log_action(
        self,
        session: AsyncSession,
        action: str,
        user_id: Optional[UUID] = None,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> AuditLog:
        """
        Create a new audit log entry.

        Args:
            session: Database session
            action: Action performed (see AUDIT_ACTIONS)
            user_id: User who performed the action (None for system)
            entity_type: Type of entity affected
            entity_id: ID of entity affected
            old_values: Previous values (for updates)
            new_values: New values (for creates/updates)
            ip_address: Client IP address
            user_agent: Client user agent string

        Returns:
            Created audit log entry
        """
        log_data = {
            "action": action,
            "user_id": user_id,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "old_values": old_values,
            "new_values": new_values,
            "ip_address": ip_address,
            "user_agent": user_agent,
        }
        return await self.create(session, log_data)

    async def log_login(
        self,
        session: AsyncSession,
        user_id: UUID,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        success: bool = True,
    ) -> AuditLog:
        """
        Log a user login attempt.

        Args:
            session: Database session
            user_id: User ID
            ip_address: Client IP
            user_agent: Client user agent
            success: Whether login succeeded

        Returns:
            Created audit log entry
        """
        action = "login_success" if success else "login_failure"
        return await self.log_action(
            session,
            action=action,
            user_id=user_id,
            entity_type="user",
            entity_id=str(user_id),
            ip_address=ip_address,
            user_agent=user_agent,
        )

    async def log_session_view(
        self,
        session: AsyncSession,
        user_id: UUID,
        session_id: str,
        ip_address: Optional[str] = None,
    ) -> AuditLog:
        """
        Log when a user views a crisis session.

        Args:
            session: Database session
            user_id: User ID
            session_id: Crisis session ID
            ip_address: Client IP

        Returns:
            Created audit log entry
        """
        return await self.log_action(
            session,
            action="session_view",
            user_id=user_id,
            entity_type="session",
            entity_id=session_id,
            ip_address=ip_address,
        )

    async def log_note_action(
        self,
        session: AsyncSession,
        action: str,
        user_id: UUID,
        note_id: UUID,
        session_id: str,
        content_preview: Optional[str] = None,
        ip_address: Optional[str] = None,
    ) -> AuditLog:
        """
        Log note create/update/delete action.

        Args:
            session: Database session
            action: One of note_create, note_update, note_delete
            user_id: User ID
            note_id: Note UUID
            session_id: Associated session ID
            content_preview: First N chars of content
            ip_address: Client IP

        Returns:
            Created audit log entry
        """
        new_values = {"session_id": session_id}
        if content_preview:
            new_values["content_preview"] = content_preview[:100]
        
        return await self.log_action(
            session,
            action=action,
            user_id=user_id,
            entity_type="note",
            entity_id=str(note_id),
            new_values=new_values,
            ip_address=ip_address,
        )

    # =========================================================================
    # Audit Log Queries by User
    # =========================================================================

    async def get_by_user(
        self,
        session: AsyncSession,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> List[AuditLog]:
        """
        Get audit logs for a specific user.

        Args:
            session: Database session
            user_id: User UUID
            skip: Records to skip
            limit: Maximum records

        Returns:
            List of audit logs
        """
        return await self.get_filtered(
            session,
            filters={"user_id": user_id},
            skip=skip,
            limit=limit,
            order_by="created_at",
            descending=True,
        )

    async def get_user_recent_activity(
        self,
        session: AsyncSession,
        user_id: UUID,
        hours: int = 24,
    ) -> List[AuditLog]:
        """
        Get recent activity for a user.

        Args:
            session: Database session
            user_id: User UUID
            hours: Hours to look back

        Returns:
            List of recent audit logs
        """
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        
        query = (
            select(AuditLog)
            .where(
                and_(
                    AuditLog.user_id == user_id,
                    AuditLog.created_at >= cutoff,
                )
            )
            .order_by(AuditLog.created_at.desc())
        )
        result = await session.execute(query)
        return list(result.scalars().all())

    # =========================================================================
    # Audit Log Queries by Entity
    # =========================================================================

    async def get_by_entity(
        self,
        session: AsyncSession,
        entity_type: str,
        entity_id: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[AuditLog]:
        """
        Get audit logs for a specific entity.

        Args:
            session: Database session
            entity_type: Entity type (user, session, note, archive)
            entity_id: Entity ID
            skip: Records to skip
            limit: Maximum records

        Returns:
            List of audit logs
        """
        return await self.get_filtered(
            session,
            filters={"entity_type": entity_type, "entity_id": entity_id},
            skip=skip,
            limit=limit,
            order_by="created_at",
            descending=True,
        )

    async def get_session_audit_trail(
        self,
        session: AsyncSession,
        session_id: str,
    ) -> List[AuditLog]:
        """
        Get complete audit trail for a crisis session.

        Args:
            session: Database session
            session_id: Crisis session ID

        Returns:
            List of all audit logs related to the session
        """
        return await self.get_by_entity(session, "session", session_id, limit=1000)

    # =========================================================================
    # Audit Log Queries by Action
    # =========================================================================

    async def get_by_action(
        self,
        session: AsyncSession,
        action: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[AuditLog]:
        """
        Get audit logs by action type.

        Args:
            session: Database session
            action: Action type
            skip: Records to skip
            limit: Maximum records

        Returns:
            List of audit logs
        """
        return await self.get_filtered(
            session,
            filters={"action": action},
            skip=skip,
            limit=limit,
            order_by="created_at",
            descending=True,
        )

    async def get_login_history(
        self,
        session: AsyncSession,
        user_id: Optional[UUID] = None,
        days: int = 30,
    ) -> List[AuditLog]:
        """
        Get login history.

        Args:
            session: Database session
            user_id: Optional user filter
            days: Days to look back

        Returns:
            List of login audit logs
        """
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        
        query = (
            select(AuditLog)
            .where(
                and_(
                    AuditLog.action.in_(["login_success", "login_failure"]),
                    AuditLog.created_at >= cutoff,
                )
            )
        )
        
        if user_id:
            query = query.where(AuditLog.user_id == user_id)
        
        query = query.order_by(AuditLog.created_at.desc())
        result = await session.execute(query)
        return list(result.scalars().all())

    # =========================================================================
    # Audit Log Queries by Time
    # =========================================================================

    async def get_in_date_range(
        self,
        session: AsyncSession,
        start_date: datetime,
        end_date: datetime,
        action: Optional[str] = None,
        entity_type: Optional[str] = None,
    ) -> List[AuditLog]:
        """
        Get audit logs within a date range.

        Args:
            session: Database session
            start_date: Range start
            end_date: Range end
            action: Optional action filter
            entity_type: Optional entity type filter

        Returns:
            List of audit logs
        """
        query = (
            select(AuditLog)
            .where(
                and_(
                    AuditLog.created_at >= start_date,
                    AuditLog.created_at <= end_date,
                )
            )
        )
        
        if action:
            query = query.where(AuditLog.action == action)
        if entity_type:
            query = query.where(AuditLog.entity_type == entity_type)
        
        query = query.order_by(AuditLog.created_at.desc())
        result = await session.execute(query)
        return list(result.scalars().all())

    async def get_recent(
        self,
        session: AsyncSession,
        hours: int = 24,
        limit: int = 100,
    ) -> List[AuditLog]:
        """
        Get recent audit logs.

        Args:
            session: Database session
            hours: Hours to look back
            limit: Maximum records

        Returns:
            List of recent audit logs
        """
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        
        query = (
            select(AuditLog)
            .where(AuditLog.created_at >= cutoff)
            .order_by(AuditLog.created_at.desc())
            .limit(limit)
        )
        result = await session.execute(query)
        return list(result.scalars().all())

    # =========================================================================
    # Statistics
    # =========================================================================

    async def get_action_counts(
        self,
        session: AsyncSession,
        days: int = 30,
    ) -> Dict[str, int]:
        """
        Get counts of each action type.

        Args:
            session: Database session
            days: Days to analyze

        Returns:
            Dictionary of action: count
        """
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        
        query = (
            select(AuditLog.action, func.count(AuditLog.id))
            .where(AuditLog.created_at >= cutoff)
            .group_by(AuditLog.action)
        )
        result = await session.execute(query)
        return dict(result.all())

    async def get_user_activity_counts(
        self,
        session: AsyncSession,
        days: int = 30,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Get most active users.

        Args:
            session: Database session
            days: Days to analyze
            limit: Number of users to return

        Returns:
            List of {user_id, action_count} dicts
        """
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        
        query = (
            select(AuditLog.user_id, func.count(AuditLog.id).label("count"))
            .where(
                and_(
                    AuditLog.created_at >= cutoff,
                    AuditLog.user_id.isnot(None),
                )
            )
            .group_by(AuditLog.user_id)
            .order_by(func.count(AuditLog.id).desc())
            .limit(limit)
        )
        result = await session.execute(query)
        return [{"user_id": row[0], "action_count": row[1]} for row in result.all()]


def create_audit_log_repository(db_manager, logging_manager) -> AuditLogRepository:
    """
    Factory function for AuditLogRepository.

    Args:
        db_manager: DatabaseManager instance
        logging_manager: LoggingManager instance

    Returns:
        Configured AuditLogRepository instance
    """
    return AuditLogRepository(db_manager, logging_manager)


__all__ = ["AuditLogRepository", "create_audit_log_repository"]
