# Dockerfile for Ash Analytics Dashboard
FROM node:18-alpine

# Install runtime dependencies
RUN apk add --no-cache curl dumb-init openssl

# Create non-root user
RUN addgroup -g 1001 -S dashuser && \
    adduser -S dashuser -u 1001

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY dashboard/package*.json ./
RUN npm install --only=production && npm cache clean --force

# Copy application files
COPY dashboard/server.js ./
COPY public/ ./public/

# Create necessary directories and set permissions
RUN mkdir -p logs data cache certs && \
    chown -R dashuser:dashuser /app

# Generate self-signed SSL certificate for development
RUN openssl req -x509 -newkey rsa:2048 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes \
    -subj '/C=US/ST=WA/L=Lacey/O=The Alphabet Cartel/CN=10.20.30.253' && \
    chown dashuser:dashuser certs/*.pem

# Switch to non-root user
USER dashuser

# Set environment variables
ENV NODE_ENV="production"
ENV PORT="8883"
ENV DASH_PORT="8883"

# SSL Configuration
ENV ENABLE_SSL="true"

# Ash Bot API (Discord Bot with Crisis Detection)
ENV ASH_BOT_API="http://10.20.30.253:8882"
ENV ASH_BOT_API_TIMEOUT="5000"

# Ash NLP Server API (Machine Learning Analysis)
ENV ASH_NLP_API="http://10.20.30.253:8881"
ENV ASH_NLP_API_TIMEOUT="10000"

# Cache Settings
ENV CACHE_TTL="300"
ENV ENABLE_ANALYTICS="true"
ENV ANALYTICS_RETENTION_DAYS="90"

# Real-time Updates
ENV ENABLE_SOCKET_IO="true"
ENV METRICS_UPDATE_INTERVAL="30000"

# LOGGING & MONITORING
ENV LOG_LEVEL="info"

# DOCKER SECRETS CONFIGURATION
ENV SSL_CERT_PATH="/app/certs/cert.pem"
ENV SSL_KEY_PATH="/app/certs/key.pem"
ENV SESSION_SECRET="/run/secrets/session_secret"

# Expose port
EXPOSE 8883

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f -k https://localhost:8883/health || curl -f http://localhost:8883/health || exit 1

# Start the application
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "server.js"]