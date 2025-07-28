const express = require('express');
const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');
const cors = require('cors');
const helmet = require('helmet');
const compression = require('compression');
const rateLimit = require('express-rate-limit');
const morgan = require('morgan');
const axios = require('axios');
const winston = require('winston');
const NodeCache = require('node-cache');
const { createServer } = require('http');
const { Server } = require('socket.io');

// Add console logging for Docker visibility
console.log('🚀 Starting Ash Dashboard...');

// Function to get the host IP address
function getHostIP() {
  const networkInterfaces = os.networkInterfaces();
  
  // Try to find the primary network interface (usually the one with a gateway)
  for (const interfaceName of Object.keys(networkInterfaces)) {
    const addresses = networkInterfaces[interfaceName];
    
    for (const address of addresses) {
      // Skip loopback and non-IPv4 addresses
      if (!address.internal && address.family === 'IPv4') {
        // Prefer addresses in common private network ranges
        if (address.address.startsWith('192.168.') || 
            address.address.startsWith('10.') || 
            address.address.startsWith('172.')) {
          return address.address;
        }
      }
    }
  }
  
  // Fallback: return the first non-internal IPv4 address
  for (const interfaceName of Object.keys(networkInterfaces)) {
    const addresses = networkInterfaces[interfaceName];
    
    for (const address of addresses) {
      if (!address.internal && address.family === 'IPv4') {
        return address.address;
      }
    }
  }
  
  // Final fallback
  return 'localhost';
}

const hostIP = getHostIP();
console.log(`🌐 Detected host IP: ${hostIP}`);

// Configuration
const config = {
  port: process.env.PORT || 8883,
  enableSSL: process.env.ENABLE_SSL === 'true',
  sslCertPath: process.env.SSL_CERT_PATH || './certs/cert.pem',
  sslKeyPath: process.env.SSL_KEY_PATH || './certs/key.pem',
  ashBotAPI: process.env.ASH_BOT_API || 'http://10.20.30.253:8882',
  ashNLPAPI: process.env.ASH_NLP_API || 'http://10.20.30.16:8881',
  cacheTimeout: parseInt(process.env.CACHE_TTL) || 300,
  metricsUpdateInterval: parseInt(process.env.METRICS_UPDATE_INTERVAL) || 30000,
  enableSocketIO: process.env.ENABLE_SOCKET_IO !== 'false',
  logLevel: process.env.LOG_LEVEL || 'info',
};

console.log('⚙️ Configuration loaded');
console.log(`📡 Port: ${config.port}`);
console.log(`🤖 Bot API: ${config.ashBotAPI}`);
console.log(`🧠 NLP API: ${config.ashNLPAPI}`);
console.log(`🔒 SSL: ${config.enableSSL ? 'Enabled' : 'Disabled'}`);

// Initialize Express app
const app = express();

// Initialize cache
const cache = new NodeCache({ stdTTL: config.cacheTimeout });

// Logger setup
const logger = winston.createLogger({
  level: config.logLevel,
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple()
      )
    }),
    new winston.transports.File({ 
      filename: process.env.LOG_FILE || 'ash-dash.log',
      maxsize: 10485760, // 10MB
      maxFiles: 5
    })
  ]
});

// Middleware setup
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'", "cdnjs.cloudflare.com"],
      styleSrc: ["'self'", "'unsafe-inline'", "fonts.googleapis.com"],
      fontSrc: ["'self'", "fonts.gstatic.com"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'", "ws:", "wss:"]
    }
  }
}));

app.use(compression());
app.use(cors({
  origin: process.env.CORS_ORIGINS?.split(',') || '*',
  credentials: true
}));

// Rate limiting
const limiter = rateLimit({
  windowMs: parseInt(process.env.RATE_LIMIT_WINDOW) || 900000, // 15 minutes
  max: parseInt(process.env.RATE_LIMIT_MAX) || 100,
  message: {
    error: process.env.RATE_LIMIT_MESSAGE || 'Too many requests, please try again later'
  }
});
app.use('/api/', limiter);

// Request logging
if (process.env.ENABLE_ACCESS_LOGS !== 'false') {
  app.use(morgan('combined', {
    stream: { write: (message) => logger.info(message.trim()) }
  }));
}

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

console.log('🔧 Middleware configured');

// API client setup with timeouts and retries
const createAPIClient = (baseURL, timeout = 5000) => {
  return axios.create({
    baseURL,
    timeout,
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'Ash-Dashboard/1.0'
    }
  });
};

const botAPI = createAPIClient(config.ashBotAPI, parseInt(process.env.ASH_BOT_API_TIMEOUT) || 5000);
const nlpAPI = createAPIClient(config.ashNLPAPI, parseInt(process.env.ASH_NLP_API_TIMEOUT) || 10000);

// Service health checker
async function checkServiceHealth(api, serviceName) {
  try {
    const start = Date.now();
    const response = await api.get('/health');
    const responseTime = Date.now() - start;
    
    return {
      status: 'healthy',
      responseTime,
      data: response.data,
      lastCheck: new Date().toISOString()
    };
  } catch (error) {
    logger.warn(`${serviceName} health check failed:`, error.message);
    return {
      status: 'unhealthy',
      error: error.message,
      lastCheck: new Date().toISOString()
    };
  }
}

// API Routes

// Dashboard health endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'ash-dashboard',
    version: '1.0.0',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// Combined service status
app.get('/api/status', async (req, res) => {
  try {
    const cacheKey = 'service_status';
    let cachedStatus = cache.get(cacheKey);
    
    if (!cachedStatus) {
      logger.info('Fetching fresh service status...');
      
      const [botHealth, nlpHealth] = await Promise.allSettled([
        checkServiceHealth(botAPI, 'Ash Bot'),
        checkServiceHealth(nlpAPI, 'NLP Server')
      ]);
      
      cachedStatus = {
        ashBot: botHealth.status === 'fulfilled' ? botHealth.value : {
          status: 'unhealthy',
          error: botHealth.reason?.message || 'Unknown error',
          lastCheck: new Date().toISOString()
        },
        nlpServer: nlpHealth.status === 'fulfilled' ? nlpHealth.value : {
          status: 'unhealthy', 
          error: nlpHealth.reason?.message || 'Unknown error',
          lastCheck: new Date().toISOString()
        },
        dashboard: {
          status: 'healthy',
          uptime: process.uptime(),
          memoryUsage: process.memoryUsage(),
          lastCheck: new Date().toISOString()
        }
      };
      
              cache.set(cacheKey, cachedStatus, 60); // Cache for 60 seconds
    }
    
    res.json(cachedStatus);
  } catch (error) {
    logger.error('Error fetching service status:', error);
    res.status(500).json({ error: 'Failed to fetch service status' });
  }
});

// Crisis detection metrics
app.get('/api/metrics', async (req, res) => {
  try {
    const cacheKey = 'crisis_metrics';
    let metrics = cache.get(cacheKey);
    
    if (!metrics) {
      logger.info('Fetching fresh crisis metrics...');
      
      try {
        const response = await botAPI.get('/api/metrics');
        metrics = response.data;
        cache.set(cacheKey, metrics, 120); // Cache for 2 minutes
      } catch (error) {
        logger.warn('Bot API unavailable, using fallback metrics');
        metrics = {
          highCrisis: 0,
          mediumCrisis: 0,
          lowCrisis: 0,
          totalMessages: 0,
          lastUpdated: new Date().toISOString(),
          source: 'fallback'
        };
      }
    }
    
    res.json(metrics);
  } catch (error) {
    logger.error('Error fetching metrics:', error);
    res.status(500).json({ error: 'Failed to fetch metrics' });
  }
});

// Crisis trends over time
app.get('/api/crisis-trends', async (req, res) => {
  try {
    const hours = parseInt(req.query.hours) || 24;
    const cacheKey = `crisis_trends_${hours}h`;
    let trends = cache.get(cacheKey);
    
    if (!trends) {
      logger.info(`Fetching ${hours}h crisis trends...`);
      
      try {
        const response = await botAPI.get(`/api/crisis-trends?hours=${hours}`);
        trends = response.data;
        cache.set(cacheKey, trends, 600); // Cache for 10 minutes
      } catch (error) {
        logger.warn('Bot API unavailable, generating mock trend data');
        trends = generateMockTrendData(hours);
      }
    }
    
    res.json(trends);
  } catch (error) {
    logger.error('Error fetching crisis trends:', error);
    res.status(500).json({ error: 'Failed to fetch crisis trends' });
  }
});

// NLP Server learning statistics
app.get('/api/learning-stats', async (req, res) => {
  try {
    const cacheKey = 'learning_stats';
    let stats = cache.get(cacheKey);
    
    if (!stats) {
      logger.info('Fetching learning statistics...');
      
      try {
        const response = await nlpAPI.get('/learning_statistics');
        stats = response.data;
        cache.set(cacheKey, stats, 180); // Cache for 3 minutes
      } catch (error) {
        logger.warn('NLP API unavailable, using fallback learning stats');
        stats = {
          falsePositives: { total: 0, today: 0, thisWeek: 0 },
          falseNegatives: { total: 0, today: 0, thisWeek: 0 },
          learningEffectiveness: 0,
          lastLearningEvent: null,
          totalAdjustments: 0,
          source: 'fallback'
        };
      }
    }
    
    res.json(stats);
  } catch (error) {
    logger.error('Error fetching learning stats:', error);
    res.status(500).json({ error: 'Failed to fetch learning statistics' });
  }
});

// NLP Server metrics
app.get('/api/nlp-metrics', async (req, res) => {
  try {
    const cacheKey = 'nlp_metrics';
    let metrics = cache.get(cacheKey);
    
    if (!metrics) {
      logger.info('Fetching NLP metrics...');
      
      try {
        const response = await nlpAPI.get('/metrics');
        metrics = response.data;
        cache.set(cacheKey, metrics, 120); // Cache for 2 minutes
      } catch (error) {
        logger.warn('NLP API unavailable, using fallback metrics');
        metrics = {
          totalAnalyses: 0,
          averageConfidence: 0,
          processingTime: 0,
          modelStatus: 'unknown',
          source: 'fallback'
        };
      }
    }
    
    res.json(metrics);
  } catch (error) {
    logger.error('Error fetching NLP metrics:', error);
    res.status(500).json({ error: 'Failed to fetch NLP metrics' });
  }
});

// Utility function to generate mock trend data when services are unavailable
function generateMockTrendData(hours) {
  const data = [];
  const now = new Date();
  
  for (let i = hours - 1; i >= 0; i--) {
    const timestamp = new Date(now - i * 60 * 60 * 1000);
    data.push({
      timestamp: timestamp.toISOString(),
      high: Math.floor(Math.random() * 3),
      medium: Math.floor(Math.random() * 8),
      low: Math.floor(Math.random() * 15),
      total: Math.floor(Math.random() * 50) + 20
    });
  }
  
  return { data, source: 'mock' };
}

// Serve dashboard HTML
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

console.log('🛣️ Routes configured');

// Error handling middleware
app.use((error, req, res, next) => {
  logger.error('Unhandled error:', error);
  res.status(500).json({ 
    error: 'Internal server error',
    timestamp: new Date().toISOString()
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ 
    error: 'Not found',
    path: req.path,
    timestamp: new Date().toISOString()
  });
});

// SSL Certificate generation function
function generateSelfSignedCert() {
  const { execSync } = require('child_process');
  const certDir = path.dirname(config.sslCertPath);
  
  try {
    // Create certs directory if it doesn't exist
    if (!fs.existsSync(certDir)) {
      fs.mkdirSync(certDir, { recursive: true });
      console.log(`📁 Created certificates directory: ${certDir}`);
    }
    
    // Generate self-signed certificate
    const cmd = `openssl req -x509 -newkey rsa:2048 -keyout "${config.sslKeyPath}" -out "${config.sslCertPath}" -days 365 -nodes -subj "/C=US/ST=WA/L=Lacey/O=The Alphabet Cartel/CN=${hostIP}"`;
    execSync(cmd, { stdio: 'pipe' });
    
    console.log(`🔐 Generated self-signed SSL certificate`);
    return true;
  } catch (error) {
    console.log('Failed to generate SSL certificate:', error.message);
    return false;
  }
}

// Server initialization
console.log('🚀 Initializing server...');

let server;

if (config.enableSSL) {
  // HTTPS server with SSL
  try {
    // Check if SSL files exist, if not, try to generate them
    if (!fs.existsSync(config.sslCertPath) || !fs.existsSync(config.sslKeyPath)) {
      console.log('🔍 SSL certificates not found, generating...');
      
      if (!generateSelfSignedCert()) {
        throw new Error('Could not generate SSL certificates');
      }
    }
    
    const sslOptions = {
      key: fs.readFileSync(config.sslKeyPath),
      cert: fs.readFileSync(config.sslCertPath)
    };
    
    server = https.createServer(sslOptions, app);
    console.log(`🔒 HTTPS server created`);
  } catch (error) {
    console.log(`⚠️ SSL setup failed, falling back to HTTP: ${error.message}`);
    server = http.createServer(app);
  }
} else {
  // HTTP server
  server = http.createServer(app);
  console.log('🔓 HTTP server created');
}

// Socket.IO setup for real-time updates
let io;
if (config.enableSocketIO) {
  console.log('🔌 Setting up Socket.IO...');
  io = new Server(server, {
    cors: {
      origin: process.env.CORS_ORIGINS?.split(',') || '*',
      methods: ['GET', 'POST']
    }
  });
  
  io.on('connection', (socket) => {
    logger.info(`Client connected: ${socket.id}`);
    
    socket.on('disconnect', () => {
      logger.info(`Client disconnected: ${socket.id}`);
    });
  });
  
  // Broadcast metrics updates
  setInterval(async () => {
    try {
      const [status, metrics, learningStats] = await Promise.allSettled([
        checkServiceHealth(botAPI, 'Ash Bot'),
        botAPI.get('/api/metrics').catch(() => null),
        nlpAPI.get('/learning_statistics').catch(() => null)
      ]);
      
      io.emit('metrics_update', {
        timestamp: new Date().toISOString(),
        status: status.status === 'fulfilled' ? status.value : null,
        metrics: metrics.status === 'fulfilled' ? metrics.value?.data : null,
        learningStats: learningStats.status === 'fulfilled' ? learningStats.value?.data : null
      });
    } catch (error) {
      logger.error('Error broadcasting metrics:', error);
    }
  }, config.metricsUpdateInterval);
  
  console.log('✅ Socket.IO configured');
}

// Start server
server.listen(config.port, '0.0.0.0', () => {
  const protocol = config.enableSSL ? 'https' : 'http';
  
  console.log('');
  console.log('=================================');
  console.log('✅ ASH DASHBOARD READY!');
  console.log('=================================');
  console.log(`🌐 ${protocol}://${hostIP}:${config.port}`);
  console.log(`💓 Health: ${protocol}://${hostIP}:${config.port}/health`);
  console.log(`📊 Status: ${protocol}://${hostIP}:${config.port}/api/status`);
  console.log('=================================');
  
  // Also use winston logger for file logging
  logger.info(`🚀 Ash Analytics Dashboard running on ${protocol}://0.0.0.0:${config.port}`);
  logger.info(`📊 Monitoring Ash Bot: ${config.ashBotAPI}`);
  logger.info(`🤖 Monitoring NLP Server: ${config.ashNLPAPI}`);
  logger.info(`⚡ Real-time updates: ${config.enableSocketIO ? 'enabled' : 'disabled'}`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('🛑 SIGTERM received, shutting down...');
  logger.info('SIGTERM received, shutting down gracefully...');
  server.close(() => {
    console.log('👋 Server stopped');
    logger.info('Server closed');
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  console.log('🛑 SIGINT received, shutting down...');
  logger.info('SIGINT received, shutting down gracefully...');
  server.close(() => {
    console.log('👋 Server stopped');
    logger.info('Server closed');
    process.exit(0);
  });
});