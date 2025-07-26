const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const path = require('path');
const helmet = require('helmet');
const cors = require('cors');
const compression = require('compression');
const rateLimit = require('express-rate-limit');
const morgan = require('morgan');
const cron = require('node-cron');
const axios = require('axios');
const NodeCache = require('node-cache');
const winston = require('winston');
require('winston-daily-rotate-file');

// Initialize Express app
const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

// Configuration
const config = {
  port: process.env.PORT || 8883,
  nodeEnv: process.env.NODE_ENV || 'development',
  ashBotApi: process.env.ASH_BOT_API || 'http://10.20.30.253:8882',
  ashNlpApi: process.env.ASH_NLP_API || 'http://10.20.30.16:8881',
  cacheTtl: parseInt(process.env.CACHE_TTL) || 300,
  logLevel: process.env.LOG_LEVEL || 'info',
  enableAnalytics: process.env.ENABLE_ANALYTICS === 'true',
  analyticsRetentionDays: parseInt(process.env.ANALYTICS_RETENTION_DAYS) || 90
};

// Initialize cache
const cache = new NodeCache({ stdTTL: config.cacheTtl });

// Initialize logger
const logger = winston.createLogger({
  level: config.logLevel,
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { service: 'ash-dash' },
  transports: [
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple()
      )
    }),
    new winston.transports.DailyRotateFile({
      filename: './logs/ash-dash-%DATE%.log',
      datePattern: 'YYYY-MM-DD',
      maxSize: '20m',
      maxFiles: '14d'
    })
  ]
});

// Middleware - Modified to prevent HTTPS enforcement
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com"],
      scriptSrc: ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'", "ws:", "wss:", "http:", "https:"],
      fontSrc: ["'self'", "https://cdnjs.cloudflare.com", "https://cdn.jsdelivr.net"],
      upgradeInsecureRequests: null  // Disable HTTPS upgrade
    }
  },
  hsts: false,  // Disable HSTS
  crossOriginOpenerPolicy: false  // Disable COOP which causes the warning
}));

// Add explicit header to prevent HTTPS upgrade
app.use((req, res, next) => {
  res.removeHeader('Strict-Transport-Security');
  res.setHeader('Content-Security-Policy', 
    "default-src 'self'; " +
    "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; " +
    "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; " +
    "img-src 'self' data: https:; " +
    "connect-src 'self' ws: wss: http: https:; " +
    "font-src 'self' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net"
  );
  next();
});

app.use(cors());
app.use(compression());
app.use(morgan('combined', { stream: { write: message => logger.info(message.trim()) } }));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later.'
});
app.use('/api/', limiter);

app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Serve static files
app.use(express.static(path.join(__dirname, 'public')));

// API Routes
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    protocol: 'http',
    services: {
      dashboard: 'online',
      cache: cache.getStats(),
      uptime: process.uptime()
    }
  });
});

// Enhanced status endpoint with better error handling
app.get('/api/status', async (req, res) => {
  try {
    const [botStatus, nlpStatus] = await Promise.allSettled([
      checkServiceHealth(config.ashBotApi),
      checkServiceHealth(config.ashNlpApi)
    ]);

    res.json({
      timestamp: new Date().toISOString(),
      services: {
        bot: {
          status: botStatus.status === 'fulfilled' ? 'online' : 'offline',
          response_time: botStatus.value?.responseTime || null,
          error: botStatus.reason?.message || null
        },
        nlp: {
          status: nlpStatus.status === 'fulfilled' ? 'online' : 'offline',
          response_time: nlpStatus.value?.responseTime || null,
          error: nlpStatus.reason?.message || null
        }
      }
    });
  } catch (error) {
    logger.error('Error checking service status:', error);
    res.status(500).json({ error: 'Failed to check service status' });
  }
});

// Mock API endpoints that return sample data when services are unavailable
app.get('/api/metrics', async (req, res) => {
  try {
    const response = await axios.get(`${config.ashBotApi}/api/metrics`, { timeout: 5000 });
    res.json(response.data);
  } catch (error) {
    logger.error('Error fetching metrics from bot API:', error.message);
    // Return mock data instead of error
    res.json({
      timestamp: new Date().toISOString(),
      crisis_metrics: {
        high: 0,
        medium: 0,
        low: 0
      },
      total_messages_analyzed: 0,
      status: 'service_unavailable'
    });
  }
});

app.get('/api/learning-stats', async (req, res) => {
  try {
    const response = await axios.get(`${config.ashNlpApi}/learning_statistics`, { timeout: 5000 });
    res.json(response.data);
  } catch (error) {
    logger.error('Error fetching learning stats:', error.message);
    // Return mock data
    res.json({
      status: 'offline',
      false_positive_reports: 0,
      false_negative_reports: 0,
      total_adjustments: 0,
      last_update: null
    });
  }
});

app.get('/api/crisis-trends', async (req, res) => {
  try {
    const timeframe = req.query.timeframe || '24h';
    const response = await axios.get(`${config.ashBotApi}/api/crisis-trends?timeframe=${timeframe}`, { timeout: 5000 });
    res.json(response.data);
  } catch (error) {
    logger.error('Error fetching crisis trends:', error.message);
    // Return mock data
    res.json({
      labels: ['No Data'],
      high: [0],
      medium: [0],
      low: [0],
      timestamp: new Date().toISOString()
    });
  }
});

// Serve main dashboard
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Helper functions
async function checkServiceHealth(serviceUrl) {
  const start = Date.now();
  const response = await axios.get(`${serviceUrl}/health`, {
    timeout: 5000,
    headers: { 'User-Agent': 'ash-dash/1.0.0' }
  });
  const responseTime = Date.now() - start;
  return { status: response.status, responseTime };
}

// Socket.IO for real-time updates
io.on('connection', (socket) => {
  logger.info(`Client connected: ${socket.id}`);

  socket.emit('welcome', {
    message: 'Connected to Ash Analytics Dashboard',
    timestamp: new Date().toISOString()
  });

  socket.on('subscribe_metrics', () => {
    socket.join('metrics');
    logger.info(`Client ${socket.id} subscribed to metrics updates`);
  });

  socket.on('unsubscribe_metrics', () => {
    socket.leave('metrics');
    logger.info(`Client ${socket.id} unsubscribed from metrics updates`);
  });

  socket.on('disconnect', () => {
    logger.info(`Client disconnected: ${socket.id}`);
  });
});

// Error handling
app.use((err, req, res, next) => {
  logger.error('Unhandled error:', err);
  res.status(500).json({
    error: config.nodeEnv === 'production' ? 'Internal server error' : err.message
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Not found' });
});

// Start server
server.listen(config.port, () => {
  logger.info(`Ash Analytics Dashboard (HTTP-only) running on port ${config.port}`);
  logger.info(`Environment: ${config.nodeEnv}`);
  logger.info(`Bot API: ${config.ashBotApi}`);
  logger.info(`NLP API: ${config.ashNlpApi}`);
  logger.info(`Access via: http://localhost:${config.port} or http://10.20.30.16:${config.port}`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  logger.info('SIGTERM received, shutting down gracefully...');
  server.close(() => {
    logger.info('Process terminated');
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  logger.info('SIGINT received, shutting down gracefully...');
  server.close(() => {
    logger.info('Process terminated');
    process.exit(0);
  });
});

module.exports = app;