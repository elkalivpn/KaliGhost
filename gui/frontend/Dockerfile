# frontend/Dockerfile
# Multi-stage build for React + Vite frontend
# Supports: linux/amd64, linux/arm64

# ============================================================================
# DEVELOPMENT STAGE - For dev with hot-reload
# ============================================================================
FROM node:20-alpine as development

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies with optimizations
RUN npm install --legacy-peer-deps --no-audit --no-fund 2>&1 | tail -20

# Copy source code
COPY frontend . .

# Expose Vite dev server port
EXPOSE 5173

# Environment for Vite
ENV VITE_BACKEND_URL=http://localhost:8000

# Run Vite dev server with host binding
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# ============================================================================
# BUILDER STAGE - Build the production bundle
# ============================================================================
FROM node:20-alpine as builder

WORKDIR /app

COPY frontend/package*.json ./

RUN npm install --legacy-peer-deps --no-audit --no-fund 2>&1 | tail -20

COPY frontend . .

# Build the React app
RUN npm run build

# ============================================================================
# PRODUCTION STAGE - Serve with Nginx (minimal, no Node)
# ============================================================================
FROM nginx:alpine as production

# Copy Nginx config
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Copy built app from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/health || exit 1

CMD ["nginx", "-g", "daemon off;"]
