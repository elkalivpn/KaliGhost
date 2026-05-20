#!/usr/bin/env python3
"""
Script de inicialización y configuración del sistema autónomo de YrYs-Agent
"""

import sys
import os
import subprocess
import logging
import json
from pathlib import Path

def setup_autonomous_system():
    """Configura el sistema autónomo"""
    print("🔧 Configurando sistema autónomo de YrYs-Agent...")
    
    # Directorios necesarios
    dirs_to_create = [
        "yrays-agent/logs",
        "yrays-agent/skills",
        "yrays-agent/profiles",
        "yrays-agent/data"
    ]
    
    for dir_path in dirs_to_create:
        full_path = Path(dir_path)
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"📁 Directorio creado: {dir_path}")
    
    # Verificar dependencias
    required_packages = [
        "psutil",      # Para monitoreo del sistema
        "schedule",    # Para programación de tareas (opcional)
        "sqlite3"      # Para persistencia (ya viene con Python)
    ]
    
    print("📦 Verificando dependencias...")
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} disponible")
        except ImportError:
            print(f"⚠️ {package} no encontrado, intentando instalar...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} instalado correctamente")
            except subprocess.CalledProcessError:
                print(f"❌ Error al instalar {package}")
    
    # Crear perfiles predeterminados
    print("👤 Creando perfiles predeterminados...")
    create_default_profiles()
    
    # Crear tareas de ejemplo
    print("🕒 Creando tareas de ejemplo...")
    create_example_tasks()
    
    print("✅ Sistema autónomo configurado correctamente")

def create_default_profiles():
    """Crea perfiles predeterminados"""
    profiles_dir = Path("yrays-agent/profiles")
    profiles_dir.mkdir(exist_ok=True)
    
    default_profiles = [
        {
            "name": "sigiloso",
            "mode": "stealth",
            "description": "Modo de bajo impacto y sigilo",
            "settings": {
                "scan_intensity": "low",
                "execution_speed": "slow",
                "resource_usage": "low",
                "alert_sensitivity": "high",
                "network_activity": "low",
                "tool_timeout": 600,
                "max_parallel_scans": 1,
                "retry_attempts": 5,
                "log_level": "DEBUG"
            }
        },
        {
            "name": "agresivo",
            "mode": "aggressive",
            "description": "Modo de exploración exhaustiva",
            "settings": {
                "scan_intensity": "high",
                "execution_speed": "fast",
                "resource_usage": "high",
                "alert_sensitivity": "low",
                "network_activity": "high",
                "tool_timeout": 180,
                "max_parallel_scans": 10,
                "retry_attempts": 1,
                "log_level": "WARNING"
            }
        },
        {
            "name": "equilibrado",
            "mode": "balanced",
            "description": "Modo de comportamiento equilibrado",
            "settings": {
                "scan_intensity": "normal",
                "execution_speed": "normal",
                "resource_usage": "moderate",
                "alert_sensitivity": "medium",
                "network_activity": "normal",
                "tool_timeout": 300,
                "max_parallel_scans": 3,
                "retry_attempts": 3,
                "log_level": "INFO"
            }
        }
    ]
    
    import json
    for profile in default_profiles:
        profile_file = profiles_dir / f"{profile['name']}.json"
        with open(profile_file, 'w') as f:
            json.dump(profile, f, indent=2)
        print(f"  • Perfil '{profile['name']}' creado")

def create_example_tasks():
    """Crea tareas de ejemplo"""
    tasks_dir = Path("yrays-agent/data")
    tasks_dir.mkdir(exist_ok=True)
    
    # Este archivo se usará para almacenar tareas programadas
    tasks_file = tasks_dir / "scheduled_tasks.json"
    if not tasks_file.exists():
        with open(tasks_file, 'w') as f:
            json.dump([], f)
        print("  • Archivo de tareas creado")

def create_startup_script():
    """Crea un script de inicio para el sistema autónomo"""
    startup_script = '''#!/bin/bash
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
'''
    
    script_path = Path("start_autonomous.sh")
    with open(script_path, 'w') as f:
        f.write(startup_script)
    
    # Hacer el script ejecutable
    script_path.chmod(0o755)
    print(f"  • Script de inicio creado: {script_path}")

def create_monitoring_script():
    """Crea un script de monitoreo del sistema"""
    monitoring_script = '''#!/usr/bin/env python3
"""
Script de monitoreo del sistema autónomo de YrYs-Agent
"""

import sys
import os
import time
import json
from pathlib import Path

def monitor_system():
    """Monitorea el estado del sistema"""
    print("👀 Monitoreando sistema autónomo de YrYs-Agent...")
    
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
        import psutil
        print("📈 Monitoreo de recursos del sistema:")
        
        while True:
            # CPU y memoria
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            print(f"  CPU: {cpu_percent:.1f}% | Memoria: {memory.percent:.1f}%")
            
            # Verificar tamaño de logs
            log_file = Path("yrays-agent/logs/yrays.log")
            if log_file.exists():
                size_mb = log_file.stat().st_size / (1024 * 1024)
                if size_mb > 10:
                    print(f"  ⚠️ Log grande: {size_mb:.1f}MB")
            
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\\n👋 Monitoreo detenido")
    except Exception as e:
        print(f"❌ Error en monitoreo: {e}")

if __name__ == "__main__":
    monitor_system()
'''
    
    script_path = Path("monitor_autonomous.py")
    with open(script_path, 'w') as f:
        f.write(monitoring_script)
    
    print(f"  • Script de monitoreo creado: {script_path}")

if __name__ == "__main__":
    print("🔧 Inicializando sistema autónomo de YrYs-Agent...")
    setup_autonomous_system()
    create_startup_script()
    create_monitoring_script()
    print("🎉 Inicialización completada")