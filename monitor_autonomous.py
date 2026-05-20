#!/usr/bin/env python3
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
            
    except ImportError:
        print("⚠️ psutil no disponible, monitoreo limitado")
        print("💡 Instala psutil con: pip install psutil")
        time.sleep(30)  # Esperar más tiempo sin psutil
    except KeyboardInterrupt:
        print("\n👋 Monitoreo detenido")
    except Exception as e:
        print(f"❌ Error en monitoreo: {e}")

if __name__ == "__main__":
    monitor_system()
