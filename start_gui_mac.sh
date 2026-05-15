#!/bin/bash

# Script para iniciar la GUI de KaliGhost directamente en MacOS

cd /Users/mrhardcore/KaliGhost/src/agent

# Verificar que estamos en el directorio correcto
echo "🔍 Directorío actual:"
pwd

# Verificar que main.py existe
echo "📁 Archivos en el directorio:"
ls -la main.py

# Instalar PySide6 si no está instalado
if ! python3 -c "import PySide6" &> /dev/null; then
    echo "
🔧 Instalando PySide6..."
    pip3 install --user PySide6
fi

# Iniciar la GUI
echo "
🚀 Iniciando GUI de KaliGhost..."
echo "Presiona Ctrl+C para salir..."

python3 main.py