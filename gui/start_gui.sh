#!/bin/bash
# Script para iniciar la GUI de KaliGhost con el dragón 3D

# Directorio base
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GUI_DIR="$BASE_DIR/gui"

# Verificar que existe el entorno virtual
if [ -d "$BASE_DIR/venv" ]; then
    echo "[$] Activando entorno virtual..."
    source "$BASE_DIR/venv/bin/activate"
else
    echo "[!] No se encontró entorno virtual, usando Python del sistema"
fi

# Verificar dependencias
echo "[$] Verificando dependencias..."

REQUIRED_PACKAGES=("PySide6" "PyOpenGL" "PyOpenGL_accelerate")
MISSING_PACKAGES=()

for package in "${REQUIRED_PACKAGES[@]}"; do
    if ! python3 -c "import $package" &> /dev/null; then
        MISSING_PACKAGES+=("$package")
    fi
done

if [ ${#MISSING_PACKAGES[@]} -ne 0 ]; then
    echo "[!] Faltan paquetes requeridos: ${MISSING_PACKAGES[*]}"
    echo "[$] Instalando dependencias..."
    
    # Intentar instalar con pip
    pip3 install PySide6 PyOpenGL PyOpenGL_accelerate
    
    if [ $? -ne 0 ]; then
        echo "[!] Error instalando dependencias. Intentando con apt..."
        sudo apt update
        sudo apt install -y python3-pyside6.qtwidgets python3-pyside6.qtcore python3-opengl
    fi
fi

# Cambiar al directorio de la GUI
cd "$GUI_DIR"

# Iniciar la GUI
echo "[$] Iniciando KaliGhost GUI con Dragón 3D..."
echo "[$] Presiona Ctrl+C para salir"
python3 dragon_3d_gui.py