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
ENV TZ="America/Los_Angeles"

ENV GLOBAL_DASH_API_PORT="8883"

# SSL Configuration
ENV DASH_ENABLE_SSL="true"
ENV DASH_SSL_CERT_PATH="/app/certs/cert.pem"
ENV DASH_SSL_KEY_PATH="/app/certs/key.pem"

# Ash Bot API (Discord Bot with Crisis Detection)
ENV GLOBAL_BOT_API_URL="http://10.20.30.253:8882"
ENV DASH_BOT_API_TIMEOUT="5000"

# Ash NLP Server API (Machine Learning Analysis)
ENV GLOBAL_NLP_API_URL="http://10.20.30.253:8881"
ENV DASH_NLP_API_TIMEOUT="10000"

# Cache Settings
ENV DASH_CACHE_TTL="300"

# Real-time Updates
ENV DASH_ENABLE_SOCKET_IO="true"
ENV DASH_METRICS_UPDATE_INTERVAL="30000"

# LOGGING & MONITORING
ENV GLOBAL_LOG_LEVEL="info"
ENV DASH_LOG_DIR="./logs"
ENV DASH_LOG_FILE="ash-dash.log"

# DOCKER SECRETS CONFIGURATION
ENV GLOBAL_SESSION_TOKEN="/run/secrets/session_secret"

# Enable Access
ENV DASH_ENABLE_ACCESS_LOGS="true"

# Rate Limits
ENV DASH_RATE_LIMIT_WINDOW="900000"
ENV DASH_RATE_LIMIT_MAX="100"
ENV DASH_RATE_LIMIT_MESSAGE="Too many requests, please try again later"

# Expose port
EXPOSE 8883

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f -k https://localhost:8883/health || curl -f http://localhost:8883/health || exit 1

# Start the application
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "server.js"]