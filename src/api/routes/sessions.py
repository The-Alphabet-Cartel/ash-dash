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
Sessions API Routes - Crisis session endpoints with search, filtering, and
state management for the dashboard with authorization.
----------------------------------------------------------------------------
FILE VERSION: v5.0-10-10.2.6-1
LAST MODIFIED: 2026-01-10
PHASE: Phase 10 - Authentication & Authorization
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

ENDPOINTS:
    GET  /api/sessions              - List sessions with search/filters
    GET  /api/sessions/active       - Get active sessions (dashboard view)
    GET  /api/sessions/stats        - Session statistics
    GET  /api/sessions/{id}         - Get session detail with analysis
    GET  /api/sessions/{id}/notes   - Get session notes
    GET  /api/sessions/user/{id}    - Get user session history with patterns
    POST /api/sessions/{id}/assign  - Assign CRT user to session
    POST /api/sessions/{id}/close   - Close a session
    POST /api/sessions/{id}/reopen  - Reopen a closed session (Lead+ only)

AUTHORIZATION (Phase 10):
    - All endpoints require CRT membership (require_member)
    - Session reopen: Requires Lead or Admin role
    - All audit logs include user_id for tracking
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel, Field

from src.repositories import (
    create_session_repository,
    create_note_repository,
    create_audit_log_repository,
)

# Phase 10: Import auth dependencies
from src.api.dependencies.auth import (
    require_member,
    require_lead,
)
from src.api.middleware.auth_middleware import UserContext

__version__ = "v5.0-10-10.2.6-1"

# Create router
router = APIRouter(prefix="/api/sessions", tags=["Sessions"])


# =============================================================================
# Response Models - Phase 5 Enhanced
# =============================================================================

class SessionSummary(BaseModel):
    """Summary view of a session for list display."""
    id: str
    discord_user_id: int
    discord_username: Optional[str] = None
    severity: str
    status: str
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    duration_display: Optional[str] = None
    crt_user_id: Optional[UUID] = None
    crt_member_name: Optional[str] = None
    note_count: int = 0
    crisis_score: Optional[float] = None

    class Config:
        from_attributes = True


class PaginatedSessionList(BaseModel):
    """Paginated list of session summaries."""
    items: List[SessionSummary]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_more: bool


class AshAnalysis(BaseModel):
    """Ash-NLP analysis data from a session."""
    crisis_score: Optional[float] = None
    confidence: Optional[float] = None
    severity: str
    signals: Dict[str, Any] = Field(default_factory=dict)
    explanation: Dict[str, Any] = Field(default_factory=dict)
    conflict_analysis: Optional[Dict[str, Any]] = None
    consensus: Optional[Dict[str, Any]] = None
    context_analysis: Optional[Dict[str, Any]] = None


class NoteSummary(BaseModel):
    """Summary view of a note."""
    id: UUID
    author_id: Optional[UUID] = None
    author_name: Optional[str] = None
    content_preview: str
    created_at: datetime
    is_locked: bool

    class Config:
        from_attributes = True


class SessionDetail(BaseModel):
    """Detailed session view with analysis and notes."""
    id: str
    discord_user_id: int
    discord_username: Optional[str] = None
    severity: str
    status: str
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    duration_display: Optional[str] = None
    message_count: int = 0
    crt_user_id: Optional[UUID] = None
    crt_member_name: Optional[str] = None
    ash_summary: Optional[str] = None
    analysis: AshAnalysis
    notes: List[NoteSummary] = []
    is_archived: bool = False
    archive_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PatternAnalysis(BaseModel):
    """Pattern analysis for a user's session history."""
    common_time_of_day: Optional[str] = None
    average_frequency_days: Optional[float] = None
    severity_trend: Optional[str] = None
    last_session_days_ago: Optional[int] = None


class UserSessionHistory(BaseModel):
    """User session history with pattern analysis."""
    discord_user_id: int
    discord_username: Optional[str] = None
    total_sessions: int
    sessions: List[SessionSummary]
    pattern_analysis: PatternAnalysis


class SessionStatsResponse(BaseModel):
    """Session statistics response."""
    period_days: int
    total_sessions: int
    by_severity: Dict[str, int]
    by_status: Dict[str, int]
    average_crisis_score: Optional[float] = None


class NoteResponse(BaseModel):
    """Full note response schema."""
    id: UUID
    session_id: str
    author_id: Optional[UUID] = None
    content: str
    content_html: Optional[str] = None
    version: int
    is_locked: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AssignRequest(BaseModel):
    """Request to assign CRT user to session."""
    crt_user_id: UUID = Field(..., description="CRT user UUID to assign")


class CloseRequest(BaseModel):
    """Request to close a session."""
    summary: Optional[str] = Field(None, description="Optional closing summary")


class MessageResponse(BaseModel):
    """Standard API message response."""
    message: str
    success: bool = True


# =============================================================================
# Helper Functions
# =============================================================================

def format_duration(seconds: Optional[int]) -> Optional[str]:
    """
    Format duration seconds into human-readable string.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted string like "23 min", "1h 15m", "2d 3h"
    """
    if seconds is None:
        return None
    
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes} min"
    elif seconds < 86400:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        if minutes > 0:
            return f"{hours}h {minutes}m"
        return f"{hours}h"
    else:
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        if hours > 0:
            return f"{days}d {hours}h"
        return f"{days}d"


def calculate_elapsed_seconds(started_at: Optional[datetime]) -> Optional[int]:
    """Calculate elapsed seconds from start time to now."""
    if started_at is None:
        return None
    now = datetime.now(timezone.utc)
    # Ensure started_at is timezone aware
    if started_at.tzinfo is None:
        started_at = started_at.replace(tzinfo=timezone.utc)
    return int((now - started_at).total_seconds())


def build_session_summary(session, crt_name: Optional[str] = None) -> SessionSummary:
    """Build a SessionSummary from a Session model."""
    # Calculate duration for active sessions
    duration = session.duration_seconds
    if duration is None and session.status == "active" and session.started_at:
        duration = calculate_elapsed_seconds(session.started_at)
    
    return SessionSummary(
        id=session.id,
        discord_user_id=session.discord_user_id,
        discord_username=session.discord_username,
        severity=session.severity,
        status=session.status,
        started_at=session.started_at,
        ended_at=session.ended_at,
        duration_seconds=duration,
        duration_display=format_duration(duration),
        crt_user_id=session.crt_user_id,
        crt_member_name=crt_name or (
            session.crt_user.display_name if session.crt_user else None
        ),
        note_count=len(session.notes) if hasattr(session, 'notes') and session.notes else 0,
        crisis_score=float(session.crisis_score) if session.crisis_score else None,
    )


def build_ash_analysis(session) -> AshAnalysis:
    """Extract Ash analysis data from a session."""
    analysis_data = session.analysis_data or {}
    
    return AshAnalysis(
        crisis_score=float(session.crisis_score) if session.crisis_score else None,
        confidence=float(session.confidence) if session.confidence else None,
        severity=session.severity,
        signals=analysis_data.get("signals", {}),
        explanation=analysis_data.get("explanation", {}),
        conflict_analysis=analysis_data.get("conflict_analysis"),
        consensus=analysis_data.get("consensus"),
        context_analysis=analysis_data.get("context_analysis"),
    )


def build_note_summary(note) -> NoteSummary:
    """Build a NoteSummary from a Note model."""
    content_preview = note.content[:200] if note.content else ""
    if len(note.content or "") > 200:
        content_preview += "..."
    
    return NoteSummary(
        id=note.id,
        author_id=note.author_id,
        author_name=note.author.display_name if note.author else None,
        content_preview=content_preview,
        created_at=note.created_at,
        is_locked=note.is_locked,
    )


def get_user_id_for_audit(user: UserContext) -> Optional[str]:
    """
    Get user ID string for audit logging.
    
    Prefers db_user_id if available, falls back to pocket_id.
    """
    if user.db_user_id:
        return str(user.db_user_id)
    if user.user_id and user.user_id != "anonymous":
        return user.user_id
    return None


# =============================================================================
# Dependency Injection Helpers
# =============================================================================

def get_session_repo(request: Request):
    """Get SessionRepository from app state."""
    return create_session_repository(
        request.app.state.database_manager,
        request.app.state.logging_manager,
    )


def get_note_repo(request: Request):
    """Get NoteRepository from app state."""
    return create_note_repository(
        request.app.state.database_manager,
        request.app.state.logging_manager,
    )


def get_audit_repo(request: Request):
    """Get AuditLogRepository from app state."""
    return create_audit_log_repository(
        request.app.state.database_manager,
        request.app.state.logging_manager,
    )


# =============================================================================
# Session List Endpoints
# =============================================================================

@router.get("", response_model=PaginatedSessionList)
async def list_sessions(
    request: Request,
    user: UserContext = Depends(require_member),
    search: Optional[str] = Query(None, description="Search by user ID, session ID, or username"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    status: Optional[str] = Query(None, description="Filter by status"),
    date_from: Optional[datetime] = Query(None, description="Filter sessions started after"),
    date_to: Optional[datetime] = Query(None, description="Filter sessions started before"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
):
    """
    List sessions with search, filtering, and pagination.
    
    Authorization:
        - Requires CRT membership (any role)
    
    Query Parameters:
        search: Search term (matches session ID, Discord user ID, username)
        severity: Filter by severity (critical, high, medium, low, safe)
        status: Filter by status (active, closed, archived)
        date_from: Filter sessions started after this datetime
        date_to: Filter sessions started before this datetime
        page: Page number (default: 1)
        page_size: Items per page (default: 20, max: 100)
    
    Returns:
        Paginated list with items, total count, and pagination metadata
    """
    session_repo = get_session_repo(request)
    db_manager = request.app.state.database_manager
    
    skip = (page - 1) * page_size
    
    async with db_manager.session() as db:
        sessions, total = await session_repo.search_sessions(
            db,
            search=search,
            severity=severity,
            status=status,
            date_from=date_from,
            date_to=date_to,
            skip=skip,
            limit=page_size,
        )
    
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    
    items = [build_session_summary(s) for s in sessions]
    
    return PaginatedSessionList(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_more=(page < total_pages),
    )


@router.get("/active", response_model=List[SessionSummary])
async def get_active_sessions(
    request: Request,
    user: UserContext = Depends(require_member),
):
    """
    Get all active sessions for the dashboard.
    
    Authorization:
        - Requires CRT membership (any role)
    
    Returns sessions ordered by severity (critical first) then by time.
    This is the primary endpoint for the real-time dashboard view.
    """
    session_repo = get_session_repo(request)
    db_manager = request.app.state.database_manager
    
    async with db_manager.session() as db:
        sessions = await session_repo.get_active_sessions(db, limit=100)
    
    return [build_session_summary(s) for s in sessions]


@router.get("/critical", response_model=List[SessionSummary])
async def get_critical_sessions(
    request: Request,
    user: UserContext = Depends(require_member),
):
    """
    Get critical severity sessions.
    
    Authorization:
        - Requires CRT membership (any role)
    
    Returns only critical sessions that need immediate attention.
    """
    session_repo = get_session_repo(request)
    db_manager = request.app.state.database_manager
    
    async with db_manager.session() as db:
        sessions = await session_repo.get_critical_sessions(db, active_only=True)
    
    return [build_session_summary(s) for s in sessions]


@router.get("/unassigned", response_model=List[SessionSummary])
async def get_unassigned_sessions(
    request: Request,
    user: UserContext = Depends(require_member),
):
    """
    Get active sessions not assigned to any CRT user.
    
    Authorization:
        - Requires CRT membership (any role)
    
    Useful for CRT members looking to pick up new sessions.
    """
    session_repo = get_session_repo(request)
    db_manager = request.app.state.database_manager
    
    async with db_manager.session() as db:
        sessions = await session_repo.get_unassigned_sessions(db, active_only=True)
    
    return [build_session_summary(s) for s in sessions]


@router.get("/stats", response_model=SessionStatsResponse)
async def get_session_stats(
    request: Request,
    user: UserContext = Depends(require_member),
    days: int = Query(30, ge=1, le=365, description="Days to analyze"),
):
    """
    Get session statistics for the specified time period.
    
    Authorization:
        - Requires CRT membership (any role)
    
    Query Parameters:
        days: Number of days to analyze (default: 30, max: 365)
    """
    session_repo = get_session_repo(request)
    db_manager = request.app.state.database_manager
    
    async with db_manager.session() as db:
        stats = await session_repo.get_statistics(db, days=days)
    
    return SessionStatsResponse(**stats)


# =============================================================================
# Session Detail Endpoints
# =============================================================================

@router.get("/{session_id}", response_model=SessionDetail)
async def get_session(
    request: Request,
    session_id: str,
    user: UserContext = Depends(require_member),
):
    """
    Get detailed session information including Ash analysis data.
    
    Authorization:
        - Requires CRT membership (any role)
    
    Path Parameters:
        session_id: Session ID (Ash-Bot format)
    
    Returns:
        Full session details with analysis, notes summary, and metadata
    """
    session_repo = get_session_repo(request)
    db_manager = request.app.state.database_manager
    
    async with db_manager.session() as db:
        session = await session_repo.get_with_all_relations(db, session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Calculate duration for display
    duration = session.duration_seconds
    if duration is None and session.status == "active" and session.started_at:
        duration = calculate_elapsed_seconds(session.started_at)
    
    # Build notes list
    notes = [build_note_summary(n) for n in session.notes] if session.notes else []
    
    return SessionDetail(
        id=session.id,
        discord_user_id=session.discord_user_id,
        discord_username=session.discord_username,
        severity=session.severity,
        status=session.status,
        started_at=session.started_at,
        ended_at=session.ended_at,
        duration_seconds=duration,
        duration_display=format_duration(duration),
        message_count=session.message_count,
        crt_user_id=session.crt_user_id,
        crt_member_name=session.crt_user.display_name if session.crt_user else None,
        ash_summary=session.ash_summary,
        analysis=build_ash_analysis(session),
        notes=notes,
        is_archived=(session.status == "archived"),
        archive_date=session.archive.archived_at if session.archive else None,
        created_at=session.created_at,
        updated_at=session.updated_at,
    )


@router.get("/{session_id}/notes", response_model=List[NoteResponse])
async def get_session_notes(
    request: Request,
    session_id: str,
    user: UserContext = Depends(require_member),
):
    """
    Get all notes for a session.
    
    Authorization:
        - Requires CRT membership (any role)
    
    Path Parameters:
        session_id: Session ID
    """
    session_repo = get_session_repo(request)
    note_repo = get_note_repo(request)
    db_manager = request.app.state.database_manager
    
    async with db_manager.session() as db:
        # Verify session exists
        session = await session_repo.get(db, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        notes = await note_repo.get_by_session(db, session_id)
    
    return [NoteResponse.model_validate(n) for n in notes]


# =============================================================================
# User History Endpoint
# =============================================================================

@router.get("/user/{discord_user_id}", response_model=UserSessionHistory)
async def get_user_sessions(
    request: Request,
    discord_user_id: int,
    user: UserContext = Depends(require_member),
    exclude_session: Optional[str] = Query(None, description="Session ID to exclude"),
    limit: int = Query(10, ge=1, le=50, description="Max sessions to return"),
):
    """
    Get session history for a Discord user with pattern analysis.
    
    Authorization:
        - Requires CRT membership (any role)
    
    Path Parameters:
        discord_user_id: Discord user snowflake ID
    
    Query Parameters:
        exclude_session: Session ID to exclude (current session)
        limit: Maximum sessions to return (default: 10, max: 50)
    
    Returns:
        User info, session history, and pattern analysis
    """
    session_repo = get_session_repo(request)
    db_manager = request.app.state.database_manager
    
    async with db_manager.session() as db:
        sessions, patterns = await session_repo.get_user_history_with_patterns(
            db,
            discord_user_id,
            exclude_session_id=exclude_session,
            limit=limit,
        )
    
    # Get username from most recent session
    discord_username = sessions[0].discord_username if sessions else None
    
    return UserSessionHistory(
        discord_user_id=discord_user_id,
        discord_username=discord_username,
        total_sessions=patterns.get("total_sessions", 0),
        sessions=[build_session_summary(s) for s in sessions],
        pattern_analysis=PatternAnalysis(
            common_time_of_day=patterns.get("common_time_of_day"),
            average_frequency_days=patterns.get("average_frequency_days"),
            severity_trend=patterns.get("severity_trend"),
            last_session_days_ago=patterns.get("last_session_days_ago"),
        ),
    )


# =============================================================================
# Session Action Endpoints
# =============================================================================

@router.post("/{session_id}/assign", response_model=SessionDetail)
async def assign_session(
    request: Request,
    session_id: str,
    assign_request: AssignRequest,
    user: UserContext = Depends(require_member),
):
    """
    Assign a CRT user to a session.
    
    Authorization:
        - Requires CRT membership (any role)
    
    Path Parameters:
        session_id: Session ID
    
    Request Body:
        crt_user_id: UUID of CRT user to assign
    """
    session_repo = get_session_repo(request)
    audit_repo = get_audit_repo(request)
    db_manager = request.app.state.database_manager
    
    async with db_manager.session() as db:
        # Get current session
        session = await session_repo.get(db, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        old_crt_id = session.crt_user_id
        
        # Assign new user
        await session_repo.assign_to_crt(
            db, session_id, assign_request.crt_user_id
        )
        
        # Log the action with user tracking (Phase 10)
        await audit_repo.log_action(
            db,
            action="session_assign",
            user_id=user.db_user_id or assign_request.crt_user_id,
            entity_type="session",
            entity_id=session_id,
            old_values={"crt_user_id": str(old_crt_id) if old_crt_id else None},
            new_values={
                "crt_user_id": str(assign_request.crt_user_id),
                "assigned_by": user.email,
            },
        )
        
        await db.commit()
        
        # Fetch updated session with relations
        updated = await session_repo.get_with_all_relations(db, session_id)
    
    return await get_session(request, session_id, user)


@router.post("/{session_id}/unassign", response_model=SessionDetail)
async def unassign_session(
    request: Request,
    session_id: str,
    user: UserContext = Depends(require_member),
):
    """
    Remove CRT user assignment from a session.
    
    Authorization:
        - Requires CRT membership (any role)
    
    Path Parameters:
        session_id: Session ID
    """
    session_repo = get_session_repo(request)
    audit_repo = get_audit_repo(request)
    db_manager = request.app.state.database_manager
    
    async with db_manager.session() as db:
        session = await session_repo.get(db, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        old_crt_id = session.crt_user_id
        
        await session_repo.unassign(db, session_id)
        
        # Log with user tracking (Phase 10)
        await audit_repo.log_action(
            db,
            action="session_unassign",
            user_id=user.db_user_id,
            entity_type="session",
            entity_id=session_id,
            old_values={"crt_user_id": str(old_crt_id) if old_crt_id else None},
            new_values={
                "crt_user_id": None,
                "unassigned_by": user.email,
            },
        )
        
        await db.commit()
    
    return await get_session(request, session_id, user)


@router.post("/{session_id}/close", response_model=SessionDetail)
async def close_session(
    request: Request,
    session_id: str,
    close_request: Optional[CloseRequest] = None,
    user: UserContext = Depends(require_member),
):
    """
    Close an active session.
    
    Authorization:
        - Requires CRT membership (any role)
    
    Actions performed:
        - Set status to 'closed'
        - Lock all session notes
        - Calculate and store duration
        - Log audit event
    
    Path Parameters:
        session_id: Session ID
    
    Request Body (optional):
        summary: Closing summary text
    """
    session_repo = get_session_repo(request)
    note_repo = get_note_repo(request)
    audit_repo = get_audit_repo(request)
    db_manager = request.app.state.database_manager
    
    async with db_manager.session() as db:
        session = await session_repo.get(db, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        if session.status != "active":
            raise HTTPException(
                status_code=400,
                detail=f"Session is already {session.status}"
            )
        
        summary = close_request.summary if close_request else None
        
        # Close the session
        await session_repo.close_session(db, session_id, summary)
        
        # Lock all notes
        await note_repo.lock_session_notes(db, session_id)
        
        # Log the action with user tracking (Phase 10)
        await audit_repo.log_action(
            db,
            action="session_close",
            user_id=user.db_user_id,
            entity_type="session",
            entity_id=session_id,
            new_values={
                "status": "closed",
                "summary": summary,
                "closed_by": user.email,
            },
        )
        
        await db.commit()
    
    return await get_session(request, session_id, user)


@router.post("/{session_id}/reopen", response_model=SessionDetail)
async def reopen_session(
    request: Request,
    session_id: str,
    user: UserContext = Depends(require_lead),  # Phase 10: Lead+ only
):
    """
    Reopen a closed session.
    
    Authorization (Phase 10):
        - Requires Lead or Admin role
    
    Actions performed:
        - Set status back to 'active'
        - Clear ended_at and duration
        - Unlock session notes
        - Log audit event
    
    Path Parameters:
        session_id: Session ID
    
    Cannot reopen archived sessions - they are permanently sealed.
    """
    session_repo = get_session_repo(request)
    note_repo = get_note_repo(request)
    audit_repo = get_audit_repo(request)
    db_manager = request.app.state.database_manager
    logging_manager = request.app.state.logging_manager
    logger = logging_manager.get_logger("sessions")
    
    async with db_manager.session() as db:
        session = await session_repo.get(db, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        if session.status == "archived":
            raise HTTPException(
                status_code=403,
                detail="Cannot reopen archived sessions. Archived sessions are permanently sealed."
            )
        
        if session.status != "closed":
            raise HTTPException(
                status_code=400,
                detail=f"Cannot reopen session with status: {session.status}"
            )
        
        old_status = session.status
        
        # Reopen the session
        await session_repo.reopen_session(db, session_id)
        
        # Unlock all notes
        await note_repo.unlock_session_notes(db, session_id)
        
        # Log the action with user tracking (Phase 10)
        await audit_repo.log_action(
            db,
            action="session_reopen",
            user_id=user.db_user_id,
            entity_type="session",
            entity_id=session_id,
            old_values={"status": old_status},
            new_values={
                "status": "active",
                "reopened_by": user.email,
                "reopened_by_role": user.role.value if user.role else None,
            },
        )
        
        await db.commit()
        
        logger.info(f"Session {session_id} reopened by {user.email} (role: {user.role.value})")
    
    return await get_session(request, session_id, user)


__all__ = ["router"]
