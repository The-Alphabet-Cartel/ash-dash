# 🔧 Ash Dashboard Troubleshooting Guide v2.1

**Problem Resolution & Maintenance Manual**  
**Repository:** https://github.com/the-alphabet-cartel/ash-dash  
**Updated for:** Dedicated Server & Production Environment

## 📋 Troubleshooting Overview

This comprehensive troubleshooting guide covers common issues, diagnostic procedures, and resolution steps for the Ash Dashboard in production deployment. All procedures are tested on the dedicated Debian 12 server environment.

### 🚨 Emergency Contacts

**Critical Issues:**
- **Discord:** #crisis-response (immediate escalation)
- **Technical Support:** #tech-support 
- **Emergency Contact:** Crisis Response Lead

**Non-Critical Issues:**
- **GitHub Issues:** https://github.com/the-alphabet-cartel/ash-dash/issues
- **Documentation:** Complete guides in `/docs` directory

## 🔍 Diagnostic Tools & Commands

### Quick System Check

```bash
#!/bin/bash
# Quick system diagnostic script

echo "=== ASH DASHBOARD SYSTEM DIAGNOSTICS ==="
echo "Timestamp: $(date)"
echo "Server: $(hostname) - $(uname -a)"
echo ""

echo "=== DOCKER SERVICES STATUS ==="
docker-compose ps
echo ""

echo "=== SYSTEM RESOURCES ==="
echo "CPU Usage:"
top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4"%"}'

echo "Memory Usage:"
free -h | awk 'NR==2{printf "Memory Usage: %s/%s (%.2f%%)\n", $3,$2,$3*100/$2 }'

echo "Disk Usage:"
df -h | awk '$NF=="/"{printf "Disk Usage: %d/%dGB (%s)\n", $3,$2,$5}'

echo ""
echo "=== APPLICATION HEALTH ==="
echo "Dashboard API:"
curl -s -k https://10.20.30.253:8883/health | jq '.' 2>/dev/null || echo "API health check failed"

echo ""
echo "Service Integration:"
curl -s -k https://10.20.30.253:8883/api/services/status | jq '.' 2>/dev/null || echo "Service status check failed"

echo ""
echo "=== DATABASE STATUS ==="
docker-compose exec postgres pg_isready -U ash_user -d ash_dashboard
echo ""

echo "=== REDIS STATUS ==="
docker-compose exec redis redis-cli ping
echo ""

echo "=== RECENT ERRORS ==="
echo "Application Errors (last 10):"
docker-compose logs ash-dash --tail=10 | grep -i error || echo "No recent application errors"

echo ""
echo "Database Errors (last 5):"
docker-compose logs postgres --tail=5 | grep -i error || echo "No recent database errors"

echo ""
echo "=== NETWORK CONNECTIVITY ==="
echo "External Service Connectivity:"
curl -s -o /dev/null -w "ash-bot: %{http_code} (%{time_total}s)\n" http://10.20.30.253:8882/health || echo "ash-bot: Connection failed"
curl -s -o /dev/null -w "ash-nlp: %{http_code} (%{time_total}s)\n" http://10.20.30.253:8881/health || echo "ash-nlp: Connection failed"
curl -s -o /dev/null -w "ash-thrash: %{http_code} (%{time_total}s)\n" http://10.20.30.253:8884/health || echo "ash-thrash: Connection failed"

echo ""
echo "=== DIAGNOSTICS COMPLETE ==="
```

Save this as `/opt/ash/ash-dash/scripts/diagnostics.sh` and run:

```bash
chmod +x /opt/ash/ash-dash/scripts/diagnostics.sh
/opt/ash/ash-dash/scripts/diagnostics.sh
```

## 🚨 Common Issues & Solutions

### Application Startup Issues

#### Issue: Dashboard Service Won't Start

**Symptoms:**
- Container exits immediately
- "Connection refused" errors
- Health check failures

**Diagnostic Steps:**
```bash
# Check container status
docker-compose ps

# View detailed logs
docker-compose logs ash-dash --tail=50

# Check environment variables
docker-compose exec ash-dash env | grep -E "(GLOBAL_ENVIRONMENT|GLOBAL_DASH_API_PORT|THRASH_DATABASE_URL)"

# Test configuration
docker-compose config
```

**Common Solutions:**

1. **Environment Variable Issues:**
```bash
# Verify .env file exists and is readable
ls -la /opt/ash/ash-dash/.env
cat /opt/ash/ash-dash/.env | head -10

# Check for missing required variables
grep -E "(THRASH_DATABASE_URL|JWT_SECRET|DISCORD_CLIENT)" /opt/ash/ash-dash/.env
```

2. **Database Connection Issues:**
```bash
# Test database connectivity
docker-compose exec postgres pg_isready -U ash_user -d ash_dashboard

# Check database credentials
docker-compose exec ash-dash node -e "
const { Pool } = require('pg');
const pool = new Pool({ connectionString: process.env.THRASH_DATABASE_URL });
pool.query('SELECT NOW()', (err, res) => {
  console.log(err ? 'DB Error: ' + err.message : 'DB Connected: ' + res.rows[0].now);
  pool.end();
});
"
```

3. **Port Conflicts:**
```bash
# Check if port 8883 is already in use
sudo netstat -tlpn | grep :8883
sudo lsof -i :8883

# Kill conflicting processes if necessary
sudo fuser -k 8883/tcp
```

4. **SSL Certificate Issues:**
```bash
# Check certificate files
ls -la /opt/ash/ash-dash/certs/
openssl x509 -in /opt/ash/ash-dash/certs/cert.pem -text -noout | grep -E "(Subject|Not After)"

# Regenerate self-signed certificates if needed
cd /opt/ash/ash-dash
openssl req -x509 -newkey rsa:4096 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes -subj "/C=US/ST=WA/L=Lacey/O=The Alphabet Cartel/CN=dashboard.alphabetcartel.net"
chmod 600 certs/key.pem
chmod 644 certs/cert.pem
```

#### Issue: Slow Application Startup

**Symptoms:**
- Long container startup times
- Timeout errors during initialization
- Health checks failing initially

**Diagnostic Steps:**
```bash
# Monitor startup process
docker-compose logs ash-dash -f &
docker-compose restart ash-dash

# Check resource usage during startup
htop &
docker stats ash-dash
```

**Solutions:**

1. **Increase Startup Timeouts:**
```yaml
# In docker-compose.yml
healthcheck:
  test: ["CMD", "curl", "-f", "https://localhost:8883/health"]
  interval: 30s
  timeout: 15s  # Increased from 10s
  retries: 5    # Increased from 3
  start_period: 180s  # Increased from 120s
```

2. **Optimize Database Connections:**
```bash
# Reduce initial connection pool size in .env
DB_POOL_MIN=2
DB_POOL_MAX=20
DB_CONNECTION_TIMEOUT=30000
```

### Database Issues

#### Issue: PostgreSQL Connection Failures

**Symptoms:**
- "Connection refused" errors
- Database queries timing out
- Transaction deadlocks

**Diagnostic Steps:**
```bash
# Check PostgreSQL container status
docker-compose logs postgres --tail=20

# Test database connectivity
docker-compose exec postgres pg_isready

# Check active connections
docker-compose exec postgres psql -U ash_user -d ash_dashboard -c "
SELECT count(*) as active_connections, 
       max_conn, 
       max_conn-count(*) as available_connections 
FROM pg_stat_activity, 
     (SELECT setting::int as max_conn FROM pg_settings WHERE name='max_connections') mc;"

# Check database locks
docker-compose exec postgres psql -U ash_user -d ash_dashboard -c "
SELECT blocked_locks.pid AS blocked_pid,
       blocked_activity.usename AS blocked_user,
       blocking_locks.pid AS blocking_pid,
       blocking_activity.usename AS blocking_user,
       blocked_activity.query AS blocked_statement,
       blocking_activity.query AS current_statement_in_blocking_process
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;"
```

**Solutions:**

1. **Connection Pool Optimization:**
```bash
# Update .env file
DB_MAX_CONNECTIONS=50
DB_IDLE_TIMEOUT=30000
DB_CONNECTION_TIMEOUT=10000

# Restart application
docker-compose restart ash-dash
```

2. **Database Performance Tuning:**
```sql
-- Connect to database
docker-compose exec postgres psql -U ash_user -d ash_dashboard

-- Analyze table statistics
ANALYZE;

-- Check slow queries
SELECT query, mean_time, calls, total_time 
FROM pg_stat_statements 
ORDER BY total_time DESC 
LIMIT 10;

-- Vacuum and reindex if needed
VACUUM ANALYZE;
REINDEX DATABASE ash_dashboard;
```

3. **Memory Configuration:**
```bash
# Increase PostgreSQL memory settings in docker-compose.yml
services:
  postgres:
    command: >
      postgres 
      -c shared_buffers=2GB
      -c effective_cache_size=12GB
      -c maintenance_work_mem=512MB
      -c checkpoint_completion_target=0.9
      -c wal_buffers=16MB
      -c default_statistics_target=100
```

#### Issue: Database Disk Space Full

**Symptoms:**
- "No space left on device" errors
- Write operations failing
- Database becoming read-only

**Diagnostic Steps:**
```bash
# Check disk usage
df -h
du -sh /opt/ash/ash-dash/data/postgres/*

# Check database sizes
docker-compose exec postgres psql -U ash_user -d ash_dashboard -c "
SELECT datname, pg_size_pretty(pg_database_size(datname)) as size 
FROM pg_database 
ORDER BY pg_database_size(datname) DESC;"

# Check table sizes
docker-compose exec postgres psql -U ash_user -d ash_dashboard -c "
SELECT schemaname,tablename,attname,n_distinct,correlation 
FROM pg_stats 
WHERE schemaname = 'public' 
ORDER BY schemaname,tablename,attname;"
```

**Solutions:**

1. **Immediate Space Recovery:**
```bash
# Clean old log files
find /opt/ash/ash-dash/logs -name "*.log" -mtime +7 -delete
docker system prune -f

# Vacuum database to reclaim space
docker-compose exec postgres psql -U ash_user -d ash_dashboard -c "VACUUM FULL;"
```

2. **Archive Old Data:**
```sql
-- Archive old audit logs (older than 90 days)
DELETE FROM audit_logs WHERE created_at < NOW() - INTERVAL '90 days';

-- Archive old system metrics (older than 30 days)
DELETE FROM system_metrics WHERE recorded_at < NOW() - INTERVAL '30 days';
```

3. **Setup Log Rotation:**
```bash
# Create logrotate configuration
sudo tee /etc/logrotate.d/ash-dashboard << EOF
/opt/ash/ash-dash/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 $(whoami) $(whoami)
    postrotate
        docker-compose -f /opt/ash/ash-dash/docker-compose.yml restart ash-dash
    endscript
}
EOF
```

### Redis Cache Issues

#### Issue: Redis Connection Failures

**Symptoms:**
- Cache misses for all requests
- Session authentication failures
- "Connection refused" to Redis

**Diagnostic Steps:**
```bash
# Check Redis container status
docker-compose logs redis --tail=20

# Test Redis connectivity
docker-compose exec redis redis-cli ping

# Check Redis memory usage
docker-compose exec redis redis-cli info memory

# Check Redis connections
docker-compose exec redis redis-cli info clients

# Test Redis operations
docker-compose exec redis redis-cli set test_key "test_value"
docker-compose exec redis redis-cli get test_key
docker-compose exec redis redis-cli del test_key
```

**Solutions:**

1. **Redis Configuration Issues:**
```bash
# Check Redis configuration
docker-compose exec redis redis-cli config get "*"

# Check Redis logs for errors
docker-compose logs redis | grep -i error

# Restart Redis service
docker-compose restart redis
```

2. **Memory Issues:**
```bash
# Check Redis memory policy
docker-compose exec redis redis-cli config get maxmemory-policy

# Set appropriate memory policy if needed
docker-compose exec redis redis-cli config set maxmemory-policy allkeys-lru

# Flush Redis if corruption suspected
docker-compose exec redis redis-cli flushall
```

3. **Persistence Issues:**
```bash
# Check Redis persistence status
docker-compose exec redis redis-cli lastsave

# Force background save
docker-compose exec redis redis-cli bgsave

# Check Redis data directory
docker-compose exec redis ls -la /data/
```

### Service Integration Issues

#### Issue: External Service Connectivity Problems

**Symptoms:**
- "Service unavailable" errors
- Integration endpoints returning 500 errors
- Timeout errors from external services

**Diagnostic Steps:**
```bash
# Test connectivity to all integrated services
echo "Testing ash-bot connectivity:"
curl -v -m 10 http://10.20.30.253:8882/health

echo "Testing ash-nlp connectivity:"
curl -v -m 10 http://10.20.30.253:8881/health

echo "Testing ash-thrash connectivity:"
curl -v -m 10 http://10.20.30.253:8884/health

# Check network connectivity
ping -c 3 10.20.30.253
telnet 10.20.30.253 8882
telnet 10.20.30.253 8881
telnet 10.20.30.253 8884

# Check firewall rules
sudo ufw status verbose

# Check service endpoints from dashboard
docker-compose exec ash-dash curl -m 10 http://10.20.30.253:8882/health
```

**Solutions:**

1. **Network Configuration:**
```bash
# Update service endpoints in .env if changed
GLOBAL_BOT_API_URL=http://10.20.30.253:8882
GLOBAL_NLP_API_URL=http://10.20.30.253:8881
ASH_TESTING_API=http://10.20.30.253:8884

# Restart dashboard to pick up changes
docker-compose restart ash-dash
```

2. **Timeout Configuration:**
```bash
# Increase service timeouts in .env
SERVICE_TIMEOUT=30000
SERVICE_RETRY_ATTEMPTS=5
SERVICE_RETRY_DELAY=2000

# Restart application
docker-compose restart ash-dash
```

3. **Service Health Monitoring:**
```bash
# Create service monitoring script
cat > /opt/ash/ash-dash/scripts/monitor_services.sh << 'EOF'
#!/bin/bash
services=("8882:ash-bot" "8881:ash-nlp" "8884:ash-thrash")

for service in "${services[@]}"; do
    port=$(echo $service | cut -d: -f1)
    name=$(echo $service | cut -d: -f2)
    
    if curl -s -m 5 http://10.20.30.253:$port/health > /dev/null; then
        echo "$name: HEALTHY"
    else
        echo "$name: UNHEALTHY - Port $port"
        # Send alert to Discord webhook
        curl -X POST "$DISCORD_WEBHOOK_URL" \
             -H "Content-Type: application/json" \
             -d "{\"content\": \"⚠️ Service Alert: $name is unhealthy on port $port\"}"
    fi
done
EOF

chmod +x /opt/ash/ash-dash/scripts/monitor_services.sh
```

### Performance Issues

#### Issue: Slow Response Times

**Symptoms:**
- API responses taking > 5 seconds
- Dashboard loading slowly
- Database query timeouts

**Diagnostic Steps:**
```bash
# Monitor real-time performance
docker stats ash-dash postgres redis

# Check application metrics
curl -s https://10.20.30.253:8883/metrics | grep -E "(response_time|request_duration)"

# Analyze slow queries
docker-compose exec postgres psql -U ash_user -d ash_dashboard -c "
SELECT query, mean_time, calls, total_time 
FROM pg_stat_statements 
WHERE mean_time > 1000
ORDER BY mean_time DESC 
LIMIT 10;"

# Check Redis performance
docker-compose exec redis redis-cli --latency-history -i 1

# Network latency test
time curl -s https://10.20.30.253:8883/api/status > /dev/null
```

**Solutions:**

1. **Database Query Optimization:**
```sql
-- Add missing indexes
CREATE INDEX CONCURRENTLY idx_crises_detected_at_status ON crises(detected_at, status);
CREATE INDEX CONCURRENTLY idx_crisis_responses_created_at ON crisis_responses(created_at);

-- Update table statistics
ANALYZE;

-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch 
FROM pg_stat_user_indexes 
ORDER BY idx_scan DESC;
```

2. **Caching Optimization:**
```bash
# Increase cache TTL values in .env
DASH_CACHE_TTL=600
SESSION_TTL=3600
RATE_LIMIT_TTL=1800

# Preload cache with frequently accessed data
docker-compose exec ash-dash node -e "
// Add cache warming script here
console.log('Cache warming completed');
"
```

3. **Resource Scaling:**
```yaml
# Update docker-compose.yml resource limits
services:
  ash-dash:
    deploy:
      resources:
        limits:
          memory: 24G  # Increased from 16G
          cpus: '6.0'  # Increased from 4.0
        reservations:
          memory: 12G
          cpus: '3.0'
```

#### Issue: High Memory Usage

**Symptoms:**
- Out of memory errors
- Container restarts due to memory limits
- System becoming unresponsive

**Diagnostic Steps:**
```bash
# Check memory usage
free -h
docker stats --no-stream

# Analyze memory usage by process
docker-compose exec ash-dash ps aux --sort=-%mem

# Check for memory leaks
docker-compose exec ash-dash node -e "
console.log('Memory Usage:', process.memoryUsage());
if (global.gc) {
  global.gc();
  console.log('After GC:', process.memoryUsage());
}
"

# Monitor memory over time
watch -n 5 'docker stats --no-stream | head -5'
```

**Solutions:**

1. **Memory Leak Detection:**
```bash
# Enable garbage collection in Node.js
# Update Dockerfile to add --expose-gc flag
CMD ["node", "--expose-gc", "dist/server.js"]

# Monitor memory patterns
docker-compose exec ash-dash node -e "
setInterval(() => {
  const mem = process.memoryUsage();
  console.log(\`\${new Date().toISOString()}: RSS=\${Math.round(mem.rss/1024/1024)}MB, Heap=\${Math.round(mem.heapUsed/1024/1024)}MB\`);
}, 10000);
"
```

2. **Memory Configuration:**
```bash
# Set Node.js memory limits in docker-compose.yml
environment:
  - NODE_OPTIONS=--max-old-space-size=8192

# Adjust garbage collection
environment:
  - NODE_OPTIONS=--max-old-space-size=8192 --gc-interval=100
```

3. **Database Connection Pool Tuning:**
```bash
# Reduce connection pool size
DB_POOL_MAX=25
DB_POOL_MIN=3
DB_IDLE_TIMEOUT=15000
```

### SSL/TLS Issues

#### Issue: Certificate Problems

**Symptoms:**
- "Certificate expired" errors
- "Certificate not trusted" warnings
- SSL handshake failures

**Diagnostic Steps:**
```bash
# Check certificate validity
openssl x509 -in /opt/ash/ash-dash/certs/cert.pem -text -noout | grep -E "(Subject|Issuer|Not Before|Not After)"

# Test SSL connection
openssl s_client -connect 10.20.30.253:8883 -servername dashboard.alphabetcartel.net

# Check certificate chain
curl -vI https://10.20.30.253:8883/health

# Verify certificate permissions
ls -la /opt/ash/ash-dash/certs/
```

**Solutions:**

1. **Certificate Renewal:**
```bash
# For Let's Encrypt certificates
sudo certbot renew --dry-run
sudo certbot renew

# Copy renewed certificates
sudo cp /etc/letsencrypt/live/dashboard.alphabetcartel.net/fullchain.pem /opt/ash/ash-dash/certs/cert.pem
sudo cp /etc/letsencrypt/live/dashboard.alphabetcartel.net/privkey.pem /opt/ash/ash-dash/certs/key.pem
sudo chown $(whoami):$(whoami) /opt/ash/ash-dash/certs/*

# Restart services
docker-compose restart nginx ash-dash
```

2. **Self-Signed Certificate Regeneration:**
```bash
# Generate new self-signed certificate
cd /opt/ash/ash-dash
openssl req -x509 -newkey rsa:4096 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes \
  -subj "/C=US/ST=WA/L=Lacey/O=The Alphabet Cartel/CN=dashboard.alphabetcartel.net" \
  -addext "subjectAltName=DNS:dashboard.alphabetcartel.net,DNS:10.20.30.253,IP:10.20.30.253"

chmod 600 certs/key.pem
chmod 644 certs/cert.pem

# Restart services
docker-compose restart nginx ash-dash
```

### Authentication Issues

#### Issue: Discord OAuth2 Problems

**Symptoms:**
- "Invalid client_id" errors
- Authentication redirects failing
- Users can't log in

**Diagnostic Steps:**
```bash
# Check Discord OAuth2 configuration
grep -E "(DISCORD_CLIENT|DISCORD_REDIRECT)" /opt/ash/ash-dash/.env

# Test OAuth2 endpoint
curl -v "https://discord.com/api/oauth2/authorize?client_id=$DISCORD_CLIENT_ID&redirect_uri=https://dashboard.alphabetcartel.net/auth/callback&response_type=code&scope=identify"

# Check application logs for auth errors
docker-compose logs ash-dash | grep -i "auth\|discord\|oauth"
```

**Solutions:**

1. **Verify Discord Application Settings:**
```bash
# Check Discord Developer Portal settings:
# - Application ID matches DISCORD_CLIENT_ID
# - Client Secret matches DISCORD_CLIENT_SECRET
# - Redirect URI matches exactly: https://dashboard.alphabetcartel.net/auth/callback
# - Bot permissions are correctly set
```

2. **Update OAuth2 Configuration:**
```bash
# Update .env with correct values
DISCORD_CLIENT_ID=your_correct_client_id
DISCORD_CLIENT_SECRET=your_correct_client_secret
DISCORD_REDIRECT_URI=https://dashboard.alphabetcartel.net/auth/callback

# Restart application
docker-compose restart ash-dash
```

3. **Session Issues:**
```bash
# Clear Redis sessions
docker-compose exec redis redis-cli flushdb

# Check session configuration
grep -E "(GLOBAL_SESSION_TOKEN|JWT_SECRET)" /opt/ash/ash-dash/.env

# Generate new session secrets if needed
openssl rand -base64 32
```

## 🔄 Recovery Procedures

### Complete System Recovery

#### Scenario: Total System Failure

**Recovery Steps:**

1. **Assess System State:**
```bash
# Check what's running
docker ps -a
systemctl status docker

# Check disk space and system resources
df -h
free -h
dmesg | tail -20
```

2. **Stop All Services:**
```bash
cd /opt/ash/ash-dash
docker-compose down -v
docker system prune -f
```

3. **Restore from Backup:**
```bash
# Find latest backup
ls -la /opt/ash/ash-dash/backups/database/ | tail -5

# Restore database
LATEST_DB_BACKUP=$(ls -t /opt/ash/ash-dash/backups/database/*.sql.gz | head -1)
echo "Restoring from: $LATEST_DB_BACKUP"

# Start only database container
docker-compose up -d postgres
sleep 30

# Restore database
gunzip -c "$LATEST_DB_BACKUP" | docker exec -i ash_dashboard_postgres psql -U ash_user -d ash_dashboard

# Restore Redis data
LATEST_REDIS_BACKUP=$(ls -t /opt/ash/ash-dash/backups/redis/*.rdb | head -1)
docker cp "$LATEST_REDIS_BACKUP" ash_dashboard_redis:/data/dump.rdb

# Restore configuration
LATEST_CONFIG_BACKUP=$(ls -t /opt/ash/ash-dash/backups/configuration/*.tar.gz | head -1)
tar -xzf "$LATEST_CONFIG_BACKUP" -C /
```

4. **Restart All Services:**
```bash
# Start all services
docker-compose up -d

# Monitor startup
docker-compose logs -f
```

5. **Verify Recovery:**
```bash
# Run full diagnostic
/opt/ash/ash-dash/scripts/diagnostics.sh

# Test critical functionality
curl -k https://10.20.30.253:8883/health
curl -k https://10.20.30.253:8883/api/services/status
```

### Database Recovery Procedures

#### Scenario: Database Corruption

**Recovery Steps:**

1. **Identify Corruption:**
```bash
# Check database integrity
docker-compose exec postgres psql -U ash_user -d ash_dashboard -c "
SELECT datname, pg_size_pretty(pg_database_size(datname)) as size 
FROM pg_database;"

# Check for corruption errors
docker-compose logs postgres | grep -i "corrupt\|error\|fatal"

# Run database checks
docker-compose exec postgres psql -U ash_user -d ash_dashboard -c "
SELECT tablename, pg_size_pretty(pg_total_relation_size(tablename::regclass)) as size
FROM pg_tables 
WHERE schemaname = 'public' 
ORDER BY pg_total_relation_size(tablename::regclass) DESC;"
```

2. **Attempt Repair:**
```bash
# Try VACUUM and REINDEX
docker-compose exec postgres psql -U ash_user -d ash_dashboard -c "
VACUUM FULL VERBOSE;
REINDEX DATABASE ash_dashboard;
ANALYZE;"

# Check if repair was successful
docker-compose exec postgres psql -U ash_user -d ash_dashboard -c "
SELECT count(*) FROM users;
SELECT count(*) FROM crises;
SELECT count(*) FROM crisis_responses;"
```

3. **Full Database Restore if Repair Fails:**
```bash
# Stop application to prevent new writes
docker-compose stop ash-dash

# Create backup of current state (for forensics)
docker exec ash_dashboard_postgres pg_dump -U ash_user -d ash_dashboard > /opt/ash/ash-dash/backups/corrupt_db_$(date +%Y%m%d_%H%M%S).sql

# Drop and recreate database
docker-compose exec postgres psql -U postgres -c "
DROP DATABASE ash_dashboard;
CREATE DATABASE ash_dashboard OWNER ash_user;"

# Restore from latest good backup
LATEST_BACKUP=$(ls -t /opt/ash/ash-dash/backups/database/*.sql.gz | head -1)
gunzip -c "$LATEST_BACKUP" | docker exec -i ash_dashboard_postgres psql -U ash_user -d ash_dashboard

# Restart application
docker-compose start ash-dash
```

### Application Recovery

#### Scenario: Application Won't Start After Update

**Recovery Steps:**

1. **Rollback to Previous Version:**
```bash
# Check available versions
docker images | grep ash-dash

# Stop current deployment
docker-compose down

# Rollback to previous image version
sed -i 's/ash-dash:latest/ash-dash:v2.0.0/' docker-compose.yml

# Start with previous version
docker-compose up -d
```

2. **Configuration Rollback:**
```bash
# Restore previous configuration
LATEST_CONFIG=$(ls -t /opt/ash/ash-dash/backups/configuration/*.tar.gz | head -1)
tar -xzf "$LATEST_CONFIG" -C /opt/ash/ash-dash/ --strip-components=4
```

3. **Verify Rollback:**
```bash
# Test functionality
curl -k https://10.20.30.253:8883/health
docker-compose logs ash-dash --tail=20
```

## 🔧 Maintenance Procedures

### Regular Maintenance Tasks

#### Daily Maintenance

```bash
#!/bin/bash
# Daily maintenance script

echo "=== DAILY MAINTENANCE - $(date) ==="

# Health checks
echo "1. Running health checks..."
/opt/ash/ash-dash/scripts/diagnostics.sh | grep -E "(FAILED|ERROR|DOWN)"

# Log rotation
echo "2. Rotating logs..."
find /opt/ash/ash-dash/logs -name "*.log" -size +100M -exec gzip {} \;

# Cleanup temporary files
echo "3. Cleaning temporary files..."
find /opt/ash/ash-dash/data/temp -type f -mtime +1 -delete

# Database maintenance
echo "4. Database maintenance..."
docker-compose exec postgres psql -U ash_user -d ash_dashboard -c "
SELECT pg_size_pretty(pg_database_size('ash_dashboard')) as db_size;
SELECT count(*) as audit_entries FROM audit_logs WHERE created_at > NOW() - INTERVAL '1 day';
"

# Monitor disk space
echo "5. Disk space check..."
df -h | awk '$NF=="/"{if($5+0 > 85) print "WARNING: Disk usage is " $5}'

# Service monitoring
echo "6. Service monitoring..."
/opt/ash/ash-dash/scripts/monitor_services.sh

echo "=== DAILY MAINTENANCE COMPLETE ==="
```

#### Weekly Maintenance

```bash
#!/bin/bash
# Weekly maintenance script

echo "=== WEEKLY MAINTENANCE - $(date) ==="

# Deep database maintenance
echo "1. Database optimization..."
docker-compose exec postgres psql -U ash_user -d ash_dashboard -c "
VACUUM ANALYZE;
REINDEX DATABASE ash_dashboard;
"

# Update system packages
echo "2. System updates..."
sudo apt update
sudo apt list --upgradable

# Security updates only
sudo unattended-upgrades

# Docker cleanup
echo "3. Docker cleanup..."
docker system prune -f
docker image prune -f

# Log analysis
echo "4. Log analysis..."
echo "Recent errors:"
docker-compose logs ash-dash --since=168h | grep -i error | tail -10

echo "Top error patterns:"
docker-compose logs ash-dash --since=168h | grep -i error | awk '{print $NF}' | sort | uniq -c | sort -nr | head -5

# Performance metrics
echo "5. Performance metrics..."
docker-compose exec ash-dash curl -s http://localhost:9090/metrics | grep -E "(http_request_duration|memory_usage|cpu_usage)" | tail -10

# Backup verification
echo "6. Backup verification..."
LATEST_BACKUP=$(ls -t /opt/ash/ash-dash/backups/database/*.sql.gz | head -1)
echo "Latest backup: $LATEST_BACKUP ($(ls -lh "$LATEST_BACKUP" | awk '{print $5}'))"

# Test backup integrity
gunzip -t "$LATEST_BACKUP" && echo "Backup integrity: OK" || echo "Backup integrity: FAILED"

echo "=== WEEKLY MAINTENANCE COMPLETE ==="
```

#### Monthly Maintenance

```bash
#!/bin/bash
# Monthly maintenance script

echo "=== MONTHLY MAINTENANCE - $(date) ==="

# Full system backup
echo "1. Creating full system backup..."
/opt/ash/ash-dash/scripts/backup.sh

# Database statistics update
echo "2. Updating database statistics..."
docker-compose exec postgres psql -U ash_user -d ash_dashboard -c "
UPDATE pg_class SET reltuples=-1, relpages=-1;
ANALYZE;
"

# Performance analysis
echo "3. Performance analysis..."
docker-compose exec postgres psql -U ash_user -d ash_dashboard -c "
SELECT schemaname, tablename, n_tup_ins, n_tup_upd, n_tup_del 
FROM pg_stat_user_tables 
ORDER BY n_tup_ins + n_tup_upd + n_tup_del DESC 
LIMIT 10;
"

# Security audit
echo "4. Security audit..."
# Check for unauthorized access attempts
docker-compose logs nginx --since=720h | grep -E "(401|403|404)" | tail -20

# Check SSL certificate expiry
openssl x509 -in /opt/ash/ash-dash/certs/cert.pem -noout -dates

# Archive old logs
echo "5. Log archival..."
find /opt/ash/ash-dash/logs -name "*.log" -mtime +30 -exec gzip {} \;
find /opt/ash/ash-dash/logs -name "*.gz" -mtime +90 -delete

# Update documentation
echo "6. Documentation updates..."
/opt/ash/ash-dash/scripts/diagnostics.sh > /opt/ash/ash-dash/docs/latest_system_status.txt

echo "=== MONTHLY MAINTENANCE COMPLETE ==="
```

### Emergency Procedures

#### Scenario: Crisis Response System Down

**Immediate Actions (< 5 minutes):**

```bash
# 1. Quick service restart
docker-compose restart ash-dash

# 2. If restart fails, emergency fallback
docker-compose down
docker-compose up -d --force-recreate

# 3. Verify critical functionality
curl -k https://10.20.30.253:8883/health
curl -k https://10.20.30.253:8883/api/services/status

# 4. Alert team immediately
curl -X POST "$DISCORD_EMERGENCY_WEBHOOK" \
     -H "Content-Type: application/json" \
     -d '{"content": "🚨 CRITICAL: Crisis Response Dashboard is DOWN - Emergency team notified"}'
```

**Escalation Procedures:**

1. **0-5 minutes:** Automatic restart attempts
2. **5-10 minutes:** Technical team notification
3. **10-15 minutes:** Crisis Response Lead notification
4. **15+ minutes:** Emergency backup procedures activated

#### Scenario: Security Breach Detected

**Immediate Response:**

```bash
# 1. Block suspicious IP addresses
SUSPICIOUS_IP="x.x.x.x"  # Replace with actual IP
sudo ufw insert 1 deny from $SUSPICIOUS_IP

# 2. Force logout all users
docker-compose exec redis redis-cli flushdb

# 3. Rotate secrets
openssl rand -base64 32 > /opt/ash/ash-dash/secrets/jwt_secret
openssl rand -base64 32 > /opt/ash/ash-dash/secrets/session_secret

# 4. Restart with new secrets
docker-compose restart ash-dash

# 5. Enable audit logging
grep -E "(login|auth|admin)" /opt/ash/ash-dash/logs/application/*.log | tail -50

# 6. Document incident
echo "Security incident $(date): $SUSPICIOUS_IP blocked, secrets rotated" >> /opt/ash/ash-dash/logs/security_incidents.log
```

## 📊 Performance Monitoring

### Real-time Monitoring Commands

```bash
# Monitor all services
watch -n 5 'docker stats --no-stream'

# Monitor API performance
watch -n 10 'curl -s -w "Response Time: %{time_total}s\n" -o /dev/null https://10.20.30.253:8883/api/status'

# Monitor database performance
watch -n 30 'docker-compose exec postgres psql -U ash_user -d ash_dashboard -c "SELECT count(*) as active_connections FROM pg_stat_activity WHERE state = '\''active'\'\';"'

# Monitor Redis performance
watch -n 30 'docker-compose exec redis redis-cli info memory | grep used_memory_human'

# Monitor disk I/O
iostat -x 1

# Monitor network traffic
iftop -i eth0
```

### Performance Alerts Setup

```bash
# Create performance monitoring script
cat > /opt/ash/ash-dash/scripts/performance_monitor.sh << 'EOF'
#!/bin/bash

# Thresholds
CPU_THRESHOLD=80
MEMORY_THRESHOLD=85
DISK_THRESHOLD=90
RESPONSE_TIME_THRESHOLD=5

# Check CPU usage
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}' | cut -d'%' -f1)
if (( $(echo "$CPU_USAGE > $CPU_THRESHOLD" | bc -l) )); then
    echo "ALERT: High CPU usage: ${CPU_USAGE}%"
fi

# Check memory usage
MEMORY_USAGE=$(free | grep Mem | awk '{printf "%.1f", $3/$2 * 100.0}')
if (( $(echo "$MEMORY_USAGE > $MEMORY_THRESHOLD" | bc -l) )); then
    echo "ALERT: High memory usage: ${MEMORY_USAGE}%"
fi

# Check disk usage
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | cut -d'%' -f1)
if [ $DISK_USAGE -gt $DISK_THRESHOLD ]; then
    echo "ALERT: High disk usage: ${DISK_USAGE}%"
fi

# Check API response time
RESPONSE_TIME=$(curl -s -w "%{time_total}" -o /dev/null https://10.20.30.253:8883/health)
if (( $(echo "$RESPONSE_TIME > $RESPONSE_TIME_THRESHOLD" | bc -l) )); then
    echo "ALERT: Slow API response: ${RESPONSE_TIME}s"
fi
EOF

chmod +x /opt/ash/ash-dash/scripts/performance_monitor.sh

# Add to crontab for regular monitoring
echo "*/5 * * * * /opt/ash/ash-dash/scripts/performance_monitor.sh >> /var/log/ash-performance.log 2>&1" | crontab -
```

## 📞 Support Resources

### Internal Support Contacts

**Crisis Response Team:**
- **Primary:** Discord #crisis-response
- **Secondary:** Crisis Response Lead direct contact
- **Emergency:** 24/7 escalation procedures

**Technical Support:**
- **Primary:** Discord #tech-support
- **GitHub Issues:** https://github.com/the-alphabet-cartel/ash-dash/issues
- **Documentation:** `/opt/ash/ash-dash/docs/`

### External Resources

**Technical Documentation:**
- **Node.js:** https://nodejs.org/docs/
- **PostgreSQL:** https://www.postgresql.org/docs/
- **Redis:** https://redis.io/documentation
- **Docker:** https://docs.docker.com/
- **Nginx:** https://nginx.org/en/docs/

**Community Support:**
- **Discord.js:** https://discord.js.org/
- **Express.js:** https://expressjs.com/
- **Vue.js:** https://vuejs.org/guide/

### Escalation Matrix

| Issue Severity | Response Time | Escalation Path |
|----------------|---------------|-----------------|
| **Critical** (Crisis system down) | < 5 minutes | Tech Support → Crisis Lead → Emergency Team |
| **High** (Performance degradation) | < 15 minutes | Tech Support → Team Lead |
| **Medium** (Non-critical features) | < 2 hours | Tech Support → GitHub Issues |
| **Low** (Enhancement requests) | < 24 hours | GitHub Issues → Feature Planning |

### Recovery Contact Information

**Emergency Contacts:**
```bash
# Store in /opt/ash/ash-dash/EMERGENCY_CONTACTS.txt
CRISIS_RESPONSE_LEAD="Discord: @CrisisLead"
TECHNICAL_LEAD="Discord: @TechLead" 
SERVER_ADMIN="Discord: @ServerAdmin"
DISCORD_WEBHOOK_CRITICAL="https://discord.com/api/webhooks/..."
DISCORD_WEBHOOK_GENERAL="https://discord.com/api/webhooks/..."
```

**Backup Resources:**
- **Server Access:** SSH keys and credentials
- **Domain Management:** DNS and certificate authority access
- **Service Accounts:** Discord application management
- **Monitoring:** External monitoring service access

---

## 🎯 Quick Reference

### Most Common Issues & Quick Fixes

1. **Service won't start:** `docker-compose restart ash-dash`
2. **Database connection failed:** `docker-compose restart postgres`
3. **SSL certificate error:** Check certificate expiry and permissions
4. **High memory usage:** `docker-compose exec ash-dash node --expose-gc -e "global.gc()"`
5. **Slow performance:** Check database connections and run `VACUUM ANALYZE`
6. **Authentication issues:** Clear Redis sessions with `docker-compose exec redis redis-cli flushdb`

### Emergency Commands

```bash
# Complete system restart
docker-compose down && docker-compose up -d

# Emergency backup
/opt/ash/ash-dash/scripts/backup.sh

# Quick diagnostics
/opt/ash/ash-dash/scripts/diagnostics.sh

# Force service recreation
docker-compose up -d --force-recreate ash-dash

# Emergency fallback (disable SSL)
# Temporarily set DASH_ENABLE_SSL=false in .env and restart
```

### Useful Aliases

Add to `/home/$(whoami)/.bashrc`:

```bash
# Ash Dashboard aliases
alias ash-status='cd /opt/ash/ash-dash && docker-compose ps'
alias ash-logs='cd /opt/ash/ash-dash && docker-compose logs -f --tail=50'
alias ash-restart='cd /opt/ash/ash-dash && docker-compose restart ash-dash'
alias ash-health='curl -s -k https://10.20.30.253:8883/health | jq .'
alias ash-diag='/opt/ash/ash-dash/scripts/diagnostics.sh'
alias ash-backup='/opt/ash/ash-dash/scripts/backup.sh'
```

---

**This troubleshooting guide provides comprehensive solutions for maintaining the Ash Dashboard in production. Keep this document updated as new issues are discovered and resolved.**

🌈 **The Alphabet Cartel** | **Discord:** https://discord.gg/alphabetcartel | **Website:** http://alphabetcartel.org