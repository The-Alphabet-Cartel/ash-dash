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
Utilities Package - Shared utility functions and helpers
----------------------------------------------------------------------------
FILE VERSION: v5.0-9-9.2-1
LAST MODIFIED: 2026-01-09
PHASE: Phase 9 - Archive System Implementation
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

AVAILABLE UTILITIES:
- encryption.py: AES-256-GCM encryption/decryption for archives (Phase 9)

PLANNED UTILITIES:
- validators.py: Common validation functions
- formatters.py: Data formatting helpers
"""

__version__ = "v5.0-9-9.2-1"

# =============================================================================
# Encryption Utilities (Phase 9)
# =============================================================================

from .encryption import (
    # Classes
    ArchiveEncryption,
    # Factory functions
    create_archive_encryption,
    create_archive_encryption_from_key,
    # Exceptions
    EncryptionError,
    DecryptionError,
    InvalidKeyError,
    # Constants
    SALT_LENGTH,
    IV_LENGTH,
    KEY_LENGTH,
    PBKDF2_ITERATIONS,
)

# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    # Encryption
    "ArchiveEncryption",
    "create_archive_encryption",
    "create_archive_encryption_from_key",
    "EncryptionError",
    "DecryptionError",
    "InvalidKeyError",
    "SALT_LENGTH",
    "IV_LENGTH",
    "KEY_LENGTH",
    "PBKDF2_ITERATIONS",
]
