#!/bin/bash
# Professional KaliGhost Pro Installation Script
# Advanced installation with dependency management and professional setup

set -e

# Professional colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Professional banner
echo -e "${CYAN}"
echo "██╗  ██╗ █████╗ ██╗     ██╗ ██████╗ ██╗  ██╗ ██████╗ "
echo "██║ ██╔╝██╔══██╗██║     ██║██╔════╝ ██║  ██║██╔═══██╗"
echo "█████╔╝ ███████║██║     ██║██║  ███╗███████║██║   ██║"
echo "██╔═██╗ ██╔══██║██║     ██║██║   ██║██╔══██║██║   ██║"
echo "██║  ██╗██║  ██║███████╗██║╚██████╔╝██║  ██║╚██████╔╝"
echo "╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ "
echo -e "${NC}"
echo -e "${PURPLE}🚀 KaliGhost Pro Professional Installation${NC}"
echo -e "${BLUE}===========================================${NC}"
echo ""

# Function to detect operating system
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v lsb_release &> /dev/null; then
            DISTRO=$(lsb_release -is)
            VERSION=$(lsb_release -rs)
            echo "linux-$DISTRO-$VERSION"
        else
            echo "linux-unknown"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos-$(sw_vers -productVersion)"
    else
        echo "unknown"
    fi
}

# Function to check if we're in the right directory
check_directory() {
    if [ ! -f "src/gui/pro_kalighost_main.py" ]; then
        echo -e "${RED}[ERROR] Professional GUI main file not found!${NC}"
        echo -e "${YELLOW}Please run this script from the KaliGhost root directory.${NC}"
        return 1
    fi
    echo -e "${GREEN}[OK] Professional GUI files located${NC}"
    return 0
}

# Function to setup virtual environment
setup_virtualenv() {
    echo -e "${BLUE}[+] Setting up professional virtual environment...${NC}"
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}[!] Creating virtual environment...${NC}"
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    echo -e "${BLUE}[+] Activating virtual environment...${NC}"
    source venv/bin/activate
    
    # Upgrade pip to latest version
    echo -e "${BLUE}[+] Upgrading pip...${NC}"
    pip install --upgrade pip
    
    echo -e "${GREEN}[✓] Virtual environment ready${NC}"
}

# Function to install system dependencies
install_system_deps() {
    echo -e "${BLUE}[+] Installing system dependencies...${NC}"
    
    OS_TYPE=$(detect_os)
    echo -e "${BLUE}[INFO] Detected OS: $OS_TYPE${NC}"
    
    case $OS_TYPE in
        linux-Kali*)
            echo -e "${YELLOW}[!] Installing Kali Linux dependencies...${NC}"
            sudo apt update
            sudo apt install -y \
                python3-pyside6.qtwidgets \
                python3-pyside6.qtcore \
                python3-pyside6.qtgui \
                python3-opengl \
                python3-opengl-accelerate \
                python3-numpy \
                python3-venv \
                libgl1-mesa-dev \
                libglu1-mesa-dev \
                build-essential \
                mesa-utils
            ;;
        linux-Ubuntu*|linux-Debian*)
            echo -e "${YELLOW}[!] Installing Ubuntu/Debian dependencies...${NC}"
            sudo apt update
            sudo apt install -y \
                python3-pyside6 \
                python3-opengl \
                python3-opengl-accelerate \
                python3-numpy \
                python3-venv \
                libgl1-mesa-dev \
                libglu1-mesa-dev \
                build-essential
            ;;
        macos*)
            echo -e "${YELLOW}[!] Installing macOS dependencies...${NC}"
            if ! command -v brew &> /dev/null; then
                echo -e "${RED}[ERROR] Homebrew not found. Please install Homebrew first:${NC}"
                echo -e "${YELLOW}/bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"${NC}"
                exit 1
            fi
            brew install python@3.9
            ;;
        *)
            echo -e "${YELLOW}[!] Unknown OS. Attempting generic installation...${NC}"
            ;;
    esac
    
    echo -e "${GREEN}[✓] System dependencies installed${NC}"
}

# Function to install Python dependencies
install_python_deps() {
    echo -e "${BLUE}[+] Installing Python dependencies...${NC}"
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install core dependencies
    echo -e "${YELLOW}[!] Installing core Python packages...${NC}"
    pip install --upgrade pip setuptools wheel
    
    # Install PySide6 with professional components
    echo -e "${YELLOW}[!] Installing PySide6 professional components...${NC}"
    pip install "PySide6>=6.5" PyOpenGL PyOpenGL-accelerate numpy
    
    # Verify installations
    echo -e "${BLUE}[+] Verifying Python dependencies...${NC}"
    python3 -c "import PySide6; print(f'PySide6 {PySide6.__version__} installed')"
    python3 -c "import OpenGL; print('PyOpenGL installed')"
    python3 -c "import numpy; print(f'NumPy {numpy.__version__} installed')"
    
    echo -e "${GREEN}[✓] Python dependencies installed and verified${NC}"
}

# Function to verify OpenGL availability
verify_opengl() {
    echo -e "${BLUE}[+] Verifying OpenGL capabilities...${NC}"
    
    source venv/bin/activate
    
    if python3 -c "from OpenGL.GL import *; from OpenGL.GLU import *; print('OpenGL core libraries available')" 2>/dev/null; then
        echo -e "${GREEN}[✓] OpenGL core libraries available${NC}"
        OPENGL_STATUS="FULL"
    elif python3 -c "import OpenGL; print('OpenGL basic libraries available')" 2>/dev/null; then
        echo -e "${YELLOW}[!] OpenGL basic libraries available (3D features may be limited)${NC}"
        OPENGL_STATUS="BASIC"
    else
        echo -e "${RED}[×] OpenGL libraries not available - falling back to 2D rendering${NC}"
        OPENGL_STATUS="NONE"
    fi
    
    echo -e "${BLUE}[INFO] OpenGL status: $OPENGL_STATUS${NC}"
}

# Function to setup macOS specific configurations
setup_macos_config() {
    OS_TYPE=$(detect_os)
    if [[ "$OS_TYPE" == "macos"* ]]; then
        echo -e "${BLUE}[+] Setting up macOS professional configuration...${NC}"
        export QT_MAC_WANTS_LAYER=1
        echo -e "${GREEN}[✓] QT_MAC_WANTS_LAYER=1${NC}"
        
        # Check if we have the right Python version
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        echo -e "${BLUE}[INFO] Python version: $PYTHON_VERSION${NC}"
    fi
}

# Function to create professional desktop entry (Linux)
create_desktop_entry() {
    OS_TYPE=$(detect_os)
    if [[ "$OS_TYPE" == "linux-"* ]]; then
        echo -e "${BLUE}[+] Creating professional desktop entry...${NC}"
        
        # Create desktop entry
        DESKTOP_FILE="$HOME/.local/share/applications/kalighost-pro.desktop"
        mkdir -p "$HOME/.local/share/applications"
        
        cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Name=KaliGhost Pro
Comment=Professional Pentesting Interface with 3D Dragon
Exec=$PWD/run_kalighost_pro.sh
Icon=applications-games
Terminal=false
Type=Application
Categories=Utility;Application;
EOF
        
        # Create run script
        cat > "run_kalighost_pro.sh" << EOF
#!/bin/bash
cd "$PWD"
source venv/bin/activate
export QT_MAC_WANTS_LAYER=1
python3 src/gui/pro_kalighost_main.py
EOF
        
        chmod +x "run_kalighost_pro.sh"
        
        echo -e "${GREEN}[✓] Desktop entry created: $DESKTOP_FILE${NC}"
        echo -e "${GREEN}[✓] Run script created: $PWD/run_kalighost_pro.sh${NC}"
    fi
}

# Function to run professional tests
run_professional_tests() {
    echo -e "${BLUE}[+] Running professional verification tests...${NC}"
    
    source venv/bin/activate
    
    # Test imports
    echo -e "${YELLOW}[!] Testing Python module imports...${NC}"
    python3 -c "
import sys
print('Python path:', sys.executable)

# Test core modules
try:
    import PySide6
    print('✓ PySide6 imported successfully')
except ImportError as e:
    print('× PySide6 import failed:', e)

try:
    import OpenGL
    print('✓ OpenGL imported successfully')
except ImportError as e:
    print('× OpenGL import failed:', e)

try:
    import numpy
    print('✓ NumPy imported successfully')
except ImportError as e:
    print('× NumPy import failed:', e)

print('All core modules tested')
"
    
    echo -e "${GREEN}[✓] Professional verification tests completed${NC}"
}

# Function to show professional usage instructions
show_usage_instructions() {
    echo ""
    echo -e "${CYAN}🎮 KaliGhost Pro Professional Usage Instructions${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo ""
    echo -e "${YELLOW}🚀 Starting KaliGhost Pro:${NC}"
    echo "   ./run_kalighost_pro.sh"
    echo "   or"
    echo "   cd src/gui && python3 pro_kalighost_main.py"
    echo ""
    echo -e "${YELLOW}🔧 Professional Features:${NC}"
    echo "   • 3D Dragon Interface with real-time animations"
    echo "   • Professional terminal with slash commands"
    echo "   • System monitoring dashboard"
    echo "   • Categorized pentesting tool palette"
    echo "   • Session management system"
    echo "   • Cyberpunk-themed professional UI"
    echo ""
    echo -e "${YELLOW}🎮 Mouse Controls:${NC}"
    echo "   • Left Click: Activate dragon"
    echo "   • Right Click: Show alert state"
    echo "   • Drag: Rotate 3D view"
    echo "   • Wheel: Zoom in/out"
    echo ""
    echo -e "${YELLOW}⌨️  Professional Commands:${NC}"
    echo "   • /help - Show help information"
    echo "   • /clear - Clear terminal"
    echo "   • /status - Show system status"
    echo "   • /scan <target> - Start network scan"
    echo ""
    echo -e "${GREEN}✅ Installation and setup complete!${NC}"
    echo -e "${BLUE}Thank you for choosing KaliGhost Professional!${NC}"
}

# Main installation function
main_installation() {
    echo -e "${CYAN}🚀 Starting KaliGhost Pro Professional Installation${NC}"
    echo -e "${BLUE}=====================================================${NC}"
    echo ""
    
    # Check directory
    if ! check_directory; then
        exit 1
    fi
    
    # Setup environment
    setup_virtualenv
    install_system_deps
    install_python_deps
    verify_opengl
    setup_macos_config
    create_desktop_entry
    run_professional_tests
    
    # Show completion message
    echo ""
    echo -e "${GREEN}🎉 KaliGhost Pro Professional Installation Complete!${NC}"
    echo -e "${BLUE}====================================================${NC}"
    
    show_usage_instructions
}

# Check if script is run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main_installation
fi