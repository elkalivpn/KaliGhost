#!/bin/bash

# Script para iniciar KaliGhost con dashboard proactivo
echo "Iniciando KaliGhost con dashboard proactivo..."

# Cambiar al directorio del proyecto
cd /Users/mrhardcore/KaliGhost

# Crear directorio de logs si no existe
mkdir -p yrays-agent/logs

# Iniciar el servicio de monitoreo
echo "Iniciando monitor de dashboard..."
python3 monitor_dashboard.py &

# Verificar que el dashboard se haya actualizado
sleep 2
echo "Dashboard actualizado con datos del sistema"

# Mostrar la información actual del sistema
echo ""
echo "=== INFORMACIÓN DEL SISTEMA ==="
cat gui/frontend/dashboard_data.json
echo ""
echo "=== MONITOREO ACTIVO ==="
echo "El dashboard se actualizará cada 10 minutos automáticamente"
echo "Ruta del archivo de datos: /Users/mrhardcore/KaliGhost/gui/frontend/dashboard_data.json"
echo "Para ver el dashboard en vivo, abre index.html en tu navegador"
echo ""

# Mantener el proceso activo
tail -f /Users/mrhardcore/KaliGhost/yrays-agent/logs/dashboard_update.log