# 📊 Ash Analytics Dashboard

> **Real-time analytics and monitoring for The Alphabet Cartel's Ash Crisis Detection System**

[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/The-Alphabet-Cartel/ash-dash)
[![Node.js](https://img.shields.io/badge/node.js-18+-green)](https://nodejs.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue)](https://docker.com/)
[![Discord](https://img.shields.io/badge/Discord-The%20Alphabet%20Cartel-purple)](https://discord.gg/alphabetcartel)

## 🎯 Overview

The Ash Analytics Dashboard provides comprehensive real-time monitoring and analytics for the Ash crisis detection ecosystem. Built specifically for **The Alphabet Cartel** Discord community, it offers visual insights into:

- **Crisis Detection Performance** - Real-time monitoring of high, medium, and low crisis alerts
- **Learning System Analytics** - Track false positive/negative learning and system adaptation
- **Service Health Monitoring** - Monitor Ash Bot and NLP Server status and performance
- **Community Safety Metrics** - Visual trends and patterns in crisis detection
- **Team Performance Insights** - Analytics for Crisis Response team effectiveness

## 🚀 Features

### 📈 **Real-Time Analytics**
- Live crisis detection metrics with auto-updating charts
- Learning system performance tracking and improvement trends
- Service health monitoring with response time tracking
- WebSocket-powered real-time updates for immediate insights

### 🧠 **Learning System Insights**
- **False Positive Learning** - Track and visualize reduction in inappropriate alerts
- **False Negative Learning** - Monitor improvements in missed crisis detection
- **Adaptation Analytics** - See how the system learns from Crisis Response team feedback
- **Performance Metrics** - Comprehensive statistics on detection accuracy improvements

### 🔍 **Service Monitoring**
- **Ash Bot Status** - Real-time health check and performance monitoring
- **NLP Server Status** - Monitor the AI analysis server (Windows 11 + RTX 3050)
- **Response Time Tracking** - Performance metrics for all services
- **Error Detection** - Immediate alerts for service issues

### 📊 **Visual Dashboard**
- **Crisis Trends Chart** - 24-hour rolling view of crisis detection patterns
- **Learning Performance Chart** - Visual representation of system improvements
- **Service Status Cards** - At-a-glance health indicators
- **Recent Activities Feed** - Real-time log of learning system actions

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Ash Analytics Dashboard                   │
│                    (Port 3000 - Node.js)                   │
└─────────────────┬───────────────────────────┬───────────────┘
                  │                           │
                  ▼                           ▼
┌─────────────────────────────┐ ┌─────────────────────────────┐
│         Ash Bot             │ │       Ash NLP Server        │
│    (Linux Docker)           │ │   (Windows 11 + RTX 3050)  │
│                             │ │        (Port 8881)          │
│ • Crisis Detection          │ │ • ML Analysis               │
│ • Discord Integration       │ │ • Learning System           │
│ • Team Commands             │ │ • Pattern Recognition       │
│ • Keyword Management        │ │ • Model Management          │
└─────────────────────────────┘ └─────────────────────────────┘
```

### **Technology Stack**
- **Frontend**: HTML5, TailwindCSS, Chart.js, Socket.IO
- **Backend**: Node.js, Express.js, Redis
- **Real-time**: WebSockets for live updates
- **Deployment**: Docker containers with health checks
- **Integration**: REST APIs to Ash Bot and NLP Server

## 🚀 Quick Start

### **Prerequisites**
- Node.js 18+ installed
- Docker and Docker Compose
- Access to Ash Bot and NLP Server APIs
- Windows 11 server with RTX 3050 GPU (for NLP Server)

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
- Open http://10.20.30.16:3000 (or your configured port)
- Dashboard will automatically connect to Ash services

### **Development Setup**

1. **Install dependencies**
```bash
npm install
```

2. **Configure environment**
```bash
cp .env.template .env
# Configure API endpoints and settings
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
PORT=3000
DASH_PORT=3000

# Service Endpoints
ASH_BOT_API=http://ash:8080
ASH_NLP_API=http://10.20.30.16:8881

# Performance Settings
CACHE_TTL=300
ENABLE_ANALYTICS=true
ANALYTICS_RETENTION_DAYS=90

# Real-time Updates
ENABLE_SOCKET_IO=true
METRICS_UPDATE_INTERVAL=300

# Dashboard Branding
DASHBOARD_TITLE="Ash Analytics Dashboard"
DASHBOARD_SUBTITLE="The Alphabet Cartel Crisis Detection Analytics"
COMMUNITY_NAME="The Alphabet Cartel"
COMMUNITY_DISCORD="https://discord.gg/alphabetcartel"

# Logging
LOG_LEVEL=info
LOG_FILE=ash-dash.log

# Security
ENABLE_CORS=true
RATE_LIMIT_WINDOW=900000
RATE_LIMIT_MAX=100
```

### **Docker Compose Integration**

The dashboard integrates seamlessly with the existing Ash ecosystem:

```yaml
# Add to your existing docker-compose.yml
services:
  ash-dash:
    image: ghcr.io/the-alphabet-cartel/ash-dash:latest
    container_name: ash-dash
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - ASH_BOT_API=http://ash:8080
      - ASH_NLP_API=http://10.20.30.16:8881
    networks:
      - ash-network
```

## 📊 Dashboard Features

### **Main Dashboard View**

1. **Service Status Row**
   - Ash Bot health and response time
   - NLP Server status and performance
   - Learning System activity indicator

2. **Crisis Detection Metrics**
   - High Crisis alerts (last 24h)
   - Medium Crisis alerts (last 24h)  
   - Low Crisis alerts (last 24h)
   - Total messages analyzed

3. **Interactive Charts**
   - Crisis detection trends over time
   - Learning system effectiveness visualization

4. **Learning Statistics**
   - False positive learning progress
   - False negative learning progress
   - Recent learning activities feed

### **Real-Time Features**

- **Auto-refresh**: Dashboard updates every 5 minutes automatically
- **WebSocket Updates**: Real-time metrics when changes occur
- **Service Monitoring**: Immediate alerts for service issues
- **Live Statistics**: Learning system changes reflected instantly

## 🔌 API Integration

### **Bot Integration Endpoints**
```javascript
GET /api/metrics          # Crisis detection statistics
GET /api/crisis-trends    # 24-hour crisis detection trends
GET /api/keyword-performance  # Keyword effectiveness metrics
GET /health               # Service health check
```

### **NLP Server Integration**
```javascript
GET /metrics              # NLP server performance stats
GET /learning_statistics  # Learning system analytics
GET /health               # NLP service health check
```

### **Dashboard APIs**
```javascript
GET /api/status           # Combined service status
GET /api/learning-stats   # Learning system analytics
GET /health               # Dashboard health check
```

## 🛠️ Development

### **Project Structure**
```
ash-dash/
├── public/               # Static frontend files
│   ├── index.html       # Main dashboard interface
│   └── assets/          # CSS, JS, images
├── server.js            # Express.js server
├── package.json         # Node.js dependencies
├── Dockerfile           # Container configuration
├── docker-compose.yml   # Service orchestration
├── .env.template        # Environment configuration template
└── README.md           # This file
```

### **Available Scripts**
```bash
npm start              # Start production server
npm run dev           # Start development server with nodemon
npm run build         # Build frontend assets
npm test              # Run test suite
npm run lint          # Run ESLint
npm run lint:fix      # Fix ESLint issues automatically
```

### **Adding New Features**

1. **Backend API endpoints**: Add routes in `server.js`
2. **Frontend components**: Modify `public/index.html` and associated JS
3. **Real-time features**: Use Socket.IO events for live updates
4. **Charts and visualizations**: Extend Chart.js configurations

## 🔧 Deployment

### **Production Deployment (Docker)**

1. **Build and deploy**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

2. **Health verification**
```bash
curl http://10.20.30.16:3000/health
```

3. **View logs**
```bash
docker-compose logs -f ash-dash
```

### **Windows 11 Server Deployment**

Since this runs on the same Windows 11 server as the NLP service:

1. **Ensure Docker Desktop is running**
2. **Configure Windows Firewall** for port 3000
3. **Set up port forwarding** if needed for external access
4. **Monitor resource usage** alongside NLP Server

### **Integration with Existing Services**

The dashboard automatically discovers and connects to:
- **Ash Bot**: via Docker network (`ash-network`)
- **NLP Server**: via direct IP connection (10.20.30.16:8881)
- **Redis**: for caching and session management

## 📈 Monitoring & Metrics

### **Key Performance Indicators**

- **Crisis Detection Accuracy**: Track false positive/negative rates
- **Learning System Effectiveness**: Measure adaptation success
- **Service Uptime**: Monitor all component availability
- **Response Times**: Track API performance across services
- **Community Safety**: Aggregate crisis intervention metrics

### **Health Checks**

The dashboard includes comprehensive health monitoring:
- **Service availability**: Regular ping checks to Bot and NLP Server
- **Response time tracking**: Performance metrics collection
- **Error rate monitoring**: Automatic detection of service issues
- **Learning system status**: Track ML model performance

## 🔒 Security & Privacy

### **Data Protection**
- **No personal data storage**: Dashboard displays aggregated metrics only
- **Local processing**: All data remains within your infrastructure
- **Secure connections**: HTTPS/WSS encryption for production
- **Access control**: Dashboard access can be restricted by IP/network

### **Privacy Considerations**
- **Anonymized analytics**: No user-identifiable information displayed
- **Local deployment**: Runs entirely on your Windows 11 server
- **Data retention**: Configurable analytics retention period
- **GDPR compliance**: No personal data collection or storage

## 🤝 Contributing

### **Development Guidelines**
1. Follow existing code style and patterns
2. Add tests for new features
3. Update documentation for changes
4. Test with real Ash Bot and NLP Server instances

### **Feature Requests**
- Use GitHub Issues for feature requests
- Include use case and community benefit
- Consider Crisis Response team workflow impact

## 📚 Documentation

### **Additional Resources**
- **[Ash Bot Documentation](https://github.com/The-Alphabet-Cartel/ash/README.md)** - Main bot documentation
- **[NLP Server Documentation](https://github.com/The-Alphabet-Cartel/ash-nlp/README.md)** - AI analysis server
- **[Team Guide](https://github.com/The-Alphabet-Cartel/ash/TEAM_GUIDE.md)** - Crisis Response team procedures
- **[API Documentation](docs/API.md)** - Complete API reference for integration

## 🛣️ Roadmap

### **v1.1 (Next Release)**
- **Enhanced Learning Visualization** - More detailed learning system analytics
- **Custom Time Ranges** - Configurable chart timeframes (1h, 6h, 24h, 7d)
- **Export Functionality** - Download reports and analytics data
- **Alert Thresholds** - Configurable notifications for crisis detection spikes

### **v1.2 (Planned)**
- **User Activity Tracking** - Crisis Response team member analytics
- **Advanced Filtering** - Filter metrics by channel, time, crisis level
- **Performance Benchmarking** - Compare current vs historical performance
- **Mobile Responsive Design** - Optimized dashboard for mobile devices

### **v2.0 (Future)**
- **Predictive Analytics** - Machine learning insights for crisis prevention
- **External Integrations** - Connect with external mental health resources
- **Multi-Community Support** - Support for multiple Discord servers
- **Advanced Reporting** - Automated report generation and distribution

## 🚨 Troubleshooting

### **Common Issues**

**Dashboard not loading:**
```bash
# Check if services are running
docker-compose ps

# Verify network connectivity
curl http://10.20.30.16:3000/health

# Check logs for errors
docker-compose logs ash-dash
```

**No data displayed:**
```bash
# Verify API connectivity
curl http://ash:8080/api/metrics
curl http://10.20.30.16:8881/metrics

# Check service endpoints in .env file
# Ensure ASH_BOT_API and ASH_NLP_API are correct
```

**Real-time updates not working:**
```bash
# Check WebSocket connection in browser console
# Verify ENABLE_SOCKET_IO=true in .env
# Check firewall settings for WebSocket connections
```

**Performance issues:**
```bash
# Monitor resource usage
docker stats ash-dash

# Check cache performance
# Consider reducing CACHE_TTL if memory constrained
# Monitor Redis performance
```

### **Windows 11 Server Specific**

**Port conflicts:**
```bash
# Check if port 3000 is available
netstat -an | findstr :3000

# Use different port if needed
# Set DASH_PORT=3001 in .env
```

**Docker Desktop issues:**
```bash
# Restart Docker Desktop
# Check Windows Docker integration settings
# Verify WSL2 backend is enabled
```

**Network connectivity:**
```bash
# Test connection to NLP server
curl http://10.20.30.16:8881/health

# Check Windows Firewall settings
# Verify Docker network configuration
```

### **Getting Help**

**For Technical Issues:**
- Check GitHub Issues for similar problems
- Include logs and error messages when reporting
- Specify your environment (Windows 11, Docker version, etc.)

**For Feature Requests:**
- Use GitHub Issues with `enhancement` label
- Describe the use case and expected benefit
- Consider impact on Crisis Response team workflow

**For Community Support:**
- Join [The Alphabet Cartel Discord](https://discord.gg/alphabetcartel)
- Ask in development/technical channels
- Tag relevant team members for assistance

## 📝 License

Built exclusively for **The Alphabet Cartel** Discord community. Internal use only.

This project is not licensed for external use or distribution. All rights reserved.

## 🙏 Acknowledgments

### **Technical Contributors**
- **Node.js Community** - Excellent runtime and ecosystem
- **Chart.js Team** - Beautiful and responsive charting library
- **TailwindCSS** - Modern utility-first CSS framework
- **Socket.IO** - Reliable real-time communication
- **Docker Community** - Containerization best practices

### **Community Contributors**
- **The Alphabet Cartel Crisis Response Team** - Requirements and feedback
- **Community Members** - Testing and usage insights
- **Beta Testers** - Early adoption and bug reports
- **Mental Health Advocates** - Guidance on effective crisis analytics

### **Open Source Ecosystem**
- **Express.js** - Fast and minimal web framework
- **Redis** - High-performance caching and data structure store
- **Winston** - Reliable logging for Node.js applications
- **GitHub Actions** - Automated CI/CD pipeline

---

## 📦 Quick Commands Reference

```bash
# Development
npm install                    # Install dependencies
npm run dev                   # Start development server
npm run build                 # Build for production

# Docker Deployment
docker-compose up -d          # Start all services
docker-compose down           # Stop all services
docker-compose logs -f        # Follow logs
docker-compose pull           # Update images

# Health Checks
curl http://10.20.30.16:3000/health     # Dashboard health
curl http://10.20.30.16:8881/health     # NLP Server health
curl http://ash:8080/health              # Bot health (from within network)

# Monitoring
docker stats                  # Resource usage
docker-compose ps            # Service status
```

---

## 🎯 Integration Checklist

When setting up the Ash Analytics Dashboard:

- [ ] **Environment configured** - .env file with correct API endpoints
- [ ] **Services running** - Ash Bot and NLP Server operational
- [ ] **Network connectivity** - Dashboard can reach both services
- [ ] **Port availability** - Port 3000 (or configured port) accessible
- [ ] **Health checks passing** - All services report healthy status
- [ ] **Real-time updates working** - WebSocket connection established
- [ ] **Data flowing** - Metrics and analytics populating correctly
- [ ] **Charts rendering** - Visual components displaying data
- [ ] **Learning stats available** - NLP Server learning system active

---

**Built with 🖤 for The Alphabet Cartel chosen family everywhere.**

*"We've all been in that dark place where everything feels impossible. You're not alone."* - Ash

**For more information, visit [The Alphabet Cartel Discord](https://discord.gg/alphabetcartel)**