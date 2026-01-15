---
title: Deployment Guide
description: Complete guide for deploying Ash-Dash to production
category: Operations
tags:
  - deployment
  - docker
  - production
  - setup
author: Tech Team
last_updated: "2026-01-10"
version: "1.0"
---

# Deployment Guide

Complete instructions for deploying Ash-Dash to production for [The Alphabet Cartel](https://discord.gg/alphabetcartel).

## Prerequisites

### Server Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| **CPU** | 2 cores | 4 cores |
| **RAM** | 2 GB | 4 GB |
| **Disk** | 20 GB | 50 GB |
| **OS** | Debian 12 / Ubuntu 24.04 | Debian 12 |

### Software Requirements

- Docker Engine 24.0+
- Docker Compose v2.20+
- Git

### Network Requirements

| Port | Service | Access |
|------|---------|--------|
| 30883 | Ash-Dash API | Internal/Reverse Proxy |
| 5432 | PostgreSQL | Internal only |

### External Services

- **Redis** — Running on Ash-Bot server (10.20.30.253)
- **MinIO** — Running on Syn VM (10.20.30.202)
- **PocketID** — OIDC provider (id.alphabetcartel.net)

## Step 1: Clone Repository

```bash
cd /storage/nas/git/ash
git clone https://github.com/the-alphabet-cartel/ash-dash.git
cd ash-dash
```

## Step 2: Create Secrets

Create the secrets directory and files:

```bash
mkdir -p secrets
chmod 700 secrets
```

### Required Secrets

| Secret File | Description | How to Generate |
|-------------|-------------|-----------------|
| `postgres_token` | PostgreSQL password | `openssl rand -base64 32` |
| `archive_master_key` | AES-256 encryption key | `openssl rand -base64 32` |
| `minio_root_user` | MinIO username | From MinIO setup |
| `minio_root_password` | MinIO password | From MinIO setup |
| `oidc_client_secret` | PocketID client secret | From PocketID setup |
| `redis_token` | Redis password | From Redis config |
| `discord_alert_token` | Discord webhook URL | Create in Discord |
| `webhook_token` | Generic webhook token | `openssl rand -hex 16` |

### Create Each Secret

```bash
# PostgreSQL password
openssl rand -base64 32 > secrets/postgres_token

# Archive encryption key (CRITICAL - BACK THIS UP!)
openssl rand -base64 32 > secrets/archive_master_key

# Copy from your MinIO setup
echo "your-minio-user" > secrets/minio_root_user
echo "your-minio-password" > secrets/minio_root_password

# Copy from PocketID
echo "your-oidc-client-secret" > secrets/oidc_client_secret

# Redis password (from Ash-Bot config)
echo "your-redis-password" > secrets/redis_token

# Discord webhook for alerts
echo "https://discord.com/api/webhooks/..." > secrets/discord_alert_token

# Generic webhook token
openssl rand -hex 16 > secrets/webhook_token
```

### Set Permissions

```bash
chmod 600 secrets/*
```

**CRITICAL:** Back up `archive_master_key` securely! Loss means permanent loss of all archives.

## Step 3: Configure Environment

Copy and edit the environment file:

```bash
cp .env.example .env
nano .env
```

### Essential Settings

```bash
# Application
DASH_ENVIRONMENT=production
DASH_LOG_LEVEL=INFO

# Database
POSTGRES_HOST=ash-dash-db
POSTGRES_PORT=5432
POSTGRES_DATABASE=ashdash
POSTGRES_USER=ash

# Redis (Ash-Bot server)
REDIS_HOST=10.20.30.253
REDIS_PORT=6379
REDIS_DATABASE=0

# MinIO (Syn VM)
MINIO_ENDPOINT=10.20.30.202:9000
MINIO_BUCKET=ash-archives
MINIO_SECURE=false

# OIDC (PocketID)
OIDC_ISSUER=https://id.alphabetcartel.net
OIDC_CLIENT_ID=ash-dash
OIDC_REDIRECT_URI=https://crt.alphabetcartel.net/auth/callback
```

See [Configuration Reference](./configuration.md) for all options.

## Step 4: Create Docker Network

If not already created:

```bash
docker network create ash-network
```

## Step 5: Build and Deploy

```bash
docker compose up -d --build
```

### Verify Deployment

```bash
# Check containers are running
docker ps | grep ash-dash

# Check logs for errors
docker logs ash-dash

# Test health endpoint
curl http://localhost:30883/health
```

Expected response:

```json
{"status": "healthy", "version": "5.0.0"}
```

## Step 6: Configure Reverse Proxy

### NGINX Configuration

Create `/etc/nginx/sites-available/ash-dash`:

```nginx
server {
    listen 80;
    server_name crt.alphabetcartel.net;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name crt.alphabetcartel.net;

    ssl_certificate /etc/letsencrypt/live/crt.alphabetcartel.net/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/crt.alphabetcartel.net/privkey.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    location / {
        proxy_pass http://127.0.0.1:30883;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:

```bash
ln -s /etc/nginx/sites-available/ash-dash /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

### SSL Certificate

Using Certbot:

```bash
certbot --nginx -d crt.alphabetcartel.net
```

## Step 7: Configure PocketID

In PocketID admin panel:

1. Create new OIDC client
2. Client ID: `ash-dash`
3. Redirect URIs: `https://crt.alphabetcartel.net/auth/callback`
4. Grant types: `authorization_code`
5. Response types: `code`
6. Scopes: `openid profile email groups`
7. Copy client secret to `secrets/oidc_client_secret`

## Step 8: Initialize Database

The database initializes automatically on first run. Verify:

```bash
docker exec ash-dash-db psql -U ash -d ashdash -c "\dt"
```

Should show tables: `sessions`, `notes`, `users`, `audit_logs`, etc.

## Step 9: Configure MinIO

Ensure the archive bucket exists:

```bash
# Using mc (MinIO client)
mc alias set syn http://10.20.30.202:9000 $MINIO_USER $MINIO_PASS
mc mb syn/ash-archives
mc policy set none syn/ash-archives
```

## Step 10: Verify Full Deployment

### Health Check

```bash
curl https://crt.alphabetcartel.net/health/detailed
```

### Login Test

1. Navigate to https://crt.alphabetcartel.net
2. Click "Sign in with PocketID"
3. Authenticate with PocketID
4. Verify dashboard loads

### Create Test Session (Development Only)

If testing, create a test session via API or let Ash-Bot create one naturally.

## Post-Deployment

### Enable Monitoring

1. Configure uptime monitoring for `/health`
2. Set up log aggregation if available
3. Configure Discord alerts

### Documentation

1. Update DNS records documentation
2. Document any custom configurations
3. Add to backup schedules

### Notify Team

1. Announce in Discord that Ash-Dash is live
2. Provide URL and basic instructions
3. Schedule training if needed

## Updating

### Standard Update

```bash
cd /storage/nas/git/ash/ash-dash
git pull
docker compose down
docker compose up -d --build
```

### Verify After Update

```bash
# Check version
curl https://crt.alphabetcartel.net/health

# Check logs
docker logs ash-dash --tail 50
```

## Rollback

If update fails:

```bash
# Find previous commit
git log --oneline -10

# Checkout previous version
git checkout <previous-commit>

# Rebuild
docker compose down
docker compose up -d --build
```

---

*Last updated: 2026-01-10*

*For troubleshooting, see the [Troubleshooting Guide](./troubleshooting.md).*

**Built with care for chosen family** 🏳️‍🌈
