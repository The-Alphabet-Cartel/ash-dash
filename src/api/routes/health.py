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
FILE VERSION: v5.0-2-2.8-1
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
__version__ = "v5.0-2-2.8-1"

# Create router
router = APIRouter(prefix="/health", tags=["Health"])

# Application info (imported from main at startup)
APP_NAME = "Ash-Dash"
APP_VERSION = "v5.0-2-2.8-1"


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
    - Database connected
    - Redis connected (optional)
    
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
    redis_manager = getattr(request.app.state, "redis_manager", None)
    sync_service = getattr(request.app.state, "sync_service", None)
    
    # Perform health checks
    checks = {
        "config": config_manager is not None,
        "logging": logging_manager is not None,
        "secrets": secrets_manager is not None,
        "database": await check_database_connection(database_manager),
        "redis": await check_redis_connection(redis_manager),
    }
    
    # Redis is optional - don't fail readiness if Redis is unavailable
    required_checks = ["config", "logging", "secrets", "database"]
    all_required_ready = all(checks[k] for k in required_checks)
    
    return {
        "status": "ready" if all_required_ready else "not_ready",
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
    - Uptime and metrics
    
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
    redis_manager = getattr(request.app.state, "redis_manager", None)
    sync_service = getattr(request.app.state, "sync_service", None)
    
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
    
    # Database Manager status
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
    
    # Redis Manager status
    if redis_manager:
        redis_health = await redis_manager.health_check()
        response["components"]["redis"] = {
            "status": "healthy" if redis_health.get("healthy") else "unhealthy",
            "connected": redis_health.get("healthy", False),
            "latency_ms": redis_health.get("latency_ms"),
            "redis_version": redis_health.get("redis_version"),
            "error": redis_health.get("error"),
        }
    else:
        # Redis is optional
        response["components"]["redis"] = {
            "status": "unavailable",
            "connected": False,
            "note": "Redis is optional - Ash-Bot may not be running",
        }
    
    # Sync Service status
    if sync_service:
        sync_stats = sync_service.stats
        response["components"]["sync_service"] = {
            "status": "healthy" if sync_service.is_running else "stopped",
            "running": sync_service.is_running,
            "cycles_completed": sync_stats.get("cycles_completed", 0),
            "sessions_created": sync_stats.get("sessions_created", 0),
            "sessions_updated": sync_stats.get("sessions_updated", 0),
            "sessions_closed": sync_stats.get("sessions_closed", 0),
            "last_sync": sync_stats.get("last_sync"),
            "errors_count": sync_stats.get("errors_count", 0),
        }
    else:
        response["components"]["sync_service"] = {
            "status": "unavailable",
            "running": False,
            "note": "Requires Redis and Database connections",
        }
    
    # Determine overall status
    # Required components: config, logging, secrets, database
    required_components = ["config_manager", "logging_manager", "secrets_manager", "database"]
    required_statuses = [
        response["components"].get(c, {}).get("status", "unknown")
        for c in required_components
    ]
    
    if all(s == "healthy" for s in required_statuses):
        response["status"] = "healthy"
    elif any(s == "not_initialized" for s in required_statuses):
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


async def check_redis_connection(redis_manager) -> bool:
    """
    Check if Redis is connected and responsive.
    
    Args:
        redis_manager: RedisManager instance or None
    
    Returns:
        True if Redis is healthy, False otherwise
    """
    try:
        if redis_manager:
            health = await redis_manager.health_check()
            return health.get("healthy", False)
        return False
    except Exception:
        return False
