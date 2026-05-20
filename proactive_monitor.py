#!/usr/bin/env python3
"""
Script de monitoreo proactivo avanzado para KaliGhost
Basado en los principios de la skill "proactive-monitoring-system"
"""

import psutil
import time
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List
import numpy as np
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/Users/mrhardcore/KaliGhost/yrays-agent/logs/advanced_monitoring.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class AdvancedProactiveMonitor:
    def __init__(self):
        self.config_file = '/Users/mrhardcore/KaliGhost/yrays-agent/profiles/continuo.json'
        self.metrics_history_file = '/Users/mrhardcore/KaliGhost/yrays-agent/data/metrics_history.json'
        self.monitoring_config_file = '/Users/mrhardcore/KaliGhost/yrays-agent/data/monitoring_config.json'
        
    def load_config(self) -> Dict[str, Any]:
        """Cargar configuración del sistema"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            return config
        except Exception as e:
            logger.error(f"Error cargando configuración principal: {e}")
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
            
    def load_monitoring_config(self) -> Dict[str, Any]:
        """Cargar configuración específica de monitoreo"""
        try:
            with open(self.monitoring_config_file, 'r') as f:
                config = json.load(f)
            return config
        except Exception as e:
            logger.warning(f"Configuración de monitoreo no encontrada, usando configuración por defecto: {e}")
            # Configuración por defecto
            return {
                "monitoring": {
                    "interval": 60,
                    "alert_thresholds": {
                        "cpu": 80,
                        "memory": 85,
                        "disk": 90
                    },
                    "predictive_analysis": {
                        "enabled": True,
                        "lookback_hours": 24,
                        "prediction_accuracy": 0.85
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
            
            # Uso de red (paquetes entrantes/salientes)
            net_io = psutil.net_io_counters()
            metrics['net_bytes_sent'] = net_io.bytes_sent
            metrics['net_bytes_recv'] = net_io.bytes_recv
            
            # Temperatura (si está disponible)
            try:
                temps = psutil.sensors_temperatures()
                if temps:
                    # Tomar la temperatura más alta de todos los sensores
                    temp_values = [temp.current for sensor in temps.values() for temp in sensor]
                    if temp_values:
                        metrics['temperature'] = max(temp_values)
            except:
                pass
                
            # Fecha y hora
            metrics['timestamp'] = datetime.now().isoformat()
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error obteniendo métricas del sistema: {e}")
            return {}

    def predict_resource_usage(self, history: List[Dict], metric_key: str) -> str:
        """
        Predecir uso futuro de recursos usando análisis de tendencias.
        Retorna 'increasing', 'decreasing', o 'stable'
        """
        try:
            if len(history) < 3:
                return 'stable'
                
            # Extraer valores del histórico para el métrico específico
            values = [item['metrics'][metric_key] for item in history if metric_key in item['metrics']]
            
            # Solo usar los últimos 20 puntos de datos para predicción
            if len(values) > 20:
                values = values[-20:]
                
            if len(values) < 3:
                return 'stable'
            
            # Calcular tendencia
            # Usar una regresión lineal simple para predecir
            x = np.array(range(len(values)))
            y = np.array(values)
            
            # Calcular pendiente de la línea de mejor ajuste
            if len(x) > 1:
                slope = np.polyfit(x, y, 1)[0]
            else:
                slope = 0
            
            # Interpretar pendiente
            if abs(slope) < 0.5:
                return 'stable'
            elif slope > 0.5:
                return 'increasing'
            else:
                return 'decreasing'
                
        except Exception as e:
            logger.warning(f"Error en predicción de tendencia: {e}")
            return 'stable'

    def calculate_prediction_confidence(self, history: List[Dict], metric_key: str) -> float:
        """Calcular confianza en la predicción basada en variabilidad"""
        try:
            if len(history) < 3:
                return 0.5
                
            values = [item['metrics'][metric_key] for item in history if metric_key in item['metrics']]
            if len(values) < 3:
                return 0.5
            
            # Calcular desviación estándar
            std_deviation = np.std(values)
            
            # Confianza inversamente proporcional a la desviación
            # Cuanto menor es la desviación, mayor la confianza
            max_std = max(10.0, np.max(values))
            confidence = 1.0 - (std_deviation / max_std)
            
            # Limitar entre 0.5 y 1.0
            return max(0.5, min(1.0, confidence))
            
        except Exception as e:
            logger.warning(f"Error calculando confianza de predicción: {e}")
            return 0.7

    def enhanced_alert_generation(self, metrics: Dict[str, float], 
                                historical_data: List[Dict]) -> List[Dict]:
        """
        Generar alertas mejoradas con inteligencia predictiva
        """
        alerts = []
        
        try:
            # Cargar configuración
            config = self.load_config()
            thresholds = config['settings']['alert_thresholds']
            monitoring_config = self.load_monitoring_config()
            prediction_enabled = monitoring_config['monitoring']['predictive_analysis']['enabled']
            
            for metric, value in metrics.items():
                # Alertas básicas por umbral
                if metric in thresholds and value > thresholds[metric]:
                    alerts.append({
                        'type': 'threshold_crossing',
                        'metric': metric,
                        'value': value,
                        'threshold': thresholds[metric],
                        'status': 'warning',
                        'message': f'{metric.upper()} (valor actual: {value:.1f}%) está por encima del umbral ({thresholds[metric]}%)',
                        'severity': 'medium'
                    })
                
                # Alertas predictivas si están habilitadas
                if prediction_enabled and metric in ['cpu', 'memory', 'disk']:
                    trend = self.predict_resource_usage(historical_data, metric)
                    confidence = self.calculate_prediction_confidence(historical_data, metric)
                    
                    if trend == 'increasing':
                        # Predecir si va a sobrepasar el umbral
                        predicted_value = value + (value * 0.1)  # Aproximación simplificada
                        
                        if predicted_value > thresholds.get(metric, 0):
                            alerts.append({
                                'type': 'predictive_alert',
                                'metric': metric,
                                'actual_value': value,
                                'predicted_value': predicted_value,
                                'threshold': thresholds[metric],
                                'trend': trend,
                                'confidence': confidence,
                                'status': 'warning',
                                'message': f'{metric.upper()} probablemente superará el umbral ({thresholds[metric]}%) en breve. Valor actual {value:.1f}%, valor esperado: {predicted_value:.1f}%. Confianza: {confidence:.2f}',
                                'severity': 'high' if confidence > 0.9 else 'medium'
                            })
                        
                        if confidence < 0.7:
                            # Alerta adicional por baja confianza
                            alerts.append({
                                'type': 'low_confidence_prediction',
                                'metric': metric,
                                'trend': trend,
                                'confidence': confidence,
                                'status': 'info',
                                'message': f'Baja confianza en predicción de {metric.upper()}. Confianza: {confidence:.2f}',
                                'severity': 'low'
                            })
                            
        except Exception as e:
            logger.error(f"Error en generación de alertas mejoradas: {e}")
            
        return alerts

    def save_metrics_history(self, metrics: Dict[str, float]):
        """Guardar métricas en historial"""
        try:
            if os.path.exists(self.metrics_history_file):
                with open(self.metrics_history_file, 'r') as f:
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
                
            with open(self.metrics_history_file, 'w') as f:
                json.dump(history, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error guardando historial de métricas: {e}")

    def cleanup_old_logs(self):
        """Limpiar logs antiguos"""
        try:
            # Eliminar logs anteriores a 30 días
            retention_days = 30
            cutoff_date = datetime.now() - timedelta(days=retention_days)
            
            log_dir = '/Users/mrhardcore/KaliGhost/yrays-agent/logs'
            for filename in os.listdir(log_dir):
                if filename.endswith('.log'):
                    filepath = os.path.join(log_dir, filename)
                    file_time = datetime.fromtimestamp(os.path.getctime(filepath))
                    if file_time < cutoff_date:
                        os.remove(filepath)
                        logger.info(f"Archivo de log eliminado: {filename}")
                        
        except Exception as e:
            logger.warning(f"Error limpiando logs antiguos: {e}")

    def run_monitoring_cycle(self):
        """Ejecutar un ciclo completo de monitoreo proactivo"""
        try:
            logger.info("Iniciando ciclo de monitoreo proactivo avanzado")
            
            # Limpiar logs antiguos
            self.cleanup_old_logs()
            
            # Cargar configuración
            config = self.load_config()
            monitoring_config = self.load_monitoring_config()
            thresholds = config['settings']['alert_thresholds']
            
            # Obtener métricas actuales
            metrics = self.get_system_metrics()
            if not metrics:
                logger.error("No se pudieron obtener métricas del sistema")
                return None
                
            logger.info(f"Métricas actuales: {metrics}")
            
            # Cargar historial
            history = []
            try:
                if os.path.exists(self.metrics_history_file):
                    with open(self.metrics_history_file, 'r') as f:
                        history = json.load(f)
                else:
                    logger.info("Historial de métricas no encontrado, creando uno nuevo")
            except Exception as e:
                logger.warning(f"No se pudo cargar historial: {e}")
            
            # Generar alertas mejoradas con análisis predictivo
            alerts = self.enhanced_alert_generation(metrics, history)
            
            # Registrar alertas
            if alerts:
                logger.warning(f"Alertas detectadas: {len(alerts)}")
                for alert in alerts:
                    # Determinar el nivel de gravedad
                    severity = alert.get('severity', 'medium')
                    if severity == 'high':
                        logger.critical(f"ALERTA ALTA GRAVEDAD: {alert['message']}")
                    elif severity == 'medium':
                        logger.warning(f"ALERTA MEDIA GRAVEDAD: {alert['message']}")
                    else:
                        logger.info(f"INFORMACIÓN: {alert['message']}")
            else:
                logger.info("No se detectaron alertas críticas")
            
            # Guardar historial
            self.save_metrics_history(metrics)
            
            logger.info("Ciclo de monitoreo avanzado completado")
            return {'metrics': metrics, 'alerts': alerts, 'timestamp': datetime.now()}
            
        except Exception as e:
            logger.error(f"Error durante el ciclo de monitoreo avanzado: {e}")
            import traceback
            logger.error(f"Detalles del error: {traceback.format_exc()}")
            raise

def main():
    """Función principal"""
    try:
        monitor = AdvancedProactiveMonitor()
        
        # Ejecutar monitoreo
        result = monitor.run_monitoring_cycle()
        
        # Si hay alertas críticas, podemos realizar acciones automáticamente
        if result and result['alerts']:
            logger.info("Ejecutando acciones preventivas por alertas")
            # Aquí podríamos integrar acciones automáticas
            pass
            
        logger.info("Monitoreo proactivo avanzado completado exitosamente")
        
    except Exception as e:
        logger.critical(f"Fallo en monitoreo proactivo avanzado: {e}")
        import traceback
        logger.critical(f"Detalles del error: {traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    main()