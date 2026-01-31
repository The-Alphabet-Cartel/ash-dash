# ============================================================================
# Ash-Dash v5.0 Production Dockerfile (Multi-Stage Build)
# ============================================================================
# FILE VERSION: v5.0-12-1.0-1
# LAST MODIFIED: 2026-01-22
# Repository: https://github.com/the-alphabet-cartel/ash-dash
# Community: The Alphabet Cartel - https://discord.gg/alphabetcartel
# ============================================================================
#
# USAGE:
#   # Build the image
#   docker build -t ghcr.io/the-alphabet-cartel/ash-dash:latest .
#
#   # Run with docker compose (recommended)
#   docker compose up -d
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
# CLEAN ARCHITECTURE COMPLIANCE:
#   - Rule #10: Environment Version Specificity (python3.12 -m pip)
#   - Rule #13: Pure Python entrypoint for PUID/PGID
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
FROM python:3.12-slim AS builder

# Set build-time environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies (including WeasyPrint build deps)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libharfbuzz0b \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements first for layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# =============================================================================
# Stage 3: Runtime - Production image
# =============================================================================
FROM python:3.12-slim AS runtime

# Labels
LABEL maintainer="PapaBearDoes <github.com/PapaBearDoes>"
LABEL org.opencontainers.image.title="Ash-NLP"
LABEL org.opencontainers.image.description="Crisis Detection Dashboard for The Alphabet Cartel"
LABEL org.opencontainers.image.version="5.0.0"
LABEL org.opencontainers.image.vendor="The Alphabet Cartel"
LABEL org.opencontainers.image.url="https://github.com/the-alphabet-cartel/ash-nlp"
LABEL org.opencontainers.image.source="https://github.com/the-alphabet-cartel/ash-nlp"

# Default user/group IDs (can be overridden at runtime via PUID/PGID)
ARG DEFAULT_UID=1000
ARG DEFAULT_GID=1000

# Set runtime environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/app \
    PATH="/opt/venv/bin:$PATH" \
    # Application defaults
    DASH_HOST=0.0.0.0 \
    DASH_PORT=30883 \
    DASH_ENVIRONMENT=production \
    DASH_LOG_LEVEL=INFO \
    DASH_LOG_FORMAT=human \
    TZ=America/Los_Angeles \
    # Force ANSI colors in Docker logs (Charter v5.2.1)
    FORCE_COLOR=1 \
    # Default PUID/PGID
    PUID=${DEFAULT_UID} \
    PGID=${DEFAULT_GID}

# Install runtime dependencies including WeasyPrint system libraries (Phase 7)
# WeasyPrint requires: Pango, HarfBuzz, Cairo, GDK-PixBuf, Fontconfig
# tini: PID 1 signal handling (Rule #13)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    tini \
    # WeasyPrint dependencies (Phase 7 - PDF generation)
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz0b \
    libfontconfig1 \
    libfreetype6 \
    libgdk-pixbuf-2.0-0 \
    libcairo2 \
    # Font support for PDF generation
    fonts-dejavu-core \
    fonts-noto-color-emoji \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Set working directory
WORKDIR ${APP_HOME}

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Create non-root user (will be modified at runtime by entrypoint if PUID/PGID differ)
RUN groupadd -g ${PGID} ash-dash && \
    useradd -m -u ${PUID} -g ${PGID} ash-dash && \
    mkdir -p ${APP_HOME}/logs ${APP_HOME}/cache ${APP_HOME}/frontend/dist && \
    chown -R ${PUID}:${PGID} ${APP_HOME}

# Copy application code
COPY --chown=${PUID}:${PGID} . .

# Copy built frontend from frontend stage
COPY --from=frontend --chown=${PUID}:${PGID} /frontend/dist ${APP_HOME}/frontend/dist

# Copy and set up entrypoint script (Rule #13: Pure Python PUID/PGID handling)
COPY docker-entrypoint.py ${APP_HOME}/docker-entrypoint.py
RUN chmod +x ${APP_HOME}/docker-entrypoint.py

# NOTE: We do NOT switch to USER ashuser here!
# The entrypoint script handles user switching at runtime after fixing permissions.
# This allows PUID/PGID to work correctly with mounted volumes.

# Expose the application port
EXPOSE 30883

# Health check using curl
# Interval: Check every 30 seconds
# Timeout: Wait up to 10 seconds for response
# Start-period: Give the app 120 seconds to start (for cold starts)
# Retries: Fail after 3 consecutive failures
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:30883/health || exit 1

# Use tini as init system for proper signal handling
# Then our Python entrypoint for PUID/PGID handling (Rule #13)
ENTRYPOINT ["/usr/bin/tini", "--", "python", "/app/docker-entrypoint.py"]

# Default command - run with uvicorn
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "30883"]
