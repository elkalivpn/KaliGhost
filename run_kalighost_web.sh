#!/bin/bash
# KaliGhost Pro - FastAPI Backend Launcher

cd "$(dirname "$0")" || exit 1

echo "╔════════════════════════════════════════════════════════════╗"
echo "║           🐉 KaliGhost Pro - FastAPI Edition              ║"
echo "║        Starting Web-based Cyberpunk Interface...          ║"
echo "╚════════════════════════════════════════════════════════════╝"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Install Python 3.9+"
    exit 1
fi

# Create virtual environment if needed
if [ ! -d "venv_kalighost" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv_kalighost
fi

# Activate virtual environment
source venv_kalighost/bin/activate

# Install/upgrade dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install fastapi uvicorn httpx pydantic > /dev/null 2>&1

# Start the server
echo ""
echo "🚀 Starting KaliGhost API Server..."
echo "📡 API: http://localhost:8000"
echo "🌐 Web UI: http://localhost:8000/kalighost_ui.html"
echo "📚 Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Auto-open UI if possible
if command -v open &> /dev/null; then
    sleep 2 && open "http://localhost:8000/kalighost_ui.html" &
fi

# Run API
python3 kalighost_api.py
