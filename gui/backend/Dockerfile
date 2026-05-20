# backend/Dockerfile
# Multi-architecture Python FastAPI backend
# Supports: linux/amd64, linux/arm64
# Build context: project root (not ./backend)

# ============================================================================
# BASE STAGE - Common dependencies
# ============================================================================
FROM python:3.11-slim as base

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies (minimal for security)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements_backend.txt .
RUN pip install --no-cache-dir -r requirements_backend.txt

# Copy application code
COPY websocket_backend.py .

# ============================================================================
# DEVELOPMENT STAGE - Used in docker-compose for dev with hot-reload
# ============================================================================
FROM base as development

# Keep all dependencies, install dev tools
RUN pip install --no-cache-dir \
    watchfiles \
    pytest \
    pytest-asyncio

EXPOSE 8000

# Uvicorn with --reload for development
CMD ["uvicorn", "websocket_backend:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ============================================================================
# PRODUCTION STAGE - Optimized for production
# ============================================================================
FROM base as production

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Change ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "websocket_backend:app", "--host", "0.0.0.0", "--port", "8000"]
