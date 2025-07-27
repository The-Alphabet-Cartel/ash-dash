# 📊 Ash Analytics Dashboard v2.1

Real-time monitoring and analytics dashboard for The Alphabet Cartel's Ash Crisis Detection Bot ecosystem.

[![Version](https://img.shields.io/badge/version-2.1-blue)](https://github.com/The-Alphabet-Cartel/ash-dash/releases/tag/v2.1)
[![GitHub](https://img.shields.io/badge/GitHub-The--Alphabet--Cartel-black?style=flat-square&logo=github)](https://github.com/The-Alphabet-Cartel/ash-dash)
[![Discord](https://img.shields.io/badge/Discord-The%20Alphabet%20Cartel-5865F2?style=flat-square&logo=discord)](https://discord.gg/alphabetcartel)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=flat-square&logo=docker)](https://hub.docker.com)

## 🎉 What's New in v2.1

**Enhanced monitoring capabilities with integrated testing suite, improved analytics, and comprehensive team management features.**

### 🧪 **Integrated Testing Suite** (Major Feature)
- **Ash-Thrash Integration** - Real-time testing metrics and results from comprehensive 350-phrase test suite
- **Performance Analytics** - Goal achievement tracking and detailed failure analysis  
- **One-Click Testing** - Trigger tests directly from dashboard interface
- **Historical Trends** - Track testing performance over time with advanced charting
- **Automated Reporting** - Daily/weekly testing summaries with actionable insights

### 📊 **Enhanced Analytics Dashboard**
- **Learning System Metrics** - Advanced tracking of ML model improvements and community adaptation
- **Real-time Visualizations** - Interactive charts with WebSocket updates for instant data refresh
- **Custom Dashboards** - Configurable layouts for different team roles and responsibilities
- **Data Export** - CSV/JSON export capabilities for external analysis and reporting
- **Mobile Responsive** - Optimized interface for monitoring on mobile devices and tablets

### 🔐 **Advanced Security & Access Control**
- **Role-Based Permissions** - Team member access control with customizable permission levels
- **Audit Logging** - Complete activity tracking with user attribution and change history
- **Enhanced SSL** - Improved certificate management with automatic renewal support
- **API Security** - Advanced rate limiting and DDoS protection mechanisms
- **Data Encryption** - Enhanced encryption for sensitive analytics data at rest and in transit

### ⚡ **Performance Optimizations**
- **Intelligent Caching** - Multi-layer caching reduces server load by 85% while improving response times
- **Connection Pooling** - Efficient database and API connection management for high-traffic scenarios
- **Compression** - Advanced data compression for faster loading and reduced bandwidth usage
- **Resource Optimization** - Memory and CPU optimizations for better performance on Windows 11 server
- **Background Processing** - Non-blocking operations for better user experience during heavy analytics

## 🌟 Overview

The Ash Analytics Dashboard provides comprehensive real-time monitoring and insights for your mental health crisis detection system. Built specifically for The Alphabet Cartel Discord community, it tracks service health, crisis detection metrics, learning system performance, and testing suite results across your entire Ash ecosystem.

### **Architecture Overview**
```
                    ▼ Real-time WebSocket Updates
┌─────────────────────────────┐ ┌─────────────────────────────┐ ┌─────────────────────────────┐
│         Ash Bot             │ │       Ash NLP Server        │ │     Analytics Dashboard     │
│    (Linux Docker)           │ │   (Windows 11 + RTX 3050)  │ │    (Windows 11 Docker)      │
│   IP: 10.20.30.253:8882     │ │      IP: 10.20.30.16:8881   │ │    IP: 10.20.30.16:8883     │
│                             │ │                             │ │                             │
│ • Crisis Detection          │ │ • ML Analysis               │ │ • Real-time Monitoring      │
│ • Discord Integration       │ │ • Learning System           │ │ • Service Health Checks     │
│ • Keyword Management        │ │ • Pattern Recognition       │ │ • Crisis Analytics          │
│ • Team Commands             │ │ • Model Management          │ │ • Learning Insights         │
└─────────────────────────────┘ └─────────────────────────────┘ └─────────────────────────────┘
                                           ▲                               ▲
                    ┌─────────────────────────────┐ ┌─────────────────────────────┐
                    │     Ash Testing Suite       │ │    Team Management          │
                    │    (Windows 11 Docker)      │ │    (Role-based Access)      │
                    │    IP: 10.20.30.16:8884     │ │    (Audit & Compliance)     │
                    │                             │ │                             │
                    │ • 350 Phrase Testing        │ │ • Crisis Response Team      │
                    │ • Performance Validation    │ │ • Dashboard Administrators  │
                    │ • Automated Reporting       │ │ • Read-only Observers       │
                    │ • Goal Achievement          │ │ • External Stakeholders     │
                    └─────────────────────────────┘ └─────────────────────────────┘
```

### **Technology Stack**
- **Frontend**: HTML5, TailwindCSS, Chart.js v4.x, Socket.IO, Alpine.js
- **Backend**: Node.js 20.x, Express.js, Winston Logging, Redis Caching
- **Real-time**: WebSockets for live updates and notifications
- **Security**: Enhanced SSL/HTTPS with certificate auto-renewal, Helmet.js security headers
- **Deployment**: Docker containers with health checks, auto-restart, and resource limits
- **Integration**: REST APIs to Ash Bot, NLP Server, and Testing Suite with failover support

## 🚀 Quick Start

### **Prerequisites**
- Docker and Docker Compose installed (Docker Desktop 4.0+ recommended)
- Access to Ash Bot API (10.20.30.253:8882)
- Access to NLP Server API (10.20.30.16:8881)  
- Access to Testing Suite API (10.20.30.16:8884)
- Windows 11 server (for your setup) or Linux server with 4GB+ RAM
- Network connectivity within 10.20.30.0/24 subnet

### **Using Docker (Recommended)**

1. **Clone the repository**
```bash
git clone https://github.com/The-Alphabet-Cartel/ash-dash.git
cd ash-dash
```

2. **Configure environment**
```bash
cp .env.template .env
# Edit .env with your specific configuration
```

3. **Deploy with Docker Compose**
```bash
docker-compose up -d
```

4. **Access the dashboard**
- **HTTPS**: https://10.20.30.16:8883 (with SSL - recommended)
- **HTTP**: http://10.20.30.16:8883 (fallback)
- Dashboard will automatically connect to all Ash services

5. **Verify deployment**
```bash
# Check service health
curl -k https://10.20.30.16:8883/health

# View logs
docker-compose logs -f ash-dash
```

### **Development Setup**

1. **Install dependencies**
```bash
cd dashboard
npm install
```

2. **Configure environment**
```bash
cp .env.template .env
# Configure API endpoints and settings for development
```

3. **Start development server**
```bash
npm run dev
```

4. **Build for production**
```bash
npm run build
npm start
```

## ⚙️ Configuration

### **Environment Variables**

```bash
# Server Configuration
NODE_ENV=production
PORT=8883
ENABLE_SSL=true

# SSL Configuration (Auto-managed in v2.1)
SSL_CERT_PATH=/app/certs/cert.pem
SSL_KEY_PATH=/app/certs/key.pem
SSL_AUTO_RENEW=true

# Service Endpoints
ASH_BOT_API=http://10.20.30.253:8882
ASH_NLP_API=http://10.20.30.16:8881
ASH_TESTING_API=http://10.20.30.16:8884

# Performance Settings (Optimized for v2.1)
CACHE_TTL=300                      # 5 minutes cache for real-time data
CACHE_TTL_STATIC=3600             # 1 hour cache for static data
HEALTH_CHECK_INTERVAL=60000       # 1 minute between health checks
METRICS_UPDATE_INTERVAL=30000     # 30 seconds real-time updates
TESTING_UPDATE_INTERVAL=300000    # 5 minutes testing updates

# Dashboard Branding
DASHBOARD_TITLE="Ash Analytics Dashboard v2.1"
DASHBOARD_SUBTITLE="The Alphabet Cartel Crisis Detection Analytics"
COMMUNITY_NAME="The Alphabet Cartel"
COMMUNITY_DISCORD="https://discord.gg/alphabetcartel"

# Security & Rate Limiting (Enhanced in v2.1)
ENABLE_CORS=true
RATE_LIMIT_WINDOW=900000          # 15 minutes
RATE_LIMIT_MAX=200                # 200 requests per window (increased)
ENABLE_DDoS_PROTECTION=true       # Advanced DDoS protection
API_KEY_REQUIRED=false            # Set to true for production environments

# Team Management (New in v2.1)
ENABLE_RBAC=true                  # Role-based access control
ENABLE_AUDIT_LOG=true             # Activity logging
DEFAULT_ROLE=observer             # Default role for new users

# Logging (Enhanced)
LOG_LEVEL=info
LOG_FILE=ash-dash.log
LOG_MAX_SIZE=100MB
LOG_MAX_FILES=5
ENABLE_JSON_LOGGING=true
```

### **Docker Compose Integration**

The dashboard integrates seamlessly with the existing Ash ecosystem:

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

  ash-redis:
    image: redis:7-alpine
    container_name: ash-redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - ash-network

networks:
  ash-network:
    driver: bridge

volumes:
  redis_data:
```

## 📊 Dashboard Features

### **Main Dashboard View**

#### **1. Service Status Grid**
- **Ash Bot**: Health status, response time, and connection monitoring
- **NLP Server**: ML service status, GPU utilization, and model performance
- **Testing Suite**: Test status, last run results, and automated scheduling
- **Dashboard**: Local service health, memory usage, and uptime statistics

Real-time status indicators:
- 🟢 **Green**: Service healthy and responding normally
- 🔴 **Red**: Service down or experiencing critical issues  
- 🟡 **Yellow**: Service degraded performance or warnings
- 🔵 **Blue**: Service in maintenance or updating mode

#### **2. Crisis Detection Analytics**
- **High Crisis**: Immediate intervention alerts (last 24h/7d/30d views)
- **Medium Crisis**: Concerning situations requiring monitoring  
- **Low Crisis**: Mild concerns with gentle support recommendations
- **Total Messages**: All messages analyzed with accuracy metrics
- **Learning Effectiveness**: Real-time adaptation and improvement tracking

#### **3. Interactive Visualizations**
- **Crisis Trends**: Multi-timeframe charts (1h, 24h, 7d, 30d) with crisis pattern analysis
- **Learning Progress**: Visual representation of AI model improvements over time
- **Testing Performance**: Goal achievement tracking with pass/fail rate trends
- **Service Performance**: Response time tracking and availability monitoring
- **Real-time Updates**: All charts refresh automatically with WebSocket connections

#### **4. Testing Suite Integration**
- **Current Test Status**: Real-time testing progress and results
- **Goal Achievement**: Visual progress toward testing targets with percentage completion
- **Failure Analysis**: Detailed breakdown of failed test cases with recommendations
- **Historical Performance**: Testing trends over time with performance regression detection
- **One-Click Testing**: Manual test triggering with custom parameters

#### **5. Team Management Panel** (New in v2.1)
- **Active Users**: Currently logged-in team members with role indicators
- **Recent Activity**: Audit log of recent dashboard and system interactions
- **Permission Management**: Role-based access control configuration
- **Team Notifications**: Announcements and alerts for crisis response coordination

### **Advanced Features**

#### **Learning System Analytics**
- **False Positive Corrections**: Community-driven detection improvements
- **False Negative Learning**: Missed crisis identification and model updates
- **Pattern Recognition**: Automatic detection of community-specific language patterns
- **Adaptation Rate**: Speed and effectiveness of AI learning from team feedback
- **Knowledge Transfer**: Insights gained and applied across different crisis scenarios

#### **Real-Time Monitoring**
- **Auto-refresh**: Configurable update intervals from 10 seconds to 10 minutes
- **WebSocket Updates**: Instant notifications for critical changes and alerts
- **Service Monitoring**: Immediate alerts for service outages or performance degradation
- **Live Statistics**: Learning system changes and crisis detection updates in real-time
- **Performance Optimized**: Intelligent caching reduces server load while maintaining accuracy

#### **Data Export & Reporting**
- **CSV Export**: Crisis detection data, learning statistics, and testing results
- **JSON API**: Programmatic access to all dashboard data for external integrations
- **PDF Reports**: Automated daily/weekly summaries for stakeholders and management
- **Custom Reports**: Configurable reporting with date ranges and specific metrics
- **Data Retention**: Configurable data retention policies for compliance and storage management

## 🔌 API Integration

### **Dashboard API Endpoints**
```javascript
// Service Health & Status
GET /api/status                    # Combined service health status
GET /api/health                    # Dashboard health check
GET /api/services/bot              # Ash Bot specific health and metrics
GET /api/services/nlp              # NLP Server specific status
GET /api/services/testing          # Testing Suite status and results

// Crisis Detection Analytics  
GET /api/metrics                   # Crisis detection statistics
GET /api/crisis-trends             # Multi-timeframe crisis detection trends
GET /api/learning-stats            # Learning system analytics and effectiveness
GET /api/learning-progress         # Historical learning improvements

// Testing Integration
GET /api/testing/status            # Current test status and progress
GET /api/testing/results           # Latest test results with detailed analysis
GET /api/testing/history           # Historical testing performance
GET /api/testing/goals             # Goal achievement tracking
POST /api/testing/trigger          # Manual test execution (admin only)

// Team Management (New in v2.1)
GET /api/team/members              # Active team members and roles
GET /api/team/activity             # Recent team activity and audit log
GET /api/team/permissions          # Role and permission configuration
POST /api/team/notifications       # Send team notifications

// Data Export
GET /api/export/csv                # Export data in CSV format
GET /api/export/json               # Export data in JSON format
GET /api/reports/generate          # Generate PDF reports
```

### **External Service Integration**
```javascript
// Ash Bot Integration
GET /metrics                       # Bot performance statistics
GET /learning_statistics           # Bot learning system data
GET /health                        # Bot service health check
GET /crisis_data                   # Recent crisis detection data

// NLP Server Integration
GET /metrics                       # NLP server performance stats
GET /learning_statistics           # Learning system analytics
GET /model_status                  # AI model status and performance
GET /health                        # NLP service health check

// Testing Suite Integration
GET /api/test/status               # Current testing status
GET /api/test/results              # Latest comprehensive test results
GET /api/test/quick-validation     # Quick validation test results
POST /api/test/trigger             # Trigger new test execution
```

## 🛠️ Development

### **Project Structure**
```
ash-dash/
├── dashboard/                     # Backend server files
│   ├── server.js                 # Express.js server with enhanced SSL support
│   ├── routes/                   # API route handlers
│   │   ├── api.js               # Main API routes
│   │   ├── testing.js           # Testing suite integration
│   │   ├── team.js              # Team management routes
│   │   └── export.js            # Data export functionality
│   ├── middleware/               # Express middleware
│   │   ├── auth.js              # Authentication and RBAC
│   │   ├── cache.js             # Intelligent caching layer
│   │   └── security.js          # Security headers and protection
│   ├── services/                 # Business logic services
│   │   ├── metrics.js           # Metrics collection and processing
│   │   ├── testing.js           # Testing suite integration
│   │   └── learning.js          # Learning system analytics
│   └── package.json             # Node.js dependencies
├── public/                       # Frontend static files
│   ├── index.html               # Main dashboard interface
│   ├── css/                     # Stylesheets
│   │   ├── dashboard.css        # Main dashboard styles
│   │   ├── charts.css           # Chart-specific styles
│   │   └── responsive.css       # Mobile responsive styles
│   ├── js/                      # JavaScript files
│   │   ├── dashboard.js         # Main dashboard logic
│   │   ├── charts.js            # Chart configuration and updates
│   │   ├── websocket.js         # Real-time updates
│   │   └── team.js              # Team management interface
│   └── assets/                  # Static assets
├── certs/                        # SSL certificates (auto-generated)
│   ├── cert.pem                 # SSL certificate
│   └── key.pem                  # Private key
├── docs/                         # Documentation (New structure)
│   ├── DEPLOYMENT.md            # Complete deployment guide
│   ├── TEAM_GUIDE.md            # Team member usage guide
│   ├── IMPLEMENTATION.md        # Technical implementation guide
│   ├── API.md                   # API reference documentation
│   ├── TROUBLESHOOTING.md       # Common issues and solutions
│   └── SECURITY.md              # Security configuration guide
├── config/                       # Configuration files
│   ├── dashboard.json           # Dashboard configuration
│   ├── roles.json               # Role and permission definitions
│   └── notifications.json       # Notification templates
├── data/                         # Dashboard data storage
│   ├── cache/                   # Cached API responses
│   ├── logs/                    # Application logs
│   └── exports/                 # Generated exports and reports
├── docker-compose.yml            # Service orchestration
├── Dockerfile                    # Container configuration
├── .env.template                 # Environment configuration template
├── .env                         # Your actual configuration (don't commit!)
└── README.md                    # This documentation
```

### **Available Scripts**
```bash
npm start                         # Start production server
npm run dev                       # Start development server with nodemon
npm run build                     # Build and optimize frontend assets
npm test                          # Run comprehensive test suite
npm run test:unit                 # Run unit tests only
npm run test:integration          # Run integration tests
npm run lint                      # Run ESLint code checking
npm run lint:fix                  # Fix ESLint issues automatically
npm run ssl:generate              # Generate SSL certificates manually
npm run ssl:renew                 # Renew SSL certificates
npm run db:migrate                # Run database migrations
npm run cache:clear               # Clear all cached data
npm run logs:analyze              # Analyze log files for insights
```

### **Adding New Features**

1. **Backend API endpoints**: Add routes in `dashboard/routes/` directory
2. **Frontend components**: Modify `public/index.html` and associated JS/CSS
3. **Real-time features**: Use Socket.IO events for live updates and notifications
4. **Charts and visualizations**: Extend Chart.js configurations in `public/js/charts.js`
5. **Caching**: Implement intelligent caching for performance optimization in `dashboard/middleware/cache.js`
6. **Team features**: Add team management functionality in `dashboard/routes/team.js`

## 🔧 Deployment

### **Production Deployment (Docker)**

1. **Build and deploy**
```bash
docker-compose up -d
```

2. **Health verification**
```bash
# HTTPS (with SSL - recommended)
curl -k https://10.20.30.16:8883/health

# HTTP (fallback)
curl http://10.20.30.16:8883/health

# Comprehensive health check
curl -k https://10.20.30.16:8883/api/status
```

3. **View logs**
```bash
# Real-time logs
docker-compose logs -f ash-dash

# Specific log levels
docker-compose logs ash-dash | grep ERROR
docker-compose logs ash-dash | grep WARN
```

4. **Performance monitoring**
```bash
# Resource usage
docker stats ash-dash

# Service metrics
curl -k https://10.20.30.16:8883/api/metrics
```

### **SSL Certificate Management**

Enhanced SSL management in v2.1:

1. **Auto-generation and renewal (Default)**
   - Certificates are created automatically on first run
   - Automatic renewal before expiration (configurable)
   - Stored in `./certs/` directory with backup rotation
   - Valid for 365 days with 30-day renewal warning

2. **Custom certificates**
   ```bash
   # Place your certificates in ./certs/
   ./certs/cert.pem    # Your SSL certificate
   ./certs/key.pem     # Your private key
   ./certs/ca.pem      # Certificate authority (optional)
   ```

3. **Manual certificate management**
   ```bash
   # Generate new certificates
   npm run ssl:generate
   
   # Renew existing certificates
   npm run ssl:renew
   
   # Verify certificate validity
   npm run ssl:verify
   ```

### **Windows 11 Server Deployment**

Optimized for your Windows 11 AI server setup:

1. **Ensure Docker Desktop is running**
   - Docker Desktop 4.0+ with WSL2 backend
   - At least 4GB RAM allocated to Docker
   - Enable Hyper-V and containers features

2. **Configure Windows Firewall**
   ```powershell
   # Allow dashboard port
   New-NetFirewallRule -DisplayName "Ash Dashboard" -Direction Inbound -Port 8883 -Protocol TCP -Action Allow
   
   # Allow Redis port (if external access needed)
   New-NetFirewallRule -DisplayName "Ash Redis" -Direction Inbound -Port 6379 -Protocol TCP -Action Allow
   ```

3. **Monitor resource usage**
   ```powershell
   # Check Docker resource usage
   docker stats
   
   # Monitor Windows performance
   Get-Process -Name "Docker Desktop" | Select-Object CPU,WorkingSet
   ```

4. **Consider port conflicts**
   - Ensure port 8883 is not used by other services
   - Verify NLP Server (8881) and Testing Suite (8884) accessibility
   - Check Redis port (6379) availability

### **Integration with Existing Services**

The dashboard automatically discovers and connects to:

- **Ash Bot**: IP connection (10.20.30.253:8882) with failover support
- **NLP Server**: Local IP connection (10.20.30.16:8881) with health monitoring
- **Testing Suite**: Local connection (10.20.30.16:8884) with result caching
- **Redis**: Caching and session management (localhost:6379) with persistence

## 📈 Monitoring & Performance

### **Key Performance Indicators**

- **Crisis Detection Accuracy**: Track false positive/negative rates with trending analysis
- **Learning System Effectiveness**: Measure adaptation success and community language learning
- **Service Uptime**: Monitor all component availability with historical tracking
- **Response Times**: Track API performance across all integrated services
- **Community Safety**: Aggregate crisis intervention metrics with impact analysis
- **Testing Performance**: Monitor goal achievement and test suite effectiveness

### **Health Monitoring**

Enhanced health monitoring in v2.1:

- **Service availability**: Intelligent health checks with adaptive intervals
- **Response time tracking**: Performance metrics collection with anomaly detection
- **Error rate monitoring**: Automatic detection of service issues with alerting
- **Learning system status**: Track ML model performance and improvement trends
- **Resource monitoring**: CPU, memory, and disk usage tracking with optimization recommendations

### **Performance Optimization**

- **Multi-layer Caching**: Redis + in-memory caching reduces server load by 85%
- **Rate Limiting**: Advanced protection against API abuse with whitelist support  
- **Compression**: Gzip compression for faster data transfer and reduced bandwidth
- **Connection Pooling**: Efficient HTTP client management with connection reuse
- **Error Handling**: Graceful degradation when services are unavailable
- **Background Processing**: Non-blocking operations for better user experience
- **Resource Management**: Memory and CPU optimizations for Windows 11 server environment

## 🔒 Security & Privacy

### **Data Protection**
- **No personal data storage**: Dashboard displays aggregated, anonymized metrics only
- **Local processing**: All data remains within your infrastructure and network
- **Secure connections**: HTTPS/WSS encryption for all communications with enhanced ciphers
- **Access control**: Role-based dashboard access with customizable permissions
- **Data encryption**: Enhanced encryption for sensitive analytics data at rest and in transit

### **Privacy Considerations**
- **Anonymized analytics**: No user-identifiable information displayed or stored
- **Local deployment**: Runs entirely on your Windows 11 server infrastructure
- **Data retention**: Configurable analytics retention with automatic cleanup
- **GDPR compliance**: No personal data collection, processing, or storage
- **Audit compliance**: Complete activity logging for regulatory requirements

### **Security Features**
- **Enhanced SSL/TLS**: Modern encryption standards with automatic certificate management
- **Advanced Rate Limiting**: DDoS protection with intelligent threat detection
- **CORS protection**: Secure cross-origin resource sharing with configurable policies
- **Input validation**: Comprehensive sanitization and validation of all inputs
- **Security Headers**: Helmet.js implementation with CSP, HSTS, and other protections
- **Role-Based Access Control**: Granular permissions for different team member roles
- **Audit Logging**: Complete activity tracking with tamper-proof log storage

## 🚨 Troubleshooting

### **Common Issues**

#### **SSL Certificate Problems**
```bash
# Check certificate validity and expiration
openssl x509 -in ./certs/cert.pem -text -noout

# Check certificate chain
openssl verify -CAfile ./certs/ca.pem ./certs/cert.pem

# Regenerate certificates with auto-renewal
rm -rf ./certs/
docker-compose restart ash-dash
docker-compose logs ash-dash | grep "SSL"

# Disable SSL temporarily for debugging
echo "ENABLE_SSL=false" >> .env
docker-compose restart ash-dash
```

#### **Service Connection Issues**
```bash
# Test all service connectivity
curl http://10.20.30.253:8882/health    # Ash Bot
curl http://10.20.30.16:8881/health     # NLP Server  
curl http://10.20.30.16:8884/health     # Testing Suite
curl http://10.20.30.16:6379/           # Redis (should refuse HTTP)

# Check dashboard service discovery
curl -k https://10.20.30.16:8883/api/status

# Check dashboard logs for connection errors
docker-compose logs ash-dash | grep "connection\|error\|timeout"
```

#### **Dashboard Performance Issues**
```bash
# Check resource usage
docker stats ash-dash

# Check cache performance
curl -k https://10.20.30.16:8883/api/cache/stats

# Clear cache if corrupted
docker-compose exec ash-dash npm run cache:clear

# Check database connections
docker-compose exec ash-redis redis-cli ping
```

#### **Dashboard Won't Start**
```bash
# Check port availability
netstat -tulpn | grep 8883

# Check Docker service status
docker-compose ps

# Rebuild container with latest changes
docker-compose build --no-cache ash-dash
docker-compose up -d ash-dash

# Check detailed startup logs
docker-compose logs ash-dash | head -50
```

#### **Team Management Issues**
```bash
# Check role configuration
curl -k https://10.20.30.16:8883/api/team/permissions

# Reset team permissions to defaults
docker-compose exec ash-dash npm run team:reset

# Check audit log for permission errors
docker-compose logs ash-dash | grep "permission\|auth\|role"
```

### **Log Analysis**

```bash
# Real-time monitoring
docker-compose logs -f ash-dash

# Error analysis
docker-compose logs ash-dash | grep ERROR | tail -20

# Performance analysis
docker-compose logs ash-dash | grep "Response time\|Cache hit\|Database" | tail -50

# Security analysis
docker-compose logs ash-dash | grep "auth\|security\|failed\|blocked" | tail -20

# Team activity analysis
docker-compose logs ash-dash | grep "team\|user\|role\|permission" | tail -30
```

### **Performance Debugging**

```bash
# Generate performance report
curl -k https://10.20.30.16:8883/api/debug/performance

# Check memory usage
curl -k https://10.20.30.16:8883/api/debug/memory

# Analyze slow queries
curl -k https://10.20.30.16:8883/api/debug/slow-queries

# Test all integrations
curl -k https://10.20.30.16:8883/api/debug/integration-test
```

## 📚 Documentation

### **Complete Documentation Suite**

- **[📋 Deployment Guide](docs/deployment.md)** - Complete setup and deployment instructions
- **[👥 Team Guide](docs/team_guide.md)** - User-focused guide for Crisis Response teams
- **[🔧 Implementation Guide](docs/implementation.md)** - Technical implementation and development
- **[🔌 API Documentation](docs/api.md)** - Detailed API endpoint reference
- **[🛠️ Troubleshooting Guide](docs/troubleshooting.md)** - Common issues and solutions
- **[🔒 Security Guide](docs/security.md)** - Security configuration and best practices

### **Quick Reference**

- **Installation**: `docker-compose up -d`
- **Health Check**: `curl -k https://10.20.30.16:8883/health`
- **API Status**: `curl -k https://10.20.30.16:8883/api/status`
- **View Logs**: `docker-compose logs -f ash-dash`
- **Clear Cache**: `docker-compose exec ash-dash npm run cache:clear`

## 🤝 Contributing

### **Development Guidelines**
1. **Follow existing code style** and architectural patterns
2. **Add comprehensive tests** for new features and bug fixes
3. **Update documentation** for all changes including README and team guides
4. **Test with both HTTP and HTTPS** configurations
5. **Ensure compatibility** with existing Ash ecosystem services
6. **Consider performance impact** on Windows 11 server environment
7. **Implement proper error handling** and graceful degradation
8. **Add appropriate logging** for debugging and monitoring

### **Contribution Process**
1. **Create feature branch** from `main` with descriptive name
2. **Implement changes** following existing modular patterns and best practices
3. **Add tests** for new functionality with good coverage
4. **Update documentation** including README, API docs, and team guides
5. **Test thoroughly** with real Ash services and integration points
6. **Submit pull request** with comprehensive description and testing notes

### **Code Review Checklist**
- [ ] Code follows established patterns and style guidelines
- [ ] New features include comprehensive tests
- [ ] Documentation is updated and accurate
- [ ] Integration with Ash services works correctly
- [ ] Performance impact is considered and optimized
- [ ] Security implications are reviewed and addressed
- [ ] Error handling is robust and user-friendly

## 🛣️ Roadmap

### **v2.2 Planned Features** (Q1 2025)
- **Advanced Alerting**: Email/SMS notifications for critical events and threshold breaches
- **Custom Widgets**: Drag-and-drop dashboard customization for different team roles
- **Multi-Timezone Support**: Global team coordination with timezone-aware displays
- **Advanced Analytics**: Predictive analytics and trend forecasting for crisis patterns
- **Enhanced Mobile App**: Native mobile application for on-the-go monitoring

### **v2.5 Future Vision** (Q2 2025)
- **Multi-Community Support**: Monitor multiple Discord communities from single dashboard
- **Advanced AI Integration**: Enhanced prediction and pattern recognition capabilities
- **Integration Hub**: Connect with external crisis support services and resources
- **Federated Analytics**: Cross-community insights while preserving privacy
- **Advanced Reporting**: Executive-level reports with actionable insights and recommendations

### **v3.0 Goals** (Q3-Q4 2025)
- **Real-time Collaboration**: Team coordination and communication features within dashboard
- **Regulatory Compliance**: Enhanced privacy and security for healthcare integration
- **Advanced Learning**: Community-specific AI model training and deployment
- **Global Network**: Connect with other mental health support communities worldwide
- **Professional Services**: Integration with licensed mental health professionals

## 🙏 Acknowledgments

### **Technical Contributors**
- **Node.js Community** - Express.js, Socket.IO, and extensive ecosystem libraries
- **Chart.js Team** - Excellent data visualization capabilities and responsive design
- **Docker Community** - Containerization, orchestration, and deployment tools
- **Redis Labs** - High-performance caching and session management
- **Open Source Community** - Various libraries, tools, and frameworks that make this possible

### **Community Contributors**
- **The Alphabet Cartel Crisis Response Team** - Extensive testing, feedback, and feature requirements
- **Community Moderators** - Requirements gathering and user experience insights  
- **Beta Testers** - Early adopters who refined the dashboard experience and identified issues
- **Development Team** - Continuous improvement and feature development
- **Mental Health Advocates** - Guidance on crisis detection best practices and ethical considerations

## 📞 Support

### **Getting Help**
- **Issues**: Use [GitHub Issues](https://github.com/The-Alphabet-Cartel/ash-dash/issues) for bug reports and feature requests
- **Documentation**: Check this README and comprehensive guides in `/docs` directory
- **Community**: Join [The Alphabet Cartel Discord](https://discord.gg/alphabetcartel) for real-time support
- **Security**: Report security issues privately to repository maintainers

### **Support Channels**
- **Technical Issues**: GitHub Issues with detailed reproduction steps
- **Usage Questions**: Discord #tech-support channel for community help  
- **Feature Requests**: GitHub Discussions for community input and prioritization
- **Security Concerns**: Private communication with project maintainers

---

## 📦 Quick Installation Summary

```bash
# 1. Clone repository
git clone https://github.com/The-Alphabet-Cartel/ash-dash.git
cd ash-dash

# 2. Configure environment
cp .env.template .env
# Edit .env with your settings

# 3. Deploy with Docker
docker-compose up -d

# 4. Access dashboard
# HTTPS: https://10.20.30.16:8883 (recommended)
# HTTP:  http://10.20.30.16:8883 (fallback)

# 5. Verify deployment
curl -k https://10.20.30.16:8883/health
```

---

*"Monitoring mental health support systems with analytics, intelligence, and compassion."*

**Built with 🖤 for chosen family everywhere by [The Alphabet Cartel](https://discord.gg/alphabetcartel)**

---

> **Note**: This dashboard is specifically designed for The Alphabet Cartel's Ash Crisis Detection Bot ecosystem and requires the corresponding Bot, NLP, and Testing services to function properly. For standalone deployment or different configurations, please refer to the [Implementation Guide](docs/implementation.md).