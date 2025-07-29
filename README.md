# 📊 Ash Dashboard (ash-dash) v2.1

**Analytics Dashboard for Crisis Detection and Community Support**  
**Repository:** https://github.com/the-alphabet-cartel/ash-dash  
**Part of:** [The Alphabet Cartel](https://discord.gg/alphabetcartel) Ash Ecosystem

## 🌟 Overview

Ash Dashboard is the comprehensive analytics and monitoring interface for the Ash Crisis Detection ecosystem. It provides real-time insights, team management capabilities, and detailed reporting for Discord community mental health support.

### 🎯 Key Features

- **Real-Time Crisis Monitoring** - Live dashboard with active crisis situations
- **Analytics & Reporting** - Detailed metrics on crisis detection accuracy and response times
- **Team Management** - Crisis Response team coordination and role management
- **Historical Analysis** - Long-term trends and pattern recognition
- **Integration Hub** - Central monitoring for all Ash ecosystem components
- **Secure Access** - Role-based access control with audit logging

## 🏗️ Architecture

The dashboard integrates with all Ash ecosystem components:

- **ash-bot** (10.20.30.253:8882) - Discord bot crisis detection events
- **ash-nlp** (10.20.30.253:8881) - NLP analysis results and confidence scores
- **ash-thrash** (10.20.30.253:8884) - Testing results and validation metrics
- **Dashboard Server** (10.20.30.253:8883) - Main dashboard application

### 🌐 Access Points

- **Primary URL:** https://dashboard.alphabetcartel.net
- **Direct Access:** https://10.20.30.253:8883
- **Development:** http://localhost:8883

## 🚀 Quick Start

### Production Deployment (Submodule Method)

```bash
# Clone main Ash repository (includes all submodules)
git clone --recursive https://github.com/the-alphabet-cartel/ash.git
cd ash/ash-dash

# Configure environment
cp .env.template .env
# Edit .env with your configuration

# Deploy with Docker
docker-compose up -d

# Verify deployment
curl https://10.20.30.253:8883/health
```

### Standalone Deployment

```bash
# Clone dashboard repository directly
git clone https://github.com/the-alphabet-cartel/ash-dash.git
cd ash-dash

# Setup environment
cp .env.template .env

# Configure service endpoints in .env
# GLOBAL_BOT_API_URL=http://10.20.30.253:8882
# GLOBAL_NLP_API_URL=http://10.20.30.253:8881
# ASH_TESTING_API=http://10.20.30.253:8884

# Deploy
docker-compose up -d
```

## 🔧 Configuration

### Essential Environment Variables

```bash
# Server Configuration
GLOBAL_DASH_API_PORT=8883
DASH_ENABLE_SSL=true

# Service Endpoints
GLOBAL_BOT_API_URL=http://10.20.30.253:8882
GLOBAL_NLP_API_URL=http://10.20.30.253:8881
ASH_TESTING_API=http://10.20.30.253:8884

# Performance Settings (Optimized for dedicated server)
DASH_CACHE_TTL=300
DASH_METRICS_UPDATE_INTERVAL=30000

# Security Settings
GLOBAL_API_ENABLE_CORS=true
DASH_RATE_LIMIT_MAX=200
ENABLE_DDoS_PROTECTION=true

# Team Management
ENABLE_RBAC=true
ENABLE_AUDIT_LOG=true
DEFAULT_ROLE=observer
```

### Hardware Optimization

**Server Specifications:**
- **OS:** Debian 12 Linux
- **CPU:** AMD Ryzen 7 5800X
- **GPU:** NVIDIA RTX 3060
- **RAM:** 64GB
- **Network:** 10.20.30.253 (Internal IP)

## 📊 Dashboard Features

### Crisis Response Dashboard
- **Active Incidents** - Real-time crisis situations requiring attention
- **Response Teams** - Team member availability and current assignments
- **Escalation Tracking** - Crisis severity changes and intervention progress
- **Communication Logs** - Secure record of crisis interventions

### Analytics Portal
- **Detection Accuracy** - NLP model performance metrics and trends
- **Response Metrics** - Average response times and resolution rates
- **Community Health** - Overall community mental health indicators
- **Predictive Insights** - Early warning systems and trend analysis

### Team Management
- **Role-Based Access** - Hierarchical permissions for different team roles
- **Shift Management** - Crisis response team scheduling and availability
- **Training Metrics** - Team member competency tracking and development
- **Communication Hub** - Secure team coordination and messaging

### System Monitoring
- **Service Health** - Real-time status of all Ash ecosystem components
- **Performance Metrics** - System resource usage and optimization insights
- **Error Tracking** - Centralized logging and error analysis
- **Capacity Planning** - Usage trends and scaling recommendations

## 🔗 Integration

### Ash Ecosystem Integration

**ash-bot Integration:**
- Real-time crisis event streaming
- Discord user context and history
- Bot command execution and monitoring
- Community engagement metrics

**ash-nlp Integration:**
- Live NLP analysis results
- Model confidence scores and accuracy
- Performance monitoring and optimization
- Custom model deployment status

**ash-thrash Integration:**
- Automated testing results display
- Testing schedule management
- Performance regression alerts
- Historical testing trends

### External Integrations

**Discord Integration:**
- OAuth2 authentication with Discord
- Server member verification
- Role synchronization
- Direct message capabilities (for authorized personnel)

**Monitoring Integration:**
- Health check endpoints for external monitoring
- Metrics export for Prometheus/Grafana
- Alert webhook integration
- Log aggregation support

## 🛡️ Security & Privacy

### Access Control
- **OAuth2 Authentication** - Secure Discord-based login
- **Role-Based Permissions** - Granular access control by team role
- **Session Management** - Secure session handling with timeout
- **Audit Logging** - Complete access and action logging

### Data Protection
- **Encrypted Communications** - All data transmission encrypted
- **Privacy Compliance** - GDPR-compliant data handling
- **Data Retention** - Configurable data retention policies
- **Anonymization** - Personal data anonymization for analytics

### Operational Security
- **Rate Limiting** - DDoS protection and abuse prevention
- **Input Validation** - Comprehensive input sanitization
- **Security Headers** - Modern web security headers implemented
- **Regular Updates** - Automated security patch management

## 🧪 Testing & Validation

### Automated Testing
```bash
# Run dashboard tests
npm test

# Integration testing with other services
npm run test:integration

# Performance testing
npm run test:performance

# Security testing
npm run test:security
```

### Manual Testing
```bash
# Health check
curl https://10.20.30.253:8883/health

# Service connectivity
curl https://10.20.30.253:8883/api/services/status

# Authentication test
curl -H "Authorization: Bearer $TOKEN" https://10.20.30.253:8883/api/user/profile
```

## 📚 Documentation

### Complete Documentation Suite

- **[Deployment Guide](docs/deployment_v2_1.md)** - Production and development deployment
- **[GitHub Release Guide](docs/github_release_v2_1.md)** - Release management procedures
- **[Team Guide](docs/team/team_guide_v2_1.md)** - Crisis Response team procedures
- **[API Documentation](docs/tech/api_v2_1.md)** - Complete REST API reference
- **[Architecture Guide](docs/tech/architecture_v2_1.md)** - System design and components
- **[Implementation Guide](docs/tech/implementation_v2_1.md)** - Technical setup and configuration
- **[Troubleshooting Guide](docs/tech/troubleshooting_v2_1.md)** - Common issues and solutions

### Quick Reference

**Essential Commands:**
```bash
# Health check
curl https://10.20.30.253:8883/health

# Restart services
docker-compose restart

# View logs
docker-compose logs ash-dash -f

# Update deployment
git pull && docker-compose up -d --build
```

**Key URLs:**
- Dashboard: https://dashboard.alphabetcartel.net
- API Documentation: https://10.20.30.253:8883/docs
- Health Status: https://10.20.30.253:8883/health
- Metrics: https://10.20.30.253:8883/metrics

## 🔧 Development

### Development Setup

```bash
# Clone for development
git clone https://github.com/the-alphabet-cartel/ash-dash.git
cd ash-dash

# Install dependencies
npm install

# Setup development environment
cp .env.template .env.development

# Start development server
npm run dev
```

### Development Workflow

1. **Create Feature Branch** - `git checkout -b feature/description`
2. **Develop and Test** - Implement changes with comprehensive testing
3. **Integration Testing** - Test with other Ash components
4. **Documentation Updates** - Update relevant documentation
5. **Pull Request** - Submit PR with detailed description
6. **Code Review** - Collaborative review and approval
7. **Deployment** - Merge and deploy via CI/CD pipeline

## 🤝 Contributing

### Contributing Guidelines

1. **Fork Repository** - Create your own fork for development
2. **Feature Branches** - Use descriptive branch names
3. **Code Standards** - Follow established coding conventions
4. **Testing Required** - All changes must include appropriate tests
5. **Documentation** - Update documentation for any new features
6. **Review Process** - All PRs require team review and approval

### Development Standards

- **Code Style** - ESLint and Prettier configurations enforced
- **Testing** - Minimum 80% code coverage required
- **Security** - Security review required for all changes
- **Performance** - Performance impact assessment for UI changes
- **Accessibility** - WCAG 2.1 AA compliance required

## 📞 Support

### Community Support
- **Discord:** https://discord.gg/alphabetcartel - #tech-support channel
- **GitHub Issues:** https://github.com/the-alphabet-cartel/ash-dash/issues
- **Documentation:** Comprehensive guides available in `/docs`

### Technical Support
- **Crisis Response Teams:** Priority support for operational issues
- **Development Support:** GitHub Discussions for development questions
- **Security Issues:** security@alphabetcartel.org

### Support Escalation
1. **Self-Service** - Documentation and troubleshooting guides
2. **Community Support** - Discord #tech-support channel
3. **GitHub Issues** - Bug reports and feature requests
4. **Direct Contact** - For urgent production issues

## 📜 License

This project is part of The Alphabet Cartel ecosystem. See individual component licenses for specific terms.

## 🏷️ Version History

- **v2.1.0** - Submodule integration and dedicated server deployment
- **v2.0.0** - Complete dashboard redesign with advanced analytics
- **v1.5.0** - Team management and role-based access control
- **v1.0.0** - Initial dashboard with basic monitoring capabilities

---

**The Alphabet Cartel** - Building inclusive gaming communities through technology.  
🌈 **Discord:** https://discord.gg/alphabetcartel | 🌐 **Website:** http://alphabetcartel.org