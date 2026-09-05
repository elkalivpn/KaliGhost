# KaliGhost IDE - Installation Script
# Automated installation for Kali Linux and Tails OS

#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
INSTALL_DIR="${INSTALL_DIR:-/opt/kalighost}"
PYTHON_VERSION="3.11"
KALIGHOST_USER="${SUDO_USER:-$USER}"

echo -e "${BLUE}"
cat << 'EOF'
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗            ║
    ║   ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝            ║
    ║   ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗            ║
    ║   ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║            ║
    ║   ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║            ║
    ║   ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝            ║
    ║                                                           ║
    ║              Installation Script v1.0.0                   ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}This script must be run as root${NC}"
   exit 1
fi

# Detect OS
detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
    else
        echo -e "${RED}Cannot detect OS${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}Detected: $OS $VER${NC}"
}

# Check requirements
check_requirements() {
    echo -e "${YELLOW}Checking requirements...${NC}"
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}Python 3 not found${NC}"
        return 1
    fi
    
    PYTHON_VER=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    if (( $(echo "$PYTHON_VER < 3.10" | bc -l) )); then
        echo -e "${RED}Python 3.10+ required (found: $PYTHON_VER)${NC}"
        return 1
    fi
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${YELLOW}Docker not found, will install${NC}"
        INSTALL_DOCKER=true
    fi
    
    # Check Git
    if ! command -v git &> /dev/null; then
        echo -e "${YELLOW}Git not found, will install${NC}"
        INSTALL_GIT=true
    fi
    
    echo -e "${GREEN}Requirements check complete${NC}"
}

# Install dependencies
install_dependencies() {
    echo -e "${YELLOW}Installing system dependencies...${NC}"
    
    apt-get update
    
    # Install Python and pip
    apt-get install -y \
        python3 \
        python3-pip \
        python3-venv \
        python3-dev
    
    # Install Git if needed
    if [ "$INSTALL_GIT" = true ]; then
        apt-get install -y git
    fi
    
    # Install Docker if needed
    if [ "$INSTALL_DOCKER" = true ]; then
        echo -e "${YELLOW}Installing Docker...${NC}"
        curl -fsSL https://get.docker.com | sh
        systemctl enable docker
        systemctl start docker
    fi
    
    # Install security tools
    apt-get install -y \
        nmap \
        netcat-traditional \
        tcpdump \
        wireshark-common \
        tshark \
        radare2 \
        gdb \
        file \
        binutils || true
    
    echo -e "${GREEN}Dependencies installed${NC}"
}

# Create user and group
setup_user() {
    echo -e "${YELLOW}Setting up user permissions...${NC}"
    
    # Add user to docker group
    usermod -aG docker $KALIGHOST_USER 2>/dev/null || true
    
    echo -e "${GREEN}User setup complete${NC}"
}

# Install application
install_application() {
    echo -e "${YELLOW}Installing KaliGhost IDE...${NC}"
    
    # Create installation directory
    mkdir -p $INSTALL_DIR
    cd $INSTALL_DIR
    
    # Copy files if running from source
    if [ -d "/workspace" ]; then
        cp -r /workspace/* $INSTALL_DIR/
    fi
    
    # Create virtual environment
    python3 -m venv venv
    source venv/bin/activate
    
    # Install Python dependencies
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Set permissions
    chown -R $KALIGHOST_USER:$KALIGHOST_USER $INSTALL_DIR
    chmod +x kalighost.py
    
    # Create systemd service
    cat > /etc/systemd/system/kalighost.service << 'EOSERVICE'
[Unit]
Description=KaliGhost IDE
After=network.target docker.service
Requires=docker.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/kalighost
Environment=PATH=/opt/kalighost/venv/bin
ExecStart=/opt/kalighost/venv/bin/python /opt/kalighost/kalighost.py start --headless
Restart=always

[Install]
WantedBy=multi-user.target
EOSERVICE
    
    systemctl daemon-reload
    systemctl enable kalighost
    
    echo -e "${GREEN}Application installed${NC}"
}

# Post-installation
post_install() {
    echo -e "${GREEN}"
    cat << 'EOF'

    ╔═══════════════════════════════════════════════════════════╗
    ║                    Installation Complete!                 ║
    ╚═══════════════════════════════════════════════════════════╝

    Next steps:

    1. Start KaliGhost IDE:
       sudo systemctl start kalighost

    2. Check status:
       sudo systemctl status kalighost

    3. Access web interface:
       http://localhost:8080

    4. CLI usage:
       cd /opt/kalighost
       ./kalighost.py --help

    Documentation: /opt/kalighost/docs/

    For support: https://github.com/kalighost/ide/issues

EOF
    echo -e "${NC}"
}

# Main execution
main() {
    detect_os
    check_requirements
    install_dependencies
    setup_user
    install_application
    post_install
}

# Parse arguments
while getopts "d:h" opt; do
    case $opt in
        d)
            INSTALL_DIR=$OPTARG
            ;;
        h)
            echo "Usage: $0 [-d installation_dir]"
            exit 0
            ;;
        \?)
            echo "Invalid option: -$OPTARG"
            exit 1
            ;;
    esac
done

main
