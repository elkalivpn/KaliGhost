#!/bin/bash
# Manual KaliGhost 3.0 Deployment Script
# Bypasses docker-compose credential errors completely

echo "🔧 Initiating manual deployment of KaliGhost 3.0..."

# Set environment for the process
export DOCKER_CLI_HINTS=false
export DOCKER_CONTENT_TRUST=0

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found!"
    exit 1
fi

# Create network
echo "🌐 Creating network..."
docker network create kalighost_net 2>/dev/null || true

# Start Redis
echo "💾 Starting Redis..."
docker run -d \
 --name kalighost-redis \
 --network kalighost_net \
 --restart unless-stopped \
 -p 6379:6379 \
 redis:7-alpine \
 redis-server --appendonly yes --requirepass changeme

# Start Postgres
echo "🗄️ Starting PostgreSQL..."
docker run -d \
 --name kalighost-postgres \
 --network kalighost_net \
 --restart unless-stopped \
 -e POSTGRES_DB=kalighost \
 -e POSTGRES_USER=kalighost \
 -e POSTGRES_PASSWORD=changeme \
 -e POSTGRES_INITDB_ARGS="--encoding=UTF8 --locale=en_US.UTF-8" \
 -v postgres_data:/var/lib/postgresql/data \
 -v $(pwd)/docker/init.sql:/docker-entrypoint-initdb.d/init.sql:ro \
 postgres:16-alpine

# Start Prometheus
echo "📈 Starting Prometheus..."
docker run -d \
 --name kalighost-prometheus \
 --network kalighost_net \
 --restart unless-stopped \
 -p 9090:9090 \
 -v $(pwd)/docker/prometheus.yml:/etc/prometheus/prometheus.yml:ro \
 -v prometheus_data:/prometheus \
 prom/prometheus:latest \
 --config.file=/etc/prometheus/prometheus.yml \
 --storage.tsdb.path=/prometheus

# Start Grafana
echo "📊 Starting Grafana..."
docker run -d \
 --name kalighost-grafana \
 --network kalighost_net \
 --restart unless-stopped \
 -p 3001:3000 \
 -e GF_SECURITY_ADMIN_USER=admin \
 -e GF_SECURITY_ADMIN_PASSWORD=admin123 \
 -e GF_USERS_ALLOW_SIGN_UP=false \
 -e GF_INSTALL_PLUGINS=grafana-piechart-panel \
 -v grafana_data:/var/lib/grafana \
 -v $(pwd)/docker/grafana/provisioning:/etc/grafana/provisioning:ro \
 grafana/grafana:latest

# Start Nginx
echo "📡 Starting Nginx..."
docker run -d \
 --name kalighost-nginx \
 --network kalighost_net \
 --restart unless-stopped \
 -p 80:80 \
 -p 443:443 \
 -v $(pwd)/docker/nginx.conf:/etc/nginx/nginx.conf:ro \
 -v $(pwd)/docker/ssl:/etc/nginx/ssl:ro \
 -v nginx_cache:/var/cache/nginx \
 nginx:alpine

echo "🏁 Manual deployment started!"
echo ""
echo "💡 Services:"
echo "   Redis:      localhost:6379"
echo "   PostgreSQL: localhost:5432"
echo "   Prometheus: localhost:9090"
echo "   Grafana:    localhost:3001"
echo "   Nginx:      localhost:80/443"
echo ""
echo "⚠️  Gateway and Provisioner require manual image builds since they use local Dockerfiles."
echo "   To complete deployment, continue with:"
echo "   cd /Users/mrhardcore/KaliGhost && docker build -f docker/Dockerfile.gateway -t kalighost:gateway ."
echo "   cd /Users/mrhardcore/KaliGhost && docker build -f docker/Dockerfile.provisioner -t kalighost:provisioner ."
echo ""
echo "Then run:"
echo "   docker run -d --name kalighost-gateway --network kalighost_net -p 8000:8000 -p 8001:8001 kalighost:gateway"
echo "   docker run -d --name kalighost-provisioner --network kalighost_net -p 9000:9000 kalighost:provisioner"
echo ""
echo "📋 Check status with: docker ps"