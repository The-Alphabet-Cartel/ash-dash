---
title: Operations Runbook
description: Standard operating procedures for Ash-Dash
category: Operations
tags:
  - runbook
  - procedures
  - maintenance
  - operations
author: Tech Team
last_updated: "2026-01-10"
version: "1.0"
---

# Operations Runbook

Standard operating procedures for Ash-Dash for [The Alphabet Cartel](https://discord.gg/alphabetcartel).

## Quick Reference

### Service Locations

| Service | Host | Port | Container |
|---------|------|------|-----------|
| Ash-Dash | Lofn (10.20.30.253) | 30883 | ash-dash |
| PostgreSQL | Lofn | 5432 | ash-dash-db |
| Redis | Lofn | 6379 | ash-bot-redis |
| MinIO | Syn (10.20.30.202) | 9000 | minio |

### Important Paths

| Path | Description |
|------|-------------|
| `/storage/nas/git/ash/ash-dash` | Application code |
| `/storage/nas/git/ash/ash-dash/logs` | Application logs |
| `/storage/nas/git/ash/ash-dash/secrets` | Docker secrets |
| `/storage/nas/git/ash/ash-dash/docs/wiki` | Wiki documentation |

## Daily Operations

### Health Check

Verify system health each day:

```bash
# Check container status
docker ps | grep ash-dash

# Check health endpoint
curl -s http://localhost:30883/health/detailed | jq .

# Check recent logs for errors
docker logs ash-dash --since 24h | grep -i error
```

### Monitoring Dashboard

1. Check uptime monitor for alerts
2. Review Discord alerts channel
3. Spot-check active sessions in Ash-Dash

## Starting Services

### Start All Services

```bash
cd /storage/nas/git/ash/ash-dash
docker compose up -d
```

### Start Individual Service

```bash
# Ash-Dash only
docker compose up -d ash-dash

# Database only
docker compose up -d ash-dash-db
```

### Verify Startup

```bash
# Watch logs during startup
docker compose logs -f ash-dash

# Check health after startup (wait 60 seconds)
curl http://localhost:30883/health
```

## Stopping Services

### Graceful Shutdown

```bash
cd /storage/nas/git/ash/ash-dash
docker compose down
```

### Emergency Stop

```bash
docker kill ash-dash
```

### Stop All (Including Volumes)

⚠️ **WARNING:** This removes database data!

```bash
docker compose down -v
```

## Restarting Services

### Restart All

```bash
docker compose restart
```

### Restart Single Service

```bash
docker compose restart ash-dash
```

### Full Rebuild Restart

```bash
docker compose down
docker compose up -d --build
```

## Log Management

### View Logs

```bash
# Last 100 lines
docker logs ash-dash --tail 100

# Follow logs
docker logs -f ash-dash

# Since specific time
docker logs ash-dash --since "2026-01-10T10:00:00"

# Filter for errors
docker logs ash-dash 2>&1 | grep ERROR
```

### Application Logs

```bash
# View app log
docker exec ash-dash cat /app/logs/app.log

# Follow app log
docker exec ash-dash tail -f /app/logs/app.log

# Search audit log
docker exec ash-dash grep "session.archived" /app/logs/audit.log
```

### Rotate Logs

Logs rotate automatically via Docker and logrotate. Manual rotation:

```bash
# Truncate container logs
truncate -s 0 $(docker inspect --format='{{.LogPath}}' ash-dash)
```

## Database Operations

### Access Database

```bash
docker exec -it ash-dash-db psql -U ash -d ashdash
```

### Common Queries

```sql
-- Count active sessions
SELECT COUNT(*) FROM sessions WHERE status = 'active';

-- Recent sessions
SELECT id, discord_user_id, severity, created_at 
FROM sessions 
ORDER BY created_at DESC 
LIMIT 10;

-- User session count
SELECT discord_user_id, COUNT(*) as session_count 
FROM sessions 
GROUP BY discord_user_id 
ORDER BY session_count DESC 
LIMIT 10;
```

### Backup Database

```bash
# Create backup
docker exec ash-dash-db pg_dump -U ash ashdash > backup_$(date +%Y%m%d).sql

# Compressed backup
docker exec ash-dash-db pg_dump -U ash ashdash | gzip > backup_$(date +%Y%m%d).sql.gz
```

### Restore Database

```bash
# From backup file
cat backup_20260110.sql | docker exec -i ash-dash-db psql -U ash ashdash
```

## Update Procedures

### Standard Update

1. **Announce maintenance** in Discord
2. **Pull latest code:**
   ```bash
   cd /storage/nas/git/ash/ash-dash
   git pull
   ```
3. **Review changes:**
   ```bash
   git log --oneline -5
   ```
4. **Rebuild and restart:**
   ```bash
   docker compose down
   docker compose up -d --build
   ```
5. **Verify health:**
   ```bash
   curl http://localhost:30883/health
   docker logs ash-dash --tail 20
   ```
6. **Announce completion** in Discord

### Hotfix Update

For urgent fixes:

```bash
git pull
docker compose up -d --build --no-deps ash-dash
```

### Rollback

```bash
# Find previous version
git log --oneline -10

# Checkout previous commit
git checkout abc1234

# Rebuild
docker compose down
docker compose up -d --build

# After verification, return to main
git checkout main
```

## Backup Procedures

### Daily Backup (Automated)

Backups run nightly via cron. Verify:

```bash
# Check recent backups
ls -la /storage/nas/backups/ash-dash/

# Verify backup integrity
gzip -t /storage/nas/backups/ash-dash/latest.sql.gz
```

### Manual Backup

```bash
# Full backup script
/storage/nas/git/ash/ash-dash/scripts/backup.sh

# Or manually:
docker exec ash-dash-db pg_dump -U ash ashdash | gzip > \
  /storage/nas/backups/ash-dash/manual_$(date +%Y%m%d_%H%M%S).sql.gz
```

### Archive Key Backup

⚠️ **CRITICAL:** The archive master key must be backed up securely!

```bash
# Copy to secure location (encrypted USB, password manager, etc.)
cat /storage/nas/git/ash/ash-dash/secrets/archive_master_key
```

Store in at least 2 secure locations.

## Security Procedures

### Rotate Database Password

1. Generate new password:
   ```bash
   openssl rand -base64 32 > /tmp/new_postgres_token
   ```

2. Update in PostgreSQL:
   ```bash
   docker exec -it ash-dash-db psql -U ash -c \
     "ALTER USER ash PASSWORD '$(cat /tmp/new_postgres_token)';"
   ```

3. Update secret:
   ```bash
   cp /tmp/new_postgres_token secrets/postgres_token
   rm /tmp/new_postgres_token
   ```

4. Restart application:
   ```bash
   docker compose restart ash-dash
   ```

### Revoke User Access

1. Remove from PocketID group immediately
2. Restart Ash-Dash to clear sessions:
   ```bash
   docker compose restart ash-dash
   ```
3. Review audit logs for user activity

### Security Incident Response

1. **Contain:** Revoke access, isolate if needed
2. **Assess:** Review audit logs, determine scope
3. **Notify:** Alert CRT leadership and relevant parties
4. **Remediate:** Fix vulnerability, rotate credentials
5. **Document:** Write incident report
6. **Review:** Update procedures to prevent recurrence

## Maintenance Windows

### Scheduled Maintenance

1. Announce 24 hours in advance
2. Set maintenance banner (if implemented)
3. Perform maintenance during low-activity hours
4. Verify all systems after maintenance
5. Remove banner and announce completion

### Emergency Maintenance

1. Post immediate notice in Discord
2. Perform necessary fixes
3. Document what happened
4. Conduct post-mortem

## Monitoring Alerts

### Alert Response

| Alert | Response |
|-------|----------|
| Health check failed | Check container status, restart if needed |
| High memory | Restart container, investigate if recurring |
| Database connection failed | Check DB container, verify credentials |
| Redis connection failed | Check Ash-Bot server Redis |
| MinIO connection failed | Check Syn VM MinIO service |

### Escalation

1. **Level 1:** On-call tech responds within 15 minutes
2. **Level 2:** Escalate to tech lead if unresolved in 30 minutes
3. **Level 3:** Escalate to admin team for critical issues

## Disaster Recovery

### Total Service Failure

1. Check server accessibility
2. Check Docker daemon: `systemctl status docker`
3. Start services: `docker compose up -d`
4. If persistent, restore from backup

### Database Corruption

1. Stop application: `docker compose stop ash-dash`
2. Restore from backup (see Backup Procedures)
3. Start application: `docker compose start ash-dash`
4. Verify data integrity

### Complete Rebuild

If everything fails:

1. Fresh clone of repository
2. Restore secrets from backup
3. Restore database from backup
4. Rebuild: `docker compose up -d --build`
5. Verify functionality

---

*Last updated: 2026-01-10*

*For troubleshooting specific issues, see the [Troubleshooting Guide](./troubleshooting.md).*

**Built with care for chosen family** 🏳️‍🌈
