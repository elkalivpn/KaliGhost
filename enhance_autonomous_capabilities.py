#!/usr/bin/env python3
"""
Script de mejora de capacidades autónomas para KaliGhost
"""

import sys
import os
import json
import time
import logging
from pathlib import Path
from datetime import datetime, timedelta

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/kalighost_autonomous_enhancement.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def enhance_autonomous_profiles():
    """Mejora los perfiles autónomos existentes y crea nuevos"""
    logger.info("Mejorando perfiles autónomos...")
    
    profiles_dir = Path("yrays-agent/profiles")
    profiles_dir.mkdir(exist_ok=True)
    
    # Perfil avanzado de monitoreo continuo
    continuous_profile = {
        "name": "continuo",
        "mode": "continuous",
        "description": "Modo de monitoreo continuo con alertas proactivas",
        "settings": {
            "scan_intensity": "low",
            "execution_speed": "normal",
            "resource_usage": "low",
            "alert_sensitivity": "high",
            "network_activity": "normal",
            "tool_timeout": 300,
            "max_parallel_scans": 2,
            "retry_attempts": 3,
            "log_level": "INFO",
            "continuous_monitoring": True,
            "alert_thresholds": {
                "cpu": 80,
                "memory": 85,
                "disk": 90
            }
        }
    }
    
    # Perfil de respuesta rápida a incidentes
    incident_profile = {
        "name": "incidente",
        "mode": "incident_response",
        "description": "Modo de respuesta rápida a incidentes de seguridad",
        "settings": {
            "scan_intensity": "high",
            "execution_speed": "fast",
            "resource_usage": "high",
            "alert_sensitivity": "critical",
            "network_activity": "high",
            "tool_timeout": 120,
            "max_parallel_scans": 5,
            "retry_attempts": 2,
            "log_level": "ERROR",
            "incident_response": True,
            "auto_isolate": True,
            "notify_external": True
        }
    }
    
    # Guardar perfiles mejorados
    continuous_file = profiles_dir / "continuo.json"
    with open(continuous_file, 'w') as f:
        json.dump(continuous_profile, f, indent=2)
    logger.info(f"Perfil 'continuo' creado: {continuous_file}")
    
    incident_file = profiles_dir / "incidente.json"
    with open(incident_file, 'w') as f:
        json.dump(incident_profile, f, indent=2)
    logger.info(f"Perfil 'incidente' creado: {incident_file}")

def setup_enhanced_scheduled_tasks():
    """Configura tareas programadas mejoradas"""
    logger.info("Configurando tareas programadas mejoradas...")
    
    tasks_dir = Path("yrays-agent/data")
    tasks_dir.mkdir(exist_ok=True)
    
    tasks_file = tasks_dir / "scheduled_tasks.json"
    
    # Tareas programadas mejoradas
    enhanced_tasks = [
        {
            "id": "daily_quick_scan",
            "name": "Escaneo rápido diario",
            "schedule": "0 8 * * *",
            "profile": "equilibrado",
            "targets": ["localhost"],
            "type": "quick_scan",
            "enabled": True,
            "last_run": None,
            "next_run": None
        },
        {
            "id": "weekly_deep_scan",
            "name": "Escaneo profundo semanal",
            "schedule": "0 2 * * 0",
            "profile": "sigiloso",
            "targets": ["localhost"],
            "type": "deep_scan",
            "enabled": True,
            "last_run": None,
            "next_run": None
        },
        {
            "id": "continuous_monitoring",
            "name": "Monitoreo continuo",
            "schedule": "*/5 * * * *",
            "profile": "continuo",
            "targets": ["localhost"],
            "type": "monitoring",
            "enabled": True,
            "last_run": None,
            "next_run": None
        },
        {
            "id": "monthly_vulnerability_assessment",
            "name": "Evaluación mensual de vulnerabilidades",
            "schedule": "0 3 1 * *",
            "profile": "agresivo",
            "targets": ["localhost"],
            "type": "vulnerability_assessment",
            "enabled": True,
            "last_run": None,
            "next_run": None
        }
    ]
    
    # Guardar tareas programadas
    with open(tasks_file, 'w') as f:
        json.dump(enhanced_tasks, f, indent=2)
    logger.info(f"Tareas programadas mejoradas guardadas: {tasks_file}")

def enhance_monitoring_script():
    """Mejora el script de monitoreo con alertas proactivas"""
    logger.info("Mejorando script de monitoreo...")
    
    enhanced_monitor_script = '''#!/usr/bin/env python3
"""
Script de monitoreo mejorado del sistema autónomo de YrYs-Agent
"""

import sys
import os
import time
import json
import logging
from pathlib import Path
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('yrays-agent/logs/monitor.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def send_alert(message, level="INFO"):
    """Enviar alerta (simulación)"""
    logger.log(getattr(logging, level), f"[ALERTA] {message}")
    # En producción, esto podría enviar notificaciones por Telegram, correo, etc.

def check_system_resources():
    """Verificar recursos del sistema"""
    try:
        import psutil
        
        # Obtener estadísticas del sistema
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Verificar umbrales
        alerts = []
        
        if cpu_percent > 80:
            alerts.append(f"Alto uso de CPU: {cpu_percent:.1f}%")
            
        if memory.percent > 85:
            alerts.append(f"Alto uso de memoria: {memory.percent:.1f}%")
            
        disk_usage_percent = (disk.used / disk.total) * 100
        if disk_usage_percent > 90:
            alerts.append(f"Alto uso de disco: {disk_usage_percent:.1f}%")
            
        # Enviar alertas si es necesario
        for alert in alerts:
            send_alert(alert, "WARNING" if "Alto" in alert else "ERROR")
            
        return {
            "cpu": cpu_percent,
            "memory": memory.percent,
            "disk": disk_usage_percent,
            "alerts": alerts
        }
        
    except ImportError:
        logger.warning("psutil no disponible, monitoreo limitado")
        return {"error": "psutil_not_available"}

def monitor_system():
    """Monitorea el estado del sistema"""
    logger.info("👀 Monitoreando sistema autónomo de YrYs-Agent...")
    
    # Directorios a monitorear
    monitored_dirs = [
        "yrays-agent/logs",
        "yrays-agent/skills",
        "yrays-agent/profiles"
    ]
    
    # Archivos a monitorear
    monitored_files = [
        "yrays-agent/logs/yrays.log",
        "yrays-agent/data/scheduled_tasks.json"
    ]
    
    try:
        while True:
            # Verificar recursos del sistema
            resources = check_system_resources()
            
            if "error" not in resources:
                logger.info(f"  CPU: {resources['cpu']:.1f}% | Memoria: {resources['memory']:.1f}% | Disco: {resources['disk']:.1f}%")
                
                # Verificar alertas
                if resources['alerts']:
                    for alert in resources['alerts']:
                        logger.warning(alert)
            
            # Verificar tamaño de logs
            log_file = Path("yrays-agent/logs/yrays.log")
            if log_file.exists():
                size_mb = log_file.stat().st_size / (1024 * 1024)
                if size_mb > 50:
                    send_alert(f"Log grande: {size_mb:.1f}MB - Considerar rotación", "WARNING")
                    
            # Esperar antes de la próxima verificación
            time.sleep(60)
            
    except KeyboardInterrupt:
        logger.info("\\n👋 Monitoreo detenido")
    except Exception as e:
        logger.error(f"❌ Error en monitoreo: {e}")

if __name__ == "__main__":
    monitor_system()
'''
    
    # Guardar script mejorado
    script_path = Path("monitor_autonomous_enhanced.py")
    with open(script_path, 'w') as f:
        f.write(enhanced_monitor_script)
    
    # Hacer ejecutable
    script_path.chmod(0o755)
    logger.info(f"Script de monitoreo mejorado creado: {script_path}")

def enhance_autonomous_startup():
    """Mejora el script de inicio autónomo"""
    logger.info("Mejorando script de inicio autónomo...")
    
    enhanced_startup_script = '''#!/bin/bash
# Script de inicio mejorado para el sistema autónomo de YrYs-Agent

echo "🚀 Iniciando sistema autónomo de YrYs-Agent..."

# Cambiar al directorio del proyecto
cd "$(dirname "$0")"

# Activar virtual environment si existe
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "🐍 Virtual environment activado"
fi

# Verificar si psutil está instalado
if ! python3 -c "import psutil" 2>/dev/null; then
    echo "⚠️ psutil no encontrado, instalando..."
    pip install psutil
fi

# Crear directorios necesarios
mkdir -p yrays-agent/logs yrays-agent/skills yrays-agent/profiles yrays-agent/data

# Iniciar el agente en modo autónomo
echo "🤖 Iniciando YrYs-Agent en modo autónomo..."
python3 yrays-agent/yrays.py "modo_autonomo" &

# Guardar PID del proceso
echo $! > /tmp/yrays_agent.pid

# Iniciar monitoreo en segundo plano
echo "👀 Iniciando monitoreo..."
python3 monitor_autonomous_enhanced.py &

echo "✅ Sistema autónomo iniciado"
echo "📄 Logs disponibles en yrays-agent/logs/"
'''
    
    # Guardar script mejorado
    script_path = Path("start_autonomous_enhanced.sh")
    with open(script_path, 'w') as f:
        f.write(enhanced_startup_script)
    
    # Hacer ejecutable
    script_path.chmod(0o755)
    logger.info(f"Script de inicio autónomo mejorado creado: {script_path}")

def main():
    """Función principal para ejecutar todas las mejoras"""
    logger.info("🔧 Iniciando mejora de capacidades autónomas de KaliGhost...")
    
    try:
        # Verificar que estamos en el directorio correcto
        if not Path("yrays-agent/yrays.py").exists():
            logger.error("❌ No se encontró el directorio yrays-agent. Ejecute este script desde el directorio raíz de KaliGhost.")
            return False
            
        # Implementar mejoras
        enhance_autonomous_profiles()
        setup_enhanced_scheduled_tasks()
        enhance_monitoring_script()
        enhance_autonomous_startup()
        
        logger.info("🎉 Mejoras de capacidades autónomas completadas exitosamente!")
        logger.info("📝 Para iniciar el sistema mejorado:")
        logger.info("   ./start_autonomous_enhanced.sh")
        logger.info("📊 Para monitorear el sistema:")
        logger.info("   python3 monitor_autonomous_enhanced.py")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error durante la mejora de capacidades autónomas: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)