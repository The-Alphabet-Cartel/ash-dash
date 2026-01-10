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
Archive API Routes - Session archiving with encryption and authorization
----------------------------------------------------------------------------
FILE VERSION: v5.0-10-10.2.7-1
LAST MODIFIED: 2026-01-10
PHASE: Phase 10 - Authentication & Authorization
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

ENDPOINTS:
    POST   /api/archives/session/{session_id}  - Archive a session
    GET    /api/archives                        - List archives with filtering
    GET    /api/archives/statistics             - Get archive statistics
    GET    /api/archives/expiring               - Get archives expiring soon
    GET    /api/archives/{archive_id}           - Get archive metadata
    GET    /api/archives/{archive_id}/download  - Retrieve and decrypt archive
    PUT    /api/archives/{archive_id}/retention - Update retention tier (Lead+)
    DELETE /api/archives/{archive_id}           - Delete archive (Admin only)

AUTHORIZATION (Phase 10):
    - All view endpoints require CRT membership (require_member)
    - Archive creation: Requires CRT membership, sets archived_by from user
    - Retention tier change: Requires Lead or Admin role
    - Archive delete: Requires Admin role only
    - All audit logs include user_id for tracking
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.managers.database import DatabaseManager
from src.repositories.archive_repository import create_archive_repository
from src.repositories.session_repository import create_session_repository
from src.repositories.note_repository import create_note_repository
from src.repositories.audit_log_repository import create_audit_log_repository
from src.managers.archive import (
    create_archive_manager,
    ArchiveListFilter,
    ArchiveManager,
)

# Phase 10: Import auth dependencies
from src.api.dependencies.auth import (
    require_member,
    require_lead,
    require_admin,
)
from src.api.middleware.auth_middleware import UserContext

__version__ = "v5.0-10-10.2.7-1"


# =============================================================================
# Router Setup
# =============================================================================

router = APIRouter(
    prefix="/api/archives",
    tags=["archives"],
)


# =============================================================================
# Request/Response Models
# =============================================================================

class ArchiveCreateRequest(BaseModel):
    """Request model for archiving a session."""
    retention_tier: str = Field(
        default="standard",
        description="Retention tier: 'standard' (1 year) or 'permanent' (7 years)",
    )


class RetentionUpdateRequest(BaseModel):
    """Request model for updating retention tier."""
    retention_tier: str = Field(
        ...,
        description="New retention tier: 'standard' or 'permanent'",
    )


class RetentionExtendRequest(BaseModel):
    """Request model for extending retention."""
    days: int = Field(
        ...,
        gt=0,
        le=3650,
        description="Days to extend retention (1-3650)",
    )


class ArchiveMetadata(BaseModel):
    """Response model for archive metadata."""
    id: str
    session_id: str
    discord_user_id: Optional[int]
    discord_user_name: Optional[str]
    severity: Optional[str]
    session_started_at: Optional[datetime]
    session_ended_at: Optional[datetime]
    archived_at: datetime
    archived_by_name: Optional[str]
    size_bytes: int
    size_mb: float
    notes_count: int
    retention_tier: str
    retention_until: Optional[datetime]
    is_expired: bool
    is_permanent: bool
    days_until_expiry: Optional[int]

    class Config:
        from_attributes = True


class ArchiveListItem(BaseModel):
    """Response model for archive list items."""
    id: str
    session_id: str
    discord_user_id: Optional[int]
    discord_user_name: Optional[str]
    severity: Optional[str]
    session_started_at: Optional[datetime]
    session_ended_at: Optional[datetime]
    archived_at: datetime
    archived_by_name: Optional[str]
    size_bytes: int
    size_mb: float
    notes_count: int
    retention_tier: str
    retention_until: Optional[datetime]
    is_expired: bool
    is_permanent: bool
    days_until_expiry: Optional[int]

    class Config:
        from_attributes = True


class ArchiveListResponse(BaseModel):
    """Response model for archive listing."""
    archives: List[ArchiveListItem]
    total: int
    skip: int
    limit: int


class ArchiveCreateResponse(BaseModel):
    """Response model for archive creation."""
    success: bool
    archive_id: Optional[str]
    storage_key: Optional[str]
    size_bytes: int
    checksum: Optional[str]
    error: Optional[str]


class ArchivePackageResponse(BaseModel):
    """Response model for retrieved archive package."""
    version: str
    archived_at: str
    session: Dict[str, Any]
    notes: List[Dict[str, Any]]
    metadata: Dict[str, Any]


class ArchiveStatistics(BaseModel):
    """Response model for archive statistics."""
    total_archives: int
    total_size_bytes: int
    total_size_mb: float
    total_size_gb: float
    encrypted_count: int
    by_bucket: Dict[str, Dict[str, Any]]
    by_retention_tier: Dict[str, Dict[str, Any]]
    by_severity: Dict[str, int]


class ExpiringArchive(BaseModel):
    """Response model for expiring archive."""
    id: str
    session_id: str
    discord_user_name: Optional[str]
    retention_until: Optional[datetime]
    days_remaining: Optional[int]
    retention_tier: str


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


def get_config_manager(request: Request):
    """Get config manager from app state."""
    return request.app.state.config_manager


def get_secrets_manager(request: Request):
    """Get secrets manager from app state."""
    return request.app.state.secrets_manager


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


async def get_archive_manager(request: Request) -> ArchiveManager:
    """
    Get or create archive manager.
    
    Note: Archive manager requires MinIO connection which may not be
    available in all environments. This will raise an error if MinIO
    is not configured.
    """
    # Check if already cached
    if hasattr(request.app.state, "archive_manager") and request.app.state.archive_manager:
        return request.app.state.archive_manager
    
    # Create archive manager on first use
    logging_manager = get_logging_manager(request)
    config_manager = get_config_manager(request)
    secrets_manager = get_secrets_manager(request)
    db_manager = get_db_manager(request)
    
    # Check if archive key is configured
    if not secrets_manager.has_archive_master_key():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Archive system not configured: missing archive master key",
        )
    
    # Create MinIO manager
    from src.managers.archive import create_minio_manager
    
    try:
        minio_manager = await create_minio_manager(
            config_manager=config_manager,
            secrets_manager=secrets_manager,
            logging_manager=logging_manager,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Archive storage unavailable: {str(e)}",
        )
    
    # Create archive repository
    archive_repo = create_archive_repository(db_manager, logging_manager)
    
    # Create archive manager
    archive_manager = await create_archive_manager(
        config_manager=config_manager,
        secrets_manager=secrets_manager,
        minio_manager=minio_manager,
        database_manager=db_manager,
        archive_repository=archive_repo,
        logging_manager=logging_manager,
    )
    
    # Cache for future requests
    request.app.state.archive_manager = archive_manager
    
    return archive_manager


# =============================================================================
# Routes - Archive Creation
# =============================================================================

@router.post(
    "/session/{session_id}",
    response_model=ArchiveCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Archive a session",
    description="Archive a completed session with encryption. Requires CRT membership.",
)
async def archive_session(
    session_id: str,
    archive_request: ArchiveCreateRequest,
    request: Request,
    user: UserContext = Depends(require_member),
    db: AsyncSession = Depends(get_db),
):
    """
    Archive a crisis session.
    
    Authorization:
        - Requires CRT membership (any role)
        - archived_by is set from authenticated user
    
    The session and all its notes are encrypted with AES-256-GCM
    and uploaded to MinIO storage on the Syn VM.
    
    Fails if:
    - Session does not exist
    - Session is already archived
    - Session is still active (not closed)
    """
    logging_manager = get_logging_manager(request)
    db_manager = get_db_manager(request)
    logger = logging_manager.get_logger("archives")
    
    session_repo = create_session_repository(db_manager, logging_manager)
    note_repo = create_note_repository(db_manager, logging_manager)
    audit_repo = create_audit_log_repository(db_manager, logging_manager)
    archive_repo = create_archive_repository(db_manager, logging_manager)
    
    # Get session
    session = await session_repo.get(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found",
        )
    
    # Check if already archived
    if await archive_repo.session_has_archive(db, session_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Session {session_id} is already archived",
        )
    
    # Check session status - should be closed
    if session.status == "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot archive active session. Close the session first.",
        )
    
    # Get archive manager
    archive_manager = await get_archive_manager(request)
    
    # Get session notes
    notes = await note_repo.get_by_session(db, session_id)
    notes_data = [
        {
            "id": str(note.id),
            "content": note.content,
            "content_html": note.content_html,
            "author_id": str(note.author_id) if note.author_id else None,
            "created_at": note.created_at.isoformat(),
            "updated_at": note.updated_at.isoformat(),
            "version": note.version,
            "is_locked": note.is_locked,
        }
        for note in notes
    ]
    
    # Build session data
    session_data = {
        "session_id": session.id,
        "user_id": session.discord_user_id,
        "user_name": session.discord_username,
        "severity": session.severity,
        "crisis_score": float(session.crisis_score) if session.crisis_score else None,
        "confidence": float(session.confidence) if session.confidence else None,
        "status": session.status,
        "started_at": session.started_at.isoformat() if session.started_at else None,
        "ended_at": session.ended_at.isoformat() if session.ended_at else None,
        "duration_seconds": session.duration_seconds,
        "message_count": session.message_count,
        "ash_summary": session.ash_summary,
        "analysis_data": session.analysis_data,
    }
    
    # Phase 10: Get archived_by from authenticated user
    archived_by_id = user.db_user_id
    archived_by_name = user.name or user.email
    
    # Archive the session
    result = await archive_manager.archive_session(
        session_id=session_id,
        session_data=session_data,
        notes=notes_data,
        archived_by_id=archived_by_id,
        archived_by_name=archived_by_name,
        retention_tier=archive_request.retention_tier,
    )
    
    if not result.success:
        logger.error(f"Failed to archive session {session_id}: {result.error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.error,
        )
    
    # Update session status to archived
    await session_repo.update(db, session_id, {"status": "archived"})
    
    # Create audit log entry with user tracking (Phase 10)
    await audit_repo.create(
        db,
        {
            "action": "archive.create",
            "user_id": get_user_id_for_audit(user),
            "entity_type": "archive",
            "entity_id": str(result.archive_id),
            "new_values": {
                "session_id": session_id,
                "retention_tier": archive_request.retention_tier,
                "size_bytes": result.size_bytes,
                "archived_by": user.email,
            },
        },
    )
    
    await db.commit()
    
    logger.info(f"Archived session {session_id} → {result.storage_key} by {user.email}")
    
    return ArchiveCreateResponse(
        success=True,
        archive_id=str(result.archive_id),
        storage_key=result.storage_key,
        size_bytes=result.size_bytes,
        checksum=result.checksum,
        error=None,
    )


# =============================================================================
# Routes - Archive Listing
# =============================================================================

@router.get(
    "",
    response_model=ArchiveListResponse,
    summary="List archives",
    description="List archives with optional filtering. Requires CRT membership.",
)
async def list_archives(
    request: Request,
    user: UserContext = Depends(require_member),
    discord_user_id: Optional[int] = Query(None, description="Filter by Discord user ID"),
    severity: Optional[str] = Query(None, description="Filter by severity level"),
    retention_tier: Optional[str] = Query(None, description="Filter by retention tier"),
    skip: int = Query(0, ge=0, description="Records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Maximum records to return"),
    db: AsyncSession = Depends(get_db),
):
    """
    List archives with optional filtering.
    
    Authorization:
        - Requires CRT membership (any role)
    
    Supports filtering by:
    - Discord user ID
    - Severity level
    - Retention tier (standard/permanent)
    """
    archive_manager = await get_archive_manager(request)
    
    # Build filter
    filters = ArchiveListFilter(
        discord_user_id=discord_user_id,
        severity=severity,
        retention_tier=retention_tier,
    )
    
    # Get archives
    archives, total = await archive_manager.list_archives(
        filters=filters,
        skip=skip,
        limit=limit,
    )
    
    return ArchiveListResponse(
        archives=[ArchiveListItem(**a) for a in archives],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/statistics",
    response_model=ArchiveStatistics,
    summary="Get archive statistics",
    description="Get storage statistics for all archives. Requires CRT membership.",
)
async def get_statistics(
    request: Request,
    user: UserContext = Depends(require_member),
):
    """
    Get archive storage statistics.
    
    Authorization:
        - Requires CRT membership (any role)
    """
    archive_manager = await get_archive_manager(request)
    
    stats = await archive_manager.get_statistics()
    
    return ArchiveStatistics(**stats)


@router.get(
    "/expiring",
    response_model=List[ExpiringArchive],
    summary="Get expiring archives",
    description="Get archives expiring within N days. Requires CRT membership.",
)
async def get_expiring_archives(
    request: Request,
    user: UserContext = Depends(require_member),
    days: int = Query(30, ge=1, le=365, description="Days until expiration"),
):
    """
    Get archives that will expire within the specified number of days.
    
    Authorization:
        - Requires CRT membership (any role)
    """
    archive_manager = await get_archive_manager(request)
    
    expiring = await archive_manager.get_expiring_soon(days=days)
    
    return [ExpiringArchive(**e) for e in expiring]


# =============================================================================
# Routes - Single Archive
# =============================================================================

@router.get(
    "/{archive_id}",
    response_model=ArchiveMetadata,
    summary="Get archive metadata",
    description="Get metadata for a specific archive. Requires CRT membership.",
)
async def get_archive(
    archive_id: UUID,
    request: Request,
    user: UserContext = Depends(require_member),
):
    """
    Get archive metadata without decrypting content.
    
    Authorization:
        - Requires CRT membership (any role)
    """
    archive_manager = await get_archive_manager(request)
    
    metadata = await archive_manager.get_archive_metadata(archive_id)
    
    if not metadata:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Archive {archive_id} not found",
        )
    
    return ArchiveMetadata(**metadata)


@router.get(
    "/{archive_id}/download",
    response_model=ArchivePackageResponse,
    summary="Download and decrypt archive",
    description="Retrieve and decrypt the full archive package. Requires CRT membership.",
)
async def download_archive(
    archive_id: UUID,
    request: Request,
    user: UserContext = Depends(require_member),
    db: AsyncSession = Depends(get_db),
):
    """
    Download and decrypt an archive.
    
    Authorization:
        - Requires CRT membership (any role)
    
    Returns the full decrypted archive package including
    session data and all notes.
    """
    logging_manager = get_logging_manager(request)
    db_manager = get_db_manager(request)
    logger = logging_manager.get_logger("archives")
    
    archive_manager = await get_archive_manager(request)
    audit_repo = create_audit_log_repository(db_manager, logging_manager)
    
    # Retrieve and decrypt
    package = await archive_manager.retrieve_archive(archive_id)
    
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Archive {archive_id} not found or could not be decrypted",
        )
    
    # Create audit log entry for archive access with user tracking (Phase 10)
    await audit_repo.create(
        db,
        {
            "action": "archive.access",
            "user_id": get_user_id_for_audit(user),
            "entity_type": "archive",
            "entity_id": str(archive_id),
            "new_values": {
                "accessed_by": user.email,
            },
        },
    )
    await db.commit()
    
    logger.info(f"Archive {archive_id} downloaded by {user.email}")
    
    return ArchivePackageResponse(
        version=package.version,
        archived_at=package.archived_at,
        session=package.session,
        notes=package.notes,
        metadata=package.metadata,
    )


# =============================================================================
# Routes - Retention Management
# =============================================================================

@router.put(
    "/{archive_id}/retention",
    response_model=ArchiveMetadata,
    summary="Update retention tier",
    description="Change the retention tier for an archive. Requires Lead or Admin role.",
)
async def update_retention(
    archive_id: UUID,
    retention_request: RetentionUpdateRequest,
    request: Request,
    user: UserContext = Depends(require_lead),  # Phase 10: Lead+ only
    db: AsyncSession = Depends(get_db),
):
    """
    Update an archive's retention tier.
    
    Authorization (Phase 10):
        - Requires Lead or Admin role
    
    Tier options:
    - "standard": 1 year retention (auto-deleted after)
    - "permanent": ~7 years retention (requires manual deletion)
    """
    logging_manager = get_logging_manager(request)
    db_manager = get_db_manager(request)
    logger = logging_manager.get_logger("archives")
    
    archive_manager = await get_archive_manager(request)
    audit_repo = create_audit_log_repository(db_manager, logging_manager)
    
    # Validate tier
    if retention_request.retention_tier not in ("standard", "permanent"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="retention_tier must be 'standard' or 'permanent'",
        )
    
    # Get current metadata for old values
    old_metadata = await archive_manager.get_archive_metadata(archive_id)
    if not old_metadata:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Archive {archive_id} not found",
        )
    
    # Phase 10: Get user from auth
    updated_by_id = user.db_user_id
    updated_by_name = user.name or user.email
    
    # Update retention
    success = await archive_manager.update_retention_tier(
        archive_id=archive_id,
        new_tier=retention_request.retention_tier,
        updated_by_id=updated_by_id,
        updated_by_name=updated_by_name,
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update retention tier",
        )
    
    # Create audit log entry with user tracking (Phase 10)
    await audit_repo.create(
        db,
        {
            "action": "archive.retention_update",
            "user_id": get_user_id_for_audit(user),
            "entity_type": "archive",
            "entity_id": str(archive_id),
            "old_values": {
                "retention_tier": old_metadata["retention_tier"],
            },
            "new_values": {
                "retention_tier": retention_request.retention_tier,
                "updated_by": user.email,
                "updated_by_role": user.role.value if user.role else None,
            },
        },
    )
    await db.commit()
    
    logger.info(
        f"Updated archive {archive_id} retention: "
        f"{old_metadata['retention_tier']} → {retention_request.retention_tier} "
        f"by {user.email} (role: {user.role.value})"
    )
    
    # Return updated metadata
    new_metadata = await archive_manager.get_archive_metadata(archive_id)
    return ArchiveMetadata(**new_metadata)


@router.post(
    "/{archive_id}/extend",
    response_model=ArchiveMetadata,
    summary="Extend retention",
    description="Extend an archive's retention by a number of days. Requires Lead or Admin role.",
)
async def extend_retention(
    archive_id: UUID,
    extend_request: RetentionExtendRequest,
    request: Request,
    user: UserContext = Depends(require_lead),  # Phase 10: Lead+ only
    db: AsyncSession = Depends(get_db),
):
    """
    Extend an archive's retention period.
    
    Authorization (Phase 10):
        - Requires Lead or Admin role
    
    Adds the specified number of days to the current retention date.
    """
    logging_manager = get_logging_manager(request)
    db_manager = get_db_manager(request)
    logger = logging_manager.get_logger("archives")
    
    archive_manager = await get_archive_manager(request)
    audit_repo = create_audit_log_repository(db_manager, logging_manager)
    
    # Check archive exists
    old_metadata = await archive_manager.get_archive_metadata(archive_id)
    if not old_metadata:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Archive {archive_id} not found",
        )
    
    # Phase 10: Get user from auth
    extended_by_name = user.name or user.email
    
    # Extend retention
    success = await archive_manager.extend_retention(
        archive_id=archive_id,
        days=extend_request.days,
        extended_by_name=extended_by_name,
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to extend retention",
        )
    
    # Create audit log entry with user tracking (Phase 10)
    await audit_repo.create(
        db,
        {
            "action": "archive.retention_extend",
            "user_id": get_user_id_for_audit(user),
            "entity_type": "archive",
            "entity_id": str(archive_id),
            "old_values": {
                "retention_until": old_metadata.get("retention_until"),
            },
            "new_values": {
                "days_extended": extend_request.days,
                "extended_by": user.email,
            },
        },
    )
    await db.commit()
    
    logger.info(f"Extended archive {archive_id} retention by {extend_request.days} days by {user.email}")
    
    # Return updated metadata
    new_metadata = await archive_manager.get_archive_metadata(archive_id)
    return ArchiveMetadata(**new_metadata)


# =============================================================================
# Routes - Archive Deletion
# =============================================================================

@router.delete(
    "/{archive_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete archive",
    description="Delete an archive. Requires Admin role.",
)
async def delete_archive(
    archive_id: UUID,
    request: Request,
    user: UserContext = Depends(require_admin),  # Phase 10: Admin only
    db: AsyncSession = Depends(get_db),
):
    """
    Delete an archive.
    
    Authorization (Phase 10):
        - Requires Admin role only
    
    This permanently deletes both the encrypted blob from MinIO
    and the metadata from PostgreSQL.
    """
    logging_manager = get_logging_manager(request)
    db_manager = get_db_manager(request)
    logger = logging_manager.get_logger("archives")
    
    archive_manager = await get_archive_manager(request)
    archive_repo = create_archive_repository(db_manager, logging_manager)
    audit_repo = create_audit_log_repository(db_manager, logging_manager)
    
    # Get archive metadata first
    metadata = await archive_manager.get_archive_metadata(archive_id)
    if not metadata:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Archive {archive_id} not found",
        )
    
    # Delete from MinIO
    from src.managers.archive import create_minio_manager
    
    config_manager = get_config_manager(request)
    secrets_manager = get_secrets_manager(request)
    
    minio_manager = await create_minio_manager(
        config_manager=config_manager,
        secrets_manager=secrets_manager,
        logging_manager=logging_manager,
    )
    
    try:
        await minio_manager.delete_archive(metadata["storage_key"])
    except Exception as e:
        logger.error(f"Failed to delete archive from MinIO: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete archive from storage: {e}",
        )
    
    # Delete from database
    deleted = await archive_repo.delete(db, archive_id)
    if not deleted:
        logger.error(f"Failed to delete archive metadata for {archive_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete archive metadata",
        )
    
    # Create audit log entry with user tracking (Phase 10)
    await audit_repo.create(
        db,
        {
            "action": "archive.delete",
            "user_id": get_user_id_for_audit(user),
            "entity_type": "archive",
            "entity_id": str(archive_id),
            "old_values": {
                "session_id": metadata["session_id"],
                "retention_tier": metadata.get("retention_tier"),
                "size_bytes": metadata.get("size_bytes"),
            },
            "new_values": {
                "deleted_by": user.email,
                "deleted_by_role": user.role.value if user.role else None,
            },
        },
    )
    await db.commit()
    
    logger.info(f"Deleted archive {archive_id} by admin {user.email}")
    
    return None


# =============================================================================
# Routes - Session Archive Check
# =============================================================================

@router.get(
    "/session/{session_id}/check",
    summary="Check if session is archived",
    description="Check if a session has been archived. Requires CRT membership.",
)
async def check_session_archived(
    session_id: str,
    request: Request,
    user: UserContext = Depends(require_member),
):
    """
    Check if a session has been archived.
    
    Authorization:
        - Requires CRT membership (any role)
    """
    archive_manager = await get_archive_manager(request)
    
    is_archived = await archive_manager.session_has_archive(session_id)
    archive_info = None
    
    if is_archived:
        archive_info = await archive_manager.get_archives_for_session(session_id)
    
    return {
        "session_id": session_id,
        "is_archived": is_archived,
        "archive": archive_info,
    }


__all__ = ["router"]
