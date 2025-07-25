# Multi-stage Dockerfile for Ash Analytics Dashboard
# Build stage
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files from dashboard subdirectory
COPY dashboard/package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy dashboard application code
COPY dashboard/ ./

# Copy public files if they exist at root level
COPY public/ ./public/ 2>/dev/null || true

# Build the application
RUN npm run build

# Production stage
FROM node:18-alpine AS production

# Install runtime dependencies
RUN apk add --no-cache \
    curl \
    dumb-init \
    && rm -rf /var/cache/apk/*

# Create non-root user
RUN addgroup -g 1001 -S dashuser && \
    adduser -S dashuser -u 1001

# Set working directory
WORKDIR /app

# Copy built application from builder
COPY --from=builder --chown=dashuser:dashuser /app/dist ./dist 2>/dev/null || true
COPY --from=builder --chown=dashuser:dashuser /app/node_modules ./node_modules
COPY --from=builder --chown=dashuser:dashuser /app/package*.json ./

# Copy server files from dashboard subdirectory
COPY --chown=dashuser:dashuser dashboard/server.js ./
COPY --chown=dashuser:dashuser public ./public

# Create necessary directories
RUN mkdir -p logs data cache && \
    chown -R dashuser:dashuser /app

# Switch to non-root user
USER dashuser

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000
ENV ASH_BOT_API=http://ash:8080
ENV ASH_NLP_API=http://10.20.30.16:8881
ENV CACHE_TTL=300
ENV LOG_LEVEL=info
ENV ENABLE_ANALYTICS=true
ENV ANALYTICS_RETENTION_DAYS=90

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# Start the application
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "server.js"]