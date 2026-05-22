#!/usr/bin/env python3
"""
Script para actualizar los datos del dashboard de KaliGhost cada 10 minutos.
Este script recopila métricas del sistema, procesos, logs y otros datos relevantes
para mantener el dashboard actualizado con información en tiempo real.
"""

import psutil
import time
import json
import logging
import os
import sys
from datetime import datetime
from typing import Dict, Any

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/Users/mrhardcore/KaliGhost/yrays-agent/logs/dashboard_update.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def get_system_metrics() -> Dict[str, Any]:
    """Obtener métricas actuales del sistema"""
    metrics = {}
    
    try:
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        metrics['cpu'] = cpu_percent
        
        # Memoria
        memory = psutil.virtual_memory()
        metrics['memory'] = memory.percent
        
        # Disco
        disk = psutil.disk_usage('/')
        metrics['disk'] = (disk.used / disk.total) * 100
        
        # Carga promedio del sistema (Linux/macOS)
        try:
            load_avg = os.getloadavg()
            metrics['load_average'] = load_avg[0]  # Carga a 1 minuto
        except:
            metrics['load_average'] = 0
            
        # Número de procesos
        metrics['processes'] = len(psutil.pids())
        
        # Procesos de KaliGhost
        kali_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                if 'kalighost' in proc.info['name'].lower():
                    kali_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'username': proc.info['username']
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        metrics['kalighost_processes'] = kali_processes
        
        # Tiempo de actividad del sistema
        metrics['uptime'] = time.time() - psutil.boot_time()
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error obteniendo métricas del sistema: {e}")
        return {}

def get_agent_status() -> Dict[str, Any]:
    """Obtener estado de los agentes autonomos"""
    status = {}
    
    try:
        # Verificar procesos de agentes
        agent_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                if any(agent_type in cmdline.lower() for agent_type in ['proactive', 'orchestrator', 'yrays', 'kalighost']):
                    agent_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cmdline': cmdline[:100] + '...' if len(cmdline) > 100 else cmdline
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
                
        status['running_agents'] = agent_processes
        status['agent_count'] = len(agent_processes)
        
        # Verificar archivos de log importantes
        log_dir = '/Users/mrhardcore/KaliGhost/yrays-agent/logs'
        log_files = {}
        if os.path.exists(log_dir):
            for filename in os.listdir(log_dir):
                if filename.endswith('.log'):
                    filepath = os.path.join(log_dir, filename)
                    try:
                        stat = os.stat(filepath)
                        log_files[filename] = {
                            'size': stat.st_size,
                            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                        }
                    except Exception as e:
                        logger.debug(f"Error al leer log file {filename}: {e}")
                        
        status['log_files'] = log_files
        
        return status
        
    except Exception as e:
        logger.error(f"Error obteniendo estado de agentes: {e}")
        return {}

def main():
    """Función principal para actualizar datos del dashboard"""
    try:
        logger.info("Actualizando datos del dashboard de KaliGhost")
        
        # Obtener métricas del sistema
        system_metrics = get_system_metrics()
        agent_status = get_agent_status()
        
        # Combinar todos los datos
        dashboard_data = {
            'timestamp': datetime.now().isoformat(),
            'system_metrics': system_metrics,
            'agent_status': agent_status
        }
        
        # Guardar datos en archivo JSON para que pueda ser leído por el dashboard
        dashboard_file = '/Users/mrhardcore/KaliGhost/yrays-agent/data/dashboard_data.json'
        os.makedirs(os.path.dirname(dashboard_file), exist_ok=True)
        
        with open(dashboard_file, 'w') as f:
            json.dump(dashboard_data, f, indent=2)
        
        logger.info(f"Datos del dashboard actualizados correctamente en {dashboard_file}")
        
        # También escribir resumen a log
        logger.info(f"CPU: {system_metrics.get('cpu', 0):.1f}%, "
                   f"Memoria: {system_metrics.get('memory', 0):.1f}%, "
                   f"Agentes ejecutándose: {agent_status.get('agent_count', 0)}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error actualizando dashboard: {e}")
        logger.debug(f"Detalles del error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)