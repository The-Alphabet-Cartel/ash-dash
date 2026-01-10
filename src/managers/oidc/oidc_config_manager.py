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
OIDC Configuration Manager - PocketID OpenID Connect Configuration
----------------------------------------------------------------------------
FILE VERSION: v5.0-10-10.4-1
LAST MODIFIED: 2026-01-10
PHASE: Phase 10 - Authentication & Authorization
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

RESPONSIBILITIES:
- Load OIDC configuration from oidc.json
- Fetch and cache OIDC discovery document from PocketID
- Provide access to OIDC endpoints (authorize, token, userinfo, etc.)
- Manage session configuration settings
- Handle role mapping from PocketID groups

OIDC DISCOVERY DOCUMENT:
    Fetched from: {issuer}/.well-known/openid-configuration
    Contains: authorization_endpoint, token_endpoint, userinfo_endpoint,
              jwks_uri, end_session_endpoint, scopes_supported, etc.

USAGE:
    oidc_config = await create_oidc_config_manager(
        config_manager=config_manager,
        logging_manager=logging_manager,
    )

    # Get OIDC endpoints
    auth_url = oidc_config.authorization_endpoint
    token_url = oidc_config.token_endpoint
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx

__version__ = "v5.0-10-10.4-1"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# OIDC Configuration Manager
# =============================================================================

class OIDCConfigManager:
    """
    Manages OIDC configuration and discovery for PocketID authentication.

    Loads configuration from oidc.json, fetches the OIDC discovery document,
    and provides access to all OIDC endpoints and settings.

    Attributes:
        _config: Loaded OIDC configuration
        _discovery: Cached OIDC discovery document
        _logger: Logger instance
    """

    # Configuration file path
    CONFIG_FILE = "oidc.json"

    def __init__(
        self,
        config: Dict[str, Any],
        logging_manager,
    ):
        """
        Initialize OIDCConfigManager (do not call directly, use factory).

        Args:
            config: Loaded OIDC configuration dictionary
            logging_manager: LoggingManager instance
        """
        self._config = config
        self._logging_manager = logging_manager
        self._logger = logging_manager.get_logger("oidc.config")
        self._discovery: Optional[Dict[str, Any]] = None
        self._discovery_fetched = False

    # =========================================================================
    # OIDC Configuration Properties
    # =========================================================================

    @property
    def enabled(self) -> bool:
        """Check if OIDC authentication is enabled."""
        return self._get_oidc_setting("enabled", True)

    @property
    def issuer_url(self) -> str:
        """Get the OIDC issuer URL (PocketID base URL)."""
        return self._get_oidc_setting("issuer_url", "https://id.alphabetcartel.net")

    @property
    def client_id(self) -> str:
        """Get the OIDC client ID."""
        return self._get_oidc_setting("client_id", "")

    @property
    def redirect_uri(self) -> str:
        """Get the OIDC redirect URI for callback."""
        return self._get_oidc_setting(
            "redirect_uri",
            "https://crt.alphabetcartel.net/auth/callback"
        )

    @property
    def post_logout_redirect_uri(self) -> str:
        """Get the post-logout redirect URI."""
        return self._get_oidc_setting(
            "post_logout_redirect_uri",
            "https://crt.alphabetcartel.net/"
        )

    @property
    def scopes(self) -> List[str]:
        """Get the requested OIDC scopes."""
        scopes = self._get_oidc_setting(
            "scopes",
            ["openid", "profile", "email", "groups"]
        )
        if isinstance(scopes, str):
            return scopes.split()
        return scopes

    # =========================================================================
    # Session Configuration Properties
    # =========================================================================

    @property
    def session_lifetime(self) -> int:
        """Get session lifetime in seconds (default: 24 hours)."""
        return self._get_session_setting("lifetime_seconds", 86400)

    @property
    def token_refresh_threshold(self) -> int:
        """Get token refresh threshold in seconds (default: 5 minutes)."""
        return self._get_session_setting("token_refresh_threshold_seconds", 300)

    @property
    def cookie_name(self) -> str:
        """Get the session cookie name."""
        return self._get_session_setting("cookie_name", "ash_session_id")

    @property
    def cookie_secure(self) -> bool:
        """Check if session cookie should be secure (HTTPS only)."""
        return self._get_session_setting("cookie_secure", True)

    @property
    def cookie_httponly(self) -> bool:
        """Check if session cookie should be HTTP-only."""
        return self._get_session_setting("cookie_httponly", True)

    @property
    def cookie_samesite(self) -> str:
        """Get session cookie SameSite setting."""
        return self._get_session_setting("cookie_samesite", "lax")

    # =========================================================================
    # Role Mapping Properties
    # =========================================================================

    @property
    def admin_group(self) -> str:
        """Get the PocketID group name for admin role."""
        return self._get_role_mapping("admin_group", "cartel_crt_admin")

    @property
    def lead_group(self) -> str:
        """Get the PocketID group name for lead role."""
        return self._get_role_mapping("lead_group", "cartel_crt_lead")

    @property
    def member_group(self) -> str:
        """Get the PocketID group name for member role."""
        return self._get_role_mapping("member_group", "cartel_crt")

    # =========================================================================
    # OIDC Discovery Document
    # =========================================================================

    async def fetch_discovery(self, force: bool = False) -> Dict[str, Any]:
        """
        Fetch and cache the OIDC discovery document.

        The discovery document is fetched from:
        {issuer_url}/.well-known/openid-configuration

        Args:
            force: Force re-fetch even if cached

        Returns:
            OIDC discovery document

        Raises:
            OIDCDiscoveryError: If discovery fetch fails
        """
        if self._discovery is not None and not force:
            return self._discovery

        discovery_url = f"{self.issuer_url}/.well-known/openid-configuration"
        self._logger.info(f"Fetching OIDC discovery from {discovery_url}")

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(discovery_url)
                response.raise_for_status()
                self._discovery = response.json()
                self._discovery_fetched = True

            self._logger.info("✅ OIDC discovery document fetched successfully")
            self._logger.debug(f"   Issuer: {self._discovery.get('issuer')}")
            self._logger.debug(
                f"   Scopes: {self._discovery.get('scopes_supported')}"
            )

            return self._discovery

        except httpx.HTTPError as e:
            self._logger.error(f"❌ Failed to fetch OIDC discovery: {e}")
            raise OIDCDiscoveryError(f"Failed to fetch discovery document: {e}")

    @property
    def discovery(self) -> Optional[Dict[str, Any]]:
        """Get the cached discovery document (may be None if not fetched)."""
        return self._discovery

    @property
    def is_discovery_fetched(self) -> bool:
        """Check if discovery document has been fetched."""
        return self._discovery_fetched

    # =========================================================================
    # OIDC Endpoint Properties (from Discovery)
    # =========================================================================

    @property
    def authorization_endpoint(self) -> str:
        """Get the authorization endpoint URL."""
        if self._discovery:
            return self._discovery.get("authorization_endpoint", "")
        # Fallback based on known PocketID structure
        return f"{self.issuer_url}/authorize"

    @property
    def token_endpoint(self) -> str:
        """Get the token endpoint URL."""
        if self._discovery:
            return self._discovery.get("token_endpoint", "")
        return f"{self.issuer_url}/api/oidc/token"

    @property
    def userinfo_endpoint(self) -> str:
        """Get the userinfo endpoint URL."""
        if self._discovery:
            return self._discovery.get("userinfo_endpoint", "")
        return f"{self.issuer_url}/api/oidc/userinfo"

    @property
    def end_session_endpoint(self) -> str:
        """Get the end session (logout) endpoint URL."""
        if self._discovery:
            return self._discovery.get("end_session_endpoint", "")
        return f"{self.issuer_url}/api/oidc/end-session"

    @property
    def jwks_uri(self) -> str:
        """Get the JWKS (JSON Web Key Set) URI."""
        if self._discovery:
            return self._discovery.get("jwks_uri", "")
        return f"{self.issuer_url}/.well-known/jwks.json"

    @property
    def introspection_endpoint(self) -> str:
        """Get the token introspection endpoint URL."""
        if self._discovery:
            return self._discovery.get("introspection_endpoint", "")
        return f"{self.issuer_url}/api/oidc/introspect"

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def _get_oidc_setting(self, key: str, default: Any) -> Any:
        """
        Get an OIDC setting with environment override support.

        Args:
            key: Setting key
            default: Default value

        Returns:
            Setting value
        """
        oidc_config = self._config.get("oidc", {})

        # Check environment variable first
        env_key = f"DASH_OIDC_{key.upper()}"
        env_value = os.environ.get(env_key)
        if env_value is not None:
            return self._parse_env_value(env_value, default)

        # Check config value
        value = oidc_config.get(key)
        if value is not None and not str(value).startswith("${"):
            return value

        # Check defaults
        defaults = oidc_config.get("defaults", {})
        return defaults.get(key, default)

    def _get_session_setting(self, key: str, default: Any) -> Any:
        """
        Get a session setting with environment override support.

        Args:
            key: Setting key
            default: Default value

        Returns:
            Setting value
        """
        session_config = self._config.get("session", {})

        # Check environment variable first
        env_key = f"DASH_SESSION_{key.upper()}"
        env_value = os.environ.get(env_key)
        if env_value is not None:
            return self._parse_env_value(env_value, default)

        # Check config value
        value = session_config.get(key)
        if value is not None and not str(value).startswith("${"):
            return value

        # Check defaults
        defaults = session_config.get("defaults", {})
        return defaults.get(key, default)

    def _get_role_mapping(self, key: str, default: str) -> str:
        """
        Get a role mapping setting.

        Args:
            key: Setting key
            default: Default value

        Returns:
            Group name
        """
        role_config = self._config.get("role_mapping", {})

        # Check environment variable first
        env_key = f"DASH_OIDC_{key.upper()}"
        env_value = os.environ.get(env_key)
        if env_value is not None:
            return env_value

        # Check config value
        value = role_config.get(key)
        if value is not None and not str(value).startswith("${"):
            return value

        # Check defaults
        defaults = role_config.get("defaults", {})
        return defaults.get(key, default)

    def _parse_env_value(self, value: str, default: Any) -> Any:
        """
        Parse environment variable value to appropriate type.

        Args:
            value: String value from environment
            default: Default value (used for type inference)

        Returns:
            Parsed value
        """
        if isinstance(default, bool):
            return value.lower() in ("true", "1", "yes", "on")
        if isinstance(default, int):
            try:
                return int(value)
            except ValueError:
                return default
        if isinstance(default, list):
            # Assume comma-separated for lists
            return [v.strip() for v in value.split(",")]
        return value

    def get_status(self) -> Dict[str, Any]:
        """
        Get OIDC configuration status (safe for logging).

        Returns:
            Status dictionary
        """
        return {
            "enabled": self.enabled,
            "issuer_url": self.issuer_url,
            "client_id_set": bool(self.client_id),
            "redirect_uri": self.redirect_uri,
            "scopes": self.scopes,
            "discovery_fetched": self._discovery_fetched,
            "session_lifetime_seconds": self.session_lifetime,
            "cookie_name": self.cookie_name,
        }


# =============================================================================
# Exceptions
# =============================================================================

class OIDCDiscoveryError(Exception):
    """Raised when OIDC discovery document fetch fails."""
    pass


class OIDCConfigError(Exception):
    """Raised when OIDC configuration is invalid."""
    pass


# =============================================================================
# Factory Function
# =============================================================================

async def create_oidc_config_manager(
    config_manager,
    logging_manager,
) -> OIDCConfigManager:
    """
    Factory function to create and initialize OIDCConfigManager.

    Following Clean Architecture v5.2 Rule #1: Factory Functions.

    Args:
        config_manager: ConfigManager instance
        logging_manager: LoggingManager instance

    Returns:
        Initialized OIDCConfigManager with discovery fetched

    Raises:
        OIDCConfigError: If configuration is invalid
        OIDCDiscoveryError: If discovery fetch fails
    """
    logger = logging_manager.get_logger("oidc.config")
    logger.info("🏭 Creating OIDCConfigManager")

    # Load OIDC configuration file
    # Path: /app/src/config/oidc.json (relative to src/managers/oidc/)
    config_path = Path(__file__).parent.parent.parent / "config" / "oidc.json"

    if not config_path.exists():
        logger.warning(f"OIDC config file not found at {config_path}, using defaults")
        config = {}
    else:
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
            logger.debug(f"Loaded OIDC config from {config_path}")
        except json.JSONDecodeError as e:
            raise OIDCConfigError(f"Invalid OIDC config JSON: {e}")

    # Create manager
    manager = OIDCConfigManager(
        config=config,
        logging_manager=logging_manager,
    )

    # Validate client_id is set
    if not manager.client_id:
        logger.warning(
            "⚠️  OIDC client_id not set! "
            "Set DASH_OIDC_CLIENT_ID environment variable."
        )

    # Fetch discovery document (with graceful failure)
    try:
        await manager.fetch_discovery()
    except OIDCDiscoveryError as e:
        logger.warning(f"⚠️  Failed to fetch OIDC discovery: {e}")
        logger.warning("   OIDC authentication may not work correctly")

    logger.info("✅ OIDCConfigManager initialized")
    return manager


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "OIDCConfigManager",
    "create_oidc_config_manager",
    "OIDCDiscoveryError",
    "OIDCConfigError",
]
