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
Notes API Routes - CRUD operations for session notes
----------------------------------------------------------------------------
FILE VERSION: v5.0-6-6.7-3
LAST MODIFIED: 2026-01-08
PHASE: Phase 6 - Notes System
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
"""

from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.managers.database import DatabaseManager
from src.repositories.note_repository import create_note_repository
from src.repositories.session_repository import create_session_repository
from src.repositories.audit_log_repository import create_audit_log_repository

__version__ = "v5.0-6-6.7-3"


# =============================================================================
# Router Setup
# =============================================================================

router = APIRouter(
    prefix="/api/notes",
    tags=["notes"],
)


# =============================================================================
# Request/Response Models
# =============================================================================

class NoteCreate(BaseModel):
    """Request model for creating a note."""
    content: str = Field(..., min_length=1, max_length=50000)
    content_html: Optional[str] = Field(None, max_length=100000)


class NoteUpdate(BaseModel):
    """Request model for updating a note."""
    content: str = Field(..., min_length=1, max_length=50000)
    content_html: Optional[str] = Field(None, max_length=100000)


class NoteDetail(BaseModel):
    """Response model for note details."""
    id: str
    session_id: str
    author_id: Optional[str]
    author_name: Optional[str]
    content: str
    content_html: Optional[str]
    created_at: datetime
    updated_at: datetime
    version: int
    is_locked: bool
    
    class Config:
        from_attributes = True


class NoteSummary(BaseModel):
    """Response model for note list items."""
    id: str
    author_id: Optional[str]
    author_name: Optional[str]
    content_preview: str
    created_at: datetime
    is_locked: bool
    version: int
    
    class Config:
        from_attributes = True


class NoteListResponse(BaseModel):
    """Response model for listing notes."""
    session_id: str
    notes: List[NoteSummary]
    total: int
    is_session_locked: bool


# =============================================================================
# Dependencies
# =============================================================================

async def get_db(request: Request) -> AsyncSession:
    """Get database session from app state."""
    db_manager: DatabaseManager = request.app.state.database_manager
    async with db_manager.session() as session:
        yield session


def get_logging_manager(request: Request):
    """Get logging manager from app state."""
    return request.app.state.logging_manager


def get_db_manager(request: Request) -> DatabaseManager:
    """Get database manager from app state."""
    return request.app.state.database_manager


# =============================================================================
# Helper Functions
# =============================================================================

def note_to_detail(note, author_name: Optional[str] = None) -> NoteDetail:
    """Convert Note model to NoteDetail response."""
    return NoteDetail(
        id=str(note.id),
        session_id=note.session_id,
        author_id=str(note.author_id) if note.author_id else None,
        author_name=author_name or (note.author.display_name if note.author else None),
        content=note.content,
        content_html=note.content_html,
        created_at=note.created_at,
        updated_at=note.updated_at,
        version=note.version,
        is_locked=note.is_locked,
    )


def note_to_summary(note, author_name: Optional[str] = None) -> NoteSummary:
    """Convert Note model to NoteSummary response."""
    # Get first 200 characters for preview
    preview = note.content[:200] if note.content else ""
    if len(note.content) > 200:
        preview += "..."
    
    return NoteSummary(
        id=str(note.id),
        author_id=str(note.author_id) if note.author_id else None,
        author_name=author_name or (note.author.display_name if note.author else None),
        content_preview=preview,
        created_at=note.created_at,
        is_locked=note.is_locked,
        version=note.version,
    )


# =============================================================================
# Routes - Session Notes
# =============================================================================

@router.get(
    "/session/{session_id}",
    response_model=NoteListResponse,
    summary="List session notes",
    description="Get all notes for a crisis session.",
)
async def list_session_notes(
    session_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Get all notes for a session.
    
    Returns notes ordered by creation time (oldest first).
    """
    logging_manager = get_logging_manager(request)
    db_manager = get_db_manager(request)
    
    note_repo = create_note_repository(db_manager, logging_manager)
    session_repo = create_session_repository(db_manager, logging_manager)
    
    # Check if session exists
    session = await session_repo.get(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found",
        )
    
    # Get notes with author info
    notes = await note_repo.get_by_session(db, session_id, include_author=True)
    
    # Determine if session is locked (closed or archived)
    is_session_locked = session.status in ("closed", "archived")
    
    # Convert to response models
    note_summaries = [note_to_summary(note) for note in notes]
    
    return NoteListResponse(
        session_id=session_id,
        notes=note_summaries,
        total=len(note_summaries),
        is_session_locked=is_session_locked,
    )


@router.post(
    "/session/{session_id}",
    response_model=NoteDetail,
    status_code=status.HTTP_201_CREATED,
    summary="Create note",
    description="Create a new note for a crisis session.",
)
async def create_note(
    session_id: str,
    note_data: NoteCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new note for the session.
    
    Fails if:
        - Session does not exist
        - Session is closed/archived (unless admin - TODO in Phase 10)
    """
    logging_manager = get_logging_manager(request)
    db_manager = get_db_manager(request)
    logger = logging_manager.get_logger("notes")
    
    note_repo = create_note_repository(db_manager, logging_manager)
    session_repo = create_session_repository(db_manager, logging_manager)
    audit_repo = create_audit_log_repository(db_manager, logging_manager)
    
    # Check if session exists
    session = await session_repo.get(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found",
        )
    
    # Check if session is locked
    if session.status in ("closed", "archived"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Cannot add notes to {session.status} session",
        )
    
    # Create the note
    # TODO: Get actual author_id from authentication (Phase 10)
    # For now, use None for author_id
    note = await note_repo.create_note(
        session=db,
        session_id=session_id,
        author_id=None,  # Will be set from auth in Phase 10
        content=note_data.content,
        content_html=note_data.content_html,
    )
    
    # Create audit log entry
    await audit_repo.create(
        db,
        {
            "action": "note.create",
            "user_id": None,  # Will be set from auth in Phase 10
            "entity_type": "note",
            "entity_id": str(note.id),
            "new_values": {
                "session_id": session_id,
                "content_length": len(note_data.content),
            },
        },
    )
    
    await db.commit()
    
    logger.info(f"Created note {note.id} for session {session_id}")
    
    return note_to_detail(note)


@router.get(
    "/{note_id}",
    response_model=NoteDetail,
    summary="Get note",
    description="Get a specific note by ID.",
)
async def get_note(
    note_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Get a specific note with full content."""
    logging_manager = get_logging_manager(request)
    db_manager = get_db_manager(request)
    
    note_repo = create_note_repository(db_manager, logging_manager)
    
    note = await note_repo.get(db, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note {note_id} not found",
        )
    
    return note_to_detail(note)


@router.put(
    "/{note_id}",
    response_model=NoteDetail,
    summary="Update note",
    description="Update an existing note's content.",
)
async def update_note(
    note_id: UUID,
    note_data: NoteUpdate,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Update an existing note.
    
    Behavior:
        - Increments version number
        - Updates updated_at timestamp
        - Fails if note is locked
    
    TODO (Phase 10 - Authentication/User Management):
        - Get current user from request.user
        - Check if current_user.id == note.author_id
        - Only allow edit if user owns the note OR user is admin
        - Return 403 Forbidden if user doesn't own the note
    """
    logging_manager = get_logging_manager(request)
    db_manager = get_db_manager(request)
    logger = logging_manager.get_logger("notes")
    
    note_repo = create_note_repository(db_manager, logging_manager)
    audit_repo = create_audit_log_repository(db_manager, logging_manager)
    
    # Get existing note
    note = await note_repo.get(db, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note {note_id} not found",
        )
    
    # Check if note is locked
    if note.is_locked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot edit locked note",
        )
    
    # TODO (Phase 10): Ownership check
    # current_user = request.state.user  # From auth middleware
    # if note.author_id and note.author_id != current_user.id:
    #     if not current_user.is_admin:
    #         raise HTTPException(
    #             status_code=status.HTTP_403_FORBIDDEN,
    #             detail="You can only edit your own notes",
    #         )
    
    # Update the note
    old_version = note.version
    updated_note = await note_repo.update_content(
        session=db,
        note_id=note_id,
        content=note_data.content,
        content_html=note_data.content_html,
    )
    
    if not updated_note:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update note",
        )
    
    # Create audit log entry
    await audit_repo.create(
        db,
        {
            "action": "note.update",
            "user_id": None,  # Will be set from auth in Phase 10
            "entity_type": "note",
            "entity_id": str(note_id),
            "old_values": {
                "version": old_version,
            },
            "new_values": {
                "session_id": note.session_id,
                "version": updated_note.version,
                "content_length": len(note_data.content),
            },
        },
    )
    
    await db.commit()
    
    logger.info(f"Updated note {note_id} to version {updated_note.version}")
    
    return note_to_detail(updated_note)


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete note",
    description="Delete a note (admin only - enforced in Phase 10).",
)
async def delete_note(
    note_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a note.
    
    Note: Admin permission check will be added in Phase 10.
    """
    logging_manager = get_logging_manager(request)
    db_manager = get_db_manager(request)
    logger = logging_manager.get_logger("notes")
    
    note_repo = create_note_repository(db_manager, logging_manager)
    audit_repo = create_audit_log_repository(db_manager, logging_manager)
    
    # Get existing note
    note = await note_repo.get(db, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note {note_id} not found",
        )
    
    session_id = note.session_id
    
    # Delete the note
    deleted = await note_repo.delete(db, note_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete note",
        )
    
    # Create audit log entry
    await audit_repo.create(
        db,
        {
            "action": "note.delete",
            "user_id": None,  # Will be set from auth in Phase 10
            "entity_type": "note",
            "entity_id": str(note_id),
            "old_values": {
                "session_id": session_id,
            },
        },
    )
    
    await db.commit()
    
    logger.info(f"Deleted note {note_id}")
    
    return None


# =============================================================================
# Routes - Note Locking
# =============================================================================

@router.post(
    "/{note_id}/lock",
    response_model=NoteDetail,
    summary="Lock note",
    description="Lock a note to prevent further edits.",
)
async def lock_note(
    note_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Manually lock a note."""
    logging_manager = get_logging_manager(request)
    db_manager = get_db_manager(request)
    logger = logging_manager.get_logger("notes")
    
    note_repo = create_note_repository(db_manager, logging_manager)
    audit_repo = create_audit_log_repository(db_manager, logging_manager)
    
    # Get existing note
    note = await note_repo.get(db, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note {note_id} not found",
        )
    
    if note.is_locked:
        # Already locked, just return it
        return note_to_detail(note)
    
    # Lock the note
    locked_note = await note_repo.lock_note(db, note_id)
    
    # Create audit log entry
    await audit_repo.create(
        db,
        {
            "action": "note.lock",
            "user_id": None,  # Will be set from auth in Phase 10
            "entity_type": "note",
            "entity_id": str(note_id),
            "old_values": {"is_locked": False},
            "new_values": {
                "session_id": note.session_id,
                "is_locked": True,
            },
        },
    )
    
    await db.commit()
    
    logger.info(f"Locked note {note_id}")
    
    return note_to_detail(locked_note)


@router.post(
    "/{note_id}/unlock",
    response_model=NoteDetail,
    summary="Unlock note",
    description="Unlock a note to allow edits (admin only - enforced in Phase 10).",
)
async def unlock_note(
    note_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Unlock a note to allow edits.
    
    Note: Admin permission check will be added in Phase 10.
    """
    logging_manager = get_logging_manager(request)
    db_manager = get_db_manager(request)
    logger = logging_manager.get_logger("notes")
    
    note_repo = create_note_repository(db_manager, logging_manager)
    audit_repo = create_audit_log_repository(db_manager, logging_manager)
    
    # Get existing note
    note = await note_repo.get(db, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note {note_id} not found",
        )
    
    if not note.is_locked:
        # Already unlocked, just return it
        return note_to_detail(note)
    
    # Unlock the note
    unlocked_note = await note_repo.unlock_note(db, note_id)
    
    # Create audit log entry
    await audit_repo.create(
        db,
        {
            "action": "note.unlock",
            "user_id": None,  # Will be set from auth in Phase 10
            "entity_type": "note",
            "entity_id": str(note_id),
            "old_values": {"is_locked": True},
            "new_values": {
                "session_id": note.session_id,
                "is_locked": False,
            },
        },
    )
    
    await db.commit()
    
    logger.info(f"Unlocked note {note_id}")
    
    return note_to_detail(unlocked_note)


# =============================================================================
# Routes - Search
# =============================================================================

@router.get(
    "/search",
    response_model=List[NoteSummary],
    summary="Search notes",
    description="Search notes by content.",
)
async def search_notes(
    q: str,
    session_id: Optional[str] = None,
    limit: int = 50,
    request: Request = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Search notes by content.
    
    Optionally filter by session_id.
    """
    logging_manager = get_logging_manager(request)
    db_manager = get_db_manager(request)
    
    note_repo = create_note_repository(db_manager, logging_manager)
    
    notes = await note_repo.search_notes(
        session=db,
        query=q,
        session_id=session_id,
        limit=min(limit, 100),
    )
    
    return [note_to_summary(note) for note in notes]


__all__ = ["router"]
