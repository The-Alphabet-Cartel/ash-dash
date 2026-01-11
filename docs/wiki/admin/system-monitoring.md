---
title: System Monitoring Guide
description: How to monitor Ash-Dash system health and performance
category: Administration
tags:
  - admin
  - monitoring
  - health
  - troubleshooting
author: Admin Team
last_updated: "2026-01-10"
version: "1.0"
---

# System Monitoring Guide

This guide covers monitoring the health and performance of Ash-Dash for [The Alphabet Cartel](https://discord.gg/alphabetcartel) administrators.

## System Health Dashboard

Navigate to **Admin → System Health** to view overall system status.

### Service Status Panel

Shows the health of each component:

| Service | Description | Healthy State |
|---------|-------------|---------------|
| **API** | FastAPI backend | Responding to requests |
| **Database** | PostgreSQL | Connected, queries working |
| **Redis** | Real-time cache | Connected to Ash-Bot |
| **MinIO** | Archive storage | Buckets accessible |

### Status Indicators

| Icon | Meaning |
|------|---------|
| 🟢 | Healthy — Service operating normally |
| 🟡 | Degraded — Service has issues but functional |
| 🔴 | Unhealthy — Service unavailable |
| ⚪ | Unknown — Cannot determine status |

## Health Check Endpoints

Ash-Dash exposes health endpoints for external monitoring:

### Basic Health

```
GET /health
```

Returns: `200 OK` if API is running

### Detailed Health

```
GET /health/detailed
```

Returns JSON with all service statuses:

```json
{
  "status": "healthy",
  "timestamp": "2026-01-10T14:30:00Z",
  "services": {
    "database": { "status": "healthy", "latency_ms": 5 },
    "redis": { "status": "healthy", "latency_ms": 2 },
    "minio": { "status": "healthy", "latency_ms": 15 }
  },
  "version": "5.0.0"
}
```

## Monitoring Key Metrics

### Response Times

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| API P95 | < 200ms | > 500ms | > 1000ms |
| Database queries | < 50ms | > 100ms | > 500ms |
| Redis operations | < 10ms | > 50ms | > 100ms |

### Resource Usage

| Resource | Target | Warning | Critical |
|----------|--------|---------|----------|
| Memory | < 256MB | > 400MB | > 512MB |
| CPU | < 25% | > 50% | > 80% |
| Disk (logs) | < 1GB | > 5GB | > 10GB |

### Application Metrics

| Metric | What to Watch |
|--------|---------------|
| Active sessions | Sudden spikes may indicate issues |
| Error rate | Should be < 1% |
| Login failures | Multiple failures may indicate attack |

## Audit Logs

Navigate to **Admin → Audit Logs** to view system activity.

### What's Logged

| Event Type | Examples |
|------------|----------|
| **Authentication** | Login, logout, token refresh |
| **Sessions** | View, create note, close, archive |
| **Admin** | Settings changes, user management |
| **System** | Health check failures, errors |

### Filtering Audit Logs

| Filter | Description |
|--------|-------------|
| **Date Range** | Events within time period |
| **Event Type** | Specific action types |
| **User** | Actions by specific user |
| **Severity** | Info, Warning, Error |

### Sample Audit Entry

```
2026-01-10 14:30:15 | INFO | session.note_created
User: alex@alphabetcartel.org
Session: sess_abc123
Action: Created note (142 characters)
IP: 10.20.30.100
```

## Common Issues and Solutions

### Database Connection Failed

**Symptoms:**
- 🔴 Database status
- "Connection refused" errors
- Sessions not loading

**Solutions:**
1. Check PostgreSQL container is running:
   ```bash
   docker ps | grep ash-dash-db
   ```
2. Verify database credentials in secrets
3. Check database logs:
   ```bash
   docker logs ash-dash-db
   ```
4. Restart database container if needed

### Redis Connection Failed

**Symptoms:**
- 🔴 Redis status
- Real-time updates not working
- Stale session data

**Solutions:**
1. Verify Redis is running (on Ash-Bot server)
2. Check network connectivity to Redis host
3. Verify Redis password in secrets
4. Check Redis logs for errors

### MinIO Connection Failed

**Symptoms:**
- 🔴 MinIO status
- Archive operations failing
- "S3 Error" messages

**Solutions:**
1. Verify MinIO is accessible at configured URL
2. Check MinIO credentials in secrets
3. Verify bucket exists and has proper permissions
4. Check MinIO logs:
   ```bash
   docker logs minio
   ```

### High Memory Usage

**Symptoms:**
- Dashboard slow or unresponsive
- Container restarts
- OOM errors in logs

**Solutions:**
1. Check for memory leaks in logs
2. Restart container to clear memory
3. Review resource limits in docker-compose
4. Consider increasing memory limit

### Slow API Responses

**Symptoms:**
- Dashboard feels sluggish
- API timeout errors
- High latency metrics

**Solutions:**
1. Check database query performance
2. Review for N+1 query issues
3. Check Redis cache hit rate
4. Verify no blocking operations

## Log Locations

### Container Logs

```bash
# API logs
docker logs ash-dash

# Database logs
docker logs ash-dash-db

# Follow logs in real-time
docker logs -f ash-dash
```

### Application Logs

Inside the container at `/app/logs/`:

| File | Contents |
|------|----------|
| `app.log` | General application logs |
| `error.log` | Error-level events only |
| `audit.log` | Security audit events |

### Accessing Logs

```bash
# View recent logs
docker exec ash-dash tail -100 /app/logs/app.log

# Search for errors
docker exec ash-dash grep ERROR /app/logs/app.log
```

## Setting Up External Monitoring

### Uptime Monitoring

Configure external uptime monitoring (e.g., UptimeRobot, Healthchecks.io):

- URL: `https://your-domain/health`
- Interval: 5 minutes
- Alert on: Non-200 response or timeout

### Discord Alerts

Ash-Dash can send alerts to Discord for critical issues:

1. Create a Discord webhook in your alerts channel
2. Add webhook URL to `secrets/discord_alert_token`
3. Configure alert thresholds in settings

### Prometheus/Grafana

For advanced monitoring, Ash-Dash exposes metrics:

```
GET /metrics
```

Configure Prometheus to scrape this endpoint for dashboards.

## Maintenance Windows

### Planned Maintenance

1. Announce in Discord with timeline
2. Set dashboard banner warning
3. Perform maintenance
4. Verify health checks pass
5. Remove banner and announce completion

### Emergency Maintenance

1. Post immediate notice in Discord
2. Perform critical fixes
3. Document what happened
4. Post-mortem review

---

*Last updated: 2026-01-10*

*For emergency support, contact the Tech team in Discord.*

**Built with care for chosen family** 🏳️‍🌈
