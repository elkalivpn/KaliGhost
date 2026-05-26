#!/bin/bash
# Fixed KaliGhost deployment script that handles Docker Desktop credential helper on macOS

set -euo pipefail

echo "🚀 Starting KaliGhost 3.0 Deployment (Fixed for Docker Desktop)"

# Add Docker Desktop's helper to PATH if on macOS
if [[ "$(uname)" == "Darwin" ]]; then
    DOCKER_DIR="/Applications/Docker.app/Contents/Resources/bin"
    if [[ -d "$DOCKER_DIR" && -x "$DOCKER_DIR/docker-credential-desktop" ]]; then
        echo "📦 Adding Docker Desktop credentials helper to PATH..."
        export PATH="$DOCKER_DIR:$PATH"
        # Also set Docker's credential helper explicitly
        export DOCKER_CREDENTIAL_HELPER="desktop"
    fi
fi

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "⚠️  Docker Desktop appears to be not running. Attempting to start..."
    # Try to start Docker Desktop (macOS)
    if [[ "$(uname)" == "Darwin" ]]; then
        open -a Docker
        # Wait for Docker to start
        echo "⏳ Waiting for Docker Desktop to start..."
        for i in {1..30}; do
            if docker info >/dev/null 2>&1; then
                echo "✅ Docker Desktop is now running"
                break
            fi
            sleep 2
            if [[ $i -eq 30 ]]; then
                echo "❌ Docker Desktop failed to start after 60 seconds"
                exit 1
            fi
        done
    else
        echo "❌ Please start Docker Desktop manually and retry"
        exit 1
    fi
fi

# Clean up previous installations
echo "🧹 Cleaning up previous installations..."
docker compose down -v --remove-orphans 2>/dev/null || true
docker network rm kalighost_net 2>/dev/null || true

# Create network
echo "🌐 Creating network..."
docker network create kalighost_net

# Pull base images
echo "📥 Pulling base images..."
docker compose pull

# Build and start all services
echo "🏗️  Building and starting services..."
docker compose up -d --build

# Wait for services to be healthy
echo "⏳ Waiting for services to become healthy..."
services=(gateway postgres redis prometheus grafana nginx)
for service in "${services[@]}"; do
    echo "   Checking $service..."
    for i in {1..30}; do
        if docker compose ps "$service" | grep -q "healthy"; then
            echo "   ✅ $service is healthy"
            break
        fi
        sleep 2
        if [[ $i -eq 30 ]]; then
            echo "   ⚠️  $service health check timed out (continuing anyway)"
        fi
    done
done

# Show status
echo ""
echo "📊 Deployment Status:"
docker compose ps

echo ""
echo "🎉 KaliGhost 3.0 Deployment Complete!"
echo ""
echo "🔗 Access Points:"
echo "   • Gateway API: http://localhost:8000"
echo "   • Gateway WebSocket: ws://localhost:8001"
echo "   • Provisioner API: http://localhost:9000"
echo "   • Grafana Dashboard: http://localhost:3001 (admin/admin123)"
echo "   • Prometheus: http://localhost:9090"
echo ""
echo "📝 Next Steps:"
echo "   1. Check logs: docker compose logs -f gateway"
echo "   2. Run demo: python3 demo_deployment.py"
echo "   3. Visit docs: https://github.com/elkalivpn/KaliGhost"
echo ""
echo "💡 Tip: Use 'hermes view' to monitor Hermes agents in real-time"