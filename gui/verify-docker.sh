#!/bin/bash
# ==============================================================================
# Quick Docker Verification for KaliGhost Pro
# ==============================================================================

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  KaliGhost Pro - Docker Verification  ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Check Docker
echo -e "${YELLOW}Checking Docker...${NC}"
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    echo -e "${GREEN}✓ ${DOCKER_VERSION}${NC}"
else
    echo -e "${RED}✗ Docker not found${NC}"
    exit 1
fi

# Check Docker Compose
echo -e "${YELLOW}Checking Docker Compose...${NC}"
if docker compose version &> /dev/null; then
    COMPOSE_VERSION=$(docker compose version 2>&1 | head -1)
    echo -e "${GREEN}✓ ${COMPOSE_VERSION}${NC}"
else
    echo -e "${RED}✗ Docker Compose not found${NC}"
    exit 1
fi

# Check Docker daemon
echo -e "${YELLOW}Checking Docker daemon...${NC}"
if docker ps &> /dev/null; then
    echo -e "${GREEN}✓ Docker daemon running${NC}"
else
    echo -e "${RED}✗ Docker daemon not accessible${NC}"
    exit 1
fi

# Validate compose file
echo -e "${YELLOW}Validating docker-compose.yml...${NC}"
if docker compose config > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Configuration valid${NC}"
else
    echo -e "${RED}✗ Configuration error${NC}"
    exit 1
fi

# Check required files
echo -e "${YELLOW}Checking required files...${NC}"
FILES=(
    "backend/Dockerfile"
    "backend/.dockerignore"
    "backend/websocket_backend.py"
    "backend/requirements_backend.txt"
    "frontend/Dockerfile"
    "frontend/.dockerignore"
    "frontend/nginx.conf"
    "frontend/package.json"
    ".env.example"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${RED}✗${NC} $file (MISSING)"
    fi
done

# Build images
echo ""
echo -e "${YELLOW}Building Docker images (this may take a few minutes)...${NC}"
if docker compose build --no-cache 2>&1 | tail -20; then
    echo -e "${GREEN}✓ Build successful${NC}"
else
    echo -e "${RED}✗ Build failed${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✓ All checks passed!                 ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo "Next steps:"
echo "  1. Review .env configuration"
echo "  2. Run: docker compose up -d"
echo "  3. Access: http://localhost:5173 (frontend)"
echo "            http://localhost:8000 (backend)"
echo ""
