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
  port: process.env.PORT || 3000,
  nodeEnv: process.env.NODE_ENV || 'development',
  ashBotApi: process.env.ASH_BOT_API || 'http://ash:8080',
  ashNlpApi: process.env.ASH_NLP_API || 'http://10.20.30.16:8881',
  cacheTtl: parseInt(process.env.CACHE_TTL) || 300, // 5 minutes
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

// Middleware
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net"],
      scriptSrc: ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'", "ws:", "wss:"]
    }
  }
}));

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

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    services: {
      dashboard: 'online',
      cache: cache.getStats(),
      uptime: process.uptime()
    }
  });
});

// Dashboard metrics endpoint
app.get('/api/metrics', async (req, res) => {
  try {
    const cacheKey = 'dashboard_metrics';
    let metrics = cache.get(cacheKey);

    if (!metrics) {
      // Fetch data from both services
      const [botMetrics, nlpMetrics] = await Promise.allSettled([
        fetchBotMetrics(),
        fetchNlpMetrics()
      ]);

      metrics = {
        timestamp: new Date().toISOString(),
        bot: botMetrics.status === 'fulfilled' ? botMetrics.value : { error: botMetrics.reason?.message },
        nlp: nlpMetrics.status === 'fulfilled' ? nlpMetrics.value : { error: nlpMetrics.reason?.message }
      };

      // Cache for 5 minutes
      cache.set(cacheKey, metrics, config.cacheTtl);
    }

    res.json(metrics);
  } catch (error) {
    logger.error('Error fetching metrics:', error);
    res.status(500).json({ error: 'Failed to fetch metrics' });
  }
});

// Learning statistics endpoint
app.get('/api/learning-stats', async (req, res) => {
  try {
    const cacheKey = 'learning_stats';
    let stats = cache.get(cacheKey);

    if (!stats) {
      stats = await fetchLearningStats();
      cache.set(cacheKey, stats, config.cacheTtl);
    }

    res.json(stats);
  } catch (error) {
    logger.error('Error fetching learning stats:', error);
    res.status(500).json({ error: 'Failed to fetch learning statistics' });
  }
});

// Crisis detection trends
app.get('/api/crisis-trends', async (req, res) => {
  try {
    const { timeframe = '24h' } = req.query;
    const cacheKey = `crisis_trends_${timeframe}`;
    let trends = cache.get(cacheKey);

    if (!trends) {
      trends = await fetchCrisisTrends(timeframe);
      cache.set(cacheKey, trends, config.cacheTtl);
    }

    res.json(trends);
  } catch (error) {
    logger.error('Error fetching crisis trends:', error);
    res.status(500).json({ error: 'Failed to fetch crisis trends' });
  }
});

// Keyword performance
app.get('/api/keyword-performance', async (req, res) => {
  try {
    const cacheKey = 'keyword_performance';
    let performance = cache.get(cacheKey);

    if (!performance) {
      performance = await fetchKeywordPerformance();
      cache.set(cacheKey, performance, config.cacheTtl);
    }

    res.json(performance);
  } catch (error) {
    logger.error('Error fetching keyword performance:', error);
    res.status(500).json({ error: 'Failed to fetch keyword performance' });
  }
});

// Server status endpoint
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

// Serve main dashboard
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Helper functions
async function fetchBotMetrics() {
  const response = await axios.get(`${config.ashBotApi}/api/metrics`, {
    timeout: 5000,
    headers: { 'User-Agent': 'ash-dash/1.0.0' }
  });
  return response.data;
}

async function fetchNlpMetrics() {
  const response = await axios.get(`${config.ashNlpApi}/metrics`, {
    timeout: 5000,
    headers: { 'User-Agent': 'ash-dash/1.0.0' }
  });
  return response.data;
}

async function fetchLearningStats() {
  const response = await axios.get(`${config.ashNlpApi}/learning_statistics`, {
    timeout: 5000,
    headers: { 'User-Agent': 'ash-dash/1.0.0' }
  });
  return response.data;
}

async function fetchCrisisTrends(timeframe) {
  const response = await axios.get(`${config.ashBotApi}/api/crisis-trends?timeframe=${timeframe}`, {
    timeout: 5000,
    headers: { 'User-Agent': 'ash-dash/1.0.0' }
  });
  return response.data;
}

async function fetchKeywordPerformance() {
  const response = await axios.get(`${config.ashBotApi}/api/keyword-performance`, {
    timeout: 5000,
    headers: { 'User-Agent': 'ash-dash/1.0.0' }
  });
  return response.data;
}

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

// Scheduled tasks
if (config.enableAnalytics) {
  // Update metrics every 5 minutes
  cron.schedule('*/5 * * * *', async () => {
    try {
      logger.info('Updating metrics cache...');
      cache.del('dashboard_metrics');
      cache.del('learning_stats');
      
      const metrics = await Promise.allSettled([
        fetchBotMetrics(),
        fetchNlpMetrics(),
        fetchLearningStats()
      ]);

      // Broadcast to connected clients
      io.to('metrics').emit('metrics_update', {
        timestamp: new Date().toISOString(),
        metrics: metrics
      });

      logger.info('Metrics cache updated and broadcasted');
    } catch (error) {
      logger.error('Error updating metrics cache:', error);
    }
  });

  // Clean up old cache entries every hour
  cron.schedule('0 * * * *', () => {
    cache.flushAll();
    logger.info('Cache cleared');
  });
}

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
  logger.info(`Ash Analytics Dashboard running on port ${config.port}`);
  logger.info(`Environment: ${config.nodeEnv}`);
  logger.info(`Bot API: ${config.ashBotApi}`);
  logger.info(`NLP API: ${config.ashNlpApi}`);
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