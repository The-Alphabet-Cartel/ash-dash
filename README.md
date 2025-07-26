# 📊 Ash Analytics Dashboard

Real-time monitoring and analytics dashboard for The Alphabet Cartel's Ash Crisis Detection Bot ecosystem.

[![GitHub](https://img.shields.io/badge/GitHub-The--Alphabet--Cartel-black?style=flat-square&logo=github)](https://github.com/The-Alphabet-Cartel/ash-dash)
[![Discord](https://img.shields.io/badge/Discord-The%20Alphabet%20Cartel-5865F2?style=flat-square&logo=discord)](https://discord.gg/alphabetcartel)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=flat-square&logo=docker)](https://hub.docker.com)

## 🌟 Overview

The Ash Analytics Dashboard provides comprehensive real-time monitoring and insights for your mental health crisis detection system. Built specifically for The Alphabet Cartel Discord community, it tracks service health, crisis detection metrics, and learning system performance across your entire Ash ecosystem.

### **Architecture Overview**
```
           ▼
┌─────────────────────────────┐ ┌─────────────────────────────┐ ┌─────────────────────────────┐
│         Ash Bot             │ │       Ash NLP Server        │ │     Analytics Dashboard     │
│    (Linux Docker)           │ │   (Windows 11 + RTX 3050)  │ │    (Windows 11 Docker)      │
│   IP: 10.20.30.253:8882     │ │      IP: 10.20.30.16:8881   │ │    IP: 10.20.30.16:8883     │
│                             │ │                             │ │                             │
│ • Crisis Detection          │ │ • ML Analysis               │ │ • Real-time Monitoring      │
│ • Discord Integration       │ │ • Learning System           │ │ • Service Health Checks     │
│ • Team Commands             │ │ • Pattern Recognition       │ │ • Crisis Analytics          │
│ • Keyword Management        │ │ • Model Management          │ │ • Learning Insights         │
└─────────────────────────────┘ └─────────────────────────────┘ └─────────────────────────────┘
```

### **Technology Stack**
- **Frontend**: HTML5, TailwindCSS, Chart.js, Socket.IO
- **Backend**: Node.js, Express.js, Winston Logging
- **Real-time**: WebSockets for live updates
- **Security**: SSL/HTTPS with self-signed certificates
- **Deployment**: Docker containers with health checks
- **Integration**: REST APIs to Ash Bot and NLP Server

## 🚀 Quick Start

### **Prerequisites**
- Docker and Docker Compose installed
- Access to Ash Bot API (10.20.30.253:8882)
- Access to NLP Server API (10.20.30.16:8881)
- Windows 11 server (for your setup) or Linux server

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
- **HTTPS**: https://10.20.30.16:8883 (with SSL)
- **HTTP**: http://10.20.30.16:8883 (fallback)
- Dashboard will automatically connect to Ash services

### **Development Setup**

1. **Install dependencies**
```bash
cd dashboard
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
PORT=8883
ENABLE_SSL=true

# SSL Configuration
SSL_CERT_PATH=/app/certs/cert.pem
SSL_KEY_PATH=/app/certs/key.pem

# Service Endpoints
ASH_BOT_API=http://10.20.30.253:8882
ASH_NLP_API=http://10.20.30.16:8881

# Performance Settings (Optimized for reduced server load)
CACHE_TTL=600                    # 10 minutes cache
HEALTH_CHECK_INTERVAL=120000     # 2 minutes between health checks
METRICS_UPDATE_INTERVAL=60000    # 1 minute real-time updates

# Dashboard Branding
DASHBOARD_TITLE="Ash Analytics Dashboard"
DASHBOARD_SUBTITLE="The Alphabet Cartel Crisis Detection Analytics"
COMMUNITY_NAME="The Alphabet Cartel"
COMMUNITY_DISCORD="https://discord.gg/alphabetcartel"

# Security & Rate Limiting
ENABLE_CORS=true
RATE_LIMIT_WINDOW=900000         # 15 minutes
RATE_LIMIT_MAX=100               # 100 requests per window

# Logging
LOG_LEVEL=info
LOG_FILE=ash-dash.log
```

### **Docker Compose Integration**

The dashboard integrates seamlessly with the existing Ash ecosystem:

```yaml
services:
  ash-dash:
    image: ghcr.io/the-alphabet-cartel/ash-dash:latest
    container_name: ash-dash
    restart: unless-stopped
    ports:
      - "8883:8883"
    environment:
      - NODE_ENV=production
      - ENABLE_SSL=true
      - ASH_BOT_API=http://10.20.30.253:8882
      - ASH_NLP_API=http://10.20.30.16:8881
    volumes:
      - ./logs:/app/logs
      - ./certs:/app/certs
    networks:
      - ash-network
    depends_on:
      - ash-redis
```

## 📊 Dashboard Features

### **Main Dashboard View**

#### **1. Service Status Row**
- **Ash Bot**: Health status and response time monitoring
- **NLP Server**: ML service status and performance metrics
- **Dashboard**: Local service health and uptime

Real-time status indicators:
- 🟢 **Green**: Service healthy and responding normally
- 🔴 **Red**: Service down or experiencing issues
- 🟡 **Yellow**: Service degraded performance

#### **2. Crisis Detection Metrics**
- **High Crisis**: Immediate intervention alerts (last 24h)
- **Medium Crisis**: Concerning situations requiring monitoring (last 24h)
- **Low Crisis**: Mild concerns with gentle support (last 24h)
- **Total Messages**: All messages analyzed by the system

#### **3. Interactive Charts**
- **Crisis Trends**: 24-hour timeline showing crisis detection patterns
- **Real-time Updates**: Charts refresh automatically with new data
- **Color Coding**: Consistent crisis level colors (Red/Yellow/Green)

#### **4. Learning System Analytics**
- **False Positives**: Corrections made to over-sensitive detections
- **False Negatives**: Missed crises that were manually reported
- **Learning Effectiveness**: Overall system improvement percentage
- **Total Adjustments**: Cumulative learning corrections applied

### **Real-Time Features**

- **Auto-refresh**: Dashboard updates every 2 minutes automatically
- **WebSocket Updates**: Instant notifications for critical changes
- **Service Monitoring**: Immediate alerts for service outages
- **Live Statistics**: Learning system changes reflected in real-time
- **Performance Optimized**: Reduced API calls to minimize server load

## 🔌 API Integration

### **Bot Integration Endpoints**
```javascript
GET /api/status              # Combined service health status
GET /api/metrics             # Crisis detection statistics  
GET /api/crisis-trends       # 24-hour crisis detection trends
GET /api/learning-stats      # Learning system analytics
GET /health                  # Dashboard health check
```

### **NLP Server Integration**
```javascript
GET /metrics                 # NLP server performance stats
GET /learning_statistics     # Learning system analytics
GET /health                  # NLP service health check
```

### **Dashboard Internal APIs**
```javascript
GET /api/nlp-metrics         # NLP server performance proxy
GET /health                  # Dashboard health and uptime
```

## 🛠️ Development

### **Project Structure**
```
ash-dash/
├── dashboard/               # Backend server files
│   ├── server.js           # Express.js server with SSL support
│   └── package.json        # Node.js dependencies
├── public/                 # Frontend static files
│   └── index.html          # Main dashboard interface
├── certs/                  # SSL certificates (auto-generated)
│   ├── cert.pem           # SSL certificate
│   └── key.pem            # Private key
├── docker-compose.yml      # Service orchestration
├── Dockerfile              # Container configuration
├── .env.template           # Environment configuration template
├── .env                    # Your actual configuration (don't commit!)
├── logs/                   # Application logs
├── data/                   # Dashboard data storage
└── README.md              # This documentation
```

### **Available Scripts**
```bash
npm start                   # Start production server
npm run dev                 # Start development server with nodemon
npm run build              # Build frontend assets (placeholder)
npm test                   # Run test suite
npm run lint               # Run ESLint code checking
npm run lint:fix           # Fix ESLint issues automatically
npm run ssl:generate       # Generate SSL certificates manually
```

### **Adding New Features**

1. **Backend API endpoints**: Add routes in `dashboard/server.js`
2. **Frontend components**: Modify `public/index.html` and associated JS
3. **Real-time features**: Use Socket.IO events for live updates
4. **Charts and visualizations**: Extend Chart.js configurations
5. **Caching**: Implement intelligent caching for performance optimization

## 🔧 Deployment

### **Production Deployment (Docker)**

1. **Build and deploy**
```bash
docker-compose up -d
```

2. **Health verification**
```bash
# HTTPS (with SSL)
curl -k https://10.20.30.16:8883/health

# HTTP (fallback)
curl http://10.20.30.16:8883/health
```

3. **View logs**
```bash
docker-compose logs -f ash-dash
```

### **SSL Certificate Setup**

The dashboard automatically generates self-signed SSL certificates, but you can provide your own:

1. **Auto-generation (Default)**
   - Certificates are created automatically on first run
   - Stored in `./certs/` directory
   - Valid for 365 days

2. **Custom certificates**
   ```bash
   # Place your certificates in ./certs/
   ./certs/cert.pem    # Your SSL certificate
   ./certs/key.pem     # Your private key
   ```

3. **Manual generation**
   ```bash
   npm run ssl:generate
   ```

### **Windows 11 Server Deployment**

Since this runs on your Windows 11 AI server:

1. **Ensure Docker Desktop is running**
2. **Configure Windows Firewall** to allow port 8883
3. **Monitor resource usage** alongside NLP Server
4. **Consider port conflicts** with other services

### **Integration with Existing Services**

The dashboard automatically discovers and connects to:
- **Ash Bot**: via IP connection (10.20.30.253:8882)
- **NLP Server**: via local IP connection (10.20.30.16:8881)
- **Redis**: for caching and session management (if configured)

## 📈 Monitoring & Performance

### **Key Performance Indicators**

- **Crisis Detection Accuracy**: Track false positive/negative rates
- **Learning System Effectiveness**: Measure adaptation success over time
- **Service Uptime**: Monitor all component availability
- **Response Times**: Track API performance across services
- **Community Safety**: Aggregate crisis intervention metrics

### **Health Monitoring**

The dashboard includes comprehensive health monitoring:
- **Service availability**: Regular health checks (every 2 minutes)
- **Response time tracking**: Performance metrics collection
- **Error rate monitoring**: Automatic detection of service issues
- **Learning system status**: Track ML model performance and improvements

### **Performance Optimization**

- **Intelligent Caching**: 2-10 minute caching reduces server load by ~75%
- **Rate Limiting**: Prevents API abuse and ensures fair usage
- **Compression**: Gzip compression for faster data transfer
- **Connection Pooling**: Efficient HTTP client management
- **Error Handling**: Graceful degradation when services are unavailable

## 🔒 Security & Privacy

### **Data Protection**
- **No personal data storage**: Dashboard displays aggregated metrics only
- **Local processing**: All data remains within your infrastructure
- **Secure connections**: HTTPS/WSS encryption for all communications
- **Access control**: Dashboard access can be restricted by IP/network

### **Privacy Considerations**
- **Anonymized analytics**: No user-identifiable information displayed
- **Local deployment**: Runs entirely on your Windows 11 server
- **Data retention**: Configurable analytics retention period
- **GDPR compliance**: No personal data collection or storage

### **Security Features**
- **SSL/TLS encryption**: All communications encrypted
- **Rate limiting**: Protection against abuse and DoS attacks
- **CORS protection**: Secure cross-origin resource sharing
- **Input validation**: Sanitized inputs and secure API calls
- **Helmet.js**: Security headers for web protection

## 🚨 Troubleshooting

### **Common Issues**

#### **SSL Certificate Problems**
```bash
# Check certificate validity
openssl x509 -in ./certs/cert.pem -text -noout

# Regenerate certificates
rm -rf ./certs/
docker-compose restart ash-dash

# Disable SSL temporarily
echo "ENABLE_SSL=false" >> .env
docker-compose restart ash-dash
```

#### **Service Connection Issues**
```bash
# Test Bot API connectivity
curl http://10.20.30.253:8882/health

# Test NLP API connectivity  
curl http://10.20.30.16:8881/health

# Check dashboard logs
docker-compose logs ash-dash
```

#### **Dashboard Won't Start**
```bash
# Check port availability
netstat -tulpn | grep 8883

# Rebuild container
docker-compose build --no-cache ash-dash
docker-compose up -d ash-dash

# Check logs for errors
docker-compose logs ash-dash
```

### **Log Analysis**

```bash
# Real-time logs
docker-compose logs -f ash-dash

# Error-only logs
docker-compose logs ash-dash | grep ERROR

# Performance logs
docker-compose logs ash-dash | grep "Response time"
```

## 📚 Documentation

- **[Deployment Guide](DEPLOYMENT.md)** - Complete setup and deployment instructions
- **[Quick Fix Guide](QUICK_FIX.md)** - Common troubleshooting solutions
- **[API Documentation](docs/API.md)** - Detailed API endpoint documentation
- **[Security Guide](docs/SECURITY.md)** - Security configuration and best practices

## 🤝 Contributing

### **Development Guidelines**
1. Follow existing code style and patterns
2. Add tests for new features
3. Update documentation for changes
4. Test with both HTTP and HTTPS configurations
5. Ensure compatibility with existing Ash ecosystem

### **Contribution Process**
1. **Create feature branch** from `main`
2. **Implement changes** following existing patterns
3. **Test thoroughly** with real Ash services
4. **Update documentation** including README and guides
5. **Submit pull request** with comprehensive description

## 🛣️ Roadmap

### **v1.1 Planned Features**
- **Advanced Charts**: More detailed analytics and visualization options
- **User Management**: Role-based access control for different team members
- **Alerting System**: Email/SMS notifications for critical events
- **Data Export**: CSV/JSON export capabilities for external analysis
- **Custom Dashboards**: Configurable layouts for different team roles

### **v1.5 Future Vision**
- **Mobile App**: Native mobile application for on-the-go monitoring
- **Advanced Analytics**: Machine learning insights and predictive analytics
- **Multi-Community**: Support for monitoring multiple Discord communities
- **Integration Hub**: Connect with external crisis support services

### **v2.0 Goals**
- **Federated Monitoring**: Cross-community analytics while preserving privacy
- **Advanced AI Integration**: Enhanced prediction and pattern recognition
- **Real-time Collaboration**: Team coordination and communication features
- **Regulatory Compliance**: Enhanced privacy and security for healthcare integration

## 🙏 Acknowledgments

### **Technical Contributors**
- **Node.js Community** - Express.js, Socket.IO, and ecosystem libraries
- **Chart.js Team** - Excellent data visualization capabilities
- **Docker Community** - Containerization and deployment tools
- **Open Source Community** - Various libraries and tools that make this possible

### **Community Contributors**
- **The Alphabet Cartel Crisis Response Team** - Extensive testing and feedback
- **Community Moderators** - Requirements gathering and user experience insights
- **Beta Testers** - Early adopters who refined the dashboard experience

## 📞 Support

- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Documentation**: Check this README and additional guides in `/docs`
- **Community**: Join [The Alphabet Cartel Discord](https://discord.gg/alphabetcartel)
- **Security**: Report security issues privately to repository maintainers

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
# HTTPS: https://10.20.30.16:8883
# HTTP:  http://10.20.30.16:8883
```

---

*"Monitoring mental health support systems with analytics and compassion."*

**Built with 🖤 for chosen family everywhere by [The Alphabet Cartel](https://discord.gg/alphabetcartel)**

---

![Dashboard Preview](docs/images/dashboard-preview.png)

> **Note**: This dashboard is specifically designed for The Alphabet Cartel's Ash Crisis Detection Bot ecosystem and requires the corresponding Bot and NLP services to function properly.