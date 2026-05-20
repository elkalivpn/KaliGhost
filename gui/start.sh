#!/bin/bash

# KaliGhost Pro - Quick Start Script
# Inicia Backend + Frontend en paralelo

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "🐉 KaliGhost Pro - Starting..."
echo ""

# Color codes
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "${RED}❌ Python 3 is required but not installed${NC}"
    exit 1
fi

# Check Node
if ! command -v node &> /dev/null; then
    echo "${RED}❌ Node.js is required but not installed${NC}"
    exit 1
fi

# Create logs directory
mkdir -p "$DIR/../logs"

# Virtual environment setup
if [ ! -d "venv_backend" ]; then
    echo "${CYAN}📦 Creating Python virtual environment...${NC}"
    python3 -m venv venv_backend
fi

# Activate venv
source venv_backend/bin/activate

# Install Python dependencies
echo "${CYAN}📦 Installing Python dependencies...${NC}"
if [ -f "requirements_backend.txt" ]; then
    pip install -q -r requirements_backend.txt
fi

# Install Node dependencies
echo "${CYAN}📦 Installing Node dependencies...${NC}"
if [ ! -d "node_modules" ]; then
    npm install --quiet
fi

echo ""
echo "${GREEN}✅ Dependencies installed${NC}"
echo ""

# Function to start backend
start_backend() {
    echo "${CYAN}🚀 Starting Backend WebSocket Server...${NC}"
    echo "${YELLOW}Backend: http://0.0.0.0:5000${NC}"
    python websocket_backend.py
}

# Function to start frontend
start_frontend() {
    echo "${CYAN}🚀 Starting Frontend Dev Server...${NC}"
    echo "${YELLOW}Frontend: http://localhost:5173${NC}"
    npm run dev
}

# Trap to cleanup on exit
cleanup() {
    echo ""
    echo "${YELLOW}🛑 Shutting down...${NC}"
    kill $(jobs -p) 2>/dev/null || true
    deactivate 2>/dev/null || true
}
trap cleanup EXIT

echo "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo "${GREEN}KaliGhost Pro - Dual Server Launch${NC}"
echo "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo "${YELLOW}Starting Backend...${NC}"
start_backend &
BACKEND_PID=$!

sleep 2

echo ""
echo "${YELLOW}Starting Frontend...${NC}"
start_frontend &
FRONTEND_PID=$!

sleep 2

echo ""
echo "${GREEN}✅ All servers running!${NC}"
echo ""
echo "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo "🌐 GUI:      http://localhost:5173"
echo "🔌 Backend:  http://localhost:5000"
echo "📊 Health:   http://localhost:5000/health"
echo "📋 Logs:     /Users/mrhardcore/KaliGhost/logs/websocket_backend.log"
echo "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo "${YELLOW}Press Ctrl+C to stop all servers${NC}"
echo ""

wait
