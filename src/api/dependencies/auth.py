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
Authentication Dependencies - FastAPI dependencies for role-based access
----------------------------------------------------------------------------
FILE VERSION: v5.0-10-10.1.4-1
LAST MODIFIED: 2026-01-10
PHASE: Phase 10 - Authentication & Authorization
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

This module provides FastAPI dependencies for authentication and authorization.
Use these dependencies in route handlers to enforce role-based access control.

USAGE:
    from src.api.dependencies.auth import require_member, require_lead, require_admin
    
    # Require any CRT member
    @router.get("/sessions")
    async def list_sessions(user: UserContext = Depends(require_member)):
        return {"user": user.email}
    
    # Require Lead or Admin
    @router.post("/sessions/{id}/reopen")
    async def reopen_session(user: UserContext = Depends(require_lead)):
        return {"reopened_by": user.email}
    
    # Require Admin only
    @router.delete("/archives/{id}")
    async def delete_archive(user: UserContext = Depends(require_admin)):
        return {"deleted_by": user.email}
    
    # Custom role requirement
    @router.put("/custom")
    async def custom_route(user: UserContext = Depends(require_role(UserRole.LEAD))):
        return {"user": user.email}
"""

from typing import Optional

from fastapi import Depends, HTTPException, Request, status

from src.api.middleware.auth_middleware import UserContext
from src.models.enums import UserRole, ROLE_HIERARCHY

__version__ = "v5.0-10-10.1.4-1"


# =============================================================================
# Core Authentication Dependency
# =============================================================================

async def get_current_user(request: Request) -> UserContext:
    """
    Get the authenticated user from request state.
    
    This is the base dependency that all other auth dependencies build upon.
    It checks that the user is authenticated and is a CRT member.
    
    Args:
        request: FastAPI request object
        
    Returns:
        UserContext for the authenticated user
        
    Raises:
        HTTPException 401: If user is not authenticated
        HTTPException 403: If user is not a CRT member
    """
    user: Optional[UserContext] = getattr(request.state, "user", None)
    
    # Check if user exists in request state
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is authenticated (not anonymous)
    if user.user_id == "anonymous":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is a CRT member
    if not user.is_crt_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: CRT membership required",
        )
    
    return user


# =============================================================================
# Role-Based Dependencies
# =============================================================================

async def require_member(
    user: UserContext = Depends(get_current_user),
) -> UserContext:
    """
    Require at least Member role (any CRT member).
    
    This is equivalent to get_current_user but with a more explicit name
    for use in route definitions where role requirements should be clear.
    
    Permissions granted to Members:
        - View dashboard and metrics
        - View sessions and session details
        - Create and edit own notes
        - Close sessions
        - Archive sessions
        - Download archives
        - View documentation
        
    Args:
        user: Authenticated user from get_current_user
        
    Returns:
        UserContext for the authenticated member
    """
    # get_current_user already ensures CRT membership
    return user


async def require_lead(
    user: UserContext = Depends(get_current_user),
) -> UserContext:
    """
    Require at least Lead role (Lead or Admin).
    
    Permissions granted to Leads (in addition to Member):
        - Reopen closed sessions
        - Unlock locked notes
        - Change archive retention tier
        - View CRT roster
        - View audit logs
        
    Args:
        user: Authenticated user from get_current_user
        
    Returns:
        UserContext for the authenticated Lead/Admin
        
    Raises:
        HTTPException 403: If user is not Lead or Admin
    """
    if not user.is_lead:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: CRT Lead or Admin required",
        )
    return user


async def require_admin(
    user: UserContext = Depends(get_current_user),
) -> UserContext:
    """
    Require Admin role.
    
    Permissions granted to Admins (in addition to Lead):
        - Edit any note (not just their own)
        - Delete notes
        - Delete archives
        - Execute cleanup jobs
        - View system health
        
    Args:
        user: Authenticated user from get_current_user
        
    Returns:
        UserContext for the authenticated Admin
        
    Raises:
        HTTPException 403: If user is not Admin
    """
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: CRT Admin required",
        )
    return user


def require_role(required_role: UserRole):
    """
    Factory function for custom role-based dependencies.
    
    Use this when you need a role check that isn't covered by the
    standard require_member/require_lead/require_admin dependencies.
    
    Args:
        required_role: The minimum role required for access
        
    Returns:
        An async dependency function that checks the role
        
    Usage:
        @router.get("/custom")
        async def custom_route(user: UserContext = Depends(require_role(UserRole.LEAD))):
            return {"user": user.email}
    """
    async def role_checker(
        user: UserContext = Depends(get_current_user),
    ) -> UserContext:
        if not user.has_permission(required_role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: {required_role.display_name} or higher required",
            )
        return user
    
    return role_checker


# =============================================================================
# Optional Authentication Dependency
# =============================================================================

async def get_optional_user(request: Request) -> Optional[UserContext]:
    """
    Get the user if authenticated, None otherwise.
    
    Use this for endpoints that have different behavior for authenticated
    vs unauthenticated users, but don't require authentication.
    
    Note: This will still return None for authenticated users who are
    not CRT members.
    
    Args:
        request: FastAPI request object
        
    Returns:
        UserContext if authenticated CRT member, None otherwise
        
    Usage:
        @router.get("/public")
        async def public_route(user: Optional[UserContext] = Depends(get_optional_user)):
            if user:
                return {"message": f"Hello, {user.name}!"}
            return {"message": "Hello, guest!"}
    """
    user: Optional[UserContext] = getattr(request.state, "user", None)
    
    # Return None if no user or anonymous
    if user is None or user.user_id == "anonymous":
        return None
    
    # Return None if not a CRT member
    if not user.is_crt_member:
        return None
    
    return user


# =============================================================================
# Database User ID Helper
# =============================================================================

async def get_user_db_id(
    user: UserContext = Depends(get_current_user),
) -> Optional[str]:
    """
    Get the database user ID as a string.
    
    Convenience dependency for routes that need to record user_id
    in audit logs or other database operations.
    
    Args:
        user: Authenticated user from get_current_user
        
    Returns:
        String representation of db_user_id, or None if not synced yet
    """
    if user.db_user_id:
        return str(user.db_user_id)
    return None


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "get_current_user",
    "get_optional_user",
    "get_user_db_id",
    "require_member",
    "require_lead",
    "require_admin",
    "require_role",
]
