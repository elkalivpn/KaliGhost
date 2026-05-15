#!/bin/bash
# Quick test script for professional KaliGhost GUI

set -e

echo "🚀 Quick Test: KaliGhost Professional GUI"
echo "========================================="

# Check if we're in the right directory
if [ ! -f "gui/professional_kalighost_gui.py" ]; then
    echo "❌ ERROR: Professional GUI file not found!"
    echo "Please run this script from the KaliGhost root directory."
    exit 1
fi

echo "✅ Professional GUI file found"

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1)
echo "🐍 $PYTHON_VERSION"

# Check dependencies
echo "📋 Checking dependencies..."

if python3 -c "import PySide6" &> /dev/null; then
    PYSIDE_VERSION=$(python3 -c "import PySide6; print(PySide6.__version__)")
    echo "✅ PySide6 $PYSIDE_VERSION: FOUND"
else
    echo "❌ PySide6: NOT FOUND"
    echo "Installing PySide6..."
    pip3 install PySide6-Essentials
fi

if python3 -c "import numpy" &> /dev/null; then
    NUMPY_VERSION=$(python3 -c "import numpy; print(numpy.__version__)")
    echo "✅ NumPy $NUMPY_VERSION: FOUND"
else
    echo "❌ NumPy: NOT FOUND"
    echo "Installing NumPy..."
    pip3 install numpy
fi

# Test OpenGL availability
if python3 -c "import OpenGL" &> /dev/null; then
    echo "✅ OpenGL: AVAILABLE"
    OPENGL_STATUS="3D"
else
    echo "⚠️  OpenGL: NOT AVAILABLE (will use 2D fallback)"
    OPENGL_STATUS="2D"
fi

echo ""
echo "🎮 Starting Professional GUI Test ($OPENGL_STATUS mode)..."
echo "Close the window to exit."

# Set environment for macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    export QT_MAC_WANTS_LAYER=1
    echo "🔧 macOS environment configured"
fi

# Run the GUI
cd gui
python3 professional_kalighost_gui.py

echo "✅ Test completed successfully!"