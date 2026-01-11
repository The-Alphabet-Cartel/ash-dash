---
title: Troubleshooting Guide
description: Common issues and solutions for Ash-Dash
category: Operations
tags:
  - troubleshooting
  - issues
  - solutions
  - debugging
author: Tech Team
last_updated: "2026-01-10"
version: "1.0"
---

# Troubleshooting Guide

Common issues and solutions for Ash-Dash for [The Alphabet Cartel](https://discord.gg/alphabetcartel).

## Quick Diagnostics

### Check Everything Fast

```bash
# Container status
docker ps | grep ash-dash

# Health check
curl -s http://localhost:30883/health/detailed | jq .

# Recent errors
docker logs ash-dash --since 10m | grep -i error

# Database connection
docker exec ash-dash-db pg_isready -U ash
```

## Application Issues

### Dashboard Won't Load

**Symptoms:**
- Blank page
- Infinite loading
- 502/503 errors

**Solutions:**

1. **Check container is running:**
   ```bash
   docker ps | grep ash-dash
   ```
   If not running:
   ```bash
   docker compose up -d ash-dash
   ```

2. **Check for startup errors:**
   ```bash
   docker logs ash-dash --tail 50
   ```

3. **Check reverse proxy (if using):**
   ```bash
   nginx -t
   systemctl status nginx
   ```

4. **Verify port binding:**
   ```bash
   curl http://localhost:30883/health
   ```

---

### Login Fails / "Unauthorized" Error

**Symptoms:**
- Redirected to login repeatedly
- "Unauthorized" error page
- PocketID login works but Ash-Dash rejects

**Solutions:**

1. **Verify user is in CRT group:**
   - Check PocketID admin → Groups
   - User must be in `ash-dash-crt` or similar

2. **Check OIDC configuration:**
   ```bash
   grep OIDC .env
   ```
   Verify issuer URL and client ID are correct.

3. **Verify client secret:**
   ```bash
   cat secrets/oidc_client_secret
   ```
   Compare with PocketID client settings.

4. **Check callback URL:**
   - Must match exactly in PocketID and .env
   - Include trailing slash if configured that way

5. **Clear browser cookies and retry**

---

### Sessions Not Showing / Stale Data

**Symptoms:**
- Dashboard shows old data
- New sessions from Ash-Bot not appearing
- "Live" indicator but no updates

**Solutions:**

1. **Check Redis connection:**
   ```bash
   docker exec ash-dash python -c "
   import redis
   r = redis.Redis(host='10.20.30.253', port=6379)
   print(r.ping())
   "
   ```

2. **Verify Redis has data:**
   ```bash
   redis-cli -h 10.20.30.253 KEYS "ash:*"
   ```

3. **Check Ash-Bot is running:**
   - Ash-Bot must be writing to Redis
   - Check Ash-Bot logs for errors

4. **Restart to reconnect:**
   ```bash
   docker compose restart ash-dash
   ```

---

### Notes Won't Save

**Symptoms:**
- Note appears to save but disappears
- Error when clicking save
- Note editor unresponsive

**Solutions:**

1. **Check database connection:**
   ```bash
   docker exec ash-dash-db pg_isready -U ash
   ```

2. **Check for database errors:**
   ```bash
   docker logs ash-dash | grep -i "database\|postgres"
   ```

3. **Verify session exists:**
   ```sql
   SELECT id, status FROM sessions WHERE id = 'sess_xxx';
   ```

4. **Check for disk space:**
   ```bash
   df -h
   ```

---

### Archive Operations Fail

**Symptoms:**
- "Archive failed" error
- Archives not appearing
- Decryption errors

**Solutions:**

1. **Check MinIO connection:**
   ```bash
   curl http://10.20.30.202:9000/minio/health/live
   ```

2. **Verify credentials:**
   ```bash
   cat secrets/minio_root_user
   cat secrets/minio_root_password
   ```

3. **Check bucket exists:**
   ```bash
   mc ls syn/ash-archives
   ```

4. **Verify master key:**
   ```bash
   # Key should be 32+ characters
   cat secrets/archive_master_key | wc -c
   ```

5. **Check MinIO logs:**
   ```bash
   docker logs minio --tail 50
   ```

## Database Issues

### Connection Refused

**Symptoms:**
- "Connection refused" errors
- Database health check fails
- Application won't start

**Solutions:**

1. **Check database container:**
   ```bash
   docker ps | grep ash-dash-db
   docker logs ash-dash-db
   ```

2. **Start if not running:**
   ```bash
   docker compose up -d ash-dash-db
   ```

3. **Check password:**
   ```bash
   # Verify secret matches what DB expects
   cat secrets/postgres_token
   ```

4. **Test connection manually:**
   ```bash
   docker exec -it ash-dash-db psql -U ash -d ashdash -c "SELECT 1;"
   ```

---

### Database Full / Out of Space

**Symptoms:**
- Write operations fail
- "No space left on device" errors
- Database becomes read-only

**Solutions:**

1. **Check disk space:**
   ```bash
   df -h
   docker system df
   ```

2. **Clean Docker resources:**
   ```bash
   docker system prune -f
   ```

3. **Archive old sessions:**
   - Move closed sessions to archive storage
   - This frees database space

4. **Vacuum database:**
   ```bash
   docker exec ash-dash-db vacuumdb -U ash -d ashdash -f
   ```

---

### Slow Queries

**Symptoms:**
- Dashboard loads slowly
- Session list takes long to load
- Timeouts on large queries

**Solutions:**

1. **Check for missing indexes:**
   ```sql
   EXPLAIN ANALYZE SELECT * FROM sessions WHERE status = 'active';
   ```

2. **Analyze tables:**
   ```bash
   docker exec ash-dash-db psql -U ash -d ashdash -c "ANALYZE;"
   ```

3. **Check connection pool:**
   - May need to increase POSTGRES_POOL_SIZE

4. **Review query patterns in logs**

## Container Issues

### Container Won't Start

**Symptoms:**
- Container exits immediately
- "Exited (1)" status
- No logs after start

**Solutions:**

1. **Check exit code and logs:**
   ```bash
   docker ps -a | grep ash-dash
   docker logs ash-dash
   ```

2. **Common causes:**
   - Missing secrets file
   - Invalid environment variable
   - Port already in use

3. **Check port conflicts:**
   ```bash
   lsof -i :30883
   ```

4. **Verify secrets exist:**
   ```bash
   ls -la secrets/
   ```

---

### Container Keeps Restarting

**Symptoms:**
- Container in restart loop
- "Restarting" status
- Logs show repeated startup/crash

**Solutions:**

1. **Check logs for crash reason:**
   ```bash
   docker logs ash-dash --tail 100
   ```

2. **Common causes:**
   - Database not ready (dependency issue)
   - Out of memory (OOM killed)
   - Configuration error

3. **Check resource limits:**
   ```bash
   docker stats ash-dash
   ```

4. **Remove restart policy temporarily:**
   ```bash
   docker update --restart=no ash-dash
   docker start ash-dash
   # Debug, then restore:
   docker update --restart=unless-stopped ash-dash
   ```

---

### Out of Memory (OOM)

**Symptoms:**
- Container killed unexpectedly
- "OOMKilled" in docker inspect
- System becomes unresponsive

**Solutions:**

1. **Check if OOM killed:**
   ```bash
   docker inspect ash-dash | grep OOMKilled
   ```

2. **Increase memory limit:**
   Edit docker-compose.yml:
   ```yaml
   deploy:
     resources:
       limits:
         memory: 1G  # Increase from 512M
   ```

3. **Investigate memory leak:**
   ```bash
   docker stats ash-dash
   ```
   Watch if memory grows continuously.

## Network Issues

### Cannot Reach External Services

**Symptoms:**
- Cannot connect to Redis
- Cannot connect to MinIO
- PocketID authentication fails

**Solutions:**

1. **Check network connectivity:**
   ```bash
   docker exec ash-dash ping -c 3 10.20.30.253
   ```

2. **Verify Docker network:**
   ```bash
   docker network inspect ash-network
   ```

3. **Check firewall rules:**
   ```bash
   iptables -L -n | grep -E "6379|9000"
   ```

4. **Test from host:**
   ```bash
   curl http://10.20.30.202:9000/minio/health/live
   ```

---

### DNS Resolution Fails

**Symptoms:**
- "Name resolution failed" errors
- Cannot reach external URLs
- PocketID connection fails

**Solutions:**

1. **Check container DNS:**
   ```bash
   docker exec ash-dash cat /etc/resolv.conf
   ```

2. **Test DNS resolution:**
   ```bash
   docker exec ash-dash nslookup id.alphabetcartel.net
   ```

3. **Use IP instead of hostname** (temporary fix)

4. **Configure Docker DNS:**
   ```json
   // /etc/docker/daemon.json
   {
     "dns": ["8.8.8.8", "8.8.4.4"]
   }
   ```

## Performance Issues

### High CPU Usage

**Solutions:**

1. **Identify the cause:**
   ```bash
   docker exec ash-dash top
   ```

2. **Check for runaway processes**

3. **Review polling intervals:**
   - Reduce SESSION_POLL_INTERVAL if too aggressive

---

### High Memory Usage

**Solutions:**

1. **Monitor memory:**
   ```bash
   docker stats ash-dash
   ```

2. **Restart to clear memory:**
   ```bash
   docker compose restart ash-dash
   ```

3. **Check for memory leaks in application logs**

---

### Slow Response Times

**Solutions:**

1. **Check each component:**
   - Database queries
   - Redis operations
   - MinIO access

2. **Enable debug logging temporarily:**
   ```bash
   DASH_LOG_LEVEL=DEBUG docker compose up -d
   ```

3. **Profile slow requests in logs**

## Getting Help

### Collect Diagnostic Information

Before asking for help, gather:

```bash
# System info
uname -a
docker version
docker compose version

# Container status
docker ps -a | grep ash-dash

# Recent logs
docker logs ash-dash --tail 200 > ash-dash-logs.txt

# Health check
curl -s http://localhost:30883/health/detailed > health.json

# Environment (redact secrets!)
grep -v TOKEN .env > env-sanitized.txt
```

### Where to Get Help

1. **Discord:** Tech support channel
2. **GitHub:** Open an issue with diagnostic info
3. **Emergency:** Contact tech lead directly

---

*Last updated: 2026-01-10*

*For standard procedures, see the [Runbook](./runbook.md).*

**Built with care for chosen family** 🏳️‍🌈
