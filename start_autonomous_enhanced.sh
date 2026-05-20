#!/bin/bash

# Script de inicio mejorado para monitoreo proactivo de KaliGhost
# Este script inicia el sistema de monitoreo proactivo junto con otros servicios

set -e

echo "Iniciando sistema de monitoreo proactivo para KaliGhost..."

# Definir colores para salida
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para mostrar mensaje con color
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar si el entorno virtual está activo
if [ -z "$VIRTUAL_ENV" ]; then
    print_warning "El entorno virtual no está activo, intentando activarlo..."
    source ~/KaliGhost/venv_kalighost/bin/activate
fi

# Verificar si los directorios necesarios existen
if [ ! -d "~/KaliGhost/yrays-agent/data" ]; then
    mkdir -p ~/KaliGhost/yrays-agent/data
    print_status "Directorio de datos creado"
fi

if [ ! -d "~/KaliGhost/yrays-agent/logs" ]; then
    mkdir -p ~/KaliGhost/yrays-agent/logs
    print_status "Directorio de logs creado"
fi

# Verificar que el script de monitoreo existe
if [ ! -f "~/KaliGhost/monitor_autonomous_enhanced.py" ]; then
    print_error "No se encontró el script de monitoreo proactivo"
    exit 1
fi

# Establecer permisos de ejecución
chmod +x ~/KaliGhost/monitor_autonomous_enhanced.py
chmod +x ~/KaliGhost/start_autonomous_enhanced.sh

# Verificar que psutil está instalado
if ! python3 -c "import psutil" >/dev/null 2>&1; then
    print_warning "psutil no está instalado, intentando instalar..."
    pip3 install psutil
fi

# Iniciar monitoreo proactivo en segundo plano
print_status "Iniciando monitoreo proactivo..."
python3 ~/KaliGhost/monitor_autonomous_enhanced.py &

print_status "Sistema de monitoreo proactivo iniciado correctamente"

# Mostrar información de versión del sistema
echo ""
print_status "Información del sistema:"
python3 -c "
import platform
import psutil
print(f'Plataforma: {platform.platform()}')
print(f'CPU: {psutil.cpu_count(logical=True)} núcleos')
print(f'Memoria total: {round(psutil.virtual_memory().total / (1024**3), 2)} GB')
print(f'Procesos activos: {len(psutil.pids())}')
"

echo ""
echo "Para ver logs de monitoreo:"
echo "tail -f ~/KaliGhost/yrays-agent/logs/monitoring.log"
echo ""
echo "Para detener el monitoreo:"
echo "kill \$(pgrep -f monitor_autonomous_enhanced.py)"
echo ""
echo "Para reiniciar monitoreo:"
echo "pkill -f monitor_autonomous_enhanced.py && ~/KaliGhost/start_autonomous_enhanced.sh"