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
OIDC Service - PocketID OAuth2/OpenID Connect Flow Implementation
----------------------------------------------------------------------------
FILE VERSION: v5.0-10-10.4-1
LAST MODIFIED: 2026-01-10
PHASE: Phase 10 - Authentication & Authorization
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

RESPONSIBILITIES:
- Generate authorization URLs with PKCE support
- Exchange authorization codes for tokens
- Validate ID tokens (signature and claims)
- Refresh access tokens
- Fetch user info from PocketID
- Generate logout URLs

OIDC FLOW:
    1. User visits protected page
    2. Redirect to /auth/login
    3. Generate authorization URL with state, nonce, PKCE
    4. User authenticates at PocketID
    5. PocketID redirects to /auth/callback with code
    6. Exchange code for tokens
    7. Validate ID token
    8. Create session with user info
    9. Redirect to original page

USAGE:
    oidc_service = create_oidc_service(
        oidc_config=oidc_config_manager,
        secrets_manager=secrets_manager,
        logging_manager=logging_manager,
    )

    # Generate authorization URL
    auth_url = oidc_service.generate_authorization_url(state, nonce, code_verifier)

    # Exchange code for tokens
    tokens = await oidc_service.exchange_code_for_tokens(code, code_verifier)
"""

import base64
import hashlib
import logging
import secrets
import time
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import httpx
from jose import jwt, JWTError

__version__ = "v5.0-10-10.4-1"

# Initialize logger
logger = logging.getLogger(__name__)


# =============================================================================
# OIDC Service
# =============================================================================

class OIDCService:
    """
    Handles OAuth2/OpenID Connect authentication flows with PocketID.

    Implements the Authorization Code flow with PKCE for secure
    browser-based authentication.

    Attributes:
        _config: OIDCConfigManager instance
        _client_secret: OIDC client secret
        _logger: Logger instance
        _jwks: Cached JWKS for token validation
    """

    def __init__(
        self,
        oidc_config,
        client_secret: str,
        logging_manager,
    ):
        """
        Initialize OIDCService (do not call directly, use factory).

        Args:
            oidc_config: OIDCConfigManager instance
            client_secret: OIDC client secret
            logging_manager: LoggingManager instance
        """
        self._config = oidc_config
        self._client_secret = client_secret
        self._logging_manager = logging_manager
        self._logger = logging_manager.get_logger("oidc.service")
        self._jwks: Optional[Dict[str, Any]] = None

    # =========================================================================
    # PKCE Support
    # =========================================================================

    @staticmethod
    def generate_code_verifier() -> str:
        """
        Generate a code verifier for PKCE.

        Returns:
            Random 64-character URL-safe string
        """
        return secrets.token_urlsafe(48)

    @staticmethod
    def generate_code_challenge(code_verifier: str) -> str:
        """
        Generate code challenge from code verifier (S256 method).

        Args:
            code_verifier: The code verifier string

        Returns:
            Base64URL-encoded SHA256 hash of verifier
        """
        digest = hashlib.sha256(code_verifier.encode()).digest()
        return base64.urlsafe_b64encode(digest).rstrip(b"=").decode()

    @staticmethod
    def generate_state() -> str:
        """Generate random state parameter for CSRF protection."""
        return secrets.token_urlsafe(32)

    @staticmethod
    def generate_nonce() -> str:
        """Generate random nonce for replay protection."""
        return secrets.token_urlsafe(32)

    # =========================================================================
    # Authorization URL Generation
    # =========================================================================

    def generate_authorization_url(
        self,
        state: str,
        nonce: str,
        code_verifier: Optional[str] = None,
        redirect_uri: Optional[str] = None,
    ) -> tuple[str, Optional[str]]:
        """
        Generate PocketID authorization URL.

        Args:
            state: CSRF protection token
            nonce: Replay protection token
            code_verifier: PKCE code verifier (generated if not provided)
            redirect_uri: Override redirect URI

        Returns:
            Tuple of (authorization_url, code_verifier)
        """
        # Generate PKCE code verifier if not provided
        if code_verifier is None:
            code_verifier = self.generate_code_verifier()

        code_challenge = self.generate_code_challenge(code_verifier)

        params = {
            "response_type": "code",
            "client_id": self._config.client_id,
            "redirect_uri": redirect_uri or self._config.redirect_uri,
            "scope": " ".join(self._config.scopes),
            "state": state,
            "nonce": nonce,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }

        auth_url = f"{self._config.authorization_endpoint}?{urlencode(params)}"

        self._logger.debug(f"Generated authorization URL for state={state[:8]}...")
        return auth_url, code_verifier

    # =========================================================================
    # Token Exchange
    # =========================================================================

    async def exchange_code_for_tokens(
        self,
        code: str,
        code_verifier: str,
        redirect_uri: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Exchange authorization code for tokens.

        Args:
            code: Authorization code from callback
            code_verifier: PKCE code verifier used in authorization
            redirect_uri: Override redirect URI (must match authorization)

        Returns:
            Token response dict with:
            - access_token
            - id_token
            - refresh_token (if granted)
            - expires_in
            - token_type

        Raises:
            OIDCTokenError: If token exchange fails
        """
        token_endpoint = self._config.token_endpoint

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri or self._config.redirect_uri,
            "client_id": self._config.client_id,
            "client_secret": self._client_secret,
            "code_verifier": code_verifier,
        }

        self._logger.debug(f"Exchanging code for tokens at {token_endpoint}")

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    token_endpoint,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )

                if response.status_code != 200:
                    error_data = response.json() if response.content else {}
                    error_msg = error_data.get(
                        "error_description",
                        error_data.get("error", f"HTTP {response.status_code}")
                    )
                    self._logger.error(f"Token exchange failed: {error_msg}")
                    raise OIDCTokenError(f"Token exchange failed: {error_msg}")

                tokens = response.json()
                self._logger.info("✅ Token exchange successful")
                return tokens

        except httpx.HTTPError as e:
            self._logger.error(f"Token exchange HTTP error: {e}")
            raise OIDCTokenError(f"Token exchange failed: {e}")

    # =========================================================================
    # Token Validation
    # =========================================================================

    async def _fetch_jwks(self, force: bool = False) -> Dict[str, Any]:
        """
        Fetch and cache JWKS for token validation.

        Args:
            force: Force re-fetch even if cached

        Returns:
            JWKS document
        """
        if self._jwks is not None and not force:
            return self._jwks

        jwks_uri = self._config.jwks_uri
        self._logger.debug(f"Fetching JWKS from {jwks_uri}")

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(jwks_uri)
                response.raise_for_status()
                self._jwks = response.json()
                return self._jwks

        except httpx.HTTPError as e:
            self._logger.error(f"Failed to fetch JWKS: {e}")
            raise OIDCTokenError(f"Failed to fetch JWKS: {e}")

    async def validate_id_token(
        self,
        id_token: str,
        nonce: str,
    ) -> Dict[str, Any]:
        """
        Validate ID token signature and claims.

        Validates:
        - Signature using JWKS
        - Issuer matches configured issuer
        - Audience matches client_id
        - Token is not expired
        - Nonce matches expected value

        Args:
            id_token: JWT ID token
            nonce: Expected nonce value

        Returns:
            Decoded token claims

        Raises:
            OIDCTokenError: If token is invalid
        """
        # Fetch JWKS
        jwks = await self._fetch_jwks()

        try:
            # Decode and validate token
            claims = jwt.decode(
                id_token,
                jwks,
                algorithms=["RS256"],
                audience=self._config.client_id,
                issuer=self._config.issuer_url,
                options={
                    "verify_aud": True,
                    "verify_iss": True,
                    "verify_exp": True,
                },
            )

            # Validate nonce
            if claims.get("nonce") != nonce:
                raise OIDCTokenError("Nonce mismatch in ID token")

            self._logger.debug(
                f"ID token validated for user: {claims.get('email', claims.get('sub'))}"
            )
            return claims

        except JWTError as e:
            self._logger.error(f"ID token validation failed: {e}")
            raise OIDCTokenError(f"Invalid ID token: {e}")

    # =========================================================================
    # Token Refresh
    # =========================================================================

    async def refresh_tokens(
        self,
        refresh_token: str,
    ) -> Dict[str, Any]:
        """
        Refresh access token using refresh token.

        Args:
            refresh_token: Valid refresh token

        Returns:
            New token set with access_token, id_token, etc.

        Raises:
            OIDCTokenError: If refresh fails
        """
        token_endpoint = self._config.token_endpoint

        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self._config.client_id,
            "client_secret": self._client_secret,
        }

        self._logger.debug("Refreshing tokens")

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    token_endpoint,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )

                if response.status_code != 200:
                    error_data = response.json() if response.content else {}
                    error_msg = error_data.get(
                        "error_description",
                        error_data.get("error", f"HTTP {response.status_code}")
                    )
                    self._logger.warning(f"Token refresh failed: {error_msg}")
                    raise OIDCTokenError(f"Token refresh failed: {error_msg}")

                tokens = response.json()
                self._logger.debug("Tokens refreshed successfully")
                return tokens

        except httpx.HTTPError as e:
            self._logger.error(f"Token refresh HTTP error: {e}")
            raise OIDCTokenError(f"Token refresh failed: {e}")

    # =========================================================================
    # User Info
    # =========================================================================

    async def get_userinfo(
        self,
        access_token: str,
    ) -> Dict[str, Any]:
        """
        Fetch user info from PocketID userinfo endpoint.

        Args:
            access_token: Valid access token

        Returns:
            User info dict (email, name, groups, etc.)

        Raises:
            OIDCTokenError: If userinfo fetch fails
        """
        userinfo_endpoint = self._config.userinfo_endpoint

        self._logger.debug(f"Fetching userinfo from {userinfo_endpoint}")

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    userinfo_endpoint,
                    headers={"Authorization": f"Bearer {access_token}"},
                )

                if response.status_code != 200:
                    self._logger.warning(
                        f"Userinfo fetch failed: HTTP {response.status_code}"
                    )
                    raise OIDCTokenError(
                        f"Userinfo fetch failed: HTTP {response.status_code}"
                    )

                userinfo = response.json()
                self._logger.debug(
                    f"Userinfo fetched for: {userinfo.get('email', userinfo.get('sub'))}"
                )
                return userinfo

        except httpx.HTTPError as e:
            self._logger.error(f"Userinfo HTTP error: {e}")
            raise OIDCTokenError(f"Userinfo fetch failed: {e}")

    # =========================================================================
    # Logout
    # =========================================================================

    def generate_logout_url(
        self,
        id_token_hint: Optional[str] = None,
        post_logout_redirect_uri: Optional[str] = None,
    ) -> str:
        """
        Generate PocketID logout URL.

        Args:
            id_token_hint: Optional ID token for logout
            post_logout_redirect_uri: Where to redirect after logout

        Returns:
            Logout URL to redirect user to
        """
        params = {}

        if id_token_hint:
            params["id_token_hint"] = id_token_hint

        redirect_uri = post_logout_redirect_uri or self._config.post_logout_redirect_uri
        if redirect_uri:
            params["post_logout_redirect_uri"] = redirect_uri

        logout_url = self._config.end_session_endpoint
        if params:
            logout_url = f"{logout_url}?{urlencode(params)}"

        return logout_url

    # =========================================================================
    # Utility Methods
    # =========================================================================

    def compute_role_from_groups(self, groups: list) -> Optional[str]:
        """
        Compute user role from PocketID groups.

        Group hierarchy:
        - admin_group -> admin
        - lead_group -> lead
        - member_group -> member

        Args:
            groups: List of group names from PocketID

        Returns:
            Role string (admin, lead, member) or None
        """
        if self._config.admin_group in groups:
            return "admin"
        if self._config.lead_group in groups:
            return "lead"
        if self._config.member_group in groups:
            return "member"
        return None


# =============================================================================
# Exceptions
# =============================================================================

class OIDCTokenError(Exception):
    """Raised when OIDC token operations fail."""
    pass


class OIDCAuthError(Exception):
    """Raised when OIDC authentication fails."""
    pass


# =============================================================================
# Factory Function
# =============================================================================

def create_oidc_service(
    oidc_config,
    secrets_manager,
    logging_manager,
) -> OIDCService:
    """
    Factory function to create OIDCService.

    Following Clean Architecture v5.2 Rule #1: Factory Functions.

    Args:
        oidc_config: OIDCConfigManager instance
        secrets_manager: SecretsManager instance
        logging_manager: LoggingManager instance

    Returns:
        Configured OIDCService instance

    Raises:
        OIDCAuthError: If client secret is not configured
    """
    logger = logging_manager.get_logger("oidc.service")
    logger.info("🏭 Creating OIDCService")

    # Get client secret
    client_secret = secrets_manager.get_oidc_client_secret()

    if not client_secret:
        logger.warning(
            "⚠️  OIDC client secret not configured! "
            "Create secrets/oidc_client_secret file."
        )
        # Allow creation but service won't work
        client_secret = ""

    service = OIDCService(
        oidc_config=oidc_config,
        client_secret=client_secret,
        logging_manager=logging_manager,
    )

    logger.info("✅ OIDCService initialized")
    return service


# =============================================================================
# Export public interface
# =============================================================================

__all__ = [
    "OIDCService",
    "create_oidc_service",
    "OIDCTokenError",
    "OIDCAuthError",
]
