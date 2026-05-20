#!/usr/bin/env python3
"""
Script principal de monitoreo proactivo para KaliGhost
Implementa características avanzadas de monitoreo con análisis predictivo
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

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/Users/mrhardcore/KaliGhost/yrays-agent/logs/monitoring.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class ProactiveMonitor:
    def __init__(self):
        self.config_file = '/Users/mrhardcore/KaliGhost/yrays-agent/profiles/continuo.json'
        self.history_file = '/Users/mrhardcore/KaliGhost/yrays-agent/data/metrics_history.json'
        
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
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error obteniendo métricas del sistema: {e}")
            logger.debug(f"Detalles del error: {traceback.format_exc()}")
            raise
    
    def predict_trends(self, metrics_history: list) -> Dict[str, str]:
        """Predecir tendencias basadas en historial"""
        try:
            if len(metrics_history) < 2:
                return {}
                
            trends = {}
            current = metrics_history[-1]
            previous = metrics_history[-2]
            
            # Predicción de CPU
            if current['cpu'] > previous['cpu']:
                trends['cpu'] = 'increasing'
            elif current['cpu'] < previous['cpu']:
                trends['cpu'] = 'decreasing'
            else:
                trends['cpu'] = 'stable'
                
            # Predicción de memoria
            if current['memory'] > previous['memory']:
                trends['memory'] = 'increasing'
            elif current['memory'] < previous['memory']:
                trends['memory'] = 'decreasing'
            else:
                trends['memory'] = 'stable'
                
            # Predicción de disco
            if current['disk'] > previous['disk']:
                trends['disk'] = 'increasing'
            elif current['disk'] < previous['disk']:
                trends['disk'] = 'decreasing'
            else:
                trends['disk'] = 'stable'
                
            return trends
            
        except Exception as e:
            logger.error(f"Error analizando tendencias: {e}")
            logger.debug(f"Detalles del error: {traceback.format_exc()}")
            return {}
    
    def check_alerts(self, metrics: Dict[str, float], thresholds: Dict[str, float]) -> list:
        """Verificar y generar alertas proactivas"""
        alerts = []
        
        try:
            for metric, value in metrics.items():
                if metric in thresholds:
                    threshold = thresholds[metric]
                    if value > threshold:
                        alerts.append({
                            'metric': metric,
                            'value': value,
                            'threshold': threshold,
                            'status': 'warning',
                            'message': f'{metric.upper()} está por encima del umbral ({threshold}%)'
                        })
            
            return alerts
            
        except Exception as e:
            logger.error(f"Error verificando alertas: {e}")
            logger.debug(f"Detalles del error: {traceback.format_exc()}")
            return []
    
    def generate_contextual_alerts(self, metrics: Dict[str, float], trends: Dict[str, str]) -> list:
        """Generar alertas contextualmente basadas en tendencias"""
        contextual_alerts = []
        
        try:
            for metric, trend in trends.items():
                if trend == 'increasing' and metrics[metric] > 70:
                    contextual_alerts.append({
                        'metric': metric,
                        'trend': trend,
                        'value': metrics[metric],
                        'status': 'warning',
                        'message': f'{metric.upper()} en aumento rápido, considerar acciones preventivas'
                    })
            
            return contextual_alerts
            
        except Exception as e:
            logger.error(f"Error generando alertas contextuales: {e}")
            logger.debug(f"Detalles del error: {traceback.format_exc()}")
            return []
    
    def save_metrics_history(self, metrics: Dict[str, float]):
        """Guardar métricas en historial"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    history = json.load(f)
            else:
                history = []
                
            # Agregar métricas actuales
            history.append({
                'timestamp': datetime.now().isoformat(),
                'metrics': metrics
            })
            
            # Mantener solo las últimas 24 horas de datos (~288 puntos de datos)
            if len(history) > 288:
                history = history[-288:]
                
            with open(self.history_file, 'w') as f:
                json.dump(history, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error guardando historial de métricas: {e}")
            logger.debug(f"Detalles del error: {traceback.format_exc()}")
    
    def run_monitoring_cycle(self):
        """Ejecutar un ciclo completo de monitoreo"""
        try:
            logger.info("Iniciando ciclo de monitoreo proactivo")
            
            # Cargar configuración
            config = self.load_config()
            thresholds = config['settings']['alert_thresholds']
            
            # Obtener métricas actuales
            metrics = self.get_system_metrics()
            logger.info(f"Métricas actuales: {metrics}")
            
            # Verificar alertas
            alerts = self.check_alerts(metrics, thresholds)
            
            # Cargar historial para análisis predictivo
            history = []
            try:
                if os.path.exists(self.history_file):
                    with open(self.history_file, 'r') as f:
                        history = json.load(f)
            except Exception as e:
                logger.warning(f"No se pudo cargar historial: {e}")
            
            # Analizar tendencias
            trends = self.predict_trends([item['metrics'] for item in history])
            logger.info(f"Tendencias detectadas: {trends}")
            
            # Generar alertas contextuales
            contextual_alerts = self.generate_contextual_alerts(metrics, trends)
            
            # Combinar todas las alertas
            all_alerts = alerts + contextual_alerts
            
            # Registrar alertas
            if all_alerts:
                logger.warning(f"Alertas detectadas: {len(all_alerts)}")
                for alert in all_alerts:
                    logger.warning(f"ALERTA: {alert['message']}")
            else:
                logger.info("No se detectaron alertas críticas")
            
            # Guardar historial
            self.save_metrics_history(metrics)
            
            logger.info("Ciclo de monitoreo completado")
            return {'metrics': metrics, 'alerts': all_alerts, 'trends': trends}
            
        except Exception as e:
            logger.error(f"Error durante el ciclo de monitoreo: {e}")
            logger.debug(f"Detalles del error: {traceback.format_exc()}")
            raise

def main():
    """Función principal"""
    try:
        monitor = ProactiveMonitor()
        
        # Ejecutar monitoreo
        result = monitor.run_monitoring_cycle()
        
        # Si hay alertas críticas, podemos realizar acciones automáticamente
        if result['alerts']:
            logger.info("Ejecutando acciones preventivas por alertas")
            # Aquí podríamos integrar acciones automáticas
            pass
            
        logger.info("Monitoreo proactivo completado exitosamente")
        
    except Exception as e:
        logger.error(f"Fallo en monitoreo proactivo: {e}")
        logger.debug(f"Detalles del error: {traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    main()