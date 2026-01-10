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
Admin API Routes - Administrative operations with authorization
----------------------------------------------------------------------------
FILE VERSION: v5.0-10-10.2.9-1
LAST MODIFIED: 2026-01-10
PHASE: Phase 10 - Authentication & Authorization
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

ENDPOINTS:
    GET  /api/admin/archives/cleanup/status   - Get cleanup status (Lead+)
    POST /api/admin/archives/cleanup/execute  - Execute archive cleanup (Admin)
    GET  /api/admin/archives/expiring         - Get archives expiring soon (Lead+)

AUTHORIZATION (Phase 10):
    - Cleanup status and expiring list: Requires Lead or Admin role
    - Cleanup execution: Requires Admin role only
    - All audit logs include user_id for tracking
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.managers.database import DatabaseManager
from src.repositories.archive_repository import create_archive_repository
from src.repositories.audit_log_repository import create_audit_log_repository

# Phase 10: Import auth dependencies
from src.api.dependencies.auth import (
    require_lead,
    require_admin,
)
from src.api.middleware.auth_middleware import UserContext


__version__ = "v5.0-10-10.2.9-1"


# =============================================================================
# Router Setup
# =============================================================================

router = APIRouter(
    prefix="/api/admin",
    tags=["admin"],
)


# =============================================================================
# Response Models
# =============================================================================

class CleanupStatusResponse(BaseModel):
    """Response model for cleanup status."""
    total_archives: int
    standard_tier_count: int
    permanent_tier_count: int
    expired_count: int
    expiring_soon_count: int  # Next 30 days
    total_size_bytes: int
    total_size_mb: float
    last_cleanup_at: Optional[datetime] = None
    last_cleanup_deleted: Optional[int] = None


class CleanupExecuteResponse(BaseModel):
    """Response model for cleanup execution."""
    success: bool
    deleted_count: int
    executed_at: datetime
    dry_run: bool
    message: str


class ExpiringArchiveResponse(BaseModel):
    """Response model for expiring archive."""
    id: str
    session_id: str
    discord_user_id: Optional[int]
    discord_user_name: Optional[str]
    severity: Optional[str]
    archived_at: datetime
    retention_until: Optional[datetime]
    days_remaining: Optional[int]
    size_bytes: int


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


async def get_archive_manager(request: Request):
    """Get or create archive manager."""
    # Check if already cached
    if hasattr(request.app.state, "archive_manager") and request.app.state.archive_manager:
        return request.app.state.archive_manager
    
    # Create on demand
    from src.managers.archive import create_minio_manager, create_archive_manager
    
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
    
    archive_repo = create_archive_repository(db_manager, logging_manager)
    
    archive_manager = await create_archive_manager(
        config_manager=config_manager,
        secrets_manager=secrets_manager,
        minio_manager=minio_manager,
        database_manager=db_manager,
        archive_repository=archive_repo,
        logging_manager=logging_manager,
    )
    
    request.app.state.archive_manager = archive_manager
    return archive_manager


# =============================================================================
# Routes - Archive Cleanup
# =============================================================================

@router.get(
    "/archives/cleanup/status",
    response_model=CleanupStatusResponse,
    summary="Get cleanup status",
    description="Get archive cleanup status and statistics. Requires Lead or Admin role.",
)
async def get_cleanup_status(
    request: Request,
    user: UserContext = Depends(require_lead),  # Phase 10: Lead+ only
    db: AsyncSession = Depends(get_db),
):
    """
    Get current archive cleanup status.
    
    Authorization (Phase 10):
        - Requires Lead or Admin role
    
    Returns:
        - Total archive counts by tier
        - Number of expired archives
        - Archives expiring soon
        - Last cleanup information (from audit log)
    """
    logging_manager = get_logging_manager(request)
    db_manager = get_db_manager(request)
    
    archive_repo = create_archive_repository(db_manager, logging_manager)
    audit_repo = create_audit_log_repository(db_manager, logging_manager)
    
    # Get statistics
    stats = await archive_repo.get_storage_statistics(db)
    
    # Get expired count
    expired = await archive_repo.get_expired_standard_tier(db, limit=1000)
    expired_count = len(list(expired))
    
    # Get expiring soon count (30 days)
    expiring = await archive_repo.get_expiring_soon(db, days=30)
    expiring_count = len(list(expiring))
    
    # Get last cleanup from audit log
    last_cleanup = await audit_repo.get_latest_by_action(db, "archive.cleanup")
    last_cleanup_at = None
    last_cleanup_deleted = None
    
    if last_cleanup:
        last_cleanup_at = last_cleanup.created_at
        if last_cleanup.new_values:
            last_cleanup_deleted = last_cleanup.new_values.get("deleted_count")
    
    # Calculate tier counts
    by_tier = stats.get("by_retention_tier", {})
    standard_count = by_tier.get("standard", {}).get("count", 0)
    permanent_count = by_tier.get("permanent", {}).get("count", 0)
    
    return CleanupStatusResponse(
        total_archives=stats.get("total_archives", 0),
        standard_tier_count=standard_count,
        permanent_tier_count=permanent_count,
        expired_count=expired_count,
        expiring_soon_count=expiring_count,
        total_size_bytes=stats.get("total_size_bytes", 0),
        total_size_mb=stats.get("total_size_mb", 0),
        last_cleanup_at=last_cleanup_at,
        last_cleanup_deleted=last_cleanup_deleted,
    )


@router.post(
    "/archives/cleanup/execute",
    response_model=CleanupExecuteResponse,
    summary="Execute archive cleanup",
    description="Delete expired standard-tier archives. Requires Admin role.",
)
async def execute_cleanup(
    request: Request,
    user: UserContext = Depends(require_admin),  # Phase 10: Admin only
    dry_run: bool = Query(True, description="If true, only report what would be deleted"),
    db: AsyncSession = Depends(get_db),
):
    """
    Execute archive cleanup.
    
    Authorization (Phase 10):
        - Requires Admin role only
    
    By default, runs in dry-run mode (no deletion).
    Set dry_run=false to actually delete expired archives.
    
    Note: Only standard-tier archives past their retention date are deleted.
    Permanent archives are never auto-deleted.
    """
    logging_manager = get_logging_manager(request)
    db_manager = get_db_manager(request)
    logger = logging_manager.get_logger("admin")
    
    archive_manager = await get_archive_manager(request)
    archive_repo = create_archive_repository(db_manager, logging_manager)
    audit_repo = create_audit_log_repository(db_manager, logging_manager)
    
    executed_at = datetime.now(timezone.utc)
    
    if dry_run:
        # Dry run - just count
        expired = await archive_repo.get_expired_standard_tier(db, limit=1000)
        expired_count = len(list(expired))
        
        logger.info(f"Cleanup dry run by admin {user.email}: {expired_count} archives would be deleted")
        
        return CleanupExecuteResponse(
            success=True,
            deleted_count=expired_count,
            executed_at=executed_at,
            dry_run=True,
            message=f"Dry run: {expired_count} archives would be deleted",
        )
    
    # Execute actual cleanup
    logger.info(f"🗑️ Admin {user.email} initiated archive cleanup")
    
    deleted_count = await archive_manager.delete_expired_archives()
    
    # Create audit log entry with user tracking (Phase 10)
    await audit_repo.create(
        db,
        {
            "action": "archive.cleanup",
            "user_id": get_user_id_for_audit(user),
            "entity_type": "system",
            "entity_id": "cleanup",
            "new_values": {
                "deleted_count": deleted_count,
                "executed_at": executed_at.isoformat(),
                "executed_by": user.email,
                "executed_by_role": user.role.value if user.role else None,
            },
        },
    )
    await db.commit()
    
    logger.info(f"✅ Archive cleanup complete by {user.email}: {deleted_count} archives deleted")
    
    return CleanupExecuteResponse(
        success=True,
        deleted_count=deleted_count,
        executed_at=executed_at,
        dry_run=False,
        message=f"Cleanup complete: {deleted_count} archives deleted",
    )


@router.get(
    "/archives/expiring",
    response_model=List[ExpiringArchiveResponse],
    summary="Get expiring archives",
    description="Get list of archives expiring within N days. Requires Lead or Admin role.",
)
async def get_expiring_archives(
    request: Request,
    user: UserContext = Depends(require_lead),  # Phase 10: Lead+ only
    days: int = Query(30, ge=1, le=365, description="Days until expiration"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get archives that will expire within the specified number of days.
    
    Authorization (Phase 10):
        - Requires Lead or Admin role
    
    Useful for:
    - Review before cleanup
    - Identifying archives that may need retention extension
    - Planning permanent tier upgrades
    """
    logging_manager = get_logging_manager(request)
    db_manager = get_db_manager(request)
    
    archive_repo = create_archive_repository(db_manager, logging_manager)
    
    expiring = await archive_repo.get_expiring_soon(db, days=days)
    
    return [
        ExpiringArchiveResponse(
            id=str(archive.id),
            session_id=archive.session_id,
            discord_user_id=archive.discord_user_id,
            discord_user_name=archive.discord_user_name,
            severity=archive.severity,
            archived_at=archive.archived_at,
            retention_until=archive.retention_until,
            days_remaining=archive.days_until_expiry,
            size_bytes=archive.size_bytes,
        )
        for archive in expiring
    ]


__all__ = ["router"]
