# 🚀 Ash Dashboard Deployment Guide v2.1

**Updated for Dedicated Server & Submodule Structure**  
**Repository:** https://github.com/the-alphabet-cartel/ash-dash

## 📋 Deployment Overview

This guide covers deployment of the Ash Dashboard on the dedicated Debian 12 server with the new submodule structure. The dashboard serves as the central monitoring and analytics interface for the Ash Crisis Detection ecosystem.

### 🏗️ Server Infrastructure

**Dedicated Server Specifications:**
- **OS:** Debian 12 Linux
- **CPU:** AMD Ryzen 7 5800X
- **GPU:** NVIDIA RTX 3060
- **RAM:** 64GB
- **Internal IP:** 10.20.30.253
- **Container Platform:** Docker
- **Service Port:** 8883

### 🌐 Network Configuration

**Service Endpoints:**
- **Dashboard:** https://10.20.30.253:8883
- **Public Access:** https://dashboard.alphabetcartel.net
- **Bot API:** http://10.20.30.253:8882
- **NLP API:** http://10.20.30.253:8881
- **Testing API:** http://10.20.30.253:8884

## 🎯 Production Deployment

### Method 1: Submodule Deployment (Recommended)

This method deploys ash-dash as part of the complete Ash ecosystem.

#### **Step 1: Repository Setup**

```bash
# Clone main Ash repository with all submodules
cd /opt
git clone --recursive https://github.com/the-alphabet-cartel/ash.git
cd ash

# Verify submodule structure
ls -la
# Should show: ash-bot/ ash-nlp/ ash-dash/ ash-thrash/

# Navigate to dashboard
cd ash-dash
```

#### **Step 2: Environment Configuration**

```bash
# Copy environment template
cp .env.template .env

# Edit configuration (use your preferred editor)
nano .env
```

**Production Environment Configuration:**
```bash
# Server Configuration
NODE_ENV=production
PORT=8883
ENABLE_SSL=true

# Service Endpoints (Updated for dedicated server)
ASH_BOT_API=http://10.20.30.253:8882
ASH_NLP_API=http://10.20.30.253:8881
ASH_TESTING_API=http://10.20.30.253:8884

# Database Configuration
DATABASE_URL=postgresql://ash_user:secure_password@10.20.30.253:5432/ash_dashboard

# Performance Settings (Optimized for dedicated hardware)
CACHE_TTL=300
HEALTH_CHECK_INTERVAL=60000
METRICS_UPDATE_INTERVAL=30000
MAX_CONCURRENT_REQUESTS=100

# Security Settings
ENABLE_CORS=true
ALLOWED_ORIGINS=https://dashboard.alphabetcartel.net,https://10.20.30.253:8883
RATE_LIMIT_MAX=200
RATE_LIMIT_WINDOW=900000
ENABLE_DDoS_PROTECTION=true

# Team Management
ENABLE_RBAC=true
ENABLE_AUDIT_LOG=true
DEFAULT_ROLE=observer
SESSION_TIMEOUT=3600000

# Monitoring & Logging
LOG_LEVEL=info
ENABLE_METRICS_EXPORT=true
PROMETHEUS_PORT=9090
GRAFANA_ENABLED=true

# Discord Integration
DISCORD_CLIENT_ID=your_discord_client_id
DISCORD_CLIENT_SECRET=your_discord_client_secret
DISCORD_REDIRECT_URI=https://dashboard.alphabetcartel.net/auth/callback
```

#### **Step 3: SSL Certificate Setup**

```bash
# Create certificates directory
mkdir -p certs

# Option A: Generate self-signed certificates for internal access
openssl req -x509 -newkey rsa:4096 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes

# Option B: Use Let's Encrypt for public domain
# (Requires external domain configuration)
certbot certonly --standalone -d dashboard.alphabetcartel.net
cp /etc/letsencrypt/live/dashboard.alphabetcartel.net/fullchain.pem certs/cert.pem
cp /etc/letsencrypt/live/dashboard.alphabetcartel.net/privkey.pem certs/key.pem
```

#### **Step 4: Docker Deployment**

```bash
# Build and start the dashboard
docker-compose up -d

# Verify deployment
docker-compose ps

# Check logs
docker-compose logs ash-dash -f

# Test health endpoint
curl -k https://10.20.30.253:8883/health
```

#### **Step 5: Database Setup**

```bash
# Initialize database (if using PostgreSQL)
docker-compose exec postgres psql -U postgres -c "CREATE DATABASE ash_dashboard;"
docker-compose exec postgres psql -U postgres -c "CREATE USER ash_user WITH PASSWORD 'secure_password';"
docker-compose exec postgres psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE ash_dashboard TO ash_user;"

# Run database migrations
docker-compose exec ash-dash npm run migrate

# Seed initial data
docker-compose exec ash-dash npm run seed
```

### Method 2: Standalone Deployment

For dashboard-only deployment or development purposes.

#### **Step 1: Direct Repository Clone**

```bash
# Clone dashboard repository directly
git clone https://github.com/the-alphabet-cartel/ash-dash.git
cd ash-dash
```

#### **Step 2: Environment Setup**

```bash
# Copy and configure environment
cp .env.template .env

# Edit with standalone configuration
nano .env
```

**Standalone Environment Configuration:**
```bash
# Use same configuration as above, but with explicit service URLs
ASH_BOT_API=http://10.20.30.253:8882
ASH_NLP_API=http://10.20.30.253:8881
ASH_TESTING_API=http://10.20.30.253:8884

# May need to configure database separately if not using ecosystem database
DATABASE_URL=postgresql://localhost:5432/ash_dashboard_standalone
```

#### **Step 3: Deploy**

```bash
# Start services
docker-compose up -d

# Verify connectivity to other services
curl http://10.20.30.253:8882/health  # Bot
curl http://10.20.30.253:8881/health  # NLP
curl http://10.20.30.253:8884/health  # Testing
```

## 🔧 Development Deployment

### Local Development Setup

For development work on Windows with Docker Desktop:

#### **Step 1: Repository Setup**

```powershell
# Clone repository (using GitHub Desktop or command line)
git clone https://github.com/the-alphabet-cartel/ash-dash.git
cd ash-dash

# Set up development branch
git checkout -b feature/your-feature-name
```

#### **Step 2: Development Environment**

```powershell
# Copy development environment template
Copy-Item .env.template .env.development

# Edit development configuration (using Atom)
atom .env.development
```

**Development Environment Variables:**
```bash
# Development Configuration
NODE_ENV=development
PORT=8883
ENABLE_SSL=false

# Service Endpoints (point to development or production services)
ASH_BOT_API=http://10.20.30.253:8882
ASH_NLP_API=http://10.20.30.253:8881
ASH_TESTING_API=http://10.20.30.253:8884

# Development-specific settings
LOG_LEVEL=debug
ENABLE_DEBUG_ROUTES=true
ENABLE_MOCK_DATA=true
CACHE_TTL=10

# Development tools
ENABLE_HOT_RELOAD=true
ENABLE_SOURCE_MAPS=true
WEBPACK_DEV_SERVER=true
```

#### **Step 3: Local Development Server**

```powershell
# Install dependencies
npm install

# Start development server
npm run dev

# Access development dashboard
Start-Process "http://localhost:8883"
```

## 🔍 Verification & Testing

### Post-Deployment Verification

```bash
# Health check
curl -k https://10.20.30.253:8883/health

# Service connectivity test
curl -k https://10.20.30.253:8883/api/services/status

# Authentication endpoints
curl -k https://10.20.30.253:8883/api/auth/status

# Dashboard access test
curl -I -k https://10.20.30.253:8883/
```

### Integration Testing

```bash
# Test bot integration
curl -k https://10.20.30.253:8883/api/services/bot/health

# Test NLP integration
curl -k https://10.20.30.253:8883/api/services/nlp/health

# Test testing suite integration
curl -k https://10.20.30.253:8883/api/services/testing/health

# Test real-time websocket connections
# (Use browser developer tools or websocket testing tool)
```

### Performance Testing

```bash
# Load testing with Apache Bench
ab -n 1000 -c 10 https://10.20.30.253:8883/api/status

# Memory and CPU monitoring
docker stats ash-dash

# Database performance
docker-compose exec postgres pg_stat_activity
```

## 🛠️ Maintenance & Updates

### Regular Maintenance

```bash
# Update to latest version
cd /opt/ash/ash-dash
git pull origin main

# Rebuild and restart
docker-compose up -d --build

# Clean up old images
docker image prune -f

# Database maintenance
docker-compose exec postgres vacuumdb -U postgres ash_dashboard
```

### Backup Procedures

```bash
# Database backup
docker-compose exec postgres pg_dump -U postgres ash_dashboard > backup_$(date +%Y%m%d_%H%M%S).sql

# Configuration backup
tar -czf config_backup_$(date +%Y%m%d).tar.gz .env docker-compose.yml certs/

# Full application backup
tar -czf ash_dash_backup_$(date +%Y%m%d).tar.gz --exclude=node_modules --exclude=.git .
```

### Log Management

```bash
# View logs
docker-compose logs ash-dash -f

# Log rotation setup
logrotate /etc/logrotate.d/ash-dash

# Archive old logs
find /var/log/ash-dash -name "*.log" -mtime +30 -exec gzip {} \;
```

## 🚨 Troubleshooting

### Common Issues

**Service Connectivity Issues:**
```bash
# Check service status
docker-compose ps

# Restart specific service
docker-compose restart ash-dash

# Check network connectivity
docker network ls
docker network inspect ash_network
```

**SSL Certificate Issues:**
```bash
# Verify certificate
openssl x509 -in certs/cert.pem -text -noout

# Regenerate certificates
rm certs/*
openssl req -x509 -newkey rsa:4096 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes
```

**Database Connection Issues:**
```bash
# Check database status
docker-compose exec postgres pg_isready

# Reset database connection
docker-compose restart postgres ash-dash

# Check database connectivity
docker-compose exec ash-dash npm run db:test
```

**Performance Issues:**
```bash
# Monitor resource usage
htop
docker stats

# Increase memory limits in docker-compose.yml
# Check for memory leaks
docker-compose exec ash-dash npm run memory:profile
```

### Emergency Recovery

**Complete Service Reset:**
```bash
# Stop all services
docker-compose down

# Remove containers and volumes
docker-compose down -v

# Rebuild from scratch
docker-compose build --no-cache
docker-compose up -d
```

**Rollback to Previous Version:**
```bash
# Find previous version
git log --oneline -10

# Rollback to specific commit
git checkout <commit-hash>
docker-compose up -d --build

# Create rollback tag
git tag rollback-$(date +%Y%m%d_%H%M%S)
```

## 📊 Monitoring & Alerting

### Health Monitoring

```bash
# Setup health check monitoring
# Add to crontab:
*/5 * * * * curl -f https://10.20.30.253:8883/health || echo "Dashboard down" | mail -s "Alert" admin@alphabetcartel.org
```

### Performance Monitoring

```bash
# Prometheus metrics endpoint
curl https://10.20.30.253:8883/metrics

# Grafana dashboard setup
# Import dashboard configuration from config/grafana/
```

### Log Monitoring

```bash
# Setup log monitoring with ELK stack or similar
# Configure log shipping to central logging system
# Set up alerts for error patterns
```

## 📞 Support Resources

### Documentation References
- **[API Documentation](./tech/api_v2_1.md)** - Complete API reference
- **[Architecture Guide](./tech/architecture_v2_1.md)** - System design overview
- **[Troubleshooting Guide](./tech/troubleshooting_v2_1.md)** - Problem resolution guide

### Community Support
- **Discord:** https://discord.gg/alphabetcartel - #tech-support channel
- **GitHub Issues:** https://github.com/the-alphabet-cartel/ash-dash/issues

### Emergency Contacts
- **Production Issues:** Contact via Discord #crisis-response channel
- **Security Issues:** security@alphabetcartel.org

---

**Deployment completed successfully!** The Ash Dashboard should now be accessible at https://dashboard.alphabetcartel.net and ready to monitor the crisis detection ecosystem.