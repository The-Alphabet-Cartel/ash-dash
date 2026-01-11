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
Users API Routes - CRT member management endpoints
----------------------------------------------------------------------------
FILE VERSION: v5.0-2-2.8-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 2 - Data Layer
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

ENDPOINTS:
    GET /api/users           - List CRT users
    GET /api/users/me        - Get current user (from auth)
    GET /api/users/{id}      - Get user detail
    GET /api/users/{id}/sessions - Get sessions assigned to user
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel, Field

from src.repositories import (
    create_user_repository,
    create_session_repository,
)

__version__ = "v5.0-2-2.8-1"

# Create router
router = APIRouter(prefix="/api/users", tags=["Users"])


# =============================================================================
# Pydantic Models (Request/Response Schemas)
# =============================================================================

class UserResponse(BaseModel):
    """User response schema."""
    id: UUID
    email: str
    display_name: str
    pocket_id_sub: Optional[str] = None
    groups: List[str] = []
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """Paginated user list response."""
    users: List[UserResponse]
    total: int


class UserSessionSummary(BaseModel):
    """Summary of user's session assignments."""
    active_sessions: int
    total_sessions: int
    sessions_this_month: int


class UserDetailResponse(UserResponse):
    """Extended user response with session summary."""
    session_summary: Optional[UserSessionSummary] = None


# =============================================================================
# Dependency Injection Helpers
# =============================================================================

def get_user_repo(request: Request):
    """Get UserRepository from app state."""
    return create_user_repository(
        request.app.state.database_manager,
        request.app.state.logging_manager,
    )


def get_session_repo(request: Request):
    """Get SessionRepository from app state."""
    return create_session_repository(
        request.app.state.database_manager,
        request.app.state.logging_manager,
    )


# =============================================================================
# User List Endpoints
# =============================================================================

@router.get("", response_model=UserListResponse)
async def list_users(
    request: Request,
    role: Optional[str] = Query(None, description="Filter by role"),
    active_only: bool = Query(True, description="Only active users"),
    search: Optional[str] = Query(None, description="Search by name/email"),
):
    """
    List CRT users with optional filters.
    
    Query Parameters:
        role: Filter by role (admin, crt_member)
        active_only: Only return active users (default: true)
        search: Search by display name or email
    """
    user_repo = get_user_repo(request)
    db_manager = request.app.state.database_manager
    
    async with db_manager.session() as db:
        if search:
            users = await user_repo.search_users(
                db, query=search, active_only=active_only
            )
        elif role:
            users = await user_repo.get_by_role(db, role, active_only=active_only)
        elif active_only:
            users = await user_repo.get_active_users(db)
        else:
            users = await user_repo.get_all(db, limit=1000)
    
    return UserListResponse(
        users=[UserResponse.model_validate(u) for u in users],
        total=len(users),
    )


@router.get("/admins", response_model=List[UserResponse])
async def get_admins(request: Request):
    """Get all admin users."""
    user_repo = get_user_repo(request)
    db_manager = request.app.state.database_manager
    
    async with db_manager.session() as db:
        admins = await user_repo.get_admins(db)
    
    return [UserResponse.model_validate(u) for u in admins]


@router.get("/crt", response_model=List[UserResponse])
async def get_crt_members(request: Request):
    """Get all CRT members."""
    user_repo = get_user_repo(request)
    db_manager = request.app.state.database_manager
    
    async with db_manager.session() as db:
        members = await user_repo.get_crt_members(db)
    
    return [UserResponse.model_validate(u) for u in members]


# =============================================================================
# Current User Endpoint
# =============================================================================

@router.get("/me", response_model=UserDetailResponse)
async def get_current_user(request: Request):
    """
    Get the current authenticated user.
    
    Note: This currently returns a placeholder until auth is fully implemented.
    In Phase 3+, this will use the Pocket-ID session to identify the user.
    """
    # TODO: Get actual user from Pocket-ID session
    # For now, return 401 if no auth mechanism is in place
    
    # Check if we have a user in request state (set by auth middleware)
    current_user = getattr(request.state, "user", None)
    
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="Authentication required. Please log in via Pocket-ID."
        )
    
    return UserDetailResponse.model_validate(current_user)


# =============================================================================
# User Detail Endpoints
# =============================================================================

@router.get("/{user_id}", response_model=UserDetailResponse)
async def get_user(request: Request, user_id: UUID):
    """
    Get a single user by ID with session summary.
    
    Path Parameters:
        user_id: User UUID
    """
    user_repo = get_user_repo(request)
    session_repo = get_session_repo(request)
    db_manager = request.app.state.database_manager
    
    async with db_manager.session() as db:
        user = await user_repo.get(db, user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get session summary
        active_sessions = await session_repo.get_by_crt_user(
            db, user_id, status="active"
        )
        all_sessions = await session_repo.get_by_crt_user(db, user_id)
        
        # Count sessions this month (using get_filtered would need date filter)
        sessions_this_month = len([
            s for s in all_sessions 
            if s.created_at and s.created_at.month == datetime.utcnow().month
        ])
    
    response = UserDetailResponse.model_validate(user)
    response.session_summary = UserSessionSummary(
        active_sessions=len(active_sessions),
        total_sessions=len(all_sessions),
        sessions_this_month=sessions_this_month,
    )
    
    return response


@router.get("/{user_id}/sessions")
async def get_user_sessions(
    request: Request,
    user_id: UUID,
    status: Optional[str] = Query(None, description="Filter by status"),
):
    """
    Get sessions assigned to a CRT user.
    
    Path Parameters:
        user_id: User UUID
    
    Query Parameters:
        status: Filter by status (active, closed, archived)
    """
    user_repo = get_user_repo(request)
    session_repo = get_session_repo(request)
    db_manager = request.app.state.database_manager
    
    async with db_manager.session() as db:
        # Verify user exists
        user = await user_repo.get(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        sessions = await session_repo.get_by_crt_user(db, user_id, status=status)
    
    # Import here to avoid circular import
    from src.api.routes.sessions import SessionResponse
    return [SessionResponse.model_validate(s) for s in sessions]
