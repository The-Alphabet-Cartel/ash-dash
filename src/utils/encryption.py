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
Encryption Utilities - AES-256-GCM for Archive Protection
----------------------------------------------------------------------------
FILE VERSION: v5.0-9-9.2-1
LAST MODIFIED: 2026-01-09
PHASE: Phase 9 - Archive System Implementation
CLEAN ARCHITECTURE: Compliant (Rule #1 Factory, Rule #2 DI)
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

RESPONSIBILITIES:
- AES-256-GCM encryption/decryption for session archives
- PBKDF2 key derivation with unique salt per archive
- Secure random generation for salt and IV
- Integrity verification via GCM authentication tag

ENCRYPTION FORMAT:
    [Salt: 16 bytes][IV: 12 bytes][Ciphertext + Auth Tag]
    
    - Salt: Random bytes for PBKDF2 key derivation
    - IV: Initialization vector for AES-GCM (nonce)
    - Ciphertext: Encrypted data with 16-byte auth tag appended

SECURITY NOTES:
- Each archive gets a unique derived key (master_key + random salt)
- PBKDF2 with 100,000 iterations provides key stretching
- AES-GCM provides both confidentiality and authenticity
- 12-byte IV is the recommended size for GCM mode

USAGE:
    from src.utils.encryption import create_archive_encryption
    from src.managers import create_secrets_manager
    
    secrets = create_secrets_manager()
    encryption = create_archive_encryption(secrets)
    
    # Encrypt session data
    plaintext = json.dumps(session_data).encode('utf-8')
    encrypted = encryption.encrypt(plaintext)
    
    # Decrypt
    decrypted = encryption.decrypt(encrypted)
    session_data = json.loads(decrypted.decode('utf-8'))
"""

import logging
import os
from typing import Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Module version
__version__ = "v5.0-9-9.2-1"

# Initialize logger
logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

# Salt length for PBKDF2 key derivation (16 bytes = 128 bits)
SALT_LENGTH = 16

# Initialization vector length for AES-GCM (12 bytes = 96 bits, recommended)
IV_LENGTH = 12

# Key length for AES-256 (32 bytes = 256 bits)
KEY_LENGTH = 32

# PBKDF2 iterations (OWASP recommends 100,000+ for SHA-256)
PBKDF2_ITERATIONS = 100_000

# Minimum size of encrypted blob: salt + iv + auth_tag (no ciphertext)
MIN_ENCRYPTED_SIZE = SALT_LENGTH + IV_LENGTH + 16  # 16-byte auth tag


# =============================================================================
# Exceptions
# =============================================================================


class EncryptionError(Exception):
    """Base exception for encryption operations."""
    pass


class DecryptionError(EncryptionError):
    """Raised when decryption fails (wrong key, corrupted data, or tampering)."""
    pass


class InvalidKeyError(EncryptionError):
    """Raised when the encryption key is invalid."""
    pass


# =============================================================================
# Archive Encryption Class
# =============================================================================


class ArchiveEncryption:
    """
    Handles AES-256-GCM encryption for session archives.
    
    Uses PBKDF2 key derivation with unique salt per archive,
    ensuring each archive has a unique encryption key even
    with the same master key.
    
    Attributes:
        _master_key: The master encryption key (32+ bytes)
        
    Example:
        >>> encryption = ArchiveEncryption(master_key)
        >>> encrypted = encryption.encrypt(b"sensitive data")
        >>> decrypted = encryption.decrypt(encrypted)
        >>> assert decrypted == b"sensitive data"
    """
    
    def __init__(self, master_key: bytes):
        """
        Initialize with master encryption key.
        
        Args:
            master_key: Master key from Docker secret (must be 32+ bytes)
            
        Raises:
            InvalidKeyError: If master_key is too short
        """
        if not master_key:
            raise InvalidKeyError("Master key cannot be empty")
        
        if len(master_key) < KEY_LENGTH:
            raise InvalidKeyError(
                f"Master key must be at least {KEY_LENGTH} bytes, "
                f"got {len(master_key)} bytes. "
                f"Regenerate with: openssl rand 32 > secrets/archive_master_key"
            )
        
        self._master_key = master_key
        logger.debug(f"ArchiveEncryption initialized with {len(master_key)}-byte key")
    
    def _derive_key(self, salt: bytes) -> bytes:
        """
        Derive encryption key from master key and salt using PBKDF2.
        
        This ensures each archive has a unique encryption key,
        even when encrypted with the same master key.
        
        Args:
            salt: Random salt for this specific archive (16 bytes)
            
        Returns:
            Derived 256-bit (32-byte) key
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=KEY_LENGTH,
            salt=salt,
            iterations=PBKDF2_ITERATIONS,
            backend=default_backend(),
        )
        return kdf.derive(self._master_key)
    
    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Encrypt data with AES-256-GCM.
        
        Generates a unique salt and IV for each encryption operation,
        ensuring that encrypting the same data twice produces
        different ciphertext.
        
        Args:
            plaintext: Data to encrypt (any bytes)
            
        Returns:
            Encrypted blob in format: [salt][iv][ciphertext + auth_tag]
            
        Raises:
            EncryptionError: If encryption fails
            
        Example:
            >>> encrypted = encryption.encrypt(b"session data")
            >>> len(encrypted) > len(b"session data")  # Has overhead
            True
        """
        if plaintext is None:
            raise EncryptionError("Cannot encrypt None")
        
        try:
            # Generate cryptographically secure random salt and IV
            salt = os.urandom(SALT_LENGTH)
            iv = os.urandom(IV_LENGTH)
            
            # Derive unique key for this archive
            derived_key = self._derive_key(salt)
            
            # Encrypt with AES-256-GCM
            aesgcm = AESGCM(derived_key)
            
            # GCM mode appends a 16-byte authentication tag to ciphertext
            ciphertext_with_tag = aesgcm.encrypt(iv, plaintext, None)
            
            # Pack: salt + iv + ciphertext (includes auth tag)
            encrypted_blob = salt + iv + ciphertext_with_tag
            
            logger.debug(
                f"Encrypted {len(plaintext):,} bytes → "
                f"{len(encrypted_blob):,} bytes "
                f"(+{len(encrypted_blob) - len(plaintext)} overhead)"
            )
            
            return encrypted_blob
            
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise EncryptionError(f"Encryption failed: {e}") from e
    
    def decrypt(self, encrypted_blob: bytes) -> bytes:
        """
        Decrypt data encrypted with encrypt().
        
        Extracts salt and IV from the blob, derives the key,
        and decrypts with authentication verification.
        
        Args:
            encrypted_blob: Data from encrypt() method
            
        Returns:
            Original plaintext bytes
            
        Raises:
            DecryptionError: If decryption fails due to:
                - Wrong master key
                - Corrupted data
                - Tampered ciphertext (auth tag mismatch)
                - Invalid blob format
                
        Example:
            >>> encrypted = encryption.encrypt(b"secret")
            >>> decrypted = encryption.decrypt(encrypted)
            >>> decrypted == b"secret"
            True
        """
        if not encrypted_blob:
            raise DecryptionError("Cannot decrypt empty data")
        
        if len(encrypted_blob) < MIN_ENCRYPTED_SIZE:
            raise DecryptionError(
                f"Encrypted blob too short: {len(encrypted_blob)} bytes, "
                f"minimum is {MIN_ENCRYPTED_SIZE} bytes"
            )
        
        try:
            # Unpack components
            salt = encrypted_blob[:SALT_LENGTH]
            iv = encrypted_blob[SALT_LENGTH:SALT_LENGTH + IV_LENGTH]
            ciphertext_with_tag = encrypted_blob[SALT_LENGTH + IV_LENGTH:]
            
            # Derive key using same salt
            derived_key = self._derive_key(salt)
            
            # Decrypt and verify authentication tag
            aesgcm = AESGCM(derived_key)
            plaintext = aesgcm.decrypt(iv, ciphertext_with_tag, None)
            
            logger.debug(
                f"Decrypted {len(encrypted_blob):,} bytes → "
                f"{len(plaintext):,} bytes"
            )
            
            return plaintext
            
        except Exception as e:
            # Don't reveal details about why decryption failed
            # (could help attackers)
            logger.error(f"Decryption failed: {type(e).__name__}")
            raise DecryptionError(
                "Decryption failed - wrong key, corrupted data, or tampering detected"
            ) from e
    
    def verify(self, encrypted_blob: bytes) -> bool:
        """
        Verify that encrypted data can be decrypted.
        
        Attempts decryption without returning the plaintext.
        Useful for integrity checks.
        
        Args:
            encrypted_blob: Data to verify
            
        Returns:
            True if decryption would succeed, False otherwise
        """
        try:
            self.decrypt(encrypted_blob)
            return True
        except DecryptionError:
            return False
    
    @staticmethod
    def get_overhead() -> int:
        """
        Get the encryption overhead in bytes.
        
        Returns:
            Number of bytes added to plaintext during encryption
            (salt + iv + auth_tag = 16 + 12 + 16 = 44 bytes)
        """
        return SALT_LENGTH + IV_LENGTH + 16  # 16-byte auth tag


# =============================================================================
# Factory Functions
# =============================================================================


def create_archive_encryption(secrets_manager) -> ArchiveEncryption:
    """
    Factory function to create ArchiveEncryption instance.
    
    Following Clean Architecture v5.2 Rule #1: Factory Functions.
    
    Args:
        secrets_manager: SecretsManager instance to get master key
        
    Returns:
        Configured ArchiveEncryption instance
        
    Raises:
        InvalidKeyError: If archive master key is not configured
        
    Example:
        >>> from src.managers import create_secrets_manager
        >>> secrets = create_secrets_manager()
        >>> encryption = create_archive_encryption(secrets)
    """
    logger.info("🏭 Creating ArchiveEncryption")
    
    master_key = secrets_manager.get_archive_master_key()
    
    if not master_key:
        raise InvalidKeyError(
            "Archive master key not found. "
            "Generate with: openssl rand 32 > secrets/archive_master_key"
        )
    
    encryption = ArchiveEncryption(master_key)
    logger.info("✅ ArchiveEncryption initialized")
    
    return encryption


def create_archive_encryption_from_key(master_key: bytes) -> ArchiveEncryption:
    """
    Factory function to create ArchiveEncryption with explicit key.
    
    Useful for testing or when key is obtained from non-standard source.
    
    Args:
        master_key: 32+ byte encryption key
        
    Returns:
        Configured ArchiveEncryption instance
        
    Raises:
        InvalidKeyError: If key is too short
    """
    return ArchiveEncryption(master_key)


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    # Classes
    "ArchiveEncryption",
    # Factory functions
    "create_archive_encryption",
    "create_archive_encryption_from_key",
    # Exceptions
    "EncryptionError",
    "DecryptionError",
    "InvalidKeyError",
    # Constants (for testing/verification)
    "SALT_LENGTH",
    "IV_LENGTH",
    "KEY_LENGTH",
    "PBKDF2_ITERATIONS",
]
