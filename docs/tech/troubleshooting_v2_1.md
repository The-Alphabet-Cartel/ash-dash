# 🛠️ Ash Analytics Dashboard Troubleshooting Guide

Common issues and solutions for ash-dash v2.1

---

## 🎯 Quick Diagnostics

### **Health Check Checklist**

Before diving into specific issues, run through this quick checklist:

```powershell
# Quick health check script
Write-Host "=== Ash Dashboard Health Check ===" -ForegroundColor Cyan

# 1. Check if dashboard is accessible
try {
    $response = Invoke-RestMethod -Uri "https://10.20.30.16:8883/health" -SkipCertificateCheck
    Write-Host "✓ Dashboard: $($response.status)" -ForegroundColor Green
} catch {
    Write-Host "✗ Dashboard: Not accessible" -ForegroundColor Red
}

# 2. Check Docker containers
$containers = @("ash-dash", "ash-redis")
foreach ($container in $containers) {
    $status = docker ps --filter "name=$container" --format "{{.Status}}"
    if ($status -like "*Up*") {
        Write-Host "✓ Container $container: Running" -ForegroundColor Green
    } else {
        Write-Host "✗ Container $container: Not running" -ForegroundColor Red
    }
}

# 3. Check service connectivity
$services = @{
    "Ash Bot" = "http://10.20.30.253:8882/health"
    "NLP Server" = "http://10.20.30.16:8881/health"
    "Testing Suite" = "http://10.20.30.16:8884/health"
}

foreach ($service in $services.GetEnumerator()) {
    try {
        $response = Invoke-RestMethod -Uri $service.Value -TimeoutSec 10
        Write-Host "✓ $($service.Key): Connected" -ForegroundColor Green
    } catch {
        Write-Host "✗ $($service.Key): Not accessible" -ForegroundColor Red
    }
}

Write-Host "=== Health Check Complete ===" -ForegroundColor Cyan
```

---

## 🚫 Dashboard Access Issues

### **Problem: Dashboard Won't Load**

#### **Symptoms**
- Browser shows "This site can't be reached"
- Connection timeout errors
- ERR_CONNECTION_REFUSED

#### **Diagnosis Steps**
```powershell
# Check if dashboard container is running
docker ps | findstr ash-dash

# Check if port is open
netstat -ano | findstr :8883

# Check Docker Desktop status
Get-Service -Name "*docker*"
```

#### **Solutions**

**1. Container Not Running**
```powershell
# Check container status
docker-compose ps

# Restart if needed
docker-compose restart ash-dash

# Check logs for errors
docker-compose logs ash-dash --tail 50
```

**2. Port Conflicts**
```powershell
# Find what's using port 8883
netstat -ano | findstr :8883

# If another process is using it, either:
# Option A: Kill the process
taskkill /PID <PID> /F

# Option B: Change dashboard port
echo "PORT=8884" >> .env
docker-compose restart ash-dash
```

**3. Windows Firewall Blocking**
```powershell
# Add firewall rule
New-NetFirewallRule -DisplayName "Ash Dashboard" -Direction Inbound -Port 8883 -Protocol TCP -Action Allow

# Or temporarily disable firewall for testing
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False
# Remember to re-enable: Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
```

### **Problem: SSL Certificate Warnings**

#### **Symptoms**
- Browser shows "Your connection is not private"
- Certificate error warnings
- NET::ERR_CERT_INVALID

#### **Solutions**

**1. Accept Self-Signed Certificate (Recommended for Internal Use)**
```text
1. Click "Advanced" in the browser warning
2. Click "Proceed to 10.20.30.16 (unsafe)"
3. Browser will remember this choice
```

**2. Regenerate Certificates**
```powershell
# Remove old certificates
Remove-Item -Recurse -Force certs

# Restart to generate new ones
docker-compose restart ash-dash

# Check certificate generation logs
docker-compose logs ash-dash | Select-String "SSL\|certificate"
```

**3. Install Custom Certificates**
```powershell
# Generate custom certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout certs/key.pem \
  -out certs/cert.pem \
  -subj "/C=US/ST=WA/L=Lacey/O=The Alphabet Cartel/CN=10.20.30.16"

# Restart dashboard
docker-compose restart ash-dash
```

**4. Disable SSL for Testing**
```powershell
# Temporarily disable SSL
echo "ENABLE_SSL=false" >> .env
docker-compose restart ash-dash

# Access via HTTP
Start-Process "http://10.20.30.16:8883"
```

### **Problem: Authentication Issues**

#### **Symptoms**
- Login failures
- "Authentication required" errors
- Frequent session timeouts

#### **Solutions**

**1. Check Authentication Configuration**
```powershell
# Check if RBAC is enabled
docker-compose exec ash-dash cat /app/.env | findstr RBAC

# Check user roles configuration
docker-compose exec ash-dash cat /app/config/roles.json
```

**2. Reset Authentication**
```powershell
# Clear authentication cache
docker-compose exec ash-dash npm run auth:clear

# Restart with clean slate
docker-compose restart ash-dash
```

---

## 📊 Data and Metrics Issues

### **Problem: No Data Showing**

#### **Symptoms**
- Dashboard shows "No data available"
- Empty charts and graphs
- All metrics show zero

#### **Diagnosis Steps**
```powershell
# Check service connectivity
curl https://10.20.30.16:8883/api/status

# Check individual services
curl http://10.20.30.253:8882/health  # Ash Bot
curl http://10.20.30.16:8881/health   # NLP Server
curl http://10.20.30.16:8884/health   # Testing Suite
```

#### **Solutions**

**1. Service Connection Issues**
```powershell
# Check if services are accessible from dashboard container
docker-compose exec ash-dash curl http://10.20.30.253:8882/health
docker-compose exec ash-dash curl http://10.20.30.16:8881/health
docker-compose exec ash-dash curl http://10.20.30.16:8884/health

# If failing, check network connectivity
docker network ls
docker network inspect ash-dash_ash-network
```

**2. Update Service Endpoints**
```powershell
# Check current configuration
docker-compose exec ash-dash cat /app/.env | findstr API

# Update if needed
echo "ASH_BOT_API=http://new-bot-address:8882" >> .env
echo "ASH_NLP_API=http://new-nlp-address:8881" >> .env
echo "ASH_TESTING_API=http://new-testing-address:8884" >> .env

docker-compose restart ash-dash
```

**3. Mock Data for Testing**
```powershell
# Enable mock data temporarily
echo "ENABLE_MOCK_DATA=true" >> .env
docker-compose restart ash-dash

# This will show sample data while troubleshooting
```

### **Problem: Stale or Outdated Data**

#### **Symptoms**
- Data hasn't updated in hours
- Timestamps show old dates
- Charts not refreshing

#### **Solutions**

**1. Clear Cache**
```powershell
# Clear Redis cache
docker-compose exec ash-redis redis-cli FLUSHALL

# Clear application cache
docker-compose exec ash-dash npm run cache:clear

# Restart dashboard
docker-compose restart ash-dash
```

**2. Check Update Intervals**
```powershell
# Check current update settings
docker-compose exec ash-dash cat /app/.env | findstr INTERVAL

# Reduce intervals for faster updates
echo "METRICS_UPDATE_INTERVAL=10000" >> .env  # 10 seconds
echo "HEALTH_CHECK_INTERVAL=30000" >> .env   # 30 seconds
docker-compose restart ash-dash
```

**3. Force Data Refresh**
```powershell
# Manual data refresh via API
curl -X POST "https://10.20.30.16:8883/api/cache/refresh" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -k
```

### **Problem: Charts Not Loading**

#### **Symptoms**
- Blank chart areas
- "Failed to load chart" errors
- JavaScript console errors

#### **Solutions**

**1. Check Browser Console**
```text
1. Press F12 to open Developer Tools
2. Go to Console tab
3. Look for JavaScript errors
4. Common errors and solutions:

- "Chart.js not found" → Clear browser cache
- "WebSocket connection failed" → Check WebSocket connectivity
- "Cannot read property of undefined" → Data format issue
```

**2. Clear Browser Cache**
```text
1. Ctrl+Shift+Delete (Windows) or Cmd+Shift+Delete (Mac)
2. Select "Cached images and files"
3. Click "Delete" or "Clear Data"
4. Refresh the dashboard page
```

**3. Test Chart Data Directly**
```powershell
# Get chart data directly
curl "https://10.20.30.16:8883/api/metrics/crisis-trends" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -k

# Check if data format is correct
```

---

## 🔌 Integration and Service Issues

### **Problem: Service Status Always Red**

#### **Symptoms**
- All service indicators show red/unhealthy
- Services are actually running fine
- Health checks failing

#### **Solutions**

**1. Check Health Check Configuration**
```powershell
# Check health check intervals
docker-compose exec ash-dash cat /app/.env | findstr HEALTH

# Increase timeout if services are slow
echo "HEALTH_CHECK_TIMEOUT=10000" >> .env  # 10 seconds
docker-compose restart ash-dash
```

**2. Test Health Endpoints Manually**
```powershell
# Test from dashboard container
docker-compose exec ash-dash curl -v http://10.20.30.253:8882/health
docker-compose exec ash-dash curl -v http://10.20.30.16:8881/health
docker-compose exec ash-dash curl -v http://10.20.30.16:8884/health

# Look for specific error messages
```

**3. Network Connectivity Issues**
```powershell
# Check if dashboard can reach services
docker-compose exec ash-dash ping 10.20.30.253
docker-compose exec ash-dash ping 10.20.30.16

# Check DNS resolution
docker-compose exec ash-dash nslookup 10.20.30.253
```

### **Problem: WebSocket Connection Failures**

#### **Symptoms**
- Real-time updates not working
- "WebSocket connection failed" errors
- Charts not auto-refreshing

#### **Solutions**

**1. Check WebSocket Configuration**
```javascript
// Test WebSocket connection manually in browser console
const ws = new WebSocket('wss://10.20.30.16:8883/ws');
ws.onopen = () => console.log('WebSocket connected');
ws.onerror = (error) => console.error('WebSocket error:', error);
ws.onclose = (event) => console.log('WebSocket closed:', event.code, event.reason);
```

**2. Proxy/Firewall Issues**
```powershell
# Check if WebSocket ports are open
Test-NetConnection -ComputerName 10.20.30.16 -Port 8883

# For proxy environments, may need to configure proxy settings
```

**3. SSL Issues with WebSockets**
```powershell
# Try with SSL disabled temporarily
echo "ENABLE_SSL=false" >> .env
docker-compose restart ash-dash

# Test with ws:// instead of wss://
# If this works, the issue is SSL-related
```

---

## 🗂️ Database and Storage Issues

### **Problem: Data Export Failures**

#### **Symptoms**
- Export buttons not working
- "Export failed" errors
- Downloaded files are empty or corrupted

#### **Solutions**

**1. Check Export Directory Permissions**
```powershell
# Check if export directory exists and is writable
docker-compose exec ash-dash ls -la /app/data/exports

# Create directory if missing
docker-compose exec ash-dash mkdir -p /app/data/exports

# Check disk space
docker-compose exec ash-dash df -h
```

**2. Memory Issues with Large Exports**
```powershell
# Check container memory usage
docker stats ash-dash

# Increase memory limit if needed
# Edit docker-compose.yml:
# deploy:
#   resources:
#     limits:
#       memory: 4G  # Increase from 2G

docker-compose up -d
```

**3. Test Export with Smaller Dataset**
```powershell
# Try exporting smaller time range
curl -X POST "https://10.20.30.16:8883/api/export" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"format":"csv","timeRange":"1h","dataTypes":["crisis_metrics"]}' \
  -k
```

### **Problem: Redis Connection Issues**

#### **Symptoms**
- Slow dashboard performance
- Cache-related errors
- "Redis connection failed" in logs

#### **Solutions**

**1. Check Redis Container**
```powershell
# Check if Redis is running
docker-compose ps ash-redis

# Test Redis connectivity
docker-compose exec ash-redis redis-cli ping

# Should return "PONG"
```

**2. Redis Memory Issues**
```powershell
# Check Redis memory usage
docker-compose exec ash-redis redis-cli info memory

# Clear Redis if memory is full
docker-compose exec ash-redis redis-cli FLUSHALL

# Restart Redis
docker-compose restart ash-redis
```

**3. Connection Configuration**
```powershell
# Check Redis URL configuration
docker-compose exec ash-dash cat /app/.env | findstr REDIS

# Should be: REDIS_URL=redis://ash-redis:6379
# Update if incorrect and restart
```

---

## ⚡ Performance Issues

### **Problem: Slow Dashboard Loading**

#### **Symptoms**
- Dashboard takes >10 seconds to load
- Timeout errors
- High CPU/memory usage

#### **Solutions**

**1. Resource Monitoring**
```powershell
# Check resource usage
docker stats

# Check Windows system resources
Get-Process -Name "Docker Desktop" | Select-Object CPU,WorkingSet
Get-Counter "\Processor(_Total)\% Processor Time"
```

**2. Optimize Cache Settings**
```powershell
# Increase cache TTL to reduce API calls
echo "CACHE_TTL=600" >> .env  # 10 minutes
echo "CACHE_TTL_STATIC=3600" >> .env  # 1 hour

# Enable cache compression
echo "ENABLE_CACHE_COMPRESSION=true" >> .env

docker-compose restart ash-dash
```

**3. Reduce Update Frequency**
```powershell
# Increase update intervals
echo "METRICS_UPDATE_INTERVAL=60000" >> .env   # 1 minute
echo "HEALTH_CHECK_INTERVAL=120000" >> .env   # 2 minutes

docker-compose restart ash-dash
```

### **Problem: High Memory Usage**

#### **Symptoms**
- Container memory usage >2GB
- System running out of memory
- Dashboard becomes unresponsive

#### **Solutions**

**1. Memory Optimization**
```powershell
# Reduce Node.js memory usage
echo "NODE_OPTIONS=--max-old-space-size=1024" >> .env

# Limit container memory
# Edit docker-compose.yml to add:
# deploy:
#   resources:
#     limits:
#       memory: 2G

docker-compose up -d
```

**2. Cache Management**
```powershell
# Reduce cache size
echo "MAX_CACHE_SIZE=128MB" >> .env

# Clear cache regularly
docker-compose exec ash-dash npm run cache:clear

docker-compose restart ash-dash
```

**3. Monitor Memory Leaks**
```powershell
# Monitor memory usage over time
for ($i = 0; $i -lt 60; $i++) {
    $mem = docker stats ash-dash --no-stream --format "{{.MemUsage}}"
    Write-Host "$(Get-Date -Format 'HH:mm:ss'): $mem"
    Start-Sleep -Seconds 60
}
```

---

## 🔧 Configuration Issues

### **Problem: Environment Variables Not Loading**

#### **Symptoms**
- Changes to .env file not taking effect
- Default values being used instead of configured values
- Configuration-related errors

#### **Solutions**

**1. Check .env File Location**
```powershell
# Ensure .env is in project root
Get-ChildItem -Name .env

# Check file contents
Get-Content .env | Select-String "NODE_ENV\|PORT\|API"
```

**2. Container Environment**
```powershell
# Check environment variables in container
docker-compose exec ash-dash env | Select-String "ASH\|NODE\|PORT"

# If variables are missing, restart container
docker-compose restart ash-dash
```

**3. Docker Compose Configuration**
```powershell
# Validate docker-compose.yml
docker-compose config

# Check if .env is properly referenced
Get-Content docker-compose.yml | Select-String "env_file\|environment"
```

### **Problem: SSL Configuration Issues**

#### **Symptoms**
- SSL not working despite ENABLE_SSL=true
- Certificate errors even with new certificates
- Mixed content warnings

#### **Solutions**

**1. Verify SSL Configuration**
```powershell
# Check SSL settings
docker-compose exec ash-dash cat /app/.env | Select-String "SSL"

# Check certificate files exist
docker-compose exec ash-dash ls -la /app/certs/
```

**2. Certificate File Permissions**
```powershell
# Fix certificate permissions
docker-compose exec ash-dash chmod 600 /app/certs/key.pem
docker-compose exec ash-dash chmod 644 /app/certs/cert.pem

docker-compose restart ash-dash
```

**3. Test SSL Configuration**
```powershell
# Test SSL connection
openssl s_client -connect 10.20.30.16:8883 -servername 10.20.30.16

# Check certificate validity
openssl x509 -in certs/cert.pem -text -noout | Select-String "Not Before\|Not After"
```

---

## 🚨 Emergency Procedures

### **Complete System Reset**

When all else fails, use this nuclear option:

```powershell
Write-Host "=== EMERGENCY SYSTEM RESET ===" -ForegroundColor Red
Write-Host "This will destroy all data and start fresh!" -ForegroundColor Red
$confirm = Read-Host "Type 'RESET' to confirm"

if ($confirm -eq "RESET") {
    # Stop all containers
    docker-compose down -v
    
    # Remove all data
    Remove-Item -Recurse -Force data, logs, certs -ErrorAction SilentlyContinue
    
    # Reset environment
    Copy-Item .env.template .env
    
    # Start fresh
    docker-compose up -d
    
    Write-Host "System reset complete. Reconfigure .env as needed." -ForegroundColor Green
} else {
    Write-Host "Reset cancelled." -ForegroundColor Yellow
}
```

### **Backup Before Troubleshooting**

Always backup before making changes:

```powershell
# Create backup
$backupDate = Get-Date -Format "yyyyMMdd-HHmmss"
$backupPath = "backup-$backupDate"

New-Item -ItemType Directory -Force -Path $backupPath

Copy-Item -Recurse .env, data, logs, certs $backupPath -ErrorAction SilentlyContinue
Compress-Archive -Path $backupPath -DestinationPath "$backupPath.zip"
Remove-Item -Recurse $backupPath

Write-Host "Backup created: $backupPath.zip" -ForegroundColor Green
```

### **Service Recovery Priority**

When multiple services are down, recover in this order:

1. **Dashboard Container** - Core functionality
2. **Redis** - Caching and session management  
3. **External Services** - Bot, NLP, Testing integration
4. **WebSocket** - Real-time updates
5. **SSL/Security** - Enhanced security features

---

## 📞 Getting Help

### **Information to Gather**

Before asking for help, collect this information:

```powershell
# System information script
Write-Host "=== SYSTEM DIAGNOSTIC INFO ===" -ForegroundColor Cyan

# Dashboard version
docker-compose exec ash-dash cat /app/package.json | Select-String "version"

# Container status
Write-Host "Container Status:" -ForegroundColor Yellow
docker-compose ps

# Recent logs
Write-Host "Recent Logs:" -ForegroundColor Yellow
docker-compose logs ash-dash --tail 20

# Environment
Write-Host "Environment:" -ForegroundColor Yellow
docker-compose exec ash-dash env | Select-String "NODE_ENV\|PORT\|ASH_"

# System resources
Write-Host "System Resources:" -ForegroundColor Yellow
docker stats --no-stream

# Network connectivity
Write-Host "Network Tests:" -ForegroundColor Yellow
Test-NetConnection -ComputerName 10.20.30.253 -Port 8882
Test-NetConnection -ComputerName 10.20.30.16 -Port 8881
Test-NetConnection -ComputerName 10.20.30.16 -Port 8884

Write-Host "=== END DIAGNOSTIC INFO ===" -ForegroundColor Cyan
```

### **Support Channels**

1. **GitHub Issues**: https://github.com/The-Alphabet-Cartel/ash-dash/issues
   - Include diagnostic information
   - Use issue templates
   - Check existing issues first

2. **Discord #tech-support**: https://discord.gg/alphabetcartel
   - Real-time community help
   - Screen sharing for complex issues
   - Quick questions and clarifications

3. **Team Documentation**: `/docs` directory
   - Check other guides first
   - API documentation for integration issues
   - Implementation guide for technical details

### **When to Escalate**

Escalate immediately for:
- Security-related issues
- Data loss or corruption
- Complete system failures lasting >1 hour
- Issues affecting crisis response capabilities

Escalate within 24 hours for:
- Performance degradation
- Integration failures
- Recurring issues
- Configuration problems

---

## 📚 Additional Resources

### **Log Analysis Tools**

```powershell
# Real-time log monitoring
docker-compose logs -f ash-dash | Select-String "ERROR\|WARN"

# Log analysis for common issues
docker-compose logs ash-dash | Select-String "SSL\|certificate" | Out-File ssl-issues.log
docker-compose logs ash-dash | Select-String "Redis\|cache" | Out-File cache-issues.log
docker-compose logs ash-dash | Select-String "Auth\|permission" | Out-File auth-issues.log
```

### **Performance Monitoring**

```powershell
# Create performance monitoring script
@"
# Monitor dashboard performance
while ($true) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $stats = docker stats ash-dash --no-stream --format "{{.CPUPerc}},{{.MemUsage}}"
    $health = try { (Invoke-RestMethod -Uri "https://10.20.30.16:8883/health" -SkipCertificateCheck).status } catch { "Error" }
    
    Write-Output "$timestamp,$stats,$health" | Out-File -Append performance.log
    Start-Sleep -Seconds 60
}
"@ | Out-File -FilePath "monitor-performance.ps1"

# Run with: PowerShell.exe -File monitor-performance.ps1
```

### **Automated Health Checks**

```powershell
# Create automated health check
@"
# Automated health check and recovery
$services = @{
    "Dashboard" = "https://10.20.30.16:8883/health"
    "Bot" = "http://10.20.30.253:8882/health"
    "NLP" = "http://10.20.30.16:8881/health"
    "Testing" = "http://10.20.30.16:8884/health"
}

foreach ($service in $services.GetEnumerator()) {
    try {
        $response = Invoke-RestMethod -Uri $service.Value -TimeoutSec 10 -SkipCertificateCheck
        Write-Host "✓ $($service.Key): Healthy" -ForegroundColor Green
    } catch {
        Write-Host "✗ $($service.Key): Failed - $($_.Exception.Message)" -ForegroundColor Red
        
        # Auto-recovery for dashboard
        if ($service.Key -eq "Dashboard") {
            Write-Host "Attempting dashboard recovery..." -ForegroundColor Yellow
            docker-compose restart ash-dash
        }
    }
}
"@ | Out-File -FilePath "health-check.ps1"

# Schedule to run every 15 minutes
schtasks /create /tn "Ash Dashboard Health Check" /tr "PowerShell.exe -File C:\Projects\ash-dash\health-check.ps1" /sc minute /mo 15
```

---

*This troubleshooting guide covers the most common issues encountered with ash-dash v2.1. For additional help, refer to the other documentation guides or reach out to the community via [Discord](https://discord.gg/alphabetcartel).*