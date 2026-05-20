#!/bin/bash
# ==============================================================================
# Multi-Architecture Build Script for KaliGhost Pro
# Supports: linux/amd64, linux/arm64
# ==============================================================================

set -e

# Configuration
REGISTRY="${REGISTRY:-docker.io}"
NAMESPACE="${NAMESPACE:-your-username}"
VERSION="${VERSION:-latest}"
PUSH="${PUSH:-false}"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== KaliGhost Pro Multi-Architecture Builder ===${NC}"
echo ""

# Check if buildx is available
if ! docker buildx version &> /dev/null; then
    echo -e "${YELLOW}Docker Buildx not found. Installing...${NC}"
    docker buildx create --name multiarch --use --bootstrap
fi

# Check if QEMU is available
echo -e "${BLUE}Setting up QEMU for multi-arch support...${NC}"
docker run --privileged --rm tonistiigi/binfmt --install all

echo ""
echo -e "${BLUE}Building for architectures: linux/amd64, linux/arm64${NC}"
echo ""

# Build backend
echo -e "${YELLOW}Building Backend Image...${NC}"
BACKEND_IMAGE="${REGISTRY}/${NAMESPACE}/kalighost-backend:${VERSION}"

docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --tag "${BACKEND_IMAGE}" \
    --file backend/Dockerfile \
    --target production \
    ${PUSH:+--push} \
    ${PUSH:---load} \
    ./backend

echo -e "${GREEN}✓ Backend image built: ${BACKEND_IMAGE}${NC}"
echo ""

# Build frontend
echo -e "${YELLOW}Building Frontend Image...${NC}"
FRONTEND_IMAGE="${REGISTRY}/${NAMESPACE}/kalighost-frontend:${VERSION}"

docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --tag "${FRONTEND_IMAGE}" \
    --file frontend/Dockerfile \
    --target production \
    ${PUSH:+--push} \
    ${PUSH:---load} \
    ./frontend

echo -e "${GREEN}✓ Frontend image built: ${FRONTEND_IMAGE}${NC}"
echo ""

# Summary
echo -e "${GREEN}=== Build Complete ===${NC}"
echo ""
echo "Backend:  ${BACKEND_IMAGE}"
echo "Frontend: ${FRONTEND_IMAGE}"
echo ""

if [ "$PUSH" = "true" ]; then
    echo -e "${GREEN}Images pushed to registry!${NC}"
else
    echo -e "${YELLOW}To push images to registry, use: --push flag${NC}"
    echo "Example: PUSH=true ./build-multiarch.sh"
fi
