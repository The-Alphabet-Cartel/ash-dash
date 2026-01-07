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
Managers Package - Core service managers for Ash-Dash
----------------------------------------------------------------------------
FILE VERSION: v5.0-1-1.2-1
LAST MODIFIED: 2026-01-06
PHASE: Phase 1 - Foundation & Infrastructure
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
"""

# Configuration Management
from src.managers.config_manager import (
    ConfigManager,
    create_config_manager,
)

# Secrets Management
from src.managers.secrets_manager import (
    SecretsManager,
    create_secrets_manager,
    get_secrets_manager,
    get_secret,
    SecretNotFoundError,
)

# Logging Management
from src.managers.logging_config_manager import (
    LoggingConfigManager,
    create_logging_config_manager,
    ColorizedFormatter,
    JSONFormatter,
    Colors,
)

__all__ = [
    # Config Manager
    "ConfigManager",
    "create_config_manager",
    # Secrets Manager
    "SecretsManager",
    "create_secrets_manager",
    "get_secrets_manager",
    "get_secret",
    "SecretNotFoundError",
    # Logging Config Manager
    "LoggingConfigManager",
    "create_logging_config_manager",
    "ColorizedFormatter",
    "JSONFormatter",
    "Colors",
]
