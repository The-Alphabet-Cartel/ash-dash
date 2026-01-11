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
Enumerations - Role definitions and Pocket-ID group mapping
----------------------------------------------------------------------------
FILE VERSION: v5.0-10-10.1.1-1
LAST MODIFIED: 2026-01-10
PHASE: Phase 10 - Authentication & Authorization
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

This module defines the role-based access control (RBAC) system for Ash-Dash.
Roles are mapped from Pocket-ID groups to provide three-tier authorization:

    Member → Base CRT access (view, create notes, close sessions)
    Lead   → Member + reopen sessions, unlock notes, manage retention
    Admin  → Lead + delete notes/archives, execute cleanup, system health

USAGE:
    from src.models.enums import UserRole, get_role_from_groups
    
    # Get role from Pocket-ID groups
    groups = ["cartel_crt", "cartel_crt_lead"]
    role = get_role_from_groups(groups)  # Returns UserRole.LEAD
    
    # Check role hierarchy
    from src.models.enums import ROLE_HIERARCHY
    if ROLE_HIERARCHY.index(user_role) >= ROLE_HIERARCHY.index(UserRole.LEAD):
        # User has Lead or higher permissions
        pass
"""

from enum import Enum
from typing import List, Optional

__version__ = "v5.0-10-10.1.1-1"


# =============================================================================
# Role Enumeration
# =============================================================================

class UserRole(str, Enum):
    """
    CRT user roles mapped from Pocket-ID groups.
    
    The role hierarchy from lowest to highest permissions:
        MEMBER < LEAD < ADMIN
    
    Each role inherits all permissions from lower roles.
    """
    
    MEMBER = "member"
    LEAD = "lead"
    ADMIN = "admin"
    
    def __str__(self) -> str:
        """Return the role value for string representation."""
        return self.value
    
    @property
    def display_name(self) -> str:
        """Human-readable role name."""
        names = {
            "member": "CRT Member",
            "lead": "CRT Lead",
            "admin": "CRT Admin",
        }
        return names.get(self.value, self.value.title())


# =============================================================================
# Pocket-ID Group Mapping
# =============================================================================

# Map Pocket-ID group names to UserRole
# These must match the exact group names configured in Pocket-ID
POCKET_ID_GROUP_MAP: dict[str, UserRole] = {
    "cartel_crt_admin": UserRole.ADMIN,
    "cartel_crt_lead": UserRole.LEAD,
    "cartel_crt": UserRole.MEMBER,
}

# Role hierarchy - higher index = more permissions
# Used for permission comparisons
ROLE_HIERARCHY: List[UserRole] = [
    UserRole.MEMBER,
    UserRole.LEAD,
    UserRole.ADMIN,
]


# =============================================================================
# Role Resolution Functions
# =============================================================================

def get_role_from_groups(groups: List[str]) -> Optional[UserRole]:
    """
    Determine the highest role from a list of Pocket-ID groups.
    
    When a user belongs to multiple CRT groups, they receive the
    highest role among their memberships (e.g., if in both
    cartel_crt and cartel_crt_lead, they get LEAD).
    
    Args:
        groups: List of Pocket-ID group names from JWT claims
        
    Returns:
        UserRole if user has any CRT group membership, None otherwise
        
    Examples:
        >>> get_role_from_groups(["cartel_crt"])
        UserRole.MEMBER
        
        >>> get_role_from_groups(["cartel_crt", "cartel_crt_admin"])
        UserRole.ADMIN
        
        >>> get_role_from_groups(["some_other_group"])
        None
    """
    if not groups:
        return None
    
    # Find all matching roles
    user_roles: List[UserRole] = []
    for group in groups:
        if group in POCKET_ID_GROUP_MAP:
            user_roles.append(POCKET_ID_GROUP_MAP[group])
    
    if not user_roles:
        return None
    
    # Return highest role based on hierarchy
    return max(user_roles, key=lambda r: ROLE_HIERARCHY.index(r))


def role_meets_requirement(user_role: Optional[UserRole], required_role: UserRole) -> bool:
    """
    Check if a user's role meets or exceeds the required role.
    
    Args:
        user_role: The user's current role (None if not a CRT member)
        required_role: The minimum required role for access
        
    Returns:
        True if user_role >= required_role in hierarchy, False otherwise
        
    Examples:
        >>> role_meets_requirement(UserRole.ADMIN, UserRole.MEMBER)
        True
        
        >>> role_meets_requirement(UserRole.MEMBER, UserRole.LEAD)
        False
        
        >>> role_meets_requirement(None, UserRole.MEMBER)
        False
    """
    if user_role is None:
        return False
    
    user_index = ROLE_HIERARCHY.index(user_role)
    required_index = ROLE_HIERARCHY.index(required_role)
    
    return user_index >= required_index


def get_role_permissions(role: UserRole) -> dict[str, bool]:
    """
    Get a dictionary of permissions for a given role.
    
    Useful for debugging and documentation purposes.
    
    Args:
        role: The role to check permissions for
        
    Returns:
        Dictionary of permission name -> boolean
    """
    is_member = role_meets_requirement(role, UserRole.MEMBER)
    is_lead = role_meets_requirement(role, UserRole.LEAD)
    is_admin = role_meets_requirement(role, UserRole.ADMIN)
    
    return {
        # Dashboard
        "view_dashboard": is_member,
        
        # Sessions
        "view_sessions": is_member,
        "close_session": is_member,
        "reopen_session": is_lead,
        
        # Notes
        "create_note": is_member,
        "edit_own_note": is_member,
        "edit_any_note": is_admin,
        "unlock_note": is_lead,
        "delete_note": is_admin,
        
        # Archives
        "view_archives": is_member,
        "create_archive": is_member,
        "download_archive": is_member,
        "change_retention": is_lead,
        "delete_archive": is_admin,
        "execute_cleanup": is_admin,
        
        # Admin
        "view_crt_roster": is_lead,
        "view_audit_logs": is_lead,
        "view_system_health": is_admin,
    }


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "UserRole",
    "POCKET_ID_GROUP_MAP",
    "ROLE_HIERARCHY",
    "get_role_from_groups",
    "role_meets_requirement",
    "get_role_permissions",
]
