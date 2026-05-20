#!/bin/bash
# ==============================================================================
# KaliGhost Pro - Development Environment Setup
# ==============================================================================

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  KaliGhost Pro - Development Setup    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Create .env if not exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env from .env.example...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ .env created${NC}"
fi

# Create necessary directories
echo -e "${YELLOW}Creating necessary directories...${NC}"
mkdir -p backend/app frontend/src secrets logs

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}⚠ Docker not found. Please install Docker Desktop.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker found${NC}"

# Build images
echo ""
echo -e "${YELLOW}Building Docker images...${NC}"
docker-compose build

echo ""
echo -e "${GREEN}✓ Images built successfully${NC}"

# Start services
echo ""
echo -e "${YELLOW}Starting services...${NC}"
docker-compose up -d

echo ""
echo -e "${BLUE}════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo -e "${BLUE}════════════════════════════════════════${NC}"
echo ""
echo "Services are running:"
echo ""
echo -e "  ${GREEN}Frontend:${NC}     http://localhost:5173"
echo -e "  ${GREEN}Backend:${NC}      http://localhost:8000"
echo -e "  ${GREEN}API Docs:${NC}     http://localhost:8000/docs"
echo -e "  ${GREEN}Database:${NC}     localhost:5432"
echo -e "  ${GREEN}Redis:${NC}        localhost:6379"
echo ""
echo "View logs:"
echo "  docker-compose logs -f frontend"
echo "  docker-compose logs -f backend"
echo ""
echo "Stop services:"
echo "  docker-compose down"
echo ""
