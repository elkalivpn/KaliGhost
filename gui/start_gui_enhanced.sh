#!/bin/bash
# Script mejorado para iniciar la GUI de KaliGhost

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Iniciando KaliGhost GUI${NC}"
echo -e "${BLUE}========================${NC}"

# Verificar que estamos en el directorio correcto
if [ ! -d "gui" ]; then
    echo -e "${RED}[ERROR] No se encuentra el directorio 'gui'. Por favor ejecuta este script desde el directorio raíz de KaliGhost.${NC}"
    exit 1
fi

# Verificar dependencias de Python
echo -e "${BLUE}[+] Verificando dependencias...${NC}"

MISSING_DEPS=()

# Verificar PySide6
if python3 -c "import PySide6" &> /dev/null; then
    PYSIDE_VERSION=$(python3 -c "import PySide6; print(PySide6.__version__)")
    echo -e "${GREEN}[✓] PySide6 $PYSIDE_VERSION encontrado${NC}"
else
    echo -e "${RED}[✗] PySide6 no encontrado${NC}"
    MISSING_DEPS+=("PySide6")
fi

# Verificar OpenGL
if python3 -c "import OpenGL" &> /dev/null; then
    echo -e "${GREEN}[✓] PyOpenGL encontrado${NC}"
else
    echo -e "${YELLOW}[!] PyOpenGL no encontrado - se usará modo 2D${NC}"
fi

# Si faltan dependencias críticas, intentar instalarlas
if [ ${#MISSING_DEPS[@]} -ne 0 ]; then
    echo -e "${YELLOW}[!] Instalando dependencias faltantes...${NC}"
    
    # Intentar instalar en virtual environment
    if [ -d "venv" ]; then
        source venv/bin/activate
        pip install "${MISSING_DEPS[@]}"
    else
        # Si estamos en macOS con Homebrew, usar --user
        if [[ "$OSTYPE" == "darwin"* ]]; then
            pip3 install --user "${MISSING_DEPS[@]}"
        else
            pip3 install "${MISSING_DEPS[@]}"
        fi
    fi
fi

# Iniciar la GUI
echo -e "${BLUE}[+] Iniciando GUI...${NC}"
echo -e "${YELLOW}💡 La ventana de KaliGhost debería aparecer en unos momentos${NC}"
echo -e "${YELLOW}💡 Cierra la ventana o presiona Ctrl+C para salir${NC}"

# Cambiar al directorio de la GUI
cd gui

# Ejecutar la GUI
python3 dragon_3d_gui.py

echo -e "${GREEN}👋 ¡Hasta pronto!${NC}"