# Ash-Dash - Analytics Dashboard

**Part of the Ash Ecosystem** | **Main Repository:** https://github.com/the-alphabet-cartel/ash

This repository contains **only the analytics dashboard component** of the Ash crisis detection system. For the complete ecosystem including Discord bot, NLP server, and testing suite, see the [main Ash repository](https://github.com/the-alphabet-cartel/ash).

**Discord Community:** https://discord.gg/alphabetcartel  
**Website:** http://alphabetcartel.org  
**Organization:** https://github.com/the-alphabet-cartel

## 📊 About Ash-Dash

Ash-Dash is the analytics and monitoring center for The Alphabet Cartel's crisis detection system. It provides real-time insights into bot performance, crisis detection accuracy, community health metrics, and team coordination tools for crisis response management.

### 🏗️ Architecture Position

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Discord Bot   │◄──►│   NLP Server    │◄──►│   Dashboard     │
│   (ash-bot)     │    │   (ash-nlp)     │    │   (THIS REPO)   │
│                 │    │                 │    │                 │
│ 10.20.30.253    │    │ 10.20.30.16     │    │ 10.20.30.16     │
│ Port: 8882      │    │ Port: 8881      │    │ Port: 8883      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                 ▲
                                 │
                       ┌─────────────────┐
                       │  Testing Suite  │
                       │  (ash-thrash)   │
                       │                 │
                       │ 10.20.30.16     │
                       │ Port: 8884      │
                       └─────────────────┘
```

## 🚀 Quick Start

### For Dashboard Development
If you're working on the dashboard specifically:

```bash
# Clone this repository
git clone https://github.com/the-alphabet-cartel/ash-dash.git
cd ash-dash

# Setup development environment
npm install

# Configure environment
cp .env.template .env
# Edit .env with API endpoints and configuration

# Run development server
npm run dev
```

### For Complete Ecosystem
If you need the full Ash system (recommended):

```bash
# Clone the main ecosystem repository
git clone --recursive https://github.com/the-alphabet-cartel/ash.git
cd ash

# Follow setup instructions in main repository
# This includes ash-dash as a submodule along with all other components
```

## 🔧 Core Features

### Real-Time Monitoring
- **System Health Dashboard**: Live status of all Ash ecosystem components
- **Crisis Alert Management**: Real-time crisis detection alerts and response coordination
- **Performance Metrics**: Bot response times, NLP accuracy, and system throughput
- **Resource Monitoring**: Server CPU, memory, and GPU utilization tracking

### Analytics & Insights
- **Detection Accuracy Tracking**: Historical crisis detection performance metrics
- **Community Health Metrics**: Trends in community well-being and support needs
- **Response Team Coordination**: Crisis response workflow management and team assignments
- **Historical Data Analysis**: Long-term trends and pattern identification

### Team Management
- **Crisis Response Workflow**: Streamlined tools for crisis intervention coordination
- **Team Member Dashboard**: Individual team member performance and availability
- **Alert Routing**: Intelligent alert distribution based on team member expertise
- **Training Integration**: Continuous improvement through testing suite integration

## 📦 Repository Structure

```
ash-dash/                         # THIS REPOSITORY
├── backend/                      # Node.js API server
│   ├── src/                      # Server source code
│   │   ├── app.js               # Express.js application setup
│   │   ├── routes/              # API route definitions
│   │   ├── middleware/          # Express middleware
│   │   ├── services/            # Business logic services
│   │   └── utils/               # Utility functions
│   ├── config/                   # Server configuration
│   └── tests/                    # Backend unit tests
├── frontend/                     # Vue.js dashboard interface
│   ├── src/                      # Frontend source code
│   │   ├── components/          # Vue components
│   │   ├── views/               # Dashboard pages
│   │   ├── store/               # Vuex state management
│   │   ├── router/              # Vue Router configuration
│   │   └── assets/              # Static assets
│   ├── public/                   # Public static files
│   └── tests/                    # Frontend unit tests
├── shared/                       # Shared utilities and types
├── docs/                         # Dashboard-specific documentation
├── docker/                       # Docker configuration
├── scripts/                      # Build and deployment scripts
├── .env.template                 # Environment configuration template
├── docker-compose.yml            # Docker deployment configuration
├── package.json                  # Node.js dependencies
└── README.md                     # This file
```

## 🛠️ Development

### Prerequisites
- Node.js 18+ and npm
- Access to Ash ecosystem APIs (bot, NLP, testing)
- Docker (for containerized deployment)
- Modern web browser with ES6+ support

### Environment Configuration

Create `.env` file from template:
```bash
cp .env.template .env
```

Required environment variables:
```bash
# Dashboard Configuration
API_PORT=8883
API_HOST=0.0.0.0
NODE_ENV=development

# Ash Ecosystem Integration
BOT_API_URL=http://10.20.30.253:8882
NLP_API_URL=http://10.20.30.16:8881
THRASH_API_URL=http://10.20.30.16:8884

# Database Configuration (Optional)
DATABASE_URL=postgresql://user:pass@localhost:5432/ash_dash
REDIS_URL=redis://localhost:6379

# Authentication
JWT_SECRET=your-secure-jwt-secret
SESSION_SECRET=your-secure-session-secret

# Dashboard Features
ENABLE_REAL_TIME_UPDATES=true
ALERT_REFRESH_INTERVAL=5000
METRICS_RETENTION_DAYS=90
```

### Development Setup

**Backend Development:**
```bash
cd backend
npm install
npm run dev
```

**Frontend Development:**
```bash
cd frontend
npm install
npm run serve
```

**Full Stack Development:**
```bash
# Run both backend and frontend
npm run dev:full
```

### Testing

```bash
# Run all tests
npm test

# Backend tests only
npm run test:backend

# Frontend tests only
npm run test:frontend

# E2E tests
npm run test:e2e
```

### Docker Deployment

```bash
# Build and run locally
docker-compose up --build

# Production deployment
docker-compose -f docker-compose.prod.yml up -d
```

## 🔗 Integration with Ash Ecosystem

### Data Sources Integration
- **Bot Metrics**: Real-time statistics from ash-bot API
- **NLP Performance**: Analysis accuracy and processing times from ash-nlp
- **Test Results**: Continuous validation data from ash-thrash
- **System Health**: Combined health monitoring across all services

### API Endpoints
```javascript
// Dashboard API endpoints
GET  /api/dashboard/overview          // System overview
GET  /api/alerts/active              // Current crisis alerts
GET  /api/metrics/performance        // Performance statistics
GET  /api/team/status                // Team member availability
POST /api/alerts/respond             // Crisis response actions
GET  /api/testing/results            // Latest test results
```

### Real-Time Features
- **WebSocket Connection**: Live updates for crisis alerts and system status
- **Server-Sent Events**: Streaming metrics and performance data
- **Auto-Refresh**: Configurable refresh intervals for different data types
- **Push Notifications**: Browser notifications for critical alerts

## 📊 Dashboard Features

### Main Dashboard Views

**System Overview:**
- Real-time status of all Ash ecosystem components
- Current crisis alert summary
- System performance metrics
- Quick action buttons for common tasks

**Crisis Management:**
- Active crisis alert queue with priority sorting
- Crisis response workflow tracking
- Team member assignment and coordination
- Historical crisis response analytics

**Performance Analytics:**
- Detection accuracy trends over time
- Response time metrics and optimization insights
- Resource utilization monitoring
- Comparative analysis of detection methods

**Testing Integration:**
- Live test suite results from ash-thrash
- Goal achievement tracking and progress visualization
- Detailed failure analysis with corrective action suggestions
- One-click test execution and result review

### User Interface

**Responsive Design:**
- Mobile-first responsive layout
- Dark/light theme support
- Accessibility compliance (WCAG 2.1)
- Touch-friendly interface for tablet use

**Data Visualization:**
- Real-time charts and graphs using Chart.js
- Interactive data exploration
- Customizable dashboard layouts
- Export functionality for reports

## 🧪 Testing

This repository includes comprehensive testing for dashboard functionality. Integration testing with the complete Ash ecosystem is coordinated through the main repository.

```bash
# Dashboard-specific testing
npm run test:unit

# Integration testing with APIs
npm run test:integration

# UI/UX testing
npm run test:e2e

# Performance testing
npm run test:performance
```

## 📈 Performance & Monitoring

### Performance Specifications
- **Server**: Windows 11 (10.20.30.16)
- **Resources**: 2GB RAM, 1 CPU core
- **Response Time**: <200ms for dashboard views
- **Concurrent Users**: 50+ simultaneous users
- **Data Refresh**: Real-time updates with 5-second intervals

### Monitoring
- **Health Endpoint**: `http://10.20.30.16:8883/health`
- **Performance Metrics**: Built-in dashboard performance tracking
- **Error Monitoring**: Comprehensive error logging and alerting
- **User Analytics**: Dashboard usage statistics and optimization insights

## 🔐 Security & Access Control

### Authentication
- **JWT-based Authentication**: Secure token-based user sessions
- **Role-Based Access Control**: Different permission levels for team members
- **Session Management**: Configurable session timeouts and security policies
- **API Security**: Rate limiting and request validation

### Data Protection
- **Encrypted Communication**: HTTPS/TLS for all data transmission
- **Data Minimization**: Only displays necessary information for crisis response
- **Privacy Compliance**: Adheres to privacy-first principles of Ash ecosystem
- **Audit Logging**: Comprehensive logs of all user actions and system changes

## 🤝 Contributing

### Development Process
1. **Fork this repository** (ash-dash specifically)
2. **Create feature branch** for your changes
3. **Write comprehensive tests** for new features
4. **Test integration** with Ash ecosystem APIs
5. **Validate responsive design** across devices
6. **Update documentation** as needed
7. **Submit pull request** to this repository

### UI/UX Development
- **Design System**: Follow established component library and design patterns
- **Accessibility**: Ensure WCAG 2.1 compliance for all new features
- **Performance**: Optimize for fast loading and smooth interactions
- **Mobile Support**: Test thoroughly on mobile and tablet devices

### Main Ecosystem
For changes affecting multiple components, coordinate with the [main ash repository](https://github.com/the-alphabet-cartel/ash) which includes this repository as a submodule.

## 📞 Support

### Dashboard-Specific Issues
- **GitHub Issues**: [ash-dash/issues](https://github.com/the-alphabet-cartel/ash-dash/issues)
- **Discord Support**: #ash-dash-support in https://discord.gg/alphabetcartel

### Ecosystem-Wide Issues
- **Main Repository**: [ash/issues](https://github.com/the-alphabet-cartel/ash/issues)
- **General Discussion**: #tech-help in https://discord.gg/alphabetcartel

### User Experience Issues
- **UI/UX Problems**: Include screenshots and browser information
- **Performance Issues**: Include network timing and system specifications
- **Access Issues**: Include user role and permission details

## 📜 License

This project is part of The Alphabet Cartel's open-source initiatives. See [LICENSE](LICENSE) file for details.

---

## ⚠️ Important Notes

### Repository Scope
This repository contains **ONLY the analytics dashboard component**. For:
- **Discord Bot**: See [ash-bot](https://github.com/the-alphabet-cartel/ash-bot)
- **NLP Server**: See [ash-nlp](https://github.com/the-alphabet-cartel/ash-nlp)
- **Testing Suite**: See [ash-thrash](https://github.com/the-alphabet-cartel/ash-thrash)
- **Complete System**: See [main ash repository](https://github.com/the-alphabet-cartel/ash)

### Development Recommendations
- **New Contributors**: Start with the [main ash repository](https://github.com/the-alphabet-cartel/ash) for complete system overview
- **Dashboard-Specific Work**: Use this repository for UI/UX and analytics development
- **System Integration**: Test changes against the full ecosystem APIs

### Data Dependencies
The dashboard requires active connections to ash-bot, ash-nlp, and ash-thrash APIs for full functionality. It can operate in limited mode if some services are unavailable.

### Crisis Response Tool
This dashboard is designed for crisis response team members and contains sensitive information related to community member welfare. Access should be restricted to authorized team members only.

---

**Built with 🖤 for LGBTQIA+ gaming communities by [The Alphabet Cartel](https://discord.gg/alphabetcartel)**