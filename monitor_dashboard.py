#!/usr/bin/env python3
"""
Monitor de dashboard simplificado para KaliGhost
Este script se ejecuta cada 10 minutos para actualizar los datos del dashboard
"""

import psutil
import json
import logging
import os
from datetime import datetime
import sys

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

def get_system_metrics():
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
        
        # Uso de red
        try:
            net_io = psutil.net_io_counters()
            metrics['net_bytes_sent'] = net_io.bytes_sent
            metrics['net_bytes_recv'] = net_io.bytes_recv
        except:
            metrics['net_bytes_sent'] = 0
            metrics['net_bytes_recv'] = 0
        
        # Fecha y hora
        metrics['timestamp'] = datetime.now().isoformat()
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error obteniendo métricas del sistema: {e}")
        return None

def generate_dashboard_data():
    """Generar datos en formato para dashboard"""
    try:
        # Obtener métricas
        metrics = get_system_metrics()
        if not metrics:
            return None
            
        # Datos base para el dashboard
        dashboard_data = {
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics,
            "system_status": "normal",
            "alerts": []
        }
        
        # Definir umbrales de alerta (basados en el perfil continuo)
        thresholds = {
            "cpu": 80,
            "memory": 85,
            "disk": 90
        }
        
        # Verificar alertas por umbrales
        for metric, value in metrics.items():
            if metric in thresholds and value > thresholds[metric]:
                severity = "high" if value > thresholds[metric] * 1.1 else "medium"
                dashboard_data["alerts"].append({
                    "type": "threshold_exceeded",
                    "metric": metric,
                    "value": value,
                    "threshold": thresholds[metric],
                    "severity": severity,
                    "message": f"{metric.upper()} excedió el umbral ({thresholds[metric]}%)"
                })
                
                # Actualizar estado del sistema
                if severity == "high":
                    dashboard_data["system_status"] = "critical"
                elif dashboard_data["system_status"] != "critical":
                    dashboard_data["system_status"] = "warning"
        
        return dashboard_data
        
    except Exception as e:
        logger.error(f"Error generando datos para dashboard: {e}")
        return None

def export_to_dashboard_file(data):
    """Exportar datos al archivo del dashboard"""
    try:
        # Directorio de destino
        dest_dir = '/Users/mrhardcore/KaliGhost/gui/frontend'
        os.makedirs(dest_dir, exist_ok=True)
        
        # Archivo de datos del dashboard
        dashboard_file = os.path.join(dest_dir, 'dashboard_data.json')
        
        # Escribir en formato JSON
        with open(dashboard_file, 'w') as f:
            json.dump(data, f, indent=2)
            
        logger.info(f"Datos exportados a {dashboard_file}")
        return True
        
    except Exception as e:
        logger.error(f"Error exportando datos para dashboard: {e}")
        return False

def main():
    """Función principal para actualización del dashboard"""
    try:
        logger.info("Actualizando datos para dashboard...")
        
        # Generar datos para dashboard
        dashboard_data = generate_dashboard_data()
        
        if dashboard_data:
            # Exportar los datos
            success = export_to_dashboard_file(dashboard_data)
            
            if success:
                logger.info("Dashboard actualizado exitosamente")
                
                # Mostrar información clave
                cpu = dashboard_data['metrics'].get('cpu', 0)
                memory = dashboard_data['metrics'].get('memory', 0)
                disk = dashboard_data['metrics'].get('disk', 0)
                
                status_msg = f"Sistema: {dashboard_data['system_status']}"
                metrics_msg = f"CPU: {cpu:.1f}%, Mem: {memory:.1f}%, Disco: {disk:.1f}%"
                
                logger.info(f"{status_msg} - {metrics_msg}")
                
                if dashboard_data['alerts']:
                    logger.warning(f"Alertas detectadas: {len(dashboard_data['alerts'])}")
                    for alert in dashboard_data['alerts']:
                        logger.warning(f"ALERTA: {alert['message']}")
            else:
                logger.error("Error al exportar datos al dashboard")
        else:
            logger.error("No se pudieron generar datos para el dashboard")
            
    except Exception as e:
        logger.error(f"Error en actualización del dashboard: {e}")
        import traceback
        logger.error(f"Detalles: {traceback.format_exc()}")

if __name__ == "__main__":
    main()