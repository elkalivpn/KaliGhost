#!/usr/bin/env python3
"""
Dashboard monitor script for KaliGhost
Exports system metrics in JSON format for dashboard consumption
"""

import psutil
import time
import json
import logging
import os
from datetime import datetime
from typing import Dict, Any
import sys
import traceback
import argparse

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/Users/mrhardcore/KaliGhost/yrays-agent/logs/dashboard_monitor.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class DashboardMonitor:
    def __init__(self):
        self.config_file = '/Users/mrhardcore/KaliGhost/yrays-agent/profiles/continuo.json'
        self.history_file = '/Users/mrhardcore/KaliGhost/yrays-agent/data/metrics_history.json'
        self.dashboard_data_file = '/Users/mrhardcore/KaliGhost/gui/frontend/dashboard_data.json'
        
    def load_config(self) -> Dict[str, Any]:
        """Cargar configuración desde el perfil continuo"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            return config
        except Exception as e:
            logger.error(f"Error cargando configuración: {e}")
            logger.debug(f"Detalles del error: {traceback.format_exc()}")
            # Configuración por defecto
            return {
                "settings": {
                    "alert_thresholds": {
                        "cpu": 80,
                        "memory": 85,
                        "disk": 90
                    }
                }
            }
    
    def get_system_metrics(self) -> Dict[str, float]:
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
            logger.debug(f"Detalles del error: {traceback.format_exc()}")
            raise
    
    def generate_dashboard_data(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """Generar datos en formato para dashboard"""
        try:
            # Cargar configuración
            config = self.load_config()
            thresholds = config['settings']['alert_thresholds']
            
            # Determinar estado del sistema
            system_status = "normal"
            if metrics.get('cpu', 0) > thresholds['cpu']:
                system_status = "warning" if metrics['cpu'] < thresholds['cpu'] * 1.1 else "critical"
            if metrics.get('memory', 0) > thresholds['memory']:
                system_status = "warning" if metrics['memory'] < thresholds['memory'] * 1.1 else "critical"
            if metrics.get('disk', 0) > thresholds['disk']:
                system_status = "warning" if metrics['disk'] < thresholds['disk'] * 1.1 else "critical"
            
            # Preparar datos para dashboard
            dashboard_data = {
                "timestamp": datetime.now().isoformat(),
                "metrics": metrics,
                "system_status": system_status,
                "alerts": [],
                "configuration": config['settings']
            }
            
            # Generar alertas basadas en umbral
            for metric, value in metrics.items():
                if metric in thresholds and value > thresholds[metric]:
                    dashboard_data["alerts"].append({
                        "type": "threshold_exceeded",
                        "metric": metric,
                        "value": value,
                        "threshold": thresholds[metric],
                        "severity": "high" if value > thresholds[metric] * 1.1 else "medium",
                        "message": f"{metric.upper()} excedió el umbral ({thresholds[metric]}%)"
                    })
            
            return dashboard_data
            
        except Exception as e:
            logger.error(f"Error generando datos para dashboard: {e}")
            logger.debug(f"Detalles del error: {traceback.format_exc()}")
            return {
                "timestamp": datetime.now().isoformat(),
                "metrics": metrics,
                "system_status": "error",
                "alerts": [{"type": "error", "message": f"Error procesando métricas: {str(e)}"}],
                "configuration": {}
            }
    
    def export_dashboard_data(self, data: Dict[str, Any]):
        """Exportar datos al archivo para el dashboard"""
        try:
            # Asegurar el directorio de destino
            os.makedirs(os.path.dirname(self.dashboard_data_file), exist_ok=True)
            
            # Escribir datos en formato JSON
            with open(self.dashboard_data_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Datos exportados a {self.dashboard_data_file}")
            
        except Exception as e:
            logger.error(f"Error exportando datos para dashboard: {e}")
            logger.debug(f"Detalles del error: {traceback.format_exc()}")
    
    def run_monitoring_cycle(self):
        """Ejecutar un ciclo completo de monitoreo para dashboard"""
        try:
            logger.info("Iniciando ciclo de monitoreo para dashboard")
            
            # Obtener métricas actuales
            metrics = self.get_system_metrics()
            logger.info(f"Métricas actuales: {metrics}")
            
            # Generar datos para dashboard
            dashboard_data = self.generate_dashboard_data(metrics)
            
            # Exportar datos para el dashboard
            self.export_dashboard_data(dashboard_data)
            
            # Loggear alertas
            if dashboard_data.get("alerts"):
                logger.warning(f"Alertas generadas: {len(dashboard_data['alerts'])}")
                for alert in dashboard_data["alerts"]:
                    logger.warning(f"ALERTA: {alert['message']}")
            else:
                logger.info("No se detectaron alertas críticas")
            
            logger.info("Ciclo de monitoreo para dashboard completado")
            return dashboard_data
            
        except Exception as e:
            logger.error(f"Error durante el ciclo de monitoreo para dashboard: {e}")
            logger.debug(f"Detalles del error: {traceback.format_exc()}")
            raise

def main():
    """Función principal"""
    try:
        parser = argparse.ArgumentParser(description='Dashboard monitor for KaliGhost')
        parser.add_argument('--export-only', action='store_true', help='Solo exportar datos, no ejecutar monitoreo')
        parser.add_argument('--interval', type=int, default=10, help='Intervalo de monitoreo en minutos')
        
        args = parser.parse_args()
        
        monitor = DashboardMonitor()
        
        # Ejecutar solo exportación si se pide
        if args.export_only:
            # Usar métricas del historial o métricas actuales
            try:
                with open(monitor.history_file, 'r') as f:
                    history = json.load(f)
                if history:
                    latest_metrics = history[-1]['metrics']
                else:
                    latest_metrics = monitor.get_system_metrics()
            except:
                latest_metrics = monitor.get_system_metrics()
                
            dashboard_data = monitor.generate_dashboard_data(latest_metrics)
            monitor.export_dashboard_data(dashboard_data)
            logger.info("Exportación completa")
        else:
            # Ejecutar ciclo completo de monitoreo
            result = monitor.run_monitoring_cycle()
            
            logger.info("Monitoreo para dashboard completado exitosamente")
            
    except Exception as e:
        logger.error(f"Fallo en monitoreo para dashboard: {e}")
        logger.debug(f"Detalles del error: {traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    main()