# Multi-stage Dockerfile for Ash Analytics Dashboard
# Build stage
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files from dashboard subdirectory
COPY dashboard/package*.json ./

# Install dependencies (use npm install since package-lock.json might not exist)
RUN npm install --only=production

# Copy dashboard application code
COPY dashboard/ ./

# Copy public files if they exist at root level
COPY public/ ./public/ 2>/dev/null || true

# Try to build if build script exists, otherwise skip
RUN npm run build 2>/dev/null || echo "No build script found, skipping build step"

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

# Copy built application from builder (if dist exists)
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