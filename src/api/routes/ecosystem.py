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
Ecosystem Routes - Proxy to Ash (Core) Ecosystem Health API
----------------------------------------------------------------------------
FILE VERSION: v5.0-2-2.6-1
LAST MODIFIED: 2026-01-17
PHASE: Phase 2 - Dashboard Integration (Ecosystem Health API)
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

PURPOSE:
    Proxies requests from the frontend to the Ash (Core) Ecosystem Health API.
    This allows the frontend to access Ash (Core) via Docker internal networking
    without requiring external URL configuration or VITE_ environment variables.

PATTERN:
    Browser → /api/ecosystem/* (Ash-Dash) → http://ash:30887/* (Ash Core)

ENDPOINTS:
    GET /api/ecosystem/health     - Full ecosystem health report
    GET /api/ecosystem/liveness   - Ash (Core) liveness check
    GET /api/ecosystem/readiness  - Ash (Core) readiness check
    GET /api/ecosystem/info       - Ash (Core) service info

USAGE:
    # Get full ecosystem health (proxied through Ash-Dash)
    curl http://localhost:30883/api/ecosystem/health

    # Direct equivalent on Ash (Core)
    curl http://ash:30887/health/ecosystem
"""

from datetime import datetime
from typing import Any, Dict

import httpx
from fastapi import APIRouter, HTTPException, Request

# Module version
__version__ = "v5.0-2-2.6-1"

# Create router
router = APIRouter(prefix="/api/ecosystem", tags=["Ecosystem"])

# =============================================================================
# Configuration
# =============================================================================

# Ash (Core) Ecosystem Health API base URL
# Uses Docker internal hostname - only accessible from within Docker network
ASH_CORE_BASE_URL = "http://ash:30887"

# Request timeout (seconds)
REQUEST_TIMEOUT = 15.0


# =============================================================================
# Proxy Endpoints
# =============================================================================

@router.get("/health")
async def proxy_ecosystem_health(request: Request) -> Dict[str, Any]:
    """
    Proxy to Ash (Core) /health/ecosystem endpoint.
    
    Returns the full ecosystem health report including:
    - Overall ecosystem status
    - Individual component health
    - Inter-component connectivity
    - Summary statistics
    
    Returns:
        JSON ecosystem health report from Ash (Core)
    
    Raises:
        HTTPException 503: If Ash (Core) is unreachable
        HTTPException 502: If Ash (Core) returns an error
    """
    return await _proxy_request("/health/ecosystem")


@router.get("/liveness")
async def proxy_liveness(request: Request) -> Dict[str, Any]:
    """
    Proxy to Ash (Core) /health endpoint (liveness check).
    
    Returns:
        JSON with status, service name, and timestamp
    
    Raises:
        HTTPException 503: If Ash (Core) is unreachable
    """
    return await _proxy_request("/health")


@router.get("/readiness")
async def proxy_readiness(request: Request) -> Dict[str, Any]:
    """
    Proxy to Ash (Core) /health/ready endpoint (readiness check).
    
    Returns:
        JSON with readiness status
    
    Raises:
        HTTPException 503: If Ash (Core) is unreachable
    """
    return await _proxy_request("/health/ready")


@router.get("/info")
async def proxy_info(request: Request) -> Dict[str, Any]:
    """
    Proxy to Ash (Core) root endpoint (service info).
    
    Returns:
        JSON with service info and available endpoints
    
    Raises:
        HTTPException 503: If Ash (Core) is unreachable
    """
    return await _proxy_request("/")


# =============================================================================
# Helper Functions
# =============================================================================

async def _proxy_request(path: str) -> Dict[str, Any]:
    """
    Make a proxied request to Ash (Core).
    
    Args:
        path: The path to request on Ash (Core) (e.g., "/health/ecosystem")
    
    Returns:
        JSON response from Ash (Core)
    
    Raises:
        HTTPException 503: If Ash (Core) is unreachable (connection error/timeout)
        HTTPException 502: If Ash (Core) returns an error response
    """
    url = f"{ASH_CORE_BASE_URL}{path}"
    
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.get(url)
            
            # Return successful responses (including 503 with health data)
            if response.status_code == 200:
                return response.json()
            
            # Ash (Core) returns 503 when ecosystem is unhealthy but still includes data
            if response.status_code == 503:
                try:
                    # Return the health data even on 503
                    return response.json()
                except Exception:
                    pass
            
            # Other error responses
            raise HTTPException(
                status_code=502,
                detail=f"Ash (Core) returned error: HTTP {response.status_code}"
            )
    
    except httpx.ConnectError as e:
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to Ash (Core) API. The service may be down."
        )
    
    except httpx.TimeoutException as e:
        raise HTTPException(
            status_code=503,
            detail="Ash (Core) API request timed out."
        )
    
    except HTTPException:
        # Re-raise HTTPExceptions as-is
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Error communicating with Ash (Core): {str(e)}"
        )
