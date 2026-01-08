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
Dashboard API Routes - Aggregated metrics and real-time data for dashboard
----------------------------------------------------------------------------
FILE VERSION: v5.0-4-4.1-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 4 - Dashboard & Metrics
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

ENDPOINTS:
    GET /api/v1/dashboard/metrics         - Aggregated metrics for cards
    GET /api/v1/dashboard/crisis-trends   - 30-day crisis trend data
    GET /api/v1/dashboard/crt-activity    - CRT member activity statistics
    GET /api/v1/dashboard/active-sessions - Real-time active session list
"""

from datetime import datetime, timezone, timedelta
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request
from pydantic import BaseModel, Field
from sqlalchemy import select, func, and_, case
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.session import Session
from src.models.user import User
from src.repositories import (
    create_session_repository,
    create_user_repository,
)

__version__ = "v5.0-4-4.1-1"

# Create router with v1 prefix for dashboard endpoints
router = APIRouter(prefix="/api/v1/dashboard", tags=["Dashboard"])


# =============================================================================
# Pydantic Response Models
# =============================================================================

class DashboardMetrics(BaseModel):
    """Aggregated metrics for dashboard cards."""
    active_sessions: int = Field(..., description="Current active session count")
    active_critical_high: int = Field(..., description="Count of critical + high severity active sessions")
    week_total: int = Field(..., description="Total sessions this week")
    week_change: int = Field(..., description="Change from last week (+/-)")
    avg_response_minutes: Optional[float] = Field(None, description="Average CRT response time in minutes")
    crt_active: int = Field(..., description="Currently active CRT members (with assigned sessions)")
    crt_total: int = Field(..., description="Total CRT members")
    last_updated: datetime = Field(..., description="Timestamp of data retrieval")


class CrisisTrendPoint(BaseModel):
    """Daily crisis session counts for trend chart."""
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    critical: int = Field(default=0, description="Critical severity count")
    high: int = Field(default=0, description="High severity count")
    medium: int = Field(default=0, description="Medium severity count")
    low: int = Field(default=0, description="Low severity count")
    total: int = Field(default=0, description="Total sessions for the day")


class CRTActivityItem(BaseModel):
    """CRT member activity statistics."""
    user_id: str = Field(..., description="User UUID")
    display_name: str = Field(..., description="Display name")
    session_count: int = Field(..., description="Sessions handled in period")
    avg_response_minutes: Optional[float] = Field(None, description="Average response time in minutes")


class ActiveSessionItem(BaseModel):
    """Active session for real-time dashboard display."""
    session_id: str = Field(..., description="Session ID (Ash-Bot format)")
    discord_user_id: Optional[int] = Field(None, description="Discord user snowflake")
    discord_username: Optional[str] = Field(None, description="Discord username")
    severity: str = Field(..., description="Severity level")
    started_at: Optional[datetime] = Field(None, description="Session start time")
    elapsed_seconds: int = Field(..., description="Seconds since session started")
    crt_member_id: Optional[str] = Field(None, description="Assigned CRT user UUID")
    crt_member_name: Optional[str] = Field(None, description="Assigned CRT display name")


# =============================================================================
# Dependency Injection Helpers
# =============================================================================

def get_session_repo(request: Request):
    """Get SessionRepository from app state."""
    return create_session_repository(
        request.app.state.database_manager,
        request.app.state.logging_manager,
    )


def get_user_repo(request: Request):
    """Get UserRepository from app state."""
    return create_user_repository(
        request.app.state.database_manager,
        request.app.state.logging_manager,
    )


# =============================================================================
# Dashboard Endpoints
# =============================================================================

@router.get("/metrics", response_model=DashboardMetrics)
async def get_dashboard_metrics(request: Request):
    """
    Get aggregated metrics for dashboard cards.
    
    Returns metrics for:
    - Active session count and critical/high breakdown
    - Weekly totals with week-over-week change
    - Average CRT response time
    - CRT member counts (active vs total)
    
    Polling interval: 30 seconds recommended
    """
    db_manager = request.app.state.database_manager
    now = datetime.now(timezone.utc)
    
    async with db_manager.session() as db:
        # ---------------------------------------------------------------------
        # Active Sessions Count
        # ---------------------------------------------------------------------
        active_query = select(func.count(Session.id)).where(
            Session.status == "active"
        )
        active_result = await db.execute(active_query)
        active_sessions = active_result.scalar() or 0
        
        # Critical + High active sessions
        critical_high_query = select(func.count(Session.id)).where(
            and_(
                Session.status == "active",
                Session.severity.in_(["critical", "high"]),
            )
        )
        critical_high_result = await db.execute(critical_high_query)
        active_critical_high = critical_high_result.scalar() or 0
        
        # ---------------------------------------------------------------------
        # Weekly Totals
        # ---------------------------------------------------------------------
        # This week (last 7 days)
        week_start = now - timedelta(days=7)
        this_week_query = select(func.count(Session.id)).where(
            Session.started_at >= week_start
        )
        this_week_result = await db.execute(this_week_query)
        week_total = this_week_result.scalar() or 0
        
        # Last week (7-14 days ago)
        last_week_start = now - timedelta(days=14)
        last_week_query = select(func.count(Session.id)).where(
            and_(
                Session.started_at >= last_week_start,
                Session.started_at < week_start,
            )
        )
        last_week_result = await db.execute(last_week_query)
        last_week_total = last_week_result.scalar() or 0
        
        week_change = week_total - last_week_total
        
        # ---------------------------------------------------------------------
        # Average Response Time
        # ---------------------------------------------------------------------
        # Response time = time from session start to CRT assignment
        # For now, we'll use duration_seconds for closed sessions as a proxy
        # TODO: Add crt_assigned_at field to Session model for accurate tracking
        avg_response_query = select(func.avg(Session.duration_seconds)).where(
            and_(
                Session.status == "closed",
                Session.duration_seconds.isnot(None),
                Session.started_at >= week_start,
            )
        )
        avg_response_result = await db.execute(avg_response_query)
        avg_duration = avg_response_result.scalar()
        
        # Convert seconds to minutes
        avg_response_minutes = None
        if avg_duration is not None:
            avg_response_minutes = round(float(avg_duration) / 60.0, 1)
        
        # ---------------------------------------------------------------------
        # CRT Member Counts
        # ---------------------------------------------------------------------
        # Total CRT members
        crt_total_query = select(func.count(User.id)).where(
            and_(
                User.role == "crt_member",
                User.is_active == True,
            )
        )
        crt_total_result = await db.execute(crt_total_query)
        crt_total = crt_total_result.scalar() or 0
        
        # CRT members with active assigned sessions
        crt_active_query = select(func.count(func.distinct(Session.crt_user_id))).where(
            and_(
                Session.status == "active",
                Session.crt_user_id.isnot(None),
            )
        )
        crt_active_result = await db.execute(crt_active_query)
        crt_active = crt_active_result.scalar() or 0
    
    return DashboardMetrics(
        active_sessions=active_sessions,
        active_critical_high=active_critical_high,
        week_total=week_total,
        week_change=week_change,
        avg_response_minutes=avg_response_minutes,
        crt_active=crt_active,
        crt_total=crt_total,
        last_updated=now,
    )


@router.get("/crisis-trends", response_model=List[CrisisTrendPoint])
async def get_crisis_trends(
    request: Request,
    days: int = Query(30, ge=1, le=90, description="Days of trend data to return"),
):
    """
    Get daily crisis session counts for trend chart.
    
    Returns daily counts broken down by severity level for the specified
    number of days. Data is returned in chronological order (oldest first)
    for easy chart rendering.
    
    Polling interval: 30 seconds recommended
    """
    db_manager = request.app.state.database_manager
    now = datetime.now(timezone.utc)
    start_date = now - timedelta(days=days)
    
    async with db_manager.session() as db:
        # Query daily counts grouped by date and severity
        # Using date truncation to group by day
        daily_query = (
            select(
                func.date(Session.started_at).label("day"),
                Session.severity,
                func.count(Session.id).label("count"),
            )
            .where(Session.started_at >= start_date)
            .group_by(func.date(Session.started_at), Session.severity)
            .order_by(func.date(Session.started_at))
        )
        
        result = await db.execute(daily_query)
        rows = result.all()
    
    # Build a dictionary of date -> severity counts
    trends_dict = {}
    
    # Initialize all days with zero counts
    for i in range(days):
        day = (start_date + timedelta(days=i)).date()
        day_str = day.isoformat()
        trends_dict[day_str] = {
            "date": day_str,
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "total": 0,
        }
    
    # Populate with actual data
    for row in rows:
        day_str = row.day.isoformat() if hasattr(row.day, 'isoformat') else str(row.day)
        severity = row.severity
        count = row.count
        
        if day_str in trends_dict and severity in ["critical", "high", "medium", "low"]:
            trends_dict[day_str][severity] = count
            trends_dict[day_str]["total"] += count
    
    # Convert to list and sort by date
    trends = [CrisisTrendPoint(**data) for data in trends_dict.values()]
    trends.sort(key=lambda x: x.date)
    
    return trends


@router.get("/crt-activity", response_model=List[CRTActivityItem])
async def get_crt_activity(
    request: Request,
    days: int = Query(7, ge=1, le=30, description="Days of activity to include"),
):
    """
    Get CRT member activity statistics.
    
    Returns session counts and average response times per CRT member
    for the specified period, sorted by session count descending.
    
    Polling interval: 30 seconds recommended
    """
    db_manager = request.app.state.database_manager
    now = datetime.now(timezone.utc)
    start_date = now - timedelta(days=days)
    
    async with db_manager.session() as db:
        # Query sessions grouped by CRT user with stats
        activity_query = (
            select(
                Session.crt_user_id,
                func.count(Session.id).label("session_count"),
                func.avg(Session.duration_seconds).label("avg_duration"),
            )
            .where(
                and_(
                    Session.crt_user_id.isnot(None),
                    Session.started_at >= start_date,
                )
            )
            .group_by(Session.crt_user_id)
            .order_by(func.count(Session.id).desc())
        )
        
        activity_result = await db.execute(activity_query)
        activity_rows = activity_result.all()
        
        # Get user display names for all CRT users in the results
        crt_user_ids = [row.crt_user_id for row in activity_rows if row.crt_user_id]
        
        users_dict = {}
        if crt_user_ids:
            users_query = select(User.id, User.display_name).where(User.id.in_(crt_user_ids))
            users_result = await db.execute(users_query)
            users_dict = {row.id: row.display_name for row in users_result.all()}
    
    # Build response
    activity_items = []
    for row in activity_rows:
        if row.crt_user_id is None:
            continue
            
        user_id = str(row.crt_user_id)
        display_name = users_dict.get(row.crt_user_id, "Unknown User")
        
        # Convert average duration to minutes
        avg_minutes = None
        if row.avg_duration is not None:
            avg_minutes = round(float(row.avg_duration) / 60.0, 1)
        
        activity_items.append(CRTActivityItem(
            user_id=user_id,
            display_name=display_name,
            session_count=row.session_count,
            avg_response_minutes=avg_minutes,
        ))
    
    return activity_items


@router.get("/active-sessions", response_model=List[ActiveSessionItem])
async def get_active_sessions(request: Request):
    """
    Get currently active sessions for real-time dashboard display.
    
    Returns active sessions with severity indicators, elapsed time,
    and assigned CRT member information. Sessions are ordered by
    severity (critical first) then by start time (oldest first).
    
    Polling interval: 10 seconds recommended
    """
    db_manager = request.app.state.database_manager
    now = datetime.now(timezone.utc)
    
    async with db_manager.session() as db:
        # Custom ordering: critical first, then high, medium, low
        # Within same severity, show oldest sessions first (need attention soonest)
        severity_order = case(
            (Session.severity == "critical", 0),
            (Session.severity == "high", 1),
            (Session.severity == "medium", 2),
            (Session.severity == "low", 3),
            else_=4
        )
        
        sessions_query = (
            select(Session)
            .where(Session.status == "active")
            .order_by(severity_order, Session.started_at.asc())
            .limit(100)
        )
        
        sessions_result = await db.execute(sessions_query)
        sessions = sessions_result.scalars().all()
        
        # Gather CRT user IDs for bulk lookup
        crt_user_ids = [s.crt_user_id for s in sessions if s.crt_user_id]
        
        crt_users_dict = {}
        if crt_user_ids:
            users_query = select(User.id, User.display_name).where(User.id.in_(crt_user_ids))
            users_result = await db.execute(users_query)
            crt_users_dict = {row.id: row.display_name for row in users_result.all()}
    
    # Build response
    active_items = []
    for session in sessions:
        # Calculate elapsed time
        elapsed_seconds = 0
        if session.started_at:
            # Handle timezone-aware comparison
            started = session.started_at
            if started.tzinfo is None:
                started = started.replace(tzinfo=timezone.utc)
            elapsed_seconds = int((now - started).total_seconds())
        
        # Get CRT member info
        crt_member_id = None
        crt_member_name = None
        if session.crt_user_id:
            crt_member_id = str(session.crt_user_id)
            crt_member_name = crt_users_dict.get(session.crt_user_id, "Unknown")
        
        active_items.append(ActiveSessionItem(
            session_id=session.id,
            discord_user_id=session.discord_user_id,
            discord_username=session.discord_username,
            severity=session.severity,
            started_at=session.started_at,
            elapsed_seconds=elapsed_seconds,
            crt_member_id=crt_member_id,
            crt_member_name=crt_member_name,
        ))
    
    return active_items
