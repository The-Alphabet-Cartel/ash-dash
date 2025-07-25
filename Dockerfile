# Dockerfile for Ash Analytics Dashboard
FROM node:18-alpine

# Install runtime dependencies
RUN apk add --no-cache curl dumb-init

# Create non-root user
RUN addgroup -g 1001 -S dashuser && \
    adduser -S dashuser -u 1001

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY dashboard/package*.json ./
RUN npm install --only=production

# Copy application files
COPY dashboard/server.js ./

# Copy entire project structure and let the app handle missing directories
COPY . .

# Ensure public directory exists
RUN mkdir -p ./public

# Create necessary directories and set permissions
RUN mkdir -p logs data cache && \
    chown -R dashuser:dashuser /app

# Switch to non-root user
USER dashuser

# Set environment variables
ENV NODE_ENV=production
ENV PORT=8883
ENV ASH_BOT_API=http://10.20.30.253:8882
ENV ASH_NLP_API=http://10.20.30.16:8881
ENV CACHE_TTL=300
ENV LOG_LEVEL=info
ENV ENABLE_ANALYTICS=true
ENV ANALYTICS_RETENTION_DAYS=90

# Expose port
EXPOSE 8883

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# Start the application
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "server.js"]