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
Test Configuration - Pytest fixtures and shared test utilities
----------------------------------------------------------------------------
FILE VERSION: v5.0-2-2.2-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 2 - Data Layer
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

USAGE:
    # Run all tests
    pytest

    # Run with coverage
    pytest --cov=src

    # Run specific test file
    pytest tests/test_api/test_health.py

FIXTURES PROVIDED:
    - config_manager: ConfigManager instance for testing
    - logging_manager: LoggingConfigManager instance for testing
    - secrets_manager: SecretsManager instance for testing
    - database_manager: DatabaseManager instance for testing (Phase 2)
    - test_client: FastAPI TestClient for API testing
    - authenticated_client: TestClient with mock authentication
    - user_context: Sample UserContext for auth testing
"""

import base64
import json
import os
import sys
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient

# Ensure project root is in path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Set test environment BEFORE imports
os.environ["DASH_ENVIRONMENT"] = "testing"
os.environ["DASH_LOG_LEVEL"] = "DEBUG"
os.environ["DASH_LOG_FORMAT"] = "human"


# =============================================================================
# Configuration Fixtures
# =============================================================================

@pytest.fixture(scope="session")
def test_config_dir() -> Path:
    """Return path to test configuration directory."""
    return PROJECT_ROOT / "src" / "config"


@pytest.fixture(scope="function")
def config_manager():
    """
    Create ConfigManager instance for testing.

    Uses the testing environment configuration.
    """
    from src.managers.config_manager import create_config_manager

    return create_config_manager(environment="testing")


@pytest.fixture(scope="function")
def logging_manager(config_manager):
    """
    Create LoggingConfigManager instance for testing.

    Depends on config_manager fixture.
    """
    from src.managers.logging_config_manager import create_logging_config_manager

    return create_logging_config_manager(
        config_manager=config_manager,
        log_level="DEBUG",
        log_format="human",
        console_output=True,
    )


@pytest.fixture(scope="function")
def secrets_manager():
    """
    Create SecretsManager instance for testing.

    Uses the local secrets directory.
    """
    from src.managers.secrets_manager import create_secrets_manager

    return create_secrets_manager(
        local_path=PROJECT_ROOT / "secrets"
    )


# =============================================================================
# FastAPI Test Client Fixtures
# =============================================================================

@pytest.fixture(scope="function")
def app():
    """
    Create FastAPI application instance for testing.

    Returns fresh app instance for each test.
    """
    # Import here to avoid circular imports
    from main import app as fastapi_app

    return fastapi_app


@pytest.fixture(scope="function")
def test_client(app) -> Generator[TestClient, None, None]:
    """
    Create TestClient for API testing.

    Yields TestClient that can be used to make requests.
    """
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def mock_session_cookie() -> str:
    """
    Create a mock Pocket-ID session cookie for testing.

    Returns a base64-encoded JWT-like cookie with test user data.
    """
    claims = {
        "sub": "test-user-uuid",
        "email": "testuser@alphabetcartel.org",
        "name": "Test User",
        "groups": ["crt"],
        "exp": 9999999999,  # Far future
    }

    # Create a fake JWT (header.payload.signature)
    header = base64.urlsafe_b64encode(
        json.dumps({"alg": "HS256", "typ": "JWT"}).encode()
    ).decode().rstrip("=")

    payload = base64.urlsafe_b64encode(
        json.dumps(claims).encode()
    ).decode().rstrip("=")

    # Fake signature (not verified in Phase 1)
    signature = "fake_signature_for_testing"

    return f"{header}.{payload}.{signature}"


@pytest.fixture(scope="function")
def mock_admin_cookie() -> str:
    """
    Create a mock admin session cookie for testing.

    Returns cookie with admin group membership.
    """
    claims = {
        "sub": "admin-user-uuid",
        "email": "admin@alphabetcartel.org",
        "name": "Admin User",
        "groups": ["admin", "crt"],
        "exp": 9999999999,
    }

    header = base64.urlsafe_b64encode(
        json.dumps({"alg": "HS256", "typ": "JWT"}).encode()
    ).decode().rstrip("=")

    payload = base64.urlsafe_b64encode(
        json.dumps(claims).encode()
    ).decode().rstrip("=")

    signature = "fake_admin_signature"

    return f"{header}.{payload}.{signature}"


@pytest.fixture(scope="function")
def authenticated_client(
    app,
    mock_session_cookie
) -> Generator[TestClient, None, None]:
    """
    Create TestClient with authentication cookie set.

    Useful for testing protected endpoints.
    """
    with TestClient(app) as client:
        client.cookies.set("pocket_id_session", mock_session_cookie)
        yield client


@pytest.fixture(scope="function")
def admin_client(
    app,
    mock_admin_cookie
) -> Generator[TestClient, None, None]:
    """
    Create TestClient with admin authentication.

    Useful for testing admin-only endpoints.
    """
    with TestClient(app) as client:
        client.cookies.set("pocket_id_session", mock_admin_cookie)
        yield client


# =============================================================================
# User Context Fixtures
# =============================================================================

@pytest.fixture(scope="function")
def user_context():
    """
    Create sample UserContext for testing.

    Returns a standard CRT member user.
    """
    from src.api.middleware.auth_middleware import UserContext

    return UserContext(
        user_id="test-user-uuid",
        email="testuser@alphabetcartel.org",
        name="Test User",
        groups=["crt"],
        is_admin=False,
        raw_claims={},
    )


@pytest.fixture(scope="function")
def admin_user_context():
    """
    Create admin UserContext for testing.

    Returns an admin user.
    """
    from src.api.middleware.auth_middleware import UserContext

    return UserContext(
        user_id="admin-user-uuid",
        email="admin@alphabetcartel.org",
        name="Admin User",
        groups=["admin", "crt"],
        is_admin=True,
        raw_claims={},
    )


# =============================================================================
# Cleanup Fixtures
# =============================================================================

@pytest.fixture(autouse=True)
def reset_environment():
    """
    Reset environment variables after each test.

    Ensures test isolation.
    """
    original_env = os.environ.copy()

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


# =============================================================================
# Test Utilities
# =============================================================================

def assert_healthy_response(response) -> None:
    """Assert that a health check response is healthy."""
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") in ("healthy", "ready")


def assert_error_response(response, expected_status: int) -> None:
    """Assert that a response is an error with expected status."""
    assert response.status_code == expected_status
    data = response.json()
    assert data.get("status") == "error"


# =============================================================================
# Database Fixtures (Phase 2)
# =============================================================================

@pytest.fixture(scope="function")
async def database_manager(config_manager, secrets_manager, logging_manager):
    """
    Create DatabaseManager instance for testing.

    Connects to the test database and yields the manager.
    Closes connection after test completes.

    Note: Requires PostgreSQL to be running for integration tests.
    For unit tests, use mock_database_manager instead.
    """
    from src.managers.database import create_database_manager

    manager = await create_database_manager(
        config_manager=config_manager,
        secrets_manager=secrets_manager,
        logging_manager=logging_manager,
        auto_connect=True,
    )

    yield manager

    await manager.close()


@pytest.fixture(scope="function")
def mock_database_manager(mocker):
    """
    Create a mock DatabaseManager for unit testing.

    Use this when you don't need actual database connectivity.
    Requires pytest-mock to be installed.
    """
    from unittest.mock import AsyncMock, MagicMock

    mock = MagicMock()
    mock.is_connected = True
    mock.health_check = AsyncMock(return_value={
        "status": "healthy",
        "connected": True,
        "latency_ms": 1.5,
        "error": None,
        "pool_size": 5,
        "pool_checked_out": 0,
    })
    mock.connect = AsyncMock(return_value=True)
    mock.close = AsyncMock()

    return mock
