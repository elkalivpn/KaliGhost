#!/bin/bash
# Script de inicio para el sistema autónomo de YrYs-Agent

echo "🚀 Iniciando sistema autónomo de YrYs-Agent..."

# Cambiar al directorio del proyecto
cd "$(dirname "$0")"

# Activar virtual environment si existe
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "🐍 Virtual environment activado"
fi

# Iniciar el agente en modo autónomo
echo "🤖 Iniciando YrYs-Agent en modo autónomo..."
python3 yrays-agent/yrays.py "modo_autonomo"

echo "✅ Sistema autónomo iniciado"
