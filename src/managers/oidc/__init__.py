"""
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================

OIDC Manager Package - PocketID OpenID Connect Integration
----------------------------------------------------------------------------
FILE VERSION: v5.0-10-10.4-1
LAST MODIFIED: 2026-01-10
PHASE: Phase 10 - Authentication & Authorization
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
"""

from src.managers.oidc.oidc_config_manager import (
    OIDCConfigManager,
    create_oidc_config_manager,
    OIDCDiscoveryError,
    OIDCConfigError,
)

__all__ = [
    "OIDCConfigManager",
    "create_oidc_config_manager",
    "OIDCDiscoveryError",
    "OIDCConfigError",
]
