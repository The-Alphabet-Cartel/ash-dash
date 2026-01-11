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
Source Package - Main application source code
----------------------------------------------------------------------------
FILE VERSION: v5.0-1-1.1-1
LAST MODIFIED: 2026-01-06
PHASE: Phase 1 - Foundation & Infrastructure
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

PACKAGE STRUCTURE:
- api/: FastAPI routes and middleware
- config/: JSON configuration files
- managers/: Service managers (config, secrets, logging, etc.)
- models/: SQLAlchemy and Pydantic models
- utils/: Shared utility functions

USAGE:
    from src.managers import create_config_manager, create_logging_config_manager
    from src.api.middleware import AuthMiddleware
"""

__version__ = "v5.0-1-1.1-1"
__author__ = "The Alphabet Cartel"
__email__ = "dev@alphabetcartel.org"
__url__ = "https://github.com/the-alphabet-cartel/ash-dash"

# Package metadata
__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "__url__",
]
