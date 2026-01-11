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
Auth Routes - OIDC Authentication Flow Endpoints
----------------------------------------------------------------------------
FILE VERSION: v5.0-10-10.4-1
LAST MODIFIED: 2026-01-10
PHASE: Phase 10 - Authentication & Authorization
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

ENDPOINTS:
    GET  /auth/login     - Initiate OIDC login flow (redirects to PocketID)
    GET  /auth/callback  - Handle OIDC callback from PocketID
    GET  /auth/logout    - Logout and redirect to PocketID logout
    GET  /api/auth/me    - Get current authenticated user info

OIDC FLOW:
    1. User visits protected page without session
    2. Frontend redirects to /auth/login?redirect=/original-path
    3. Backend generates state, nonce, PKCE, stores in cookie
    4. Backend redirects to PocketID authorization endpoint
    5. User authenticates at PocketID
    6. PocketID redirects to /auth/callback with code
    7. Backend exchanges code for tokens
    8. Backend validates ID token
    9. Backend creates session in Redis
    10. Backend syncs user to database
    11. Backend sets session cookie and redirects to original path

SECURITY:
    - PKCE (S256) for code exchange
    - State parameter for CSRF protection
    - Nonce for replay protection
    - HTTP-only, Secure, SameSite cookies
"""

import secrets
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from src.api.dependencies.auth import get_current_user
from src.api.middleware.auth_middleware import UserContext
from src.services.oidc_service import OIDCTokenError


__version__ = "v5.0-10-10.4-1"


# =============================================================================
# Router Setup
# =============================================================================

# Auth flow routes (no /api prefix - these handle redirects)
router = APIRouter(tags=["auth"])

# API routes for user info (with /api prefix)
api_router = APIRouter(prefix="/api/auth", tags=["auth"])


# =============================================================================
# Response Models
# =============================================================================

class CurrentUserResponse(BaseModel):
    """Response model for current user info."""
    id: Optional[str] = None
    pocket_id: str
    email: str
    name: str
    role: Optional[str] = None
    groups: List[str] = []
    is_admin: bool = False
    is_lead: bool = False


class AuthStatusResponse(BaseModel):
    """Response model for auth status check."""
    authenticated: bool
    user: Optional[CurrentUserResponse] = None


# =============================================================================
# OIDC Flow Routes
# =============================================================================

@router.get("/auth/login")
async def login(
    request: Request,
    redirect: str = "/",
):
    """
    Initiate OIDC login flow.

    1. Generate state, nonce, and PKCE code verifier
    2. Store in temporary cookie for callback verification
    3. Redirect to PocketID authorization endpoint

    Args:
        request: FastAPI request
        redirect: URL to redirect to after successful login

    Returns:
        Redirect to PocketID authorization endpoint
    """
    oidc_service = request.app.state.oidc_service
    oidc_config = request.app.state.oidc_config

    # Check if OIDC is enabled
    if not oidc_config.enabled:
        raise HTTPException(
            status_code=503,
            detail="OIDC authentication is disabled"
        )

    # Generate security tokens
    state = secrets.token_urlsafe(32)
    nonce = secrets.token_urlsafe(32)

    # Generate authorization URL with PKCE
    auth_url, code_verifier = oidc_service.generate_authorization_url(
        state=state,
        nonce=nonce,
    )

    # Create response with redirect
    response = RedirectResponse(url=auth_url, status_code=302)

    # Store state, nonce, code_verifier, and redirect in temporary cookie
    # Format: state:nonce:code_verifier:redirect
    auth_data = f"{state}:{nonce}:{code_verifier}:{redirect}"
    response.set_cookie(
        key="oidc_auth_state",
        value=auth_data,
        httponly=True,
        secure=oidc_config.cookie_secure,
        samesite="lax",
        max_age=600,  # 10 minutes
    )

    return response


@router.get("/auth/callback")
async def callback(
    request: Request,
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
    error_description: Optional[str] = None,
):
    """
    Handle OIDC callback from PocketID.

    1. Verify state matches cookie
    2. Exchange code for tokens
    3. Validate ID token
    4. Create session in Redis
    5. Sync user to database
    6. Set session cookie
    7. Redirect to original destination

    Args:
        request: FastAPI request
        code: Authorization code from PocketID
        state: State parameter for CSRF verification
        error: Error code if auth failed
        error_description: Human-readable error description

    Returns:
        Redirect to original destination or error page
    """
    oidc_service = request.app.state.oidc_service
    oidc_config = request.app.state.oidc_config
    session_manager = request.app.state.session_manager
    user_sync_service = request.app.state.user_sync_service
    database_manager = request.app.state.database_manager

    # Handle errors from PocketID
    if error:
        error_msg = error_description or error
        # Redirect to frontend error page
        return RedirectResponse(
            url=f"/unauthorized?error={error_msg}",
            status_code=302
        )

    # Validate required parameters
    if not code or not state:
        return RedirectResponse(
            url="/unauthorized?error=Missing+authorization+code+or+state",
            status_code=302
        )

    # Get and validate auth state cookie
    auth_state_cookie = request.cookies.get("oidc_auth_state")
    if not auth_state_cookie:
        return RedirectResponse(
            url="/unauthorized?error=Missing+authentication+state",
            status_code=302
        )

    try:
        stored_state, nonce, code_verifier, redirect_uri = auth_state_cookie.split(":", 3)
    except ValueError:
        return RedirectResponse(
            url="/unauthorized?error=Invalid+authentication+state",
            status_code=302
        )

    # Verify state matches
    if state != stored_state:
        return RedirectResponse(
            url="/unauthorized?error=State+mismatch+-+possible+CSRF+attack",
            status_code=302
        )

    try:
        # Exchange code for tokens
        tokens = await oidc_service.exchange_code_for_tokens(
            code=code,
            code_verifier=code_verifier,
        )

        # Validate ID token
        claims = await oidc_service.validate_id_token(
            id_token=tokens.get("id_token", ""),
            nonce=nonce,
        )

        # Get additional user info from userinfo endpoint
        try:
            userinfo = await oidc_service.get_userinfo(tokens.get("access_token", ""))
            # Merge claims - userinfo takes precedence
            user_data = {**claims, **userinfo}
        except OIDCTokenError:
            # Use ID token claims if userinfo fails
            user_data = claims

        # Create session
        session_id = await session_manager.create_session(
            user_data=user_data,
            tokens=tokens,
        )

        # Sync user to database
        db_user_id = None
        if database_manager and database_manager.is_connected:
            try:
                async with database_manager.session() as db:
                    db_user = await user_sync_service.sync_user(
                        pocket_id_sub=user_data.get("sub", ""),
                        email=user_data.get("email", ""),
                        name=user_data.get("name", user_data.get("preferred_username", "")),
                        groups=user_data.get("groups", []),
                        db=db,
                    )
                    if db_user:
                        db_user_id = str(db_user.id)

                # Update session with database user ID
                if db_user_id:
                    await session_manager.update_db_user_id(session_id, db_user_id)

            except Exception as e:
                # Log but don't fail - session is still valid
                request.app.state.logging_manager.get_logger("auth").warning(
                    f"Failed to sync user to database: {e}"
                )

        # Create response with redirect
        response = RedirectResponse(url=redirect_uri or "/", status_code=302)

        # Set session cookie
        response.set_cookie(
            key=session_manager.cookie_name,
            value=session_id,
            httponly=session_manager.cookie_httponly,
            secure=session_manager.cookie_secure,
            samesite=session_manager.cookie_samesite,
            max_age=session_manager.session_lifetime,
        )

        # Clear auth state cookie
        response.delete_cookie("oidc_auth_state")

        return response

    except OIDCTokenError as e:
        return RedirectResponse(
            url=f"/unauthorized?error=Authentication+failed:+{str(e)}",
            status_code=302
        )
    except Exception as e:
        request.app.state.logging_manager.get_logger("auth").error(
            f"OIDC callback error: {e}"
        )
        return RedirectResponse(
            url="/unauthorized?error=Authentication+failed",
            status_code=302
        )


@router.get("/auth/logout")
async def logout(request: Request):
    """
    Logout user and redirect to PocketID logout.

    1. Get session from cookie
    2. Destroy session in Redis
    3. Clear session cookie
    4. Redirect to PocketID end session endpoint
    5. PocketID redirects back to /auth/login

    Returns:
        Redirect to PocketID logout
    """
    oidc_service = request.app.state.oidc_service
    session_manager = request.app.state.session_manager

    # Get session
    session_id = request.cookies.get(session_manager.cookie_name)
    id_token_hint = None

    if session_id:
        # Get session to extract ID token for logout
        session = await session_manager.get_session(session_id)
        if session:
            id_token_hint = session.id_token

        # Destroy session
        await session_manager.destroy_session(session_id)

    # Generate PocketID logout URL - redirect to login page after logout
    # Build full URL for post_logout_redirect_uri
    base_url = str(request.base_url).rstrip("/")
    post_logout_uri = f"{base_url}/auth/login"
    
    logout_url = oidc_service.generate_logout_url(
        id_token_hint=id_token_hint,
        post_logout_redirect_uri=post_logout_uri,
    )

    # Create response with redirect to PocketID logout
    response = RedirectResponse(url=logout_url, status_code=302)

    # Clear session cookie
    response.delete_cookie(session_manager.cookie_name)

    return response


# =============================================================================
# API Routes
# =============================================================================

@api_router.get(
    "/me",
    response_model=CurrentUserResponse,
    summary="Get current user",
    description="Get current authenticated user information including role and permissions.",
)
async def get_current_user_info(request: Request):
    """
    Get current authenticated user information.

    Returns user data from session, including database ID, PocketID,
    email, name, role, groups, and permission flags.
    """
    # Check if we have a session
    session_manager = request.app.state.session_manager
    session_id = request.cookies.get(session_manager.cookie_name)

    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session = await session_manager.get_session(session_id)

    if not session:
        raise HTTPException(status_code=401, detail="Session expired or invalid")

    # Check CRT membership
    if not session.is_crt_member:
        raise HTTPException(
            status_code=403,
            detail="Access denied: CRT membership required"
        )

    return CurrentUserResponse(
        id=session.db_user_id,
        pocket_id=session.user_id,
        email=session.email,
        name=session.name,
        role=session.role,
        groups=session.groups,
        is_admin=session.is_admin,
        is_lead=session.is_lead,
    )


@api_router.get(
    "/status",
    response_model=AuthStatusResponse,
    summary="Check auth status",
    description="Check if the current request is authenticated.",
)
async def get_auth_status(request: Request):
    """
    Check authentication status.

    Returns whether the user is authenticated and their info if so.
    Useful for frontend to check login state without triggering redirects.
    """
    session_manager = request.app.state.session_manager
    session_id = request.cookies.get(session_manager.cookie_name)

    if not session_id:
        return AuthStatusResponse(authenticated=False)

    session = await session_manager.get_session(session_id)

    if not session:
        return AuthStatusResponse(authenticated=False)

    # Must be CRT member
    if not session.is_crt_member:
        return AuthStatusResponse(authenticated=False)

    return AuthStatusResponse(
        authenticated=True,
        user=CurrentUserResponse(
            id=session.db_user_id,
            pocket_id=session.user_id,
            email=session.email,
            name=session.name,
            role=session.role,
            groups=session.groups,
            is_admin=session.is_admin,
            is_lead=session.is_lead,
        ),
    )


__all__ = ["router", "api_router"]
