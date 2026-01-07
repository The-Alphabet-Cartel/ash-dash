# ============================================================================
# Ash-Dash v5.0 Production Dockerfile (Multi-Stage Build)
# ============================================================================
# FILE VERSION: v5.0-3-3.1-2
# LAST MODIFIED: 2026-01-07
# Repository: https://github.com/the-alphabet-cartel/ash-dash
# Community: The Alphabet Cartel - https://discord.gg/alphabetcartel
# ============================================================================
#
# USAGE:
#   # Build the image
#   docker build -t ghcr.io/the-alphabet-cartel/ash-dash:latest .
#
#   # Run with docker-compose (recommended)
#   docker-compose up -d
#
# MULTI-STAGE BUILD:
#   Stage 1 (frontend): Build Vue.js frontend with Node.js
#   Stage 2 (builder): Install Python dependencies
#   Stage 3 (runtime): Minimal production image with built frontend
#
# DOCKER-FIRST PHILOSOPHY:
#   - No Node.js required on host machine
#   - Frontend built entirely inside Docker
#   - FastAPI serves static files in production
#
# CLEAN ARCHITECTURE: Rule #12 - Environment Version Specificity
#   All pip commands use python3.11 -m pip for version consistency
#
# ============================================================================

# =============================================================================
# Stage 1: Frontend Builder - Build Vue.js application
# =============================================================================
FROM node:20-alpine AS frontend

WORKDIR /frontend

# Copy package files first for layer caching
COPY frontend/package*.json ./

# Install dependencies (generates package-lock.json)
RUN npm install --no-audit --no-fund

# Copy frontend source
COPY frontend/ ./

# Build for production
RUN npm run build


# =============================================================================
# Stage 2: Python Builder - Install Python dependencies
# =============================================================================
FROM python:3.11-slim AS builder

# Set build-time environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY requirements.txt .

# Install Python dependencies
# Rule #12: Use python3.11 -m pip for version specificity
RUN python3.11 -m pip install --upgrade pip && \
    python3.11 -m pip install --no-cache-dir -r requirements.txt


# =============================================================================
# Stage 3: Runtime - Production image
# =============================================================================
FROM python:3.11-slim AS runtime

# Set runtime environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    # Application defaults
    DASH_HOST=0.0.0.0 \
    DASH_PORT=30883 \
    DASH_ENVIRONMENT=production \
    DASH_LOG_LEVEL=INFO \
    DASH_LOG_FORMAT=human \
    TZ=America/Los_Angeles

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Create non-root user for security
RUN groupadd -g 1001 ashgroup && \
    useradd -m -u 1001 -g ashgroup ashuser && \
    mkdir -p /app/logs /app/cache /app/frontend/dist && \
    chown -R ashuser:ashgroup /app

# Copy application code
COPY --chown=ashuser:ashgroup . .

# Copy built frontend from frontend stage
COPY --from=frontend --chown=ashuser:ashgroup /frontend/dist /app/frontend/dist

# Switch to non-root user
USER ashuser

# Expose the application port
EXPOSE 30883

# Health check using curl
# Interval: Check every 30 seconds
# Timeout: Wait up to 10 seconds for response
# Start-period: Give the app 120 seconds to start (for cold starts)
# Retries: Fail after 3 consecutive failures
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:30883/health || exit 1

# Default command - run with uvicorn
# Using python -m uvicorn for proper module resolution
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "30883"]
