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
Session Repository - Data access layer for Crisis Session entities
----------------------------------------------------------------------------
FILE VERSION: v5.0-2-2.5-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 2 - Data Layer
CLEAN ARCHITECTURE: Compliant (Rule #1 Factory, Rule #2 DI)
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
"""

from datetime import datetime, timezone, timedelta
from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

from sqlalchemy import select, func, and_, or_, case
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.session import Session, SEVERITY_LEVELS, SESSION_STATUSES
from src.repositories.base import BaseRepository

__version__ = "v5.0-2-2.5-1"


class SessionRepository(BaseRepository[Session, str]):
    """
    Repository for Crisis Session entity operations.

    Provides CRUD operations plus crisis-specific queries like
    filtering by severity, status, Discord user, and date ranges.
    """

    def __init__(self, db_manager, logging_manager):
        """
        Initialize SessionRepository.

        Args:
            db_manager: DatabaseManager instance
            logging_manager: LoggingManager instance
        """
        super().__init__(Session, db_manager, logging_manager)

    # =========================================================================
    # Session Queries by Status
    # =========================================================================

    async def get_active_sessions(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Session]:
        """
        Get all active (open) crisis sessions.

        Args:
            session: Database session
            skip: Records to skip
            limit: Maximum records

        Returns:
            List of active sessions ordered by severity then start time
        """
        # Custom ordering: critical first, then by started_at descending
        severity_order = case(
            (Session.severity == "critical", 0),
            (Session.severity == "high", 1),
            (Session.severity == "medium", 2),
            (Session.severity == "low", 3),
            else_=4
        )
        
        query = (
            select(Session)
            .where(Session.status == "active")
            .order_by(severity_order, Session.started_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(query)
        return list(result.scalars().all())

    async def get_closed_sessions(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Session]:
        """
        Get closed sessions.

        Args:
            session: Database session
            skip: Records to skip
            limit: Maximum records

        Returns:
            List of closed sessions
        """
        return await self.get_filtered(
            session,
            filters={"status": "closed"},
            skip=skip,
            limit=limit,
            order_by="ended_at",
            descending=True,
        )

    async def get_archived_sessions(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Session]:
        """
        Get archived sessions.

        Args:
            session: Database session
            skip: Records to skip
            limit: Maximum records

        Returns:
            List of archived sessions
        """
        return await self.get_filtered(
            session,
            filters={"status": "archived"},
            skip=skip,
            limit=limit,
            order_by="started_at",
            descending=True,
        )

    # =========================================================================
    # Session Queries by Severity
    # =========================================================================

    async def get_by_severity(
        self,
        session: AsyncSession,
        severity: str,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Session]:
        """
        Get sessions by severity level.

        Args:
            session: Database session
            severity: Severity level (critical, high, medium, low, safe)
            status: Optional status filter
            skip: Records to skip
            limit: Maximum records

        Returns:
            List of matching sessions
        """
        if severity not in SEVERITY_LEVELS:
            raise ValueError(f"Invalid severity: {severity}")
        
        filters = {"severity": severity}
        if status:
            if status not in SESSION_STATUSES:
                raise ValueError(f"Invalid status: {status}")
            filters["status"] = status
        
        return await self.get_filtered(
            session,
            filters=filters,
            skip=skip,
            limit=limit,
            order_by="started_at",
            descending=True,
        )

    async def get_critical_sessions(
        self,
        session: AsyncSession,
        active_only: bool = True,
    ) -> List[Session]:
        """
        Get critical severity sessions.

        Args:
            session: Database session
            active_only: If True, only return active sessions

        Returns:
            List of critical sessions
        """
        filters = {"severity": "critical"}
        if active_only:
            filters["status"] = "active"
        
        return await self.get_filtered(
            session,
            filters=filters,
            order_by="started_at",
            descending=True,
            limit=1000,
        )

    async def get_high_priority_sessions(
        self,
        session: AsyncSession,
        active_only: bool = True,
    ) -> List[Session]:
        """
        Get critical and high severity sessions.

        Args:
            session: Database session
            active_only: If True, only return active sessions

        Returns:
            List of high priority sessions
        """
        query = select(Session).where(
            Session.severity.in_(["critical", "high"])
        )
        
        if active_only:
            query = query.where(Session.status == "active")
        
        # Order by severity (critical first) then by time
        severity_order = case(
            (Session.severity == "critical", 0),
            else_=1
        )
        query = query.order_by(severity_order, Session.started_at.desc())
        
        result = await session.execute(query)
        return list(result.scalars().all())

    # =========================================================================
    # Session Queries by Discord User
    # =========================================================================

    async def get_by_discord_user(
        self,
        session: AsyncSession,
        discord_user_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Session]:
        """
        Get all sessions for a Discord user.

        Args:
            session: Database session
            discord_user_id: Discord user snowflake ID
            skip: Records to skip
            limit: Maximum records

        Returns:
            List of sessions for the user
        """
        return await self.get_filtered(
            session,
            filters={"discord_user_id": discord_user_id},
            skip=skip,
            limit=limit,
            order_by="started_at",
            descending=True,
        )

    async def get_user_session_history(
        self,
        session: AsyncSession,
        discord_user_id: int,
        days: int = 30,
    ) -> List[Session]:
        """
        Get session history for a Discord user within a time period.

        Args:
            session: Database session
            discord_user_id: Discord user snowflake ID
            days: Number of days to look back

        Returns:
            List of sessions within the time period
        """
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        
        query = (
            select(Session)
            .where(
                and_(
                    Session.discord_user_id == discord_user_id,
                    Session.started_at >= cutoff,
                )
            )
            .order_by(Session.started_at.desc())
        )
        result = await session.execute(query)
        return list(result.scalars().all())

    async def count_user_sessions(
        self,
        session: AsyncSession,
        discord_user_id: int,
        severity: Optional[str] = None,
    ) -> int:
        """
        Count sessions for a Discord user.

        Args:
            session: Database session
            discord_user_id: Discord user snowflake ID
            severity: Optional severity filter

        Returns:
            Number of sessions
        """
        filters = {"discord_user_id": discord_user_id}
        if severity:
            filters["severity"] = severity
        
        return await self.count(session, filters)

    # =========================================================================
    # Session Queries by CRT Assignment
    # =========================================================================

    async def get_by_crt_user(
        self,
        session: AsyncSession,
        crt_user_id: UUID,
        status: Optional[str] = None,
    ) -> List[Session]:
        """
        Get sessions assigned to a CRT user.

        Args:
            session: Database session
            crt_user_id: CRT user UUID
            status: Optional status filter

        Returns:
            List of assigned sessions
        """
        filters = {"crt_user_id": crt_user_id}
        if status:
            filters["status"] = status
        
        return await self.get_filtered(
            session,
            filters=filters,
            order_by="started_at",
            descending=True,
            limit=1000,
        )

    async def get_unassigned_sessions(
        self,
        session: AsyncSession,
        active_only: bool = True,
    ) -> List[Session]:
        """
        Get sessions not assigned to any CRT user.

        Args:
            session: Database session
            active_only: If True, only return active sessions

        Returns:
            List of unassigned sessions
        """
        query = select(Session).where(Session.crt_user_id.is_(None))
        
        if active_only:
            query = query.where(Session.status == "active")
        
        # Priority ordering
        severity_order = case(
            (Session.severity == "critical", 0),
            (Session.severity == "high", 1),
            (Session.severity == "medium", 2),
            (Session.severity == "low", 3),
            else_=4
        )
        query = query.order_by(severity_order, Session.started_at.desc())
        
        result = await session.execute(query)
        return list(result.scalars().all())

    # =========================================================================
    # Session Queries by Date Range
    # =========================================================================

    async def get_sessions_in_range(
        self,
        session: AsyncSession,
        start_date: datetime,
        end_date: datetime,
        severity: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[Session]:
        """
        Get sessions within a date range.

        Args:
            session: Database session
            start_date: Range start (inclusive)
            end_date: Range end (inclusive)
            severity: Optional severity filter
            status: Optional status filter

        Returns:
            List of sessions in the range
        """
        query = select(Session).where(
            and_(
                Session.started_at >= start_date,
                Session.started_at <= end_date,
            )
        )
        
        if severity:
            query = query.where(Session.severity == severity)
        if status:
            query = query.where(Session.status == status)
        
        query = query.order_by(Session.started_at.desc())
        result = await session.execute(query)
        return list(result.scalars().all())

    async def get_recent_sessions(
        self,
        session: AsyncSession,
        hours: int = 24,
        limit: int = 100,
    ) -> List[Session]:
        """
        Get sessions from the last N hours.

        Args:
            session: Database session
            hours: Number of hours to look back
            limit: Maximum records

        Returns:
            List of recent sessions
        """
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        
        query = (
            select(Session)
            .where(Session.started_at >= cutoff)
            .order_by(Session.started_at.desc())
            .limit(limit)
        )
        result = await session.execute(query)
        return list(result.scalars().all())

    # =========================================================================
    # Session with Relationships
    # =========================================================================

    async def get_with_notes(
        self,
        session: AsyncSession,
        session_id: str,
    ) -> Optional[Session]:
        """
        Get a session with its notes eagerly loaded.

        Args:
            session: Database session
            session_id: Session ID

        Returns:
            Session with notes or None
        """
        query = (
            select(Session)
            .options(selectinload(Session.notes))
            .where(Session.id == session_id)
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def get_with_all_relations(
        self,
        session: AsyncSession,
        session_id: str,
    ) -> Optional[Session]:
        """
        Get a session with all relationships loaded.

        Args:
            session: Database session
            session_id: Session ID

        Returns:
            Session with all relations or None
        """
        query = (
            select(Session)
            .options(
                selectinload(Session.crt_user),
                selectinload(Session.notes),
                selectinload(Session.archive),
            )
            .where(Session.id == session_id)
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()

    # =========================================================================
    # Session Actions
    # =========================================================================

    async def assign_to_crt(
        self,
        session: AsyncSession,
        session_id: str,
        crt_user_id: UUID,
    ) -> Optional[Session]:
        """
        Assign a session to a CRT user.

        Args:
            session: Database session
            session_id: Session ID
            crt_user_id: CRT user UUID

        Returns:
            Updated session or None
        """
        return await self.update(session, session_id, {"crt_user_id": crt_user_id})

    async def unassign(
        self,
        session: AsyncSession,
        session_id: str,
    ) -> Optional[Session]:
        """
        Remove CRT assignment from a session.

        Args:
            session: Database session
            session_id: Session ID

        Returns:
            Updated session or None
        """
        return await self.update(session, session_id, {"crt_user_id": None})

    async def close_session(
        self,
        session: AsyncSession,
        session_id: str,
        summary: Optional[str] = None,
    ) -> Optional[Session]:
        """
        Close a session.

        Args:
            session: Database session
            session_id: Session ID
            summary: Optional closing summary

        Returns:
            Updated session or None
        """
        db_session = await self.get(session, session_id)
        if not db_session:
            return None
        
        now = datetime.now(timezone.utc)
        updates = {
            "status": "closed",
            "ended_at": now,
        }
        
        if db_session.started_at:
            duration = now - db_session.started_at
            updates["duration_seconds"] = int(duration.total_seconds())
        
        if summary:
            updates["ash_summary"] = summary
        
        return await self.update(session, session_id, updates)

    async def mark_archived(
        self,
        session: AsyncSession,
        session_id: str,
    ) -> Optional[Session]:
        """
        Mark a session as archived.

        Args:
            session: Database session
            session_id: Session ID

        Returns:
            Updated session or None
        """
        return await self.update(session, session_id, {"status": "archived"})

    # =========================================================================
    # Statistics
    # =========================================================================

    async def get_statistics(
        self,
        session: AsyncSession,
        days: int = 30,
    ) -> Dict[str, Any]:
        """
        Get session statistics for a time period.

        Args:
            session: Database session
            days: Number of days to analyze

        Returns:
            Dictionary of statistics
        """
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        
        # Count by severity
        severity_query = (
            select(Session.severity, func.count(Session.id))
            .where(Session.started_at >= cutoff)
            .group_by(Session.severity)
        )
        severity_result = await session.execute(severity_query)
        severity_counts = dict(severity_result.all())
        
        # Count by status
        status_query = (
            select(Session.status, func.count(Session.id))
            .where(Session.started_at >= cutoff)
            .group_by(Session.status)
        )
        status_result = await session.execute(status_query)
        status_counts = dict(status_result.all())
        
        # Total count
        total = sum(severity_counts.values())
        
        # Average crisis score
        avg_score_query = (
            select(func.avg(Session.crisis_score))
            .where(Session.started_at >= cutoff)
        )
        avg_result = await session.execute(avg_score_query)
        avg_score = avg_result.scalar()
        
        return {
            "period_days": days,
            "total_sessions": total,
            "by_severity": severity_counts,
            "by_status": status_counts,
            "average_crisis_score": float(avg_score) if avg_score else None,
        }


def create_session_repository(db_manager, logging_manager) -> SessionRepository:
    """
    Factory function for SessionRepository.

    Args:
        db_manager: DatabaseManager instance
        logging_manager: LoggingManager instance

    Returns:
        Configured SessionRepository instance
    """
    return SessionRepository(db_manager, logging_manager)


__all__ = ["SessionRepository", "create_session_repository"]
