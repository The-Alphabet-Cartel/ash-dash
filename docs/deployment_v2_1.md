# 🚀 Ash Analytics Dashboard Deployment Guide

Complete setup and deployment instructions for ash-dash v2.1

---

## 📋 Prerequisites

### **System Requirements**

**Minimum Hardware:**
- CPU: 2 cores / 4 threads
- RAM: 4GB available
- Storage: 10GB free space
- Network: Stable internet connection

**Recommended Hardware (Your Setup):**
- CPU: AMD Ryzen 7 7700X (8 cores / 16 threads)
- RAM: 64GB (4GB allocated to dashboard)
- Storage: SSD with 50GB+ free space
- Network: Gigabit ethernet with local subnet access

**Operating System:**
- Windows 11 (Primary - your setup)
- Windows 10 (Supported)
- Linux (Ubuntu 20.04+, Debian 11+)
- macOS (Intel/Apple Silicon)

### **Software Dependencies**

**Required:**
- Docker Desktop 4.0+ (Windows/macOS) or Docker Engine 20.10+ (Linux)
- Docker Compose 2.0+
- Git for repository cloning

**Optional but Recommended:**
- GitHub Desktop (for your Windows environment)
- Atom Editor (for configuration editing)
- PowerShell 7+ (Windows) or Bash (Linux/macOS)

### **Network Requirements**

**Internal Network Access:**
- Ash Bot: `10.20.30.253:8882` (must be accessible)
- NLP Server: `10.20.30.16:8881` (must be accessible) 
- Testing Suite: `10.20.30.16:8884` (must be accessible)
- Dashboard Port: `8883` (will be opened)
- Redis Port: `6379` (internal use)

**Firewall Configuration:**
```powershell
# Windows Firewall Rules
New-NetFirewallRule -DisplayName "Ash Dashboard HTTPS" -Direction Inbound -Port 8883 -Protocol TCP -Action Allow
New-NetFirewallRule -DisplayName "Ash Dashboard HTTP" -Direction Inbound -Port 8883 -Protocol TCP -Action Allow
```

---

## 🛠️ Installation Methods

### **Method 1: Docker Deployment (Recommended)**

This is the recommended method for production deployment on your Windows 11 server.

#### **Step 1: Repository Setup**

```powershell
# Clone the repository
git clone https://github.com/The-Alphabet-Cartel/ash-dash.git
cd ash-dash

# Verify repository structure
Get-ChildItem -Recurse -Depth 1
```

#### **Step 2: Environment Configuration**

```powershell
# Copy environment template
Copy-Item .env.template .env

# Edit configuration file (using your preferred editor)
atom .env
# OR
notepad .env
```

**Essential Configuration:**
```bash
# Server Configuration
NODE_ENV=production
PORT=8883
ENABLE_SSL=true

# Service Endpoints (Update if different)
ASH_BOT_API=http://10.20.30.253:8882
ASH_NLP_API=http://10.20.30.16:8881
ASH_TESTING_API=http://10.20.30.16:8884

# Performance Settings (Optimized for your hardware)
CACHE_TTL=300
HEALTH_CHECK_INTERVAL=60000
METRICS_UPDATE_INTERVAL=30000

# Security Settings
ENABLE_CORS=true
RATE_LIMIT_MAX=200
ENABLE_DDoS_PROTECTION=true

# Team Management
ENABLE_RBAC=true
ENABLE_AUDIT_LOG=true
DEFAULT_ROLE=observer
```

#### **Step 3: SSL Certificate Setup**

**Option A: Auto-Generated Certificates (Recommended)**
```powershell
# Certificates will be auto-generated on first startup
# No additional configuration needed
```

**Option B: Custom Certificates**
```powershell
# Create certificates directory if it doesn't exist
New-Item -ItemType Directory -Force -Path "certs"

# Copy your certificates
Copy-Item "path\to\your\cert.pem" "certs\cert.pem"
Copy-Item "path\to\your\key.pem" "certs\key.pem"
```

#### **Step 4: Docker Deployment**

```powershell
# Start all services
docker-compose up -d

# Verify deployment
docker-compose ps

# Check logs for any issues
docker-compose logs ash-dash

# Verify health
curl -k https://10.20.30.16:8883/health
```

#### **Step 5: Verification**

```powershell
# Test dashboard access
Start-Process "https://10.20.30.16:8883"

# Check service connectivity
curl https://10.20.30.16:8883/api/status

# Verify all integrations
curl https://10.20.30.16:8883/api/services/bot
curl https://10.20.30.16:8883/api/services/nlp  
curl https://10.20.30.16:8883/api/services/testing
```

### **Method 2: Development Deployment**

For development, testing, or customization work.

#### **Step 1: Node.js Setup**

```powershell
# Install Node.js dependencies
cd dashboard
npm install

# Install development dependencies
npm install --save-dev
```

#### **Step 2: Development Configuration**

```powershell
# Copy environment template
Copy-Item .env.template .env

# Configure for development
atom .env
```

**Development Configuration:**
```bash
NODE_ENV=development
PORT=8883
ENABLE_SSL=false  # Disable SSL for development

# Service endpoints (same as production)
ASH_BOT_API=http://10.20.30.253:8882
ASH_NLP_API=http://10.20.30.16:8881
ASH_TESTING_API=http://10.20.30.16:8884

# Development settings
LOG_LEVEL=debug
ENABLE_DETAILED_LOGGING=true
CACHE_TTL=60  # Shorter cache for development
```

#### **Step 3: Development Server**

```powershell
# Start development server with auto-reload
npm run dev

# Or start production-like server
npm start
```

#### **Step 4: Development Verification**

```powershell
# Test development server
curl http://localhost:8883/health

# Access development dashboard
Start-Process "http://localhost:8883"
```

### **Method 3: Hybrid Deployment**

Combination of Docker for services and local development.

```powershell
# Start only Redis with Docker
docker-compose up -d ash-redis

# Run dashboard locally
cd dashboard
npm run dev
```

---

## ⚙️ Configuration Deep Dive

### **Environment Variables Reference**

#### **Server Configuration**
```bash
NODE_ENV=production              # Environment: development|production|staging
PORT=8883                       # Dashboard port (default: 8883)
BIND_ADDRESS=0.0.0.0            # Bind address (0.0.0.0 for all interfaces)
ENABLE_SSL=true                 # Enable HTTPS (recommended: true)
SSL_CERT_PATH=/app/certs/cert.pem
SSL_KEY_PATH=/app/certs/key.pem
SSL_AUTO_RENEW=true             # Auto-renew certificates
```

#### **Service Endpoints**
```bash
ASH_BOT_API=http://10.20.30.253:8882     # Ash Bot API endpoint
ASH_NLP_API=http://10.20.30.16:8881      # NLP Server API endpoint
ASH_TESTING_API=http://10.20.30.16:8884  # Testing Suite API endpoint
REDIS_URL=redis://localhost:6379         # Redis connection string
API_TIMEOUT=30000                        # API request timeout (ms)
CONNECTION_RETRY_ATTEMPTS=3              # Connection retry attempts
```

#### **Performance Settings**
```bash
# Caching Configuration
CACHE_TTL=300                   # Default cache TTL (seconds)
CACHE_TTL_STATIC=3600          # Static data cache TTL (seconds)
ENABLE_CACHE_COMPRESSION=true   # Compress cached data
MAX_CACHE_SIZE=256MB           # Maximum cache size

# Health Check Intervals
HEALTH_CHECK_INTERVAL=60000     # Service health check interval (ms)
METRICS_UPDATE_INTERVAL=30000   # Metrics update interval (ms)
TESTING_UPDATE_INTERVAL=300000  # Testing data update interval (ms)

# Connection Pooling
MAX_CONNECTIONS=20              # Maximum concurrent connections
CONNECTION_KEEPALIVE=true       # Enable connection keepalive
```

#### **Security Configuration**
```bash
# Rate Limiting
RATE_LIMIT_WINDOW=900000        # Rate limit window (ms)
RATE_LIMIT_MAX=200             # Max requests per window
ENABLE_DDoS_PROTECTION=true    # Enable DDoS protection
RATE_LIMIT_SKIP_TRUSTED=true   # Skip rate limiting for trusted IPs

# CORS Settings
ENABLE_CORS=true               # Enable CORS
CORS_ORIGIN=*                  # Allowed origins (* for all)
CORS_CREDENTIALS=true          # Allow credentials

# Security Headers
ENABLE_HELMET=true             # Enable Helmet.js security headers
ENABLE_CSP=true                # Enable Content Security Policy
ENABLE_HSTS=true               # Enable HTTP Strict Transport Security
```

#### **Team Management**
```bash
# Role-Based Access Control
ENABLE_RBAC=true               # Enable role-based access control
DEFAULT_ROLE=observer          # Default role for new users
ADMIN_ROLE=admin               # Administrator role name
MODERATOR_ROLE=moderator       # Moderator role name

# Audit Logging
ENABLE_AUDIT_LOG=true          # Enable audit logging
AUDIT_LOG_RETENTION=90         # Audit log retention (days)
AUDIT_LOG_LEVEL=info           # Audit log level
```

#### **Logging Configuration**
```bash
LOG_LEVEL=info                 # Logging level: debug|info|warn|error
LOG_FILE=ash-dash.log          # Log file name
LOG_MAX_SIZE=100MB             # Maximum log file size
LOG_MAX_FILES=5                # Maximum number of log files
ENABLE_JSON_LOGGING=true       # Enable JSON log format
ENABLE_CONSOLE_LOGGING=true    # Enable console logging
```

### **Docker Compose Configuration**

**Production docker-compose.yml:**
```yaml
version: '3.8'

services:
  ash-dash:
    image: ghcr.io/the-alphabet-cartel/ash-dash:v2.1
    container_name: ash-dash
    restart: unless-stopped
    ports:
      - "8883:8883"
    environment:
      - NODE_ENV=production
      - ENABLE_SSL=true
      - ASH_BOT_API=http://10.20.30.253:8882
      - ASH_NLP_API=http://10.20.30.16:8881
      - ASH_TESTING_API=http://10.20.30.16:8884
      - REDIS_URL=redis://ash-redis:6379
      - ENABLE_RBAC=true
      - ENABLE_AUDIT_LOG=true
    volumes:
      - ./logs:/app/logs
      - ./certs:/app/certs
      - ./data:/app/data
      - ./config:/app/config
    networks:
      - ash-network
    depends_on:
      - ash-redis
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 512M
          cpus: '0.5'
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8883/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  ash-redis:
    image: redis:7-alpine
    container_name: ash-redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
      - ./config/redis.conf:/usr/local/etc/redis/redis.conf
    networks:
      - ash-network
    command: redis-server /usr/local/etc/redis/redis.conf
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

networks:
  ash-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16

volumes:
  redis_data:
    driver: local
```

**Development docker-compose.override.yml:**
```yaml
version: '3.8'

services:
  ash-dash:
    environment:
      - NODE_ENV=development
      - LOG_LEVEL=debug
      - ENABLE_SSL=false
    volumes:
      - ./dashboard:/app/dashboard
      - ./public:/app/public
    ports:
      - "8883:8883"
      - "9229:9229"  # Node.js debugging port
    command: npm run dev
```

---

## 🔧 Advanced Configuration

### **SSL Certificate Management**

#### **Auto-Generated Certificates**
```bash
# Certificates are generated automatically on startup
# Configuration in docker-compose.yml
SSL_AUTO_GENERATE=true
SSL_CERT_VALIDITY_DAYS=365
SSL_CERT_COUNTRY=US
SSL_CERT_STATE=State
SSL_CERT_CITY=City
SSL_CERT_ORG="The Alphabet Cartel"
SSL_CERT_OU="IT Department"
```

#### **Custom Certificate Installation**
```powershell
# Create certificate directory
New-Item -ItemType Directory -Force -Path "certs"

# Install custom certificates
Copy-Item "C:\path\to\your\certificate.crt" "certs\cert.pem"
Copy-Item "C:\path\to\your\private.key" "certs\key.pem"
Copy-Item "C:\path\to\your\ca-bundle.crt" "certs\ca.pem"

# Set appropriate permissions
icacls "certs\key.pem" /inheritance:r /grant:r "Administrators:F"
```

#### **Certificate Renewal**
```bash
# Auto-renewal configuration
SSL_AUTO_RENEW=true
SSL_RENEW_DAYS_BEFORE=30
SSL_RENEW_NOTIFICATION=true
SSL_RENEW_EMAIL=admin@yourdomain.com
```

### **Performance Tuning**

#### **Redis Configuration**
```bash
# Create config/redis.conf
maxmemory 256mb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
appendonly yes
appendfsync everysec
```

#### **Node.js Optimization**
```bash
# Memory and CPU optimization
NODE_OPTIONS="--max-old-space-size=1024 --max-semi-space-size=128"
UV_THREADPOOL_SIZE=16
```

#### **Caching Strategy**
```bash
# Multi-level caching configuration
ENABLE_MEMORY_CACHE=true
ENABLE_REDIS_CACHE=true
ENABLE_HTTP_CACHE=true

# Cache invalidation
CACHE_INVALIDATION_STRATEGY=ttl
CACHE_WARM_ON_STARTUP=true
CACHE_PRELOAD_ROUTES=true
```

### **Monitoring Configuration**

#### **Health Checks**
```bash
# Advanced health check configuration
HEALTH_CHECK_ENDPOINTS=true
HEALTH_CHECK_DEPENDENCIES=true
HEALTH_CHECK_DETAILED=true
HEALTH_CHECK_TIMEOUT=5000
```

#### **Metrics Collection**
```bash
# Enable metrics collection
ENABLE_METRICS=true
METRICS_ENDPOINT=/metrics
METRICS_INCLUDE_SYSTEM=true
METRICS_INCLUDE_HTTP=true
METRICS_INCLUDE_CACHE=true
```

---

## 🐛 Troubleshooting

### **Common Deployment Issues**

#### **Docker Issues**

**Problem: Container won't start**
```powershell
# Check Docker Desktop status
Get-Service -Name "Docker Desktop Service"

# Check container logs
docker-compose logs ash-dash

# Check resource usage
docker stats

# Restart Docker Desktop if needed
Restart-Service -Name "Docker Desktop Service"
```

**Problem: Port conflicts**
```powershell
# Check what's using port 8883
netstat -ano | findstr :8883

# Kill process if needed (replace PID)
taskkill /PID <PID> /F

# Or change dashboard port in .env
echo "PORT=8884" >> .env
```

**Problem: Network connectivity**
```powershell
# Test service connectivity
Test-NetConnection -ComputerName 10.20.30.253 -Port 8882  # Ash Bot
Test-NetConnection -ComputerName 10.20.30.16 -Port 8881   # NLP Server
Test-NetConnection -ComputerName 10.20.30.16 -Port 8884   # Testing Suite

# Check Docker network
docker network ls
docker network inspect ash-dash_ash-network
```

#### **SSL Certificate Issues**

**Problem: SSL certificate errors**
```powershell
# Check certificate validity
openssl x509 -in certs/cert.pem -text -noout

# Regenerate certificates
Remove-Item -Recurse -Force certs
docker-compose restart ash-dash

# Temporary SSL disable for debugging
echo "ENABLE_SSL=false" >> .env
docker-compose restart ash-dash
```

**Problem: Certificate permission errors**
```powershell
# Fix certificate permissions
icacls certs /inheritance:r
icacls certs /grant:r "Users:RX"
icacls certs /grant:r "Administrators:F"
```

#### **Performance Issues**

**Problem: Slow dashboard loading**
```powershell
# Check resource usage
docker stats ash-dash

# Clear cache
docker-compose exec ash-dash npm run cache:clear

# Check cache hit rate
curl https://10.20.30.16:8883/api/debug/cache-stats

# Increase cache TTL
echo "CACHE_TTL=600" >> .env
docker-compose restart ash-dash
```

**Problem: High memory usage**
```powershell
# Check memory usage
docker stats ash-dash

# Optimize memory settings
echo "NODE_OPTIONS=--max-old-space-size=512" >> .env
docker-compose restart ash-dash

# Check for memory leaks
curl https://10.20.30.16:8883/api/debug/memory
```

#### **Service Integration Issues**

**Problem: Cannot connect to Ash services**
```powershell
# Test each service individually
curl http://10.20.30.253:8882/health    # Ash Bot
curl http://10.20.30.16:8881/health     # NLP Server
curl http://10.20.30.16:8884/health     # Testing Suite

# Check dashboard service discovery
curl https://10.20.30.16:8883/api/status

# Update service endpoints if needed
echo "ASH_BOT_API=http://new-bot-address:8882" >> .env
docker-compose restart ash-dash
```

**Problem: Redis connection issues**
```powershell
# Check Redis connectivity
docker-compose exec ash-redis redis-cli ping

# Check Redis logs
docker-compose logs ash-redis

# Reset Redis data if corrupted
docker-compose down
docker volume rm ash-dash_redis_data
docker-compose up -d
```

### **Diagnostic Commands**

#### **System Diagnostics**
```powershell
# Complete system check
./scripts/system-check.ps1

# Service connectivity test
./scripts/connectivity-test.ps1

# Performance benchmark
./scripts/performance-test.ps1
```

#### **Log Analysis**
```powershell
# Real-time log monitoring
docker-compose logs -f ash-dash

# Error log analysis
docker-compose logs ash-dash | Select-String "ERROR|WARN"

# Performance log analysis
docker-compose logs ash-dash | Select-String "Response time|Cache"

# Security log analysis
docker-compose logs ash-dash | Select-String "auth|security|blocked"
```

#### **Health Check Scripts**
```powershell
# Create health check script
@"
# Health Check Script
$services = @(
    "https://10.20.30.16:8883/health",
    "http://10.20.30.253:8882/health",
    "http://10.20.30.16:8881/health",
    "http://10.20.30.16:8884/health"
)

foreach ($service in $services) {
    try {
        $response = Invoke-RestMethod -Uri $service -TimeoutSec 10
        Write-Host "$service : OK" -ForegroundColor Green
    } catch {
        Write-Host "$service : FAILED - $($_.Exception.Message)" -ForegroundColor Red
    }
}
"@ | Out-File -FilePath "health-check.ps1"

# Run health check
PowerShell.exe -ExecutionPolicy Bypass -File "health-check.ps1"
```

---

## 🔄 Deployment Scenarios

### **Production Deployment**

**Requirements:**
- High availability and reliability
- SSL certificates and security
- Performance optimization
- Monitoring and alerting

**Configuration:**
```bash
NODE_ENV=production
ENABLE_SSL=true
ENABLE_RBAC=true
ENABLE_AUDIT_LOG=true
CACHE_TTL=300
HEALTH_CHECK_INTERVAL=60000
LOG_LEVEL=info
```

**Commands:**
```powershell
# Production deployment
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Verify production deployment
curl -k https://10.20.30.16:8883/api/status
```

### **Development Deployment**

**Requirements:**
- Fast iteration and debugging
- Detailed logging
- Hot reloading
- Easy configuration changes

**Configuration:**
```bash
NODE_ENV=development
ENABLE_SSL=false
LOG_LEVEL=debug
CACHE_TTL=60
ENABLE_DETAILED_LOGGING=true
```

**Commands:**
```powershell
# Development deployment
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Or local development
cd dashboard
npm run dev
```

### **Testing Deployment**

**Requirements:**
- Isolated environment
- Test data and fixtures
- Automated testing support
- Easy reset and cleanup

**Configuration:**
```bash
NODE_ENV=testing
ENABLE_SSL=false
USE_TEST_DATA=true
CACHE_TTL=10
AUTO_RESET_DATA=true
```

**Commands:**
```powershell
# Testing deployment
docker-compose -f docker-compose.yml -f docker-compose.test.yml up -d

# Run automated tests
npm run test:integration
```

---

## 📚 Post-Deployment

### **Initial Setup**

1. **Access Dashboard**
   ```powershell
   Start-Process "https://10.20.30.16:8883"
   ```

2. **Verify Service Connections**
   - Check all service status indicators are green
   - Verify crisis detection metrics are updating
   - Confirm testing suite integration is working

3. **Configure Team Access**
   - Set up user roles and permissions
   - Configure audit logging preferences
   - Set notification preferences

4. **Performance Optimization**
   - Monitor resource usage
   - Adjust cache settings if needed
   - Configure automated reports

### **Maintenance Tasks**

#### **Daily Tasks**
- Check service health status
- Review error logs for issues
- Monitor resource usage
- Verify backup integrity

#### **Weekly Tasks**
- Update SSL certificates if needed
- Review audit logs
- Analyze performance metrics
- Update documentation

#### **Monthly Tasks**
- Update Docker images
- Review security settings
- Optimize cache configuration
- Archive old logs

### **Backup Strategy**

```powershell
# Create backup script
@"
$date = Get-Date -Format "yyyyMMdd-HHmmss"
$backupPath = "C:\Backups\ash-dash\$date"

# Create backup directory
New-Item -ItemType Directory -Force -Path $backupPath

# Backup configuration
Copy-Item -Recurse .env $backupPath
Copy-Item -Recurse config $backupPath
Copy-Item -Recurse certs $backupPath

# Backup data
docker-compose exec ash-redis redis-cli BGSAVE
Copy-Item -Recurse data $backupPath

# Backup logs
Copy-Item -Recurse logs $backupPath

Write-Host "Backup completed: $backupPath"
"@ | Out-File -FilePath "backup.ps1"

# Schedule daily backups
schtasks /create /tn "Ash Dashboard Backup" /tr "PowerShell.exe -File C:\Projects\ash-dash\backup.ps1" /sc daily /st 02:00
```

---

## 🎯 Success Checklist

### **Deployment Success Criteria**

- [ ] Dashboard accessible via HTTPS
- [ ] All service status indicators are green
- [ ] Crisis detection metrics are updating
- [ ] Testing suite integration is functional
- [ ] SSL certificates are valid and auto-renewing
- [ ] Team access control is working
- [ ] Audit logging is enabled
- [ ] Performance metrics are within acceptable ranges
- [ ] All API endpoints respond correctly
- [ ] Real-time updates are working
- [ ] Data export functionality works
- [ ] Error handling is graceful
- [ ] Logs are being written correctly
- [ ] Backup strategy is in place
- [ ] Monitoring is configured

### **Verification Commands**

```powershell
# Complete verification script
@"
Write-Host "=== Ash Dashboard Deployment Verification ===" -ForegroundColor Cyan

# Test HTTPS access
try {
    $response = Invoke-RestMethod -Uri "https://10.20.30.16:8883/health" -SkipCertificateCheck
    Write-Host "✓ Dashboard Health: OK" -ForegroundColor Green
} catch {
    Write-Host "✗ Dashboard Health: FAILED