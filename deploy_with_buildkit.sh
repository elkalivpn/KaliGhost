#!/bin/bash
# KaliGhost 3.0 Deployment Script with BuildKit
# Uses Docker BuildKit to avoid credential issues during build

export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_CLI_HINTS=false
export DOCKER_CONTENT_TRUST=0

echo "🚀 Starting KaliGhost 3.0 Deployment with BuildKit"

# Clean up
echo "🧹 Cleaning up previous installations..."
docker rm -f kalighost-gateway kalighost-sandbox kalighost-provisioner kalighost-postgres kalighost-redis kalighost-prometheus kalighost-grafana kalighost-nginx 2>/dev/null || true
docker network rm kalighost_net 2>/dev/null || true

# Create network
echo "🌐 Creating network..."
docker network create kalighost_net

# Pull base images
echo "📥 Pulling base images with BuildKit..."
for image in redis:7-alpine postgres:16-alpine prom/prometheus:latest grafana/grafana:latest nginx:alpine; do
    echo "Pulling $image..."
    docker pull $image || echo "Warning: Failed to pull $image"
done

# Build images with BuildKit
echo "🏗️  Building custom images with BuildKit..."
cd docker

echo "Building gateway image..."
time docker build \
  --progress=plain \
  -f Dockerfile.gateway \
  -t kalighost:gateway \
  .. || {
    echo "❌ Gateway build failed"
    cd ..
    exit 1
  }

echo "Building provisioner image..."
time docker build \
  --progress=plain \
  -f Dockerfile.provisioner \
  -t kalighost:provisioner \
  .. || {
    echo "❌ Provisioner build failed"
    cd ..
    exit 1
  }
cd ..

# Set up volumes
echo "📁 Setting up volume directories..."
mkdir -p data/{memory,logs} .kalighost/memory

# Start services
echo "🚀 Starting services..."

# Redis
docker run -d \
 --name kalighost-redis \
 --network kalighost_net \
 --restart unless-stopped \
 -p 6379:6379 \
 redis:7-alpine \
 redis-server --appendonly yes --requirepass changeme

# PostgreSQL
docker run -d \
 --name kalighost-postgres \
 --network kalighost_net \
 --restart unless-stopped \
 -e POSTGRES_DB=kalighost \
 -e POSTGRES_USER=kalighost \
 -e POSTGRES_PASSWORD=changeme \
 -v $(pwd)/data/postgres_data:/var/lib/postgresql/data \
 -v $(pwd)/docker/init.sql:/docker-entrypoint-initdb.d/init.sql:ro \
 postgres:16-alpine

# Prometheus
docker run -d \
 --name kalighost-prometheus \
 --network kalighost_net \
 --restart unless-stopped \
 -p 9090:9090 \
 -v $(pwd)/docker/prometheus.yml:/etc/prometheus/prometheus.yml:ro \
 -v $(pwd)/data/prometheus_data:/prometheus \
 prom/prometheus:latest \
 --config.file=/etc/prometheus/prometheus.yml \
 --storage.tsdb.path=/prometheus

# Grafana
docker run -d \
 --name kalighost-grafana \
 --network kalighost_net \
 --restart unless-stopped \
 -p 3001:3000 \
 -e GF_SECURITY_ADMIN_USER=admin \
 -e GF_SECURITY_ADMIN_PASSWORD=admin123 \
 -e GF_USERS_ALLOW_SIGN_UP=false \
 -e GF_INSTALL_PLUGINS=grafana-piechart-panel \
 -v $(pwd)/data/grafana_data:/var/lib/grafana \
 -v $(pwd)/docker/grafana/provisioning:/etc/grafana/provisioning:ro \
 grafana/grafana:latest

# Nginx
docker run -d \
 --name kalighost-nginx \
 --network kalighost_net \
 --restart unless-stopped \
 -p 80:80 \
 -p 443:443 \
 -v $(pwd)/docker/nginx.conf:/etc/nginx/nginx.conf:ro \
 -v $(pwd)/docker/ssl:/etc/nginx/ssl:ro \
 -v $(pwd)/data/nginx_cache:/var/cache/nginx \
 nginx:alpine

# Gateway
docker run -d \
 --name kalighost-gateway \
 --network kalighost_net \
 -p 8000:8000 \
 -p 8001:8001 \
 kalighost:gateway

# Provisioner
docker run -d \
 --name kalighost-provisioner \
 --network kalighost_net \
 -p 9000:9000 \
 kalighost:provisioner

echo ""
echo "✅ DEPLOYMENT COMPLETE"
echo ""
echo "📋 Service Status Summary:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""
echo "🔧 Access Points:"
echo "   • API Gateway:     http://localhost:8000"
echo "   • API Docs:        http://localhost:8000/docs"
echo "   • WebChat:         http://localhost:8001"
echo "   • Grafana:         http://localhost:3001"
echo "   • Prometheus:      http://localhost:9090"
echo ""
echo "📁 Data Directories:"
echo "   • Logs:       ./data/logs"
echo "   • Memory:     ./data/memory"
echo "   • Database:   ./data/postgres_data"