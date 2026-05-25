#!/bin/bash
# 🐉 KaliGhost 3.0 - Complete Deployment Fix Script
# This script addresses known issues preventing deployment

set -e

echo "🔧 Fixing KaliGhost deployment issues..."

# 1. Remove deprecated version field in docker-compose.yml
echo "1. Fixing docker-compose.yml..."
sed -i '' '/version: '\''3.9'\''/d' docker-compose.yml

# 2. Check that all required directories exist
echo "2. Setting up required directories..."
mkdir -p backend config data skills gui examples scripts docker

# 3. Create required config files if missing
echo "3. Creating essential configuration files..."

# Create a basic config file if missing
if [ ! -f config/kalighost_config.yaml ]; then
    cat > config/kalighost_config.yaml << EOF
---
# KaliGhost Configuration
# This file contains default settings for the system
services:
  gateway:
    port: 8000
    host: 0.0.0.0
  webchat:
    port: 8001
    host: 0.0.0.0
  postgres:
    port: 5432
    host: postgres
  redis:
    port: 6379
    host: redis
  monitoring:
    prometheus_port: 9090
    grafana_port: 3001
EOF
fi

# 4. Validate Docker setup
echo "4. Verifying Docker setup..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found - please install Docker Desktop"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found - please install Docker Compose"
    exit 1
fi

echo "✅ Docker setup verified"

# 5. Fix permissions on start script
echo "5. Setting up executable permissions..."
chmod +x start.sh

echo "🔧 Deployment fixes complete!"
echo ""
echo "✅ Ready to deploy with:"
echo "   docker-compose up -d"
echo ""
echo "📝 To verify deployment:"
echo "   docker-compose ps"
echo "   curl -X GET http://localhost:8000/health"