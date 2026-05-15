#!/bin/bash
# Professional KaliGhost GUI Starter Script

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}"
echo "██╗  ██╗ █████╗ ██╗     ██╗ ██████╗ ██╗  ██╗ ██████╗ "
echo "██║ ██╔╝██╔══██╗██║     ██║██╔════╝ ██║  ██║██╔═══██╗"
echo "█████╔╝ ███████║██║     ██║██║  ███╗███████║██║   ██║"
echo "██╔═██╗ ██╔══██║██║     ██║██║   ██║██╔══██║██║   ██║"
echo "██║  ██╗██║  ██║███████╗██║╚██████╔╝██║  ██║╚██████╔╝"
echo "╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ "
echo -e "${NC}"
echo -e "${PURPLE}🚀 KaliGhost Professional Cyberpunk Interface${NC}"
echo -e "${BLUE}==============================================${NC}"
echo ""

# Detect operating system
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    else
        echo "unknown"
    fi
}

OS_TYPE=$(detect_os)
echo -e "${BLUE}[INFO] Detected OS: $OS_TYPE${NC}"

# Check if we're in the right directory
if [ ! -f "gui/professional_kalighost_gui.py" ]; then
    echo -e "${RED}[ERROR] Professional GUI file not found!${NC}"
    echo -e "${YELLOW}Please run this script from the KaliGhost root directory.${NC}"
    exit 1
fi

# Setup virtual environment if it doesn't exist
setup_virtualenv() {
    if [ ! -d "venv" ]; then
        echo -e "${BLUE}[+] Creating virtual environment...${NC}"
        python3 -m venv venv
    fi
    
    echo -e "${BLUE}[+] Activating virtual environment...${NC}"
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
}

# Install dependencies
install_dependencies() {
    echo -e "${BLUE}[+] Installing professional GUI dependencies...${NC}"
    
    case $OS_TYPE in
        "linux")
            # For Kali Linux
            if command -v apt &> /dev/null; then
                echo -e "${YELLOW}[!] Updating package lists...${NC}"
                sudo apt update
                
                echo -e "${YELLOW}[!] Installing system dependencies...${NC}"
                sudo apt install -y python3-pyside6.qtwidgets python3-opengl python3-venv
                
                echo -e "${YELLOW}[!] Installing Python packages...${NC}"
                pip install PySide6-Essentials PyOpenGL PyOpenGL-accelerate numpy
            fi
            ;;
        "macos")
            # For macOS
            if command -v brew &> /dev/null; then
                echo -e "${YELLOW}[!] Installing Homebrew packages...${NC}"
                brew install python@3.9
                
                echo -e "${YELLOW}[!] Installing Python packages in virtual environment...${NC}"
                source venv/bin/activate
                pip install "PySide6-Essentials>=6.5" PyOpenGL PyOpenGL-accelerate numpy
            else
                echo -e "${YELLOW}[!] Installing Python packages directly...${NC}"
                pip3 install --user "PySide6-Essentials>=6.5" PyOpenGL PyOpenGL-accelerate numpy
            fi
            ;;
        *)
            echo -e "${YELLOW}[!] Installing Python packages...${NC}"
            pip install PySide6-Essentials PyOpenGL PyOpenGL-accelerate numpy
            ;;
    esac
}

# Verify dependencies
verify_dependencies() {
    echo -e "${BLUE}[+] Verifying dependencies...${NC}"
    
    source venv/bin/activate 2>/dev/null || true
    
    MISSING_DEPS=()
    
    # Check PySide6
    if python3 -c "import PySide6" &> /dev/null; then
        VERSION=$(python3 -c "import PySide6; print(PySide6.__version__)")
        echo -e "${GREEN}[✓] PySide6 $VERSION found${NC}"
    else
        echo -e "${RED}[✗] PySide6 not found${NC}"
        MISSING_DEPS+=("PySide6")
    fi
    
    # Check OpenGL
    if python3 -c "import OpenGL" &> /dev/null; then
        echo -e "${GREEN}[✓] PyOpenGL found${NC}"
    else
        echo -e "${YELLOW}[!] PyOpenGL not found - will use 2D fallback${NC}"
    fi
    
    # Check NumPy
    if python3 -c "import numpy" &> /dev/null; then
        VERSION=$(python3 -c "import numpy; print(numpy.__version__)")
        echo -e "${GREEN}[✓] NumPy $VERSION found${NC}"
    else
        echo -e "${RED}[✗] NumPy not found${NC}"
        MISSING_DEPS+=("numpy")
    fi
    
    # Install missing dependencies
    if [ ${#MISSING_DEPS[@]} -ne 0 ]; then
        echo -e "${YELLOW}[!] Installing missing dependencies: ${MISSING_DEPS[*]}${NC}"
        case $OS_TYPE in
            "macos")
                pip3 install --user "${MISSING_DEPS[@]}"
                ;;
            *)
                pip3 install "${MISSING_DEPS[@]}"
                ;;
        esac
    fi
}

# Set environment variables for macOS
set_macos_env() {
    if [[ "$OS_TYPE" == "macos" ]]; then
        echo -e "${BLUE}[+] Setting macOS environment variables...${NC}"
        export QT_MAC_WANTS_LAYER=1
        echo -e "${GREEN}[✓] QT_MAC_WANTS_LAYER=1${NC}"
    fi
}

# Main execution
main() {
    # Setup environment
    setup_virtualenv
    install_dependencies
    verify_dependencies
    set_macos_env
    
    # Change to gui directory
    cd gui
    
    # Show startup message
    echo ""
    echo -e "${CYAN}🔥 Starting KaliGhost Professional Cyberpunk Interface${NC}"
    echo -e "${YELLOW}💡 The professional 3D dragon interface will appear shortly${NC}"
    echo -e "${YELLOW}💡 Close the window or press Ctrl+C to exit${NC}"
    echo ""
    
    # Run the professional GUI
    if [[ "$OS_TYPE" == "macos" ]]; then
        python3 professional_kalighost_gui.py
    else
        python3 professional_kalighost_gui.py
    fi
    
    # Show exit message
    echo ""
    echo -e "${GREEN}✅ KaliGhost Professional Interface shutdown complete${NC}"
    echo -e "${BLUE}Thank you for using KaliGhost!${NC}"
}

# Run main function
main