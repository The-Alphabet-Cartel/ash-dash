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
FILE VERSION: v5.0-10-10.4-1
LAST MODIFIED: 2026-01-10
PHASE: Phase 10 - Authentication & Authorization
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

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.managers.config_manager import create_config_manager
from src.managers.logging_config_manager import create_logging_config_manager
from src.managers.secrets_manager import create_secrets_manager
from src.managers.database import create_database_manager
from src.managers.redis import create_redis_manager
from src.managers.oidc import create_oidc_config_manager
from src.managers.session import create_session_manager
from src.services import create_sync_service, create_user_sync_service, create_oidc_service
from src.api.middleware.auth_middleware import AuthMiddleware
from src.api.routes.health import router as health_router
from src.api.routes.sessions import router as sessions_router
from src.api.routes.users import router as users_router
from src.api.routes.dashboard import router as dashboard_router
from src.api.routes.notes import router as notes_router
from src.api.routes.wiki import router as wiki_router
from src.api.routes.archives import router as archives_router
from src.api.routes.admin import router as admin_router
from src.api.routes.auth import router as auth_router, api_router as auth_api_router

# =============================================================================
# Module Info
# =============================================================================

__version__ = "v5.0-10-10.4-1"

# Frontend build directory
FRONTEND_DIR = Path(__file__).parent / "frontend" / "dist"
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
user_sync_service = None
oidc_config = None
oidc_service = None
session_manager = None
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
    - OIDC and session services (Phase 10)
    - Background service startup
    - Resource cleanup at shutdown
    """
    global config_manager, logging_manager, secrets_manager
    global database_manager, redis_manager, sync_service, user_sync_service
    global oidc_config, oidc_service, session_manager, logger

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

    # Initialize Redis manager (Phase 2 - for Ash-Bot data on DB 0)
    try:
        redis_manager = await create_redis_manager(
            config_manager=config_manager,
            secrets_manager=secrets_manager,
            logging_manager=logging_manager,
        )
        if redis_manager.is_connected:
            logger.info("Redis manager initialized and connected (DB 0 - Ash-Bot data)")
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

    # Initialize User Sync Service (Phase 10 - for auth)
    user_sync_service = create_user_sync_service(
        db_manager=database_manager,
        logging_manager=logging_manager,
    )
    logger.info("User sync service initialized")

    # =========================================================================
    # OIDC Authentication Services (Phase 10)
    # =========================================================================

    # Initialize OIDC Config Manager
    try:
        oidc_config = await create_oidc_config_manager(
            config_manager=config_manager,
            logging_manager=logging_manager,
        )
        logger.info("OIDC config manager initialized")

        # Check for required configuration
        if not oidc_config.client_id:
            logger.warning(
                "⚠️  OIDC Client ID not configured! "
                "Set DASH_OIDC_CLIENT_ID in environment."
            )
        if not secrets_manager.has_oidc_credentials():
            logger.warning(
                "⚠️  OIDC Client Secret not configured! "
                "Create secrets/oidc_client_secret file."
            )

    except Exception as e:
        logger.error(f"Failed to initialize OIDC config: {e}")
        oidc_config = None

    # Initialize OIDC Service
    if oidc_config:
        try:
            oidc_service = create_oidc_service(
                oidc_config=oidc_config,
                secrets_manager=secrets_manager,
                logging_manager=logging_manager,
            )
            logger.info("OIDC service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize OIDC service: {e}")
            oidc_service = None
    else:
        logger.warning("OIDC service not initialized (config not available)")
        oidc_service = None

    # Initialize Session Manager (uses separate Redis DB)
    if oidc_config:
        try:
            session_manager = await create_session_manager(
                config_manager=config_manager,
                secrets_manager=secrets_manager,
                oidc_config=oidc_config,
                logging_manager=logging_manager,
            )
            logger.info("Session manager initialized")
        except Exception as e:
            logger.error(f"Failed to initialize session manager: {e}")
            logger.warning("Authentication will not be available!")
            session_manager = None
    else:
        logger.warning("Session manager not initialized (OIDC config not available)")
        session_manager = None

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
    app.state.user_sync_service = user_sync_service
    app.state.oidc_config = oidc_config
    app.state.oidc_service = oidc_service
    app.state.session_manager = session_manager

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

    # Close session manager (separate Redis connection)
    if session_manager:
        await session_manager.close()

    # Cleanup Redis connection (Ash-Bot data)
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

# CORS Middleware (must be added AFTER auth middleware due to reverse order)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication Middleware (Phase 10 - OIDC Session-Based)
# Note: Middleware is applied in reverse order, so CORS runs first, then Auth
#
# This middleware:
# - Reads session ID from cookie
# - Validates session against Redis session store
# - Computes role from session data
# - Injects UserContext into request.state.user
# - Returns 401 for unauthenticated requests (except bypass paths)
# - Returns 403 for non-CRT members
#
# The middleware checks DASH_OIDC_ENABLED env var automatically.
# To disable auth for development, set DASH_OIDC_ENABLED=false in .env
# WARNING: Never disable authentication in production!
app.add_middleware(
    AuthMiddleware,
    bypass_paths=[
        "/health",
        "/health/ready",
        "/health/detailed",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/auth/login",
        "/auth/callback",
        "/auth/logout",
    ],
)


# =============================================================================
# Routes
# =============================================================================

# Health check routes
app.include_router(health_router)

# API routes
app.include_router(sessions_router)
app.include_router(users_router)
app.include_router(dashboard_router)
app.include_router(notes_router)
app.include_router(wiki_router)
app.include_router(archives_router)
app.include_router(admin_router)

# Auth routes (OIDC flow - no /api prefix)
app.include_router(auth_router)
# Auth API routes (/api/auth/me, etc.)
app.include_router(auth_api_router)


# =============================================================================
# Frontend Static Files (Phase 3)
# =============================================================================

# Check if frontend is built
if FRONTEND_DIR.exists() and (FRONTEND_DIR / "index.html").exists():
    # Mount static assets (CSS, JS, images)
    app.mount(
        "/assets",
        StaticFiles(directory=FRONTEND_DIR / "assets"),
        name="assets",
    )

    # Serve favicon
    @app.get("/favicon.svg", include_in_schema=False)
    async def favicon():
        """Serve favicon."""
        favicon_path = FRONTEND_DIR / "favicon.svg"
        if favicon_path.exists():
            return FileResponse(favicon_path, media_type="image/svg+xml")
        return FileResponse(status_code=404)

    # SPA Fallback - serve index.html for all non-API routes
    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(request: Request, full_path: str):
        """
        Serve the Vue.js SPA for all non-API routes.
        This enables client-side routing to work correctly.
        """
        # Don't serve SPA for API routes (they're handled by routers)
        # The routers are already registered and will take precedence
        index_path = FRONTEND_DIR / "index.html"
        return FileResponse(index_path)

else:
    # Frontend not built - show API info at root
    @app.get("/", tags=["Root"])
    async def root():
        """
        Root endpoint with service information.
        Shows when frontend is not built.
        """
        return {
            "service": __app_name__,
            "description": __description__,
            "version": __version__,
            "docs": "/docs",
            "health": "/health",
            "frontend": "Not built - run 'npm run build' in frontend/",
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
