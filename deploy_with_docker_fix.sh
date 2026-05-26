#!/bin/bash
# KaliGhost 3.0 Deployment with Docker credential fix

echo "🚀 Starting KaliGhost 3.0 Deployment with Docker credential fix"

# Function to check if Docker Desktop is running and start if not
start_docker_desktop() {
    if ! docker info >/dev/null 2>&1; then
        echo "🐳 Docker Desktop is not running. Attempting to start..."
        open -a Docker
        # Wait for Docker to start (max 30 seconds)
        for i in {1..30}; do
            if docker info >/dev/null 2>&1; then
                echo "✅ Docker Desktop started."
                return 0
            fi
            sleep 1
        done
        echo "❌ Failed to start Docker Desktop after 30 seconds."
        return 1
    else
        echo "🐳 Docker Desktop is already running."
        return 0
    fi
}

# Start Docker Desktop if needed
start_docker_desktop || exit 1

# Set Docker config to a temporary empty directory to avoid credential issues
export DOCKER_CONFIG=$(mktemp -d)
echo "🔧 Using temporary Docker config: $DOCKER_CONFIG"

# Disable content trust and hints to avoid interactive prompts
export DOCKER_CONTENT_TRUST=0
export DOCKER_CLI_HINTS=false

echo "🧹 Cleaning up previous installations..."
docker rm -f kalighost-gateway kalighost-sandbox kalighost-provisioner kalighost-postgres kalighost-redis kalighost-prometheus kalighost-grafana kalighost-nginx 2>/dev/null || true
docker network rm kalighost_net 2>/dev/null || true

echo "🌐 Creating network..."
docker network create kalighost_net

echo "📥 Pulling base images..."
# Pull base images one by one to see which one fails
for image in redis:7-alpine postgres:16-alpine prom/prometheus:latest grafana/grafana:latest nginx:alpine; do
    echo "Pulling $image..."
    if ! docker pull $image; then
        echo "❌ Failed to pull $image. Trying to continue..."
    fi
done

echo "🏗️  Building custom images..."
cd docker
echo "Building gateway image..."
if ! docker build -f Dockerfile.gateway -t kalighost:gateway ..; then
    echo "❌ Failed to build gateway image."
    cd ..
    exit 1
fi
echo "Building provisioner image..."
if ! docker build -f Dockerfile.provisioner -t kalighost:provisioner ..; then
    echo "❌ Failed to build provisioner image."
    cd ..
    exit 1
fi
cd ..

echo "📁 Setting up volume directories..."
mkdir -p data/{memory,logs} .kalighost/memory

echo "🚀 Starting services..."

# Redis
echo "Starting Redis..."
docker run -d \
 --name kalighost-redis \
 --network kalighost_net \
 --restart unless-stopped \
 -p 6379:6379 \
 redis:7-alpine \
 redis-server --appendonly yes --requirepass changeme

# PostgreSQL
echo "Starting PostgreSQL..."
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
echo "Starting Prometheus..."
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
echo "Starting Grafana..."
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
echo "Starting Nginx..."
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
echo "Starting Gateway..."
docker run -d \
 --name kalighost-gateway \
 --network kalighost_net \
 -p 8000:8000 \
 -p 8001:8001 \
 kalighost:gateway

# Provisioner
echo "Starting Provisioner..."
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
echo ""
echo "🧹 Temporary Docker config: $DOCKER_CONFIG (will be cleaned on reboot)"