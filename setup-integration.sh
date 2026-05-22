#!/bin/bash

set -e

echo "🐉 KaliGhost - Dashboard Principal Integrado"
echo "============================================="
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. Instalar dependencias Python
echo -e "${YELLOW}[1/3]${NC} Installing Python dependencies..."
pip install -r requirements.txt --quiet

# 2. Instalar dependencias Node.js
echo -e "${YELLOW}[2/3]${NC} Installing Node.js dependencies..."
bun install --frozen-lockfile --quiet

# 3. Generar build
echo -e "${YELLOW}[3/3]${NC} Building Next.js..."
bun run build

echo ""
echo "✓ Setup complete!"
echo ""
echo "To start the KaliGhost Dashboard:"
echo "  docker-compose up -d"
echo ""
echo "Or run services individually:"
echo "  # Terminal 1 - Backend"
echo "  python -m gui.websocket_backend"
echo ""
echo "  # Terminal 2 - Frontend"
echo "  bun run dev"
echo ""
echo "Dashboard (Main): http://localhost:3000"
echo "Backend API: http://localhost:5001"
echo ""
