#!/bin/bash
# 🐉 KaliGhost 3.0 - Startup Script
# Production-ready initialization

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logo
echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                   🐉 KaliGhost 3.0                            ║"
echo "║          Elite Developer Agentic Environment                  ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# ============================================================================
# ENVIRONMENT SETUP
# ============================================================================

echo -e "${BLUE}[1/5]${NC} Setting up environment..."

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env not found. Creating from template...${NC}"
    cp .env.example .env 2>/dev/null || echo "OPENAI_API_KEY=your_key_here" > .env
    echo -e "${YELLOW}📝 Please edit .env with your API keys${NC}"
    exit 1
fi

# Load environment
source .env

echo -e "${GREEN}✅ Environment loaded${NC}"

# ============================================================================
# DEPENDENCY CHECK
# ============================================================================

echo -e "${BLUE}[2/5]${NC} Checking dependencies..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python 3 found${NC}"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Docker found${NC}"

# Check pip packages
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install -q -r requirements.txt
echo -e "${GREEN}✅ Dependencies installed${NC}"

# ============================================================================
# DIRECTORY SETUP
# ============================================================================

echo -e "${BLUE}[3/5]${NC} Setting up directories..."

mkdir -p backend
mkdir -p examples
mkdir -p docker
mkdir -p config
mkdir -p skills
mkdir -p data/{memory,logs}
mkdir -p .kalighost/memory

echo -e "${GREEN}✅ Directories created${NC}"

# ============================================================================
# DOCKER SETUP
# ============================================================================

echo -e "${BLUE}[4/5]${NC} Preparing Docker environment..."

# Build custom Dockerfiles
if [ -f "docker/Dockerfile.gateway" ]; then
    echo -e "${YELLOW}Building gateway image...${NC}"
    docker build -f docker/Dockerfile.gateway -t kalighost:gateway . &>/dev/null &
    DOCKER_PID=$!
fi

if [ -f "docker/Dockerfile.provisioner" ]; then
    echo -e "${YELLOW}Building provisioner image...${NC}"
    docker build -f docker/Dockerfile.provisioner -t kalighost:provisioner . &>/dev/null &
    DOCKER_PID2=$!
fi

# Wait for builds
wait $DOCKER_PID 2>/dev/null || true
wait $DOCKER_PID2 2>/dev/null || true

echo -e "${GREEN}✅ Docker images ready${NC}"

# ============================================================================
# DATABASE SETUP
# ============================================================================

echo -e "${BLUE}[5/5]${NC} Starting services..."

# Start docker-compose services
echo -e "${YELLOW}Starting Docker Compose stack...${NC}"
docker-compose up -d

# Wait for services to start
echo -e "${YELLOW}Waiting for services to be healthy...${NC}"
sleep 10

# Check if gateway is running
if docker-compose ps gateway | grep -q "Up"; then
    echo -e "${GREEN}✅ Gateway is running${NC}"
else
    echo -e "${RED}❌ Gateway failed to start${NC}"
    docker-compose logs gateway
    exit 1
fi

# ============================================================================
# VERIFICATION
# ============================================================================

echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ KaliGhost 3.0 is ready!${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}Access Points:${NC}"
echo -e "  • API Gateway:     ${YELLOW}http://localhost:8000${NC}"
echo -e "  • API Docs:        ${YELLOW}http://localhost:8000/docs${NC}"
echo -e "  • WebChat:         ${YELLOW}http://localhost:8001${NC}"
echo -e "  • Grafana:         ${YELLOW}http://localhost:3001${NC}"
echo -e "  • Prometheus:      ${YELLOW}http://localhost:9090${NC}"
echo ""
echo -e "${BLUE}Quick Commands:${NC}"
echo -e "  ${YELLOW}kalighost orchestrate execute \"Build a Node.js SaaS\"${NC}"
echo -e "  ${YELLOW}kalighost memory add preference \"Use TypeScript\"${NC}"
echo -e "  ${YELLOW}kalighost security audit ./src${NC}"
echo -e "  ${YELLOW}python examples/complete_examples.py${NC}"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo -e "  1. Open ${YELLOW}http://localhost:8001${NC} for WebChat interface"
echo -e "  2. Or use CLI: ${YELLOW}kalighost orchestrate execute <task>${NC}"
echo -e "  3. Check logs: ${YELLOW}docker-compose logs -f gateway${NC}"
echo ""

# Show status
echo -e "${BLUE}Service Status:${NC}"
docker-compose ps
