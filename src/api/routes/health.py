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
Health Routes - Liveness, Readiness, and Detailed Health Checks
----------------------------------------------------------------------------
FILE VERSION: v5.0-2-2.2-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 2 - Data Layer
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

ENDPOINTS:
    GET /health          - Basic liveness check (for load balancers)
    GET /health/ready    - Readiness check (verifies dependencies)
    GET /health/detailed - Comprehensive health information

USAGE:
    # Check if service is alive
    curl http://localhost:30883/health

    # Check if service is ready to accept traffic
    curl http://localhost:30883/health/ready

    # Get detailed health information
    curl http://localhost:30883/health/detailed
"""

from datetime import datetime
from typing import Any, Dict

from fastapi import APIRouter, Request

# Module version
__version__ = "v5.0-2-2.2-1"

# Create router
router = APIRouter(prefix="/health", tags=["Health"])

# Application info (imported from main at startup)
APP_NAME = "Ash-Dash"
APP_VERSION = "v5.0-2-2.2-1"


# =============================================================================
# Health Endpoints
# =============================================================================

@router.get("")
@router.get("/")
async def health_check() -> Dict[str, Any]:
    """
    Basic liveness check.
    
    Returns 200 if the service is running.
    Used by Docker health checks and load balancers.
    
    Returns:
        JSON with status, service name, and version
    """
    return {
        "status": "healthy",
        "service": APP_NAME,
        "version": APP_VERSION,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@router.get("/ready")
async def readiness_check(request: Request) -> Dict[str, Any]:
    """
    Readiness check for service dependencies.
    
    Verifies that all required services are available:
    - Configuration loaded
    - Logging initialized
    - Database connected (Phase 2)
    - Redis connected (Phase 2)
    
    Args:
        request: FastAPI request (to access app state)
    
    Returns:
        JSON with status and individual component checks
    """
    # Get managers from app state
    config_manager = getattr(request.app.state, "config_manager", None)
    logging_manager = getattr(request.app.state, "logging_manager", None)
    secrets_manager = getattr(request.app.state, "secrets_manager", None)
    database_manager = getattr(request.app.state, "database_manager", None)
    
    # Perform health checks
    checks = {
        "config": config_manager is not None,
        "logging": logging_manager is not None,
        "secrets": secrets_manager is not None,
        "database": await check_database_connection(database_manager),
        # Phase 2 Step 2.6: Add Redis check
        # "redis": await check_redis_connection(request),
    }
    
    all_ready = all(checks.values())
    
    return {
        "status": "ready" if all_ready else "not_ready",
        "checks": checks,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@router.get("/detailed")
async def detailed_health(request: Request) -> Dict[str, Any]:
    """
    Detailed health information for debugging and monitoring.
    
    Returns comprehensive system status including:
    - Service information
    - Configuration state
    - Component status
    - Uptime and metrics (Phase 2+)
    
    Args:
        request: FastAPI request (to access app state)
    
    Returns:
        JSON with detailed health information
    """
    # Get managers from app state
    config_manager = getattr(request.app.state, "config_manager", None)
    logging_manager = getattr(request.app.state, "logging_manager", None)
    secrets_manager = getattr(request.app.state, "secrets_manager", None)
    database_manager = getattr(request.app.state, "database_manager", None)
    
    # Build detailed response
    response = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": {
            "name": APP_NAME,
            "version": APP_VERSION,
            "environment": (
                config_manager.get_environment() 
                if config_manager 
                else "unknown"
            ),
        },
        "components": {},
    }
    
    # Config Manager status
    if config_manager:
        validation_errors = config_manager.get_validation_errors()
        response["components"]["config_manager"] = {
            "status": "healthy",
            "environment": config_manager.get_environment(),
            "validation_errors": len(validation_errors),
            "is_debug": config_manager.is_debug(),
        }
    else:
        response["components"]["config_manager"] = {
            "status": "not_initialized",
        }
    
    # Logging Manager status
    if logging_manager:
        response["components"]["logging_manager"] = {
            "status": "healthy",
            "level": logging_manager.get_level(),
            "format": logging_manager.get_format(),
        }
    else:
        response["components"]["logging_manager"] = {
            "status": "not_initialized",
        }
    
    # Secrets Manager status
    if secrets_manager:
        # Don't expose actual secret values, just availability
        response["components"]["secrets_manager"] = {
            "status": "healthy",
            "secrets_available": list(secrets_manager.list_available().keys()),
        }
    else:
        response["components"]["secrets_manager"] = {
            "status": "not_initialized",
        }
    
    # Database Manager status (Phase 2)
    if database_manager:
        db_health = await database_manager.health_check()
        response["components"]["database"] = {
            "status": db_health.get("status", "unknown"),
            "connected": db_health.get("connected", False),
            "latency_ms": db_health.get("latency_ms"),
            "pool_size": db_health.get("pool_size", 0),
            "pool_checked_out": db_health.get("pool_checked_out", 0),
            "error": db_health.get("error"),
        }
    else:
        response["components"]["database"] = {
            "status": "not_initialized",
        }
    
    # Phase 2 Step 2.6: Add Redis status
    # response["components"]["redis"] = await get_redis_status(request)
    
    # Determine overall status
    component_statuses = [
        c.get("status", "unknown") 
        for c in response["components"].values()
    ]
    if all(s == "healthy" for s in component_statuses):
        response["status"] = "healthy"
    elif any(s == "not_initialized" for s in component_statuses):
        response["status"] = "degraded"
    else:
        response["status"] = "unhealthy"
    
    return response


# =============================================================================
# Helper Functions
# =============================================================================


async def check_database_connection(database_manager) -> bool:
    """
    Check if database is connected and responsive.
    
    Args:
        database_manager: DatabaseManager instance or None
    
    Returns:
        True if database is healthy, False otherwise
    """
    try:
        if database_manager:
            health = await database_manager.health_check()
            return health.get("status") == "healthy"
        return False
    except Exception:
        return False


# Phase 2 Step 2.6: Uncomment when RedisManager is implemented
# async def check_redis_connection(request: Request) -> bool:
#     """Check if Redis is connected and responsive."""
#     try:
#         redis_manager = getattr(request.app.state, "redis_manager", None)
#         if redis_manager:
#             return await redis_manager.ping()
#         return False
#     except Exception:
#         return False
