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
FILE VERSION: v5.0-6-6.7-2
LAST MODIFIED: 2026-01-08
PHASE: Phase 6 - Notes System
CLEAN ARCHITECTURE: Compliant (Rule #1 Factory, Rule #2 DI)
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
"""

from datetime import datetime, timezone, timedelta
from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

from sqlalchemy import select, func, and_, or_, case, cast, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from src.models.session import Session, SEVERITY_LEVELS, SESSION_STATUSES
from src.repositories.base import BaseRepository

__version__ = "v5.0-6-6.7-2"


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
            .options(
                selectinload(Session.crt_user),
                selectinload(Session.notes),
            )
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
        # Import Note here to access Note.author for nested loading
        from src.models.note import Note
        
        query = (
            select(Session)
            .options(
                selectinload(Session.crt_user),
                selectinload(Session.notes).selectinload(Note.author),
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
    # Search and Advanced Filtering
    # =========================================================================

    async def search_sessions(
        self,
        session: AsyncSession,
        search: Optional[str] = None,
        severity: Optional[str] = None,
        status: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> Tuple[List[Session], int]:
        """
        Search sessions with filters and pagination.

        Searches across session_id, discord_user_id, and discord_username.
        Returns both results and total count for pagination.

        Args:
            session: Database session
            search: Search term (matches id, user_id, username)
            severity: Filter by severity level
            status: Filter by session status
            date_from: Filter sessions started after this date
            date_to: Filter sessions started before this date
            skip: Records to skip (pagination offset)
            limit: Maximum records to return

        Returns:
            Tuple of (list of sessions, total count)
        """
        # Build base query with eager loading for relationships
        query = (
            select(Session)
            .options(
                selectinload(Session.crt_user),
                selectinload(Session.notes),
            )
        )
        count_query = select(func.count(Session.id))

        # Build filter conditions
        conditions = []

        # Search filter - searches across multiple fields
        if search:
            search_term = f"%{search}%"
            search_conditions = [
                Session.id.ilike(search_term),
                Session.discord_username.ilike(search_term),
            ]
            # Also try to match discord_user_id if search is numeric
            if search.isdigit():
                search_conditions.append(
                    cast(Session.discord_user_id, String).like(f"%{search}%")
                )
            conditions.append(or_(*search_conditions))

        # Severity filter
        if severity:
            if severity not in SEVERITY_LEVELS:
                raise ValueError(f"Invalid severity: {severity}")
            conditions.append(Session.severity == severity)

        # Status filter
        if status:
            if status not in SESSION_STATUSES:
                raise ValueError(f"Invalid status: {status}")
            conditions.append(Session.status == status)

        # Date range filters
        if date_from:
            conditions.append(Session.started_at >= date_from)
        if date_to:
            conditions.append(Session.started_at <= date_to)

        # Apply conditions to both queries
        if conditions:
            query = query.where(and_(*conditions))
            count_query = count_query.where(and_(*conditions))

        # Get total count
        count_result = await session.execute(count_query)
        total = count_result.scalar() or 0

        # Apply ordering and pagination
        severity_order = case(
            (Session.severity == "critical", 0),
            (Session.severity == "high", 1),
            (Session.severity == "medium", 2),
            (Session.severity == "low", 3),
            else_=4
        )
        query = (
            query
            .order_by(severity_order, Session.started_at.desc())
            .offset(skip)
            .limit(limit)
        )

        # Execute query
        result = await session.execute(query)
        sessions = list(result.scalars().all())

        return sessions, total

    async def get_user_history_with_patterns(
        self,
        session: AsyncSession,
        discord_user_id: int,
        exclude_session_id: Optional[str] = None,
        limit: int = 10,
    ) -> Tuple[List[Session], Dict[str, Any]]:
        """
        Get user session history with pattern analysis.

        Returns sessions for a Discord user along with detected patterns
        like common time of day, frequency, and severity trends.

        Args:
            session: Database session
            discord_user_id: Discord user snowflake ID
            exclude_session_id: Session ID to exclude (current session)
            limit: Maximum sessions to return

        Returns:
            Tuple of (list of sessions, pattern analysis dict)
        """
        # Build query for user sessions
        query = (
            select(Session)
            .where(Session.discord_user_id == discord_user_id)
        )

        if exclude_session_id:
            query = query.where(Session.id != exclude_session_id)

        query = query.order_by(Session.started_at.desc()).limit(limit)

        result = await session.execute(query)
        sessions = list(result.scalars().all())

        # Get total count for this user
        count_query = (
            select(func.count(Session.id))
            .where(Session.discord_user_id == discord_user_id)
        )
        if exclude_session_id:
            count_query = count_query.where(Session.id != exclude_session_id)
        count_result = await session.execute(count_query)
        total_sessions = count_result.scalar() or 0

        # Calculate pattern analysis
        patterns = await self._analyze_user_patterns(session, discord_user_id, sessions)
        patterns["total_sessions"] = total_sessions

        return sessions, patterns

    async def _analyze_user_patterns(
        self,
        session: AsyncSession,
        discord_user_id: int,
        recent_sessions: List[Session],
    ) -> Dict[str, Any]:
        """
        Analyze patterns in user's session history.

        Args:
            session: Database session
            discord_user_id: Discord user ID
            recent_sessions: Recent sessions to analyze

        Returns:
            Pattern analysis dictionary
        """
        patterns: Dict[str, Any] = {
            "common_time_of_day": None,
            "average_frequency_days": None,
            "severity_trend": None,
            "last_session_days_ago": None,
        }

        if not recent_sessions:
            return patterns

        # Calculate days since last session
        now = datetime.now(timezone.utc)
        if recent_sessions[0].started_at:
            delta = now - recent_sessions[0].started_at
            patterns["last_session_days_ago"] = delta.days

        # Analyze time of day patterns
        time_buckets = {"Morning (6AM-12PM)": 0, "Afternoon (12PM-6PM)": 0,
                        "Evening (6PM-12AM)": 0, "Night (12AM-6AM)": 0}
        for s in recent_sessions:
            if s.started_at:
                hour = s.started_at.hour
                if 6 <= hour < 12:
                    time_buckets["Morning (6AM-12PM)"] += 1
                elif 12 <= hour < 18:
                    time_buckets["Afternoon (12PM-6PM)"] += 1
                elif 18 <= hour < 24:
                    time_buckets["Evening (6PM-12AM)"] += 1
                else:
                    time_buckets["Night (12AM-6AM)"] += 1

        if any(time_buckets.values()):
            patterns["common_time_of_day"] = max(time_buckets, key=time_buckets.get)

        # Calculate average frequency (days between sessions)
        if len(recent_sessions) >= 2:
            dates = [s.started_at for s in recent_sessions if s.started_at]
            if len(dates) >= 2:
                total_days = (dates[0] - dates[-1]).days
                patterns["average_frequency_days"] = round(
                    total_days / (len(dates) - 1), 1
                ) if total_days > 0 else None

        # Analyze severity trend
        if len(recent_sessions) >= 3:
            severity_scores = {
                "critical": 4, "high": 3, "medium": 2, "low": 1, "safe": 0
            }
            recent_scores = [
                severity_scores.get(s.severity, 0)
                for s in recent_sessions[:3]
            ]
            older_scores = [
                severity_scores.get(s.severity, 0)
                for s in recent_sessions[-3:]
            ]
            recent_avg = sum(recent_scores) / len(recent_scores)
            older_avg = sum(older_scores) / len(older_scores)

            if recent_avg > older_avg + 0.5:
                patterns["severity_trend"] = "escalating"
            elif recent_avg < older_avg - 0.5:
                patterns["severity_trend"] = "improving"
            else:
                patterns["severity_trend"] = "stable"

        return patterns

    async def reopen_session(
        self,
        session: AsyncSession,
        session_id: str,
    ) -> Optional[Session]:
        """
        Reopen a closed session (admin action).

        Args:
            session: Database session
            session_id: Session ID

        Returns:
            Updated session or None
        """
        db_session = await self.get(session, session_id)
        if not db_session:
            return None

        if db_session.status not in ("closed", "archived"):
            raise ValueError(f"Cannot reopen session with status: {db_session.status}")

        updates = {
            "status": "active",
            "ended_at": None,
            "duration_seconds": None,
        }

        return await self.update(session, session_id, updates)

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
