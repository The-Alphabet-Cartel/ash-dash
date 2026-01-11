---
title: Configuration Reference
description: Complete reference for all Ash-Dash configuration options
category: Operations
tags:
  - configuration
  - environment
  - settings
  - reference
author: Tech Team
last_updated: "2026-01-10"
version: "1.0"
---

# Configuration Reference

Complete reference for all configuration options in Ash-Dash for [The Alphabet Cartel](https://discord.gg/alphabetcartel).

## Configuration Sources

Ash-Dash uses three configuration sources (in order of precedence):

1. **Environment Variables** — Highest priority, from `.env` file
2. **Docker Secrets** — Sensitive values mounted as files
3. **JSON Config Files** — Default values in `config/` directory

## Environment Variables

### Application Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `DASH_ENVIRONMENT` | `development` | Environment: `development`, `staging`, `production` |
| `DASH_HOST` | `0.0.0.0` | Host to bind to |
| `DASH_PORT` | `30883` | Port to listen on |
| `DASH_LOG_LEVEL` | `INFO` | Log level: `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `DASH_LOG_FORMAT` | `human` | Log format: `human`, `json` |
| `TZ` | `America/Los_Angeles` | Timezone for timestamps |

### Database (PostgreSQL)

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRES_HOST` | `ash-dash-db` | PostgreSQL hostname |
| `POSTGRES_PORT` | `5432` | PostgreSQL port |
| `POSTGRES_DATABASE` | `ashdash` | Database name |
| `POSTGRES_USER` | `ash` | Database user |
| `POSTGRES_POOL_SIZE` | `5` | Connection pool size |
| `POSTGRES_POOL_MAX` | `10` | Maximum pool connections |

**Note:** Password is read from Docker secret `postgres_token`.

### Redis

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_HOST` | `localhost` | Redis hostname |
| `REDIS_PORT` | `6379` | Redis port |
| `REDIS_DATABASE` | `0` | Redis database number |
| `REDIS_PREFIX` | `ash:` | Key prefix for namespacing |

**Note:** Password is read from Docker secret `redis_token`.

### MinIO (Object Storage)

| Variable | Default | Description |
|----------|---------|-------------|
| `MINIO_ENDPOINT` | `localhost:9000` | MinIO server endpoint |
| `MINIO_BUCKET` | `ash-archives` | Bucket for archives |
| `MINIO_SECURE` | `false` | Use HTTPS for MinIO |
| `MINIO_REGION` | `us-east-1` | MinIO region |

**Note:** Credentials read from Docker secrets `minio_root_user` and `minio_root_password`.

### OIDC (PocketID)

| Variable | Default | Description |
|----------|---------|-------------|
| `OIDC_ENABLED` | `true` | Enable OIDC authentication |
| `OIDC_ISSUER` | — | PocketID issuer URL (required) |
| `OIDC_CLIENT_ID` | — | OIDC client ID (required) |
| `OIDC_REDIRECT_URI` | — | OAuth callback URL (required) |
| `OIDC_SCOPES` | `openid profile email groups` | Requested scopes |
| `OIDC_SESSION_LIFETIME` | `86400` | Session duration (seconds) |

**Note:** Client secret read from Docker secret `oidc_client_secret`.

### Archive Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `ARCHIVE_ENCRYPTION` | `AES-256-GCM` | Encryption algorithm |
| `ARCHIVE_RETENTION_DEFAULT` | `365` | Default retention (days) |
| `ARCHIVE_RETENTION_EXTENDED` | `1095` | Extended retention (days) |
| `ARCHIVE_RETENTION_PERMANENT` | `2555` | Permanent retention (days) |

**Note:** Master key read from Docker secret `archive_master_key`.

### Alerting

| Variable | Default | Description |
|----------|---------|-------------|
| `ALERTS_ENABLED` | `true` | Enable Discord alerts |
| `ALERTS_MIN_SEVERITY` | `high` | Minimum severity to alert |
| `ALERTS_COOLDOWN` | `300` | Seconds between alerts |

**Note:** Discord webhook read from Docker secret `discord_alert_token`.

### Session Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `SESSION_POLL_INTERVAL` | `10` | Active session poll (seconds) |
| `SESSION_METRICS_INTERVAL` | `30` | Metrics poll (seconds) |
| `SESSION_AUTO_CLOSE_HOURS` | `72` | Auto-close inactive sessions |

## Docker Secrets

All sensitive values use Docker secrets:

| Secret File | Used For |
|-------------|----------|
| `secrets/postgres_token` | PostgreSQL password |
| `secrets/archive_master_key` | Archive encryption key |
| `secrets/minio_root_user` | MinIO username |
| `secrets/minio_root_password` | MinIO password |
| `secrets/oidc_client_secret` | PocketID client secret |
| `secrets/redis_token` | Redis password |
| `secrets/discord_alert_token` | Discord webhook URL |
| `secrets/webhook_token` | Generic webhook auth |

### Reading Secrets in Code

Secrets are mounted at `/run/secrets/<name>`:

```python
def read_secret(name: str) -> str:
    path = f"/run/secrets/{name}"
    with open(path) as f:
        return f.read().strip()
```

## JSON Configuration Files

Located in `config/` directory:

### config/app.json

```json
{
  "name": "Ash-Dash",
  "version": "5.0.0",
  "description": "Crisis Response Dashboard",
  "api": {
    "title": "Ash-Dash API",
    "version": "5.0",
    "docs_url": "/api/docs",
    "redoc_url": "/api/redoc"
  },
  "cors": {
    "origins": ["*"],
    "allow_credentials": true
  }
}
```

### config/logging.json

```json
{
  "version": 1,
  "disable_existing_loggers": false,
  "formatters": {
    "human": {
      "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    },
    "json": {
      "class": "pythonjsonlogger.jsonlogger.JsonFormatter"
    }
  },
  "handlers": {
    "console": {
      "class": "logging.StreamHandler",
      "formatter": "human",
      "stream": "ext://sys.stdout"
    },
    "file": {
      "class": "logging.handlers.RotatingFileHandler",
      "filename": "/app/logs/app.log",
      "maxBytes": 10485760,
      "backupCount": 5
    }
  },
  "root": {
    "level": "INFO",
    "handlers": ["console", "file"]
  }
}
```

### config/wiki.json

```json
{
  "base_path": "/app/docs/wiki",
  "default_category": "general",
  "categories": {
    "crt": "CRT Operations",
    "admin": "Administration",
    "reference": "Reference",
    "training": "Training",
    "operations": "Operations"
  },
  "cache_ttl": 300
}
```

## Environment-Specific Configs

### Development

```bash
DASH_ENVIRONMENT=development
DASH_LOG_LEVEL=DEBUG
OIDC_ENABLED=false
```

### Staging

```bash
DASH_ENVIRONMENT=staging
DASH_LOG_LEVEL=INFO
OIDC_ENABLED=true
```

### Production

```bash
DASH_ENVIRONMENT=production
DASH_LOG_LEVEL=INFO
DASH_LOG_FORMAT=json
OIDC_ENABLED=true
```

## Sample .env File

```bash
# =============================================================================
# Ash-Dash Environment Configuration
# =============================================================================

# Application
DASH_ENVIRONMENT=production
DASH_HOST=0.0.0.0
DASH_PORT=30883
DASH_LOG_LEVEL=INFO
DASH_LOG_FORMAT=human
TZ=America/Los_Angeles

# Database
POSTGRES_HOST=ash-dash-db
POSTGRES_PORT=5432
POSTGRES_DATABASE=ashdash
POSTGRES_USER=ash
POSTGRES_POOL_SIZE=5

# Redis
REDIS_HOST=10.20.30.253
REDIS_PORT=6379
REDIS_DATABASE=0
REDIS_PREFIX=ash:

# MinIO
MINIO_ENDPOINT=10.20.30.202:9000
MINIO_BUCKET=ash-archives
MINIO_SECURE=false
MINIO_REGION=us-east-1

# OIDC (PocketID)
OIDC_ENABLED=true
OIDC_ISSUER=https://id.alphabetcartel.net
OIDC_CLIENT_ID=ash-dash
OIDC_REDIRECT_URI=https://ash-dash.alphabetcartel.net/auth/callback
OIDC_SCOPES=openid profile email groups
OIDC_SESSION_LIFETIME=86400

# Archives
ARCHIVE_RETENTION_DEFAULT=365
ARCHIVE_RETENTION_EXTENDED=1095
ARCHIVE_RETENTION_PERMANENT=2555

# Alerts
ALERTS_ENABLED=true
ALERTS_MIN_SEVERITY=high
ALERTS_COOLDOWN=300

# Session Behavior
SESSION_POLL_INTERVAL=10
SESSION_METRICS_INTERVAL=30
SESSION_AUTO_CLOSE_HOURS=72

# User/Group IDs (for Docker)
PUID=1000
PGID=1000
```

## Validation

Configuration is validated at startup. Errors are logged and the application will not start with invalid configuration.

Common validation errors:

| Error | Cause | Solution |
|-------|-------|----------|
| `OIDC_ISSUER required` | Missing issuer URL | Set OIDC_ISSUER |
| `Invalid POSTGRES_PORT` | Non-numeric port | Use numeric value |
| `Secret not found` | Missing secret file | Create secret file |

---

*Last updated: 2026-01-10*

*For deployment instructions, see the [Deployment Guide](./deployment.md).*

**Built with care for chosen family** 🏳️‍🌈
