#!/bin/bash
"""
Script de inicio de la GUI de KaliGhost
"""

set -e

KALIGHOST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GUI_DIR="$KALIGHOST_DIR/gui"

# Verificar dependencias
if ! command -v python3 &> /dev/null; then
    echo "[!] Python3 no está instalado"
    exit 1
fi

if ! python3 -c "from PySide6 import QtWidgets" &> /dev/null; then
    echo "[!] PySide6 no está instalado. Instálalo con: pip install PySide6"
    exit 1
fi

# Iniciar GUI
echo "🚀 Iniciando GUI de KaliGhost..."
cd "$GUI_DIR"
python3 main.py

# Si falla, intentar con ruta absoluta
if [ $? -ne 0 ]; then
    echo "[!] Error al iniciar la GUI. Verifica que PySide6 esté instalado."
    echo "    Instalación: pip install PySide6"
    exit 1
fi