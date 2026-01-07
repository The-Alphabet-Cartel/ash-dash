#!/usr/bin/env python3
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
Main Entry Point - FastAPI Application Bootstrap
----------------------------------------------------------------------------
FILE VERSION: v5.0-2-2.7-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 2 - Data Layer
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

USAGE:
    # Run with uvicorn (development)
    python -m uvicorn main:app --host 0.0.0.0 --port 30883 --reload

    # Run with Docker (production)
    docker-compose up -d

ENVIRONMENT VARIABLES:
    DASH_ENVIRONMENT    - Environment name (production, testing, development)
    DASH_HOST           - Host to bind to (default: 0.0.0.0)
    DASH_PORT           - Port to listen on (default: 30883)
    DASH_DEBUG          - Enable debug mode (default: false)
    DASH_LOG_LEVEL      - Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    DASH_LOG_FORMAT     - Log format (human, json)
"""

import os
import sys
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.managers.config_manager import create_config_manager
from src.managers.logging_config_manager import create_logging_config_manager
from src.managers.secrets_manager import create_secrets_manager
from src.managers.database import create_database_manager
from src.managers.redis import create_redis_manager
from src.services import create_sync_service
from src.api.routes.health import router as health_router

# =============================================================================
# Module Info
# =============================================================================

__version__ = "v5.0-2-2.7-1"
__app_name__ = "Ash-Dash"
__description__ = "Crisis Detection Dashboard for The Alphabet Cartel"

# =============================================================================
# Global Managers (initialized at startup)
# =============================================================================

config_manager = None
logging_manager = None
secrets_manager = None
database_manager = None
redis_manager = None
sync_service = None
logger = None


# =============================================================================
# Application Lifespan
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager for startup and shutdown events.

    This handles:
    - Manager initialization at startup
    - Background service startup
    - Resource cleanup at shutdown
    """
    global config_manager, logging_manager, secrets_manager
    global database_manager, redis_manager, sync_service, logger

    # =========================================================================
    # STARTUP
    # =========================================================================

    # Initialize configuration manager
    config_manager = create_config_manager()

    # Initialize logging manager (uses config)
    logging_manager = create_logging_config_manager(config_manager)
    logger = logging_manager.get_logger("main")

    # Print startup banner
    logger.info("=" * 60)
    logger.info(f"  {__app_name__} - {__description__}")
    logger.info(f"  Version: {__version__}")
    logger.info(f"  Environment: {config_manager.get_environment()}")
    logger.info("=" * 60)

    # Initialize secrets manager
    secrets_manager = create_secrets_manager()
    logger.info("Secrets manager initialized")

    # Initialize database manager (Phase 2)
    database_manager = await create_database_manager(
        config_manager=config_manager,
        secrets_manager=secrets_manager,
        logging_manager=logging_manager,
    )
    if database_manager.is_connected:
        logger.info("Database manager initialized and connected")
    else:
        logger.warning(
            "Database manager initialized but not connected - "
            "system will retry on first use"
        )

    # Initialize Redis manager (Phase 2 - optional, graceful degradation)
    try:
        redis_manager = await create_redis_manager(
            config_manager=config_manager,
            secrets_manager=secrets_manager,
            logging_manager=logging_manager,
        )
        if redis_manager.is_connected:
            logger.info("Redis manager initialized and connected")
        else:
            logger.warning("Redis manager initialized but not connected")
    except Exception as e:
        # Redis is optional - Ash-Bot may not be running
        logger.warning(f"Redis connection failed (optional): {e}")
        logger.info("Continuing without Redis - session sync will be unavailable")
        redis_manager = None

    # Initialize Sync Service (Phase 2 - requires both Redis and Database)
    if redis_manager and redis_manager.is_connected and database_manager.is_connected:
        try:
            sync_service = await create_sync_service(
                redis_manager=redis_manager,
                database_manager=database_manager,
                logging_manager=logging_manager,
                config_manager=config_manager,
            )
            await sync_service.start()
            logger.info("Sync service started")
        except Exception as e:
            logger.warning(f"Sync service failed to start: {e}")
            sync_service = None
    else:
        logger.info("Sync service not started (requires Redis and Database)")
        sync_service = None

    # Log configuration
    server_config = config_manager.get_server_config()
    logger.info(f"Server: {server_config.get('host')}:{server_config.get('port')}")
    logger.info(f"Debug mode: {server_config.get('debug')}")

    # Store managers in app state for access in routes
    app.state.config_manager = config_manager
    app.state.logging_manager = logging_manager
    app.state.secrets_manager = secrets_manager
    app.state.database_manager = database_manager
    app.state.redis_manager = redis_manager
    app.state.sync_service = sync_service

    logger.info("Application startup complete")

    # Yield control to the application
    yield

    # =========================================================================
    # SHUTDOWN
    # =========================================================================

    logger.info("Application shutdown initiated")

    # Stop sync service first (before closing connections it depends on)
    if sync_service:
        await sync_service.stop()

    # Cleanup Redis connection
    if redis_manager:
        await redis_manager.close()

    # Cleanup database connection
    if database_manager:
        await database_manager.close()

    logger.info("Application shutdown complete")


# =============================================================================
# FastAPI Application
# =============================================================================

app = FastAPI(
    title=__app_name__,
    description=__description__,
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


# =============================================================================
# Middleware
# =============================================================================

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication Middleware (Phase 1 - prepared but not active)
# To enable authentication, uncomment the following lines:
#
# from src.api.middleware.auth_middleware import AuthMiddleware
#
# app.add_middleware(
#     AuthMiddleware,
#     config_manager=config_manager,  # Will need to be set after startup
# )
#
# NOTE: For Phase 1, auth middleware is ready but not enabled because:
# 1. Pocket-ID integration needs testing with actual cookies
# 2. Health endpoints should remain accessible without auth
# 3. We want to verify core functionality first


# =============================================================================
# Routes
# =============================================================================

# Health check routes
app.include_router(health_router)


# Root Route
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with service information.
    """
    return {
        "service": __app_name__,
        "description": __description__,
        "version": __version__,
        "docs": "/docs",
        "health": "/health",
        "community": "The Alphabet Cartel - https://discord.gg/alphabetcartel",
    }


# =============================================================================
# Main Entry Point
# =============================================================================

def main() -> None:
    """
    Main entry point for running the service directly.

    For production, use: docker-compose up -d
    For development, use: python -m uvicorn main:app --reload
    """
    import uvicorn

    # Get configuration
    config = create_config_manager()
    server_config = config.get_server_config()

    host = server_config.get("host", "0.0.0.0")
    port = server_config.get("port", 30883)
    debug = server_config.get("debug", False)
    workers = server_config.get("workers", 1)

    print(f"Starting {__app_name__} v{__version__}")
    print(f"Listening on {host}:{port}")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        workers=1 if debug else workers,
        log_level="debug" if debug else "info",
    )


if __name__ == "__main__":
    main()
