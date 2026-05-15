#!/bin/bash
# Script para instalar dependencias de la GUI de KaliGhost

set -e  # Salir inmediatamente si un comando falla

# Colores para salida
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner de bienvenida
echo -e "${BLUE}"
echo " ██╗  ██╗ █████╗ ██╗     ██╗ ██████╗ ██╗  ██╗ ██████╗ "
echo " ██║ ██╔╝██╔══██╗██║     ██║██╔════╝ ██║  ██║██╔═══██╗"
echo " █████╔╝ ███████║██║     ██║██║  ███╗███████║██║   ██║"
echo " ██╔═██╗ ██╔══██║██║     ██║██║   ██║██╔══██║██║   ██║"
echo " ██║  ██╗██║  ██║███████╗██║╚██████╔╝██║  ██║╚██████╔╝"
echo " ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ "
echo -e "${NC}"
echo -e "${YELLOW}Instalador de Dependencias para GUI de KaliGhost${NC}"
echo -e "${BLUE}==================================================${NC}"
echo ""

# Detectar sistema operativo
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS_TYPE="linux"
    if command -v apt &> /dev/null; then
        PACKAGE_MANAGER="apt"
    elif command -v yum &> /dev/null; then
        PACKAGE_MANAGER="yum"
    elif command -v pacman &> /dev/null; then
        PACKAGE_MANAGER="pacman"
    else
        PACKAGE_MANAGER="unknown"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS_TYPE="macos"
    if command -v brew &> /dev/null; then
        PACKAGE_MANAGER="brew"
    else
        PACKAGE_MANAGER="unknown"
    fi
else
    OS_TYPE="unknown"
    PACKAGE_MANAGER="unknown"
fi

echo -e "${BLUE}[INFO] Sistema detectado: $OS_TYPE${NC}"
echo -e "${BLUE}[INFO] Administrador de paquetes: $PACKAGE_MANAGER${NC}"
echo ""

# Verificar Python
echo -e "${BLUE}[+] Verificando Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}[✓] $PYTHON_VERSION encontrado${NC}"
else
    echo -e "${RED}[✗] Python 3 no encontrado${NC}"
    echo -e "${YELLOW}Por favor, instale Python 3 antes de continuar${NC}"
    exit 1
fi

# Verificar pip
echo -e "${BLUE}[+] Verificando pip...${NC}"
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}[✓] pip encontrado${NC}"
else
    echo -e "${YELLOW}[!] pip no encontrado, intentando instalar...${NC}"
    if [[ "$PACKAGE_MANAGER" == "apt" ]]; then
        sudo apt update
        sudo apt install -y python3-pip
    elif [[ "$PACKAGE_MANAGER" == "brew" ]]; then
        brew install python3
    fi
fi

# Lista de paquetes requeridos
REQUIRED_PACKAGES=(
    "PySide6"
    "PyOpenGL"
    "PyOpenGL_accelerate"
)

# Paquetes del sistema según OS
if [[ "$OS_TYPE" == "linux" ]]; then
    if [[ "$PACKAGE_MANAGER" == "apt" ]]; then
        SYSTEM_PACKAGES=(
            "python3-pyside6.qtwidgets"
            "python3-opengl"
            "python3-dev"
            "build-essential"
            "libgl1-mesa-dev"
            "libglu1-mesa-dev"
        )
    elif [[ "$PACKAGE_MANAGER" == "yum" ]]; then
        SYSTEM_PACKAGES=(
            "python3-pyside6"
            "python3-opengl"
            "python3-devel"
            "gcc"
            "make"
            "mesa-libGL-devel"
            "mesa-libGLU-devel"
        )
    fi
elif [[ "$OS_TYPE" == "macos" ]]; then
    SYSTEM_PACKAGES=(
        "python@3.9"
    )
fi

# Instalar paquetes del sistema si es necesario
if [[ "$OS_TYPE" == "linux" ]] && [[ ${#SYSTEM_PACKAGES[@]} -gt 0 ]]; then
    echo ""
    echo -e "${BLUE}[+] Verificando paquetes del sistema...${NC}"
    
    for package in "${SYSTEM_PACKAGES[@]}"; do
        # Esta verificación es simplificada, en la práctica sería más compleja
        echo -e "${YELLOW}[!] Instalando $package${NC}"
        if [[ "$PACKAGE_MANAGER" == "apt" ]]; then
            sudo apt install -y "$package"
        elif [[ "$PACKAGE_MANAGER" == "yum" ]]; then
            sudo yum install -y "$package"
        fi
    done
fi

# Verificar paquetes Python instalados
echo ""
echo -e "${BLUE}[+] Verificando paquetes Python...${NC}"
MISSING_PACKAGES=()

for package in "${REQUIRED_PACKAGES[@]}"; do
    if python3 -c "import $package" &> /dev/null; then
        echo -e "${GREEN}[✓] $package ya está instalado${NC}"
    else
        echo -e "${YELLOW}[!] $package no encontrado${NC}"
        MISSING_PACKAGES+=("$package")
    fi
done

# Instalar paquetes faltantes
if [ ${#MISSING_PACKAGES[@]} -ne 0 ]; then
    echo ""
    echo -e "${BLUE}[+] Instalando paquetes faltantes...${NC}"
    
    for package in "${MISSING_PACKAGES[@]}"; do
        echo -e "${YELLOW}[!] Instalando $package${NC}"
        pip3 install "$package"
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}[✓] $package instalado correctamente${NC}"
        else
            echo -e "${RED}[✗] Error instalando $package${NC}"
        fi
    done
else
    echo -e "${GREEN}[✓] Todos los paquetes Python están instalados${NC}"
fi

# Verificación final
echo ""
echo -e "${BLUE}[+] Verificando instalación completa...${NC}"

ALL_INSTALLED=true
for package in "${REQUIRED_PACKAGES[@]}"; do
    if ! python3 -c "import $package" &> /dev/null; then
        echo -e "${RED}[✗] $package no se pudo importar${NC}"
        ALL_INSTALLED=false
    fi
done

if [ "$ALL_INSTALLED" = true ]; then
    echo -e "${GREEN}[✓] ¡Todas las dependencias instaladas correctamente!${NC}"
    echo ""
    echo -e "${BLUE}Para iniciar la GUI:${NC}"
    echo -e "  cd $(pwd)/.."
    echo -e "  ./gui/start_gui.sh"
    echo ""
    echo -e "${BLUE}O directamente:${NC}"
    echo -e "  python3 $(pwd)/dragon_3d_gui.py"
else
    echo -e "${RED}[✗] Algunas dependencias no se pudieron instalar${NC}"
    echo -e "${YELLOW}Consulte los errores anteriores para más información${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 Instalación completada exitosamente${NC}"
echo -e "${BLUE}Disfrute de la GUI de KaliGhost con el dragón 3D animado${NC}"