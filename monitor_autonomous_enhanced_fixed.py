     1|#!/usr/bin/env python3
     2|"""
     3|Script principal de monitoreo proactivo para KaliGhost
     4|Implementa características avanzadas de monitoreo con análisis predictivo
     5|"""
     6|
     7|import psutil
     8|import time
     9|import json
    10|import logging
    11|import os
    12|from datetime import datetime
    13|from typing import Dict, Any
    14|import sys
    15|import traceback
    16|
    17|# Configurar logging
    18|logging.basicConfig(
    19|    level=logging.INFO,
    20|    format='%(asctime)s - %(levelname)s - %(message)s',
    21|    handlers=[
    22|        logging.FileHandler('/Users/mrhardcore/KaliGhost/yrays-agent/logs/monitoring.log'),
    23|        logging.StreamHandler(sys.stdout)
    24|    ]
    25|)
    26|
    27|logger = logging.getLogger(__name__)
    28|
    29|class ProactiveMonitor:
    30|    def __init__(self):
    31|        self.config_file = '/Users/mrhardcore/KaliGhost/yrays-agent/profiles/continuo.json'
    32|        self.history_file = '/Users/mrhardcore/KaliGhost/yrays-agent/data/metrics_history.json'
    33|        
    34|    def load_config(self) -> Dict[str, Any]:
    35|        """Cargar configuración desde el perfil continuo"""
    36|        try:
    37|            with open(self.config_file, 'r') as f:
    38|                config = json.load(f)
    39|            return config
    40|        except Exception as e:
    41|            logger.error(f"Error cargando configuración: {e}")
    42|            logger.debug(f"Detalles del error: {traceback.format_exc()}")
    43|            # Configuración por defecto
    44|            return {
    45|                "settings": {
    46|                    "alert_thresholds": {
    47|                        "cpu": 80,
    48|                        "memory": 85,
    49|                        "disk": 90
    50|                    }
    51|                }
    52|            }
    53|    
    54|    def get_system_metrics(self) -> Dict[str, float]:
    55|        """Obtener métricas actuales del sistema"""
    56|        metrics = {}
    57|        
    58|        try:
    59|            # CPU
    60|            cpu_percent = psutil.cpu_percent(interval=1)
    61|            metrics['cpu'] = cpu_percent
    62|            
    63|            # Memoria
    64|            memory = psutil.virtual_memory()
    65|            metrics['memory'] = memory.percent
    66|            
    67|            # Disco
    68|            disk = psutil.disk_usage('/')
    69|            metrics['disk'] = (disk.used / disk.total) * 100
    70|            
    71|            # Carga promedio del sistema (Linux/macOS)
    72|            try:
    73|                load_avg = os.getloadavg()
    74|                metrics['load_average'] = load_avg[0]  # Carga a 1 minuto
    75|            except:
    76|                metrics['load_average'] = 0
    77|                
    78|            # Número de procesos
    79|            metrics['processes'] = len(psutil.pids())
    80|            
    81|            return metrics
    82|            
    83|        except Exception as e:
    84|            logger.error(f"Error obteniendo métricas del sistema: {e}")
    85|            logger.debug(f"Detalles del error: {traceback.format_exc()}")
    86|            raise
    87|    
    88|    def predict_trends(self, metrics_history: list) -> Dict[str, str]:
        try:
            if len(metrics_history) < 2:
                return {}
                
            trends = {}
            current = metrics_history[-1]
            previous = metrics_history[-2]
            
            # Predicción de CPU
            if 'cpu' in current and 'cpu' in previous:
                if current['cpu'] > previous['cpu']:
                    trends['cpu'] = 'increasing'
                elif current['cpu'] < previous['cpu']:
                    trends['cpu'] = 'decreasing'
                else:
                    trends['cpu'] = 'stable'
                
            # Predicción de memoria
            if 'memory' in current and 'memory' in previous:
                if current['memory'] > previous['memory']:
                    trends['memory'] = 'increasing'
                elif current['memory'] < previous['memory']:
                    trends['memory'] = 'decreasing'
                else:
                    trends['memory'] = 'stable'
                
            # Predicción de disco
            if 'disk' in current and 'disk' in previous:
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
    89|        """Predecir tendencias basadas en historial"""
    90|        try:
    91|            if len(metrics_history) < 2:
    92|                return {}
    93|                
    94|            trends = {}
    95|            current = metrics_history[-1]
    96|            previous = metrics_history[-2]
    97|            
    98|            # Predicción de CPU
    99|            if current['cpu'] > previous['cpu']:
   100|                trends['cpu'] = 'increasing'
   101|            elif current['cpu'] < previous['cpu']:
   102|                trends['cpu'] = 'decreasing'
   103|            else:
   104|                trends['cpu'] = 'stable'
   105|                
   106|            # Predicción de memoria
   107|            if current['memory'] > previous['memory']:
   108|                trends['memory'] = 'increasing'
   109|            elif current['memory'] < previous['memory']:
   110|                trends['memory'] = 'decreasing'
   111|            else:
   112|                trends['memory'] = 'stable'
   113|                
   114|            # Predicción de disco
   115|            if current['disk'] > previous['disk']:
   116|                trends['disk'] = 'increasing'
   117|            elif current['disk'] < previous['disk']:
   118|                trends['disk'] = 'decreasing'
   119|            else:
   120|                trends['disk'] = 'stable'
   121|                
   122|            return trends
   123|            
   124|        except Exception as e:
   125|            logger.error(f"Error analizando tendencias: {e}")
   126|            logger.debug(f"Detalles del error: {traceback.format_exc()}")
   127|            return {}
   128|    
   129|    def check_alerts(self, metrics: Dict[str, float], thresholds: Dict[str, float]) -> list:
   130|        """Verificar y generar alertas proactivas"""
   131|        alerts = []
   132|        
   133|        try:
   134|            for metric, value in metrics.items():
   135|                if metric in thresholds:
   136|                    threshold = thresholds[metric]
   137|                    if value > threshold:
   138|                        alerts.append({
   139|                            'metric': metric,
   140|                            'value': value,
   141|                            'threshold': threshold,
   142|                            'status': 'warning',
   143|                            'message': f'{metric.upper()} está por encima del umbral ({threshold}%)'
   144|                        })
   145|            
   146|            return alerts
   147|            
   148|        except Exception as e:
   149|            logger.error(f"Error verificando alertas: {e}")
   150|            logger.debug(f"Detalles del error: {traceback.format_exc()}")
   151|            return []
   152|    
   153|    def generate_contextual_alerts(self, metrics: Dict[str, float], trends: Dict[str, str]) -> list:
   154|        """Generar alertas contextualmente basadas en tendencias"""
   155|        contextual_alerts = []
   156|        
   157|        try:
   158|            for metric, trend in trends.items():
   159|                if trend == 'increasing' and metrics[metric] > 70:
   160|                    contextual_alerts.append({
   161|                        'metric': metric,
   162|                        'trend': trend,
   163|                        'value': metrics[metric],
   164|                        'status': 'warning',
   165|                        'message': f'{metric.upper()} en aumento rápido, considerar acciones preventivas'
   166|                    })
   167|            
   168|            return contextual_alerts
   169|            
   170|        except Exception as e:
   171|            logger.error(f"Error generando alertas contextuales: {e}")
   172|            logger.debug(f"Detalles del error: {traceback.format_exc()}")
   173|            return []
   174|    
   175|    def save_metrics_history(self, metrics: Dict[str, float]):
   176|        """Guardar métricas en historial"""
   177|        try:
   178|            if os.path.exists(self.history_file):
   179|                with open(self.history_file, 'r') as f:
   180|                    history = json.load(f)
   181|            else:
   182|                history = []
   183|                
   184|            # Agregar métricas actuales
   185|            history.append({
   186|                'timestamp': datetime.now().isoformat(),
   187|                'metrics': metrics
   188|            })
   189|            
   190|            # Mantener solo las últimas 24 horas de datos (~288 puntos de datos)
   191|            if len(history) > 288:
   192|                history = history[-288:]
   193|                
   194|            with open(self.history_file, 'w') as f:
   195|                json.dump(history, f, indent=2)
   196|                
   197|        except Exception as e:
   198|            logger.error(f"Error guardando historial de métricas: {e}")
   199|            logger.debug(f"Detalles del error: {traceback.format_exc()}")
   200|    
   201|    def run_monitoring_cycle(self):
   202|        """Ejecutar un ciclo completo de monitoreo"""
   203|        try:
   204|            logger.info("Iniciando ciclo de monitoreo proactivo")
   205|            
   206|            # Cargar configuración
   207|            config = self.load_config()
   208|            # Ajustar para manejar la estructura correcta del perfil
   209|            if 'settings' in config and 'alert_thresholds' in config['settings']:
   210|                thresholds = config['settings']['alert_thresholds']
   211|            elif 'alert_thresholds' in config:
   212|                thresholds = config['alert_thresholds']
   213|            else:
   214|                # Configuración por defecto
   215|                thresholds = {
   216|                    'cpu': 80,
   217|                    'memory': 85,
   218|                    'disk': 90
   219|                }
   220|            
   221|            # Obtener métricas actuales
   222|            metrics = self.get_system_metrics()
   223|            logger.info(f"Métricas actuales: {metrics}")
   224|            
   225|            # Verificar alertas
   226|            alerts = self.check_alerts(metrics, thresholds)
   227|            
   228|            # Cargar historial para análisis predictivo
   229|            history = []
   230|            try:
   231|                if os.path.exists(self.history_file):
   232|                    with open(self.history_file, 'r') as f:
   233|                        history = json.load(f)
   234|            except Exception as e:
   235|                logger.warning(f"No se pudo cargar historial: {e}")
   236|            
   237|            # Analizar tendencias
   238|            trends = self.predict_trends([item['metrics'] for item in history])
   239|            logger.info(f"Tendencias detectadas: {trends}")
   240|            
   241|            # Generar alertas contextuales
   242|            contextual_alerts = self.generate_contextual_alerts(metrics, trends)
   243|            
   244|            # Combinar todas las alertas
   245|            all_alerts = alerts + contextual_alerts
   246|            
   247|            # Registrar alertas
   248|            if all_alerts:
   249|                logger.warning(f"Alertas detectadas: {len(all_alerts)}")
   250|                for alert in all_alerts:
   251|                    logger.warning(f"ALERTA: {alert['message']}")
   252|            else:
   253|                logger.info("No se detectaron alertas críticas")
   254|            
   255|            # Guardar historial
   256|            self.save_metrics_history(metrics)
   257|            
   258|            logger.info("Ciclo de monitoreo completado")
   259|            return {'metrics': metrics, 'alerts': all_alerts, 'trends': trends}
   260|            
   261|        except Exception as e:
   262|            logger.error(f"Error durante el ciclo de monitoreo: {e}")
   263|            logger.debug(f"Detalles del error: {traceback.format_exc()}")
   264|            raise
   265|    
   266|def main():
   267|    """Función principal"""
   268|    try:
   269|        monitor = ProactiveMonitor()
   270|        
   271|        # Ejecutar monitoreo
   272|        result = monitor.run_monitoring_cycle()
   273|        
   274|        # Si hay alertas críticas, podemos realizar acciones automáticamente
   275|        if result['alerts']:
   276|            logger.info("Ejecutando acciones preventivas por alertas")
   277|            # Aquí podríamos integrar acciones automáticas
   278|            pass
   279|        
   280|        logger.info("Monitoreo proactivo completado exitosamente")
   281|        
   282|    except Exception as e:
   283|        logger.error(f"Fallo en monitoreo proactivo: {e}")
   284|        logger.debug(f"Detalles del error: {traceback.format_exc()}")
   285|        sys.exit(1)
   286|
   287|if __name__ == "__main__":
   288|    main()