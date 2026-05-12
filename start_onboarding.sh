#!/bin/bash
"""
Script de inicio de KaliGhost
Ejecuta el onboarding si es la primera vez
"""

set -e  # Salir si hay errores

KALIGHOST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ONBOARDING_DONE_FLAG="$KALIGHOST_DIR/.onboarding_completed"

if [[ ! -f "$ONBOARDING_DONE_FLAG" ]]; then
    echo ""
    echo "🚀 ¡Bienvenido a KaliGhost! Iniciando el asistente de configuración..."
    echo ""
    
    cd "$KALIGHOST_DIR/onboarding"
    
    # Asegurar permisos
    chmod +x wizard.py
    
    # Ejecutar onboarding
    python3 wizard.py
    
    # Verificar que se completó
    if [[ ! -f "$ONBOARDING_DONE_FLAG" ]]; then
        echo ""
        echo "[!] El onboarding no se completó. Reinicia cuando estés listo."
        exit 1
    fi
else
    echo ""
    echo "✅ KaliGhost ya está configurado."
    echo "🚀 Para iniciar el agente: cd KaliGhost && python3 YrYs-Agent/main.py"
    echo ""
fi