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
Sessions API Routes - Crisis session endpoints for the dashboard
----------------------------------------------------------------------------
FILE VERSION: v5.0-2-2.8-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 2 - Data Layer
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

ENDPOINTS:
    GET /api/sessions              - List sessions with filters
    GET /api/sessions/active       - Get active sessions (dashboard view)
    GET /api/sessions/stats        - Session statistics
    GET /api/sessions/{id}         - Get session detail
    GET /api/sessions/{id}/notes   - Get session notes
    POST /api/sessions/{id}/assign - Assign CRT user to session
    POST /api/sessions/{id}/close  - Close a session
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

__version__ = "v5.0-2-2.8-1"

# Create router
router = APIRouter(prefix="/api/sessions", tags=["Sessions"])


# =============================================================================
# Pydantic Models (Request/Response Schemas)
# =============================================================================

class SessionResponse(BaseModel):
    """Session response schema."""
    id: str
    discord_user_id: Optional[int] = None
    discord_username: Optional[str] = None
    discord_display_name: Optional[str] = None
    channel_id: Optional[int] = None
    guild_id: Optional[int] = None
    status: str
    severity: str
    crisis_score: Optional[float] = None
    confidence: Optional[float] = None
    detected_topics: List[str] = []
    message_count: int = 0
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    crt_user_id: Optional[UUID] = None
    ash_summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SessionListResponse(BaseModel):
    """Paginated session list response."""
    sessions: List[SessionResponse]
    total: int
    page: int
    per_page: int
    has_more: bool


class SessionStatsResponse(BaseModel):
    """Session statistics response."""
    period_days: int
    total_sessions: int
    by_severity: Dict[str, int]
    by_status: Dict[str, int]
    average_crisis_score: Optional[float] = None


class NoteResponse(BaseModel):
    """Note response schema."""
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

@router.get("", response_model=SessionListResponse)
async def list_sessions(
    request: Request,
    status: Optional[str] = Query(None, description="Filter by status"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
):
    """
    List sessions with optional filters and pagination.
    
    Query Parameters:
        status: Filter by status (active, closed, archived)
        severity: Filter by severity (critical, high, medium, low, safe)
        page: Page number (default: 1)
        per_page: Items per page (default: 20, max: 100)
    """
    session_repo = get_session_repo(request)
    db_manager = request.app.state.database_manager
    
    skip = (page - 1) * per_page
    filters = {}
    
    if status:
        filters["status"] = status
    if severity:
        filters["severity"] = severity
    
    async with db_manager.session() as db:
        if filters:
            sessions = await session_repo.get_filtered(
                db, filters=filters, skip=skip, limit=per_page,
                order_by="started_at", descending=True
            )
            total = await session_repo.count(db, filters)
        else:
            sessions = await session_repo.get_all(
                db, skip=skip, limit=per_page,
                order_by="started_at", descending=True
            )
            total = await session_repo.count(db)
    
    return SessionListResponse(
        sessions=[SessionResponse.model_validate(s) for s in sessions],
        total=total,
        page=page,
        per_page=per_page,
        has_more=(skip + len(sessions)) < total,
    )


@router.get("/active", response_model=List[SessionResponse])
async def get_active_sessions(request: Request):
    """
    Get all active sessions for the dashboard.
    
    Returns sessions ordered by severity (critical first) then by time.
    This is the primary endpoint for the real-time dashboard view.
    """
    session_repo = get_session_repo(request)
    db_manager = request.app.state.database_manager
    
    async with db_manager.session() as db:
        sessions = await session_repo.get_active_sessions(db, limit=100)
    
    return [SessionResponse.model_validate(s) for s in sessions]


@router.get("/critical", response_model=List[SessionResponse])
async def get_critical_sessions(request: Request):
    """
    Get critical severity sessions.
    
    Returns only critical sessions that need immediate attention.
    """
    session_repo = get_session_repo(request)
    db_manager = request.app.state.database_manager
    
    async with db_manager.session() as db:
        sessions = await session_repo.get_critical_sessions(db, active_only=True)
    
    return [SessionResponse.model_validate(s) for s in sessions]


@router.get("/unassigned", response_model=List[SessionResponse])
async def get_unassigned_sessions(request: Request):
    """
    Get active sessions not assigned to any CRT user.
    
    Useful for CRT members looking to pick up new sessions.
    """
    session_repo = get_session_repo(request)
    db_manager = request.app.state.database_manager
    
    async with db_manager.session() as db:
        sessions = await session_repo.get_unassigned_sessions(db, active_only=True)
    
    return [SessionResponse.model_validate(s) for s in sessions]


@router.get("/stats", response_model=SessionStatsResponse)
async def get_session_stats(
    request: Request,
    days: int = Query(30, ge=1, le=365, description="Days to analyze"),
):
    """
    Get session statistics for the specified time period.
    
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

@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(request: Request, session_id: str):
    """
    Get a single session by ID.
    
    Path Parameters:
        session_id: Session ID (Ash-Bot format)
    """
    session_repo = get_session_repo(request)
    db_manager = request.app.state.database_manager
    
    async with db_manager.session() as db:
        session = await session_repo.get(db, session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return SessionResponse.model_validate(session)


@router.get("/{session_id}/notes", response_model=List[NoteResponse])
async def get_session_notes(request: Request, session_id: str):
    """
    Get all notes for a session.
    
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
# Session Action Endpoints
# =============================================================================

@router.post("/{session_id}/assign", response_model=SessionResponse)
async def assign_session(
    request: Request,
    session_id: str,
    assign_request: AssignRequest,
):
    """
    Assign a CRT user to a session.
    
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
        updated = await session_repo.assign_to_crt(
            db, session_id, assign_request.crt_user_id
        )
        
        # Log the action
        await audit_repo.log_action(
            db,
            action="session_assign",
            user_id=assign_request.crt_user_id,
            entity_type="session",
            entity_id=session_id,
            old_values={"crt_user_id": str(old_crt_id) if old_crt_id else None},
            new_values={"crt_user_id": str(assign_request.crt_user_id)},
        )
        
        await db.commit()
    
    return SessionResponse.model_validate(updated)


@router.post("/{session_id}/unassign", response_model=SessionResponse)
async def unassign_session(request: Request, session_id: str):
    """
    Remove CRT user assignment from a session.
    
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
        
        updated = await session_repo.unassign(db, session_id)
        
        await audit_repo.log_action(
            db,
            action="session_unassign",
            entity_type="session",
            entity_id=session_id,
            old_values={"crt_user_id": str(old_crt_id) if old_crt_id else None},
            new_values={"crt_user_id": None},
        )
        
        await db.commit()
    
    return SessionResponse.model_validate(updated)


@router.post("/{session_id}/close", response_model=SessionResponse)
async def close_session(
    request: Request,
    session_id: str,
    close_request: Optional[CloseRequest] = None,
):
    """
    Close a session.
    
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
        updated = await session_repo.close_session(db, session_id, summary)
        
        # Lock all notes
        await note_repo.lock_session_notes(db, session_id)
        
        # Log the action
        await audit_repo.log_action(
            db,
            action="session_close",
            entity_type="session",
            entity_id=session_id,
            new_values={
                "status": "closed",
                "summary": summary,
            },
        )
        
        await db.commit()
    
    return SessionResponse.model_validate(updated)


# =============================================================================
# Session History Endpoints
# =============================================================================

@router.get("/user/{discord_user_id}", response_model=List[SessionResponse])
async def get_user_sessions(
    request: Request,
    discord_user_id: int,
    days: int = Query(30, ge=1, le=365, description="Days to look back"),
):
    """
    Get session history for a Discord user.
    
    Path Parameters:
        discord_user_id: Discord user snowflake ID
    
    Query Parameters:
        days: Days to look back (default: 30)
    """
    session_repo = get_session_repo(request)
    db_manager = request.app.state.database_manager
    
    async with db_manager.session() as db:
        sessions = await session_repo.get_user_session_history(
            db, discord_user_id, days=days
        )
    
    return [SessionResponse.model_validate(s) for s in sessions]
