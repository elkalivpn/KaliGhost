1|     1|#!/usr/bin/env python3
2|     2|"""
3|     3|Script principal de monitoreo proactivo para KaliGhost
4|     4|Implementa características avanzadas de monitoreo con análisis predictivo
5|     5|"""
6|     6|
7|     7|import psutil
8|     8|import time
9|     9|import json
10|    10|import logging
11|    11|import os
12|    12|from datetime import datetime
13|    13|from typing import Dict, Any
14|    14|import sys
15|    15|import traceback
16|    16|
17|    17|# Configurar logging
18|    18|logging.basicConfig(
19|    19|    level=logging.INFO,
20|    20|    format='%(asctime)s - %(levelname)s - %(message)s',
21|    21|    handlers=[
22|    22|        logging.FileHandler('/Users/mrhardcore/KaliGhost/yrays-agent/logs/monitoring.log'),
23|    23|        logging.StreamHandler(sys.stdout)
24|    24|    ]
25|    25|)
26|    26|
27|    27|logger = logging.getLogger(__name__)
28|    28|
29|    29|class ProactiveMonitor:
30|    30|    def __init__(self):
31|    31|        self.config_file = '/Users/mrhardcore/KaliGhost/yrays-agent/profiles/continuo.json'
32|    32|        self.history_file = '/Users/mrhardcore/KaliGhost/yrays-agent/data/metrics_history.json'
33|    33|        
34|    34|    def load_config(self) -> Dict[str, Any]:
35|    35|        """Cargar configuración desde el perfil continuo"""
36|    36|        try:
37|    37|            with open(self.config_file, 'r') as f:
38|    38|                config = json.load(f)
39|    39|            return config
40|    40|        except Exception as e:
41|    41|            logger.error(f"Error cargando configuración: {e}")
42|    42|            logger.debug(f"Detalles del error: {traceback.format_exc()}")
43|    43|            # Configuración por defecto
44|    44|            return {
45|    45|                "settings": {
46|    46|                    "alert_thresholds": {
47|    47|                        "cpu": 80,
48|    48|                        "memory": 85,
49|    49|                        "disk": 90
50|    50|                    }
51|    51|                }
52|    52|            }
53|    53|    
54|    54|    def get_system_metrics(self) -> Dict[str, float]:
55|    55|        """Obtener métricas actuales del sistema"""
56|    56|        metrics = {}
57|    57|        
58|    58|        try:
59|    59|            # CPU
60|    60|            cpu_percent = psutil.cpu_percent(interval=1)
61|    61|            metrics['cpu'] = cpu_percent
62|    62|            
63|    63|            # Memoria
64|    64|            memory = psutil.virtual_memory()
65|    65|            metrics['memory'] = memory.percent
66|    66|            
67|    67|            # Disco
68|    68|            disk = psutil.disk_usage('/')
69|    69|            metrics['disk'] = (disk.used / disk.total) * 100
70|    70|            
71|    71|            # Carga promedio del sistema (Linux/macOS)
72|    72|            try:
73|    73|                load_avg = os.getloadavg()
74|    74|                metrics['load_average'] = load_avg[0]  # Carga a 1 minuto
75|    75|            except:
76|    76|                metrics['load_average'] = 0
77|    77|                
78|    78|            # Número de procesos
79|    79|            metrics['processes'] = len(psutil.pids())
80|    80|            
81|    81|            return metrics
82|    82|            
83|    83|        except Exception as e:
84|    84|            logger.error(f"Error obteniendo métricas del sistema: {e}")
85|    85|            logger.debug(f"Detalles del error: {traceback.format_exc()}")
86|    86|            raise
87|    87|    
88|    88|    def predict_trends(self, metrics_history: list) -> Dict[str, str]:
89|    89|        """Predecir tendencias basadas en historial"""
90|    90|        try:
91|    91|            if len(metrics_history) < 2:
92|    92|                return {}
93|    93|                
94|    94|            trends = {}
95|    95|            current = metrics_history[-1]
96|    96|            previous = metrics_history[-2]
97|    97|            
98|    98|            # Predicción de CPU
99|    99|            if current['cpu'] > previous['cpu']:
100|   100|                trends['cpu'] = 'increasing'
101|   101|            elif current['cpu'] < previous['cpu']:
102|   102|                trends['cpu'] = 'decreasing'
103|   103|            else:
104|   104|                trends['cpu'] = 'stable'
105|   105|                
106|   106|            # Predicción de memoria
107|   107|            if current['memory'] > previous['memory']:
108|   108|                trends['memory'] = 'increasing'
109|   109|            elif current['memory'] < previous['memory']:
110|   110|                trends['memory'] = 'decreasing'
111|   111|            else:
112|   112|                trends['memory'] = 'stable'
113|   113|                
114|   114|            # Predicción de disco
115|   115|            if current['disk'] > previous['disk']:
116|   116|                trends['disk'] = 'increasing'
117|   117|            elif current['disk'] < previous['disk']:
118|   118|                trends['disk'] = 'decreasing'
119|   119|            else:
120|   120|                trends['disk'] = 'stable'
121|   121|                
122|   122|            return trends
123|   123|            
124|   124|        except Exception as e:
125|   125|            logger.error(f"Error analizando tendencias: {e}")
126|   126|            logger.debug(f"Detalles del error: {traceback.format_exc()}")
127|   127|            return {}
128|   128|    
129|   129|    def check_alerts(self, metrics: Dict[str, float], thresholds: Dict[str, float]) -> list:
130|   130|        """Verificar y generar alertas proactivas"""
131|   131|        alerts = []
132|   132|        
133|   133|        try:
134|   134|            for metric, value in metrics.items():
135|   135|                if metric in thresholds:
136|   136|                    threshold = thresholds[metric]
137|   137|                    if value > threshold:
138|   138|                        alerts.append({
139|   139|                            'metric': metric,
140|   140|                            'value': value,
141|   141|                            'threshold': threshold,
142|   142|                            'status': 'warning',
143|   143|                            'message': f'{metric.upper()} está por encima del umbral ({threshold}%)'
144|   144|                        })
145|   145|            
146|   146|            return alerts
147|   147|            
148|   148|        except Exception as e:
149|   149|            logger.error(f"Error verificando alertas: {e}")
150|   150|            logger.debug(f"Detalles del error: {traceback.format_exc()}")
151|   151|            return []
152|   152|    
153|   153|    def generate_contextual_alerts(self, metrics: Dict[str, float], trends: Dict[str, str]) -> list:
154|   154|        """Generar alertas contextualmente basadas en tendencias"""
155|   155|        contextual_alerts = []
156|   156|        
157|   157|        try:
158|   158|            for metric, trend in trends.items():
159|   159|                if trend == 'increasing' and metrics[metric] > 70:
160|   160|                    contextual_alerts.append({
161|   161|                        'metric': metric,
162|   162|                        'trend': trend,
163|   163|                        'value': metrics[metric],
164|   164|                        'status': 'warning',
165|   165|                        'message': f'{metric.upper()} en aumento rápido, considerar acciones preventivas'
166|   166|                    })
167|   167|            
168|   168|            return contextual_alerts
169|   169|            
170|   170|        except Exception as e:
171|   171|            logger.error(f"Error generando alertas contextuales: {e}")
172|   172|            logger.debug(f"Detalles del error: {traceback.format_exc()}")
173|   173|            return []
174|   174|    
175|   175|    def save_metrics_history(self, metrics: Dict[str, float]):
176|   176|        """Guardar métricas en historial"""
177|   177|        try:
178|   178|            if os.path.exists(self.history_file):
179|   179|                with open(self.history_file, 'r') as f:
180|   180|                    history = json.load(f)
181|   181|            else:
182|   182|                history = []
183|   183|                
184|   184|            # Agregar métricas actuales
185|   185|            history.append({
186|   186|                'timestamp': datetime.now().isoformat(),
187|   187|                'metrics': metrics
188|   188|            })
189|   189|            
190|   190|            # Mantener solo las últimas 24 horas de datos (~288 puntos de datos)
191|   191|            if len(history) > 288:
192|   192|                history = history[-288:]
193|   193|                
194|   194|            with open(self.history_file, 'w') as f:
195|   195|                json.dump(history, f, indent=2)
196|   196|                
197|   197|        except Exception as e:
198|   198|            logger.error(f"Error guardando historial de métricas: {e}")
199|   199|            logger.debug(f"Detalles del error: {traceback.format_exc()}")
200|   200|    
201|   201|    def run_monitoring_cycle(self):
202|   202|        """Ejecutar un ciclo completo de monitoreo"""
203|   203|        try:
204|   204|            logger.info("Iniciando ciclo de monitoreo proactivo")
205|   205|            
206|   206|        # Cargar configuración
207|   207|        config = self.load_config()
208|        # Ajustar para manejar la estructura correcta del perfil
209|        if 'settings' in config and 'alert_thresholds' in config['settings']:
210|            thresholds = config['settings']['alert_thresholds']
211|        elif 'alert_thresholds' in config:
212|            thresholds = config['alert_thresholds']
213|        else:
214|            # Configuración por defecto
215|            thresholds = {
216|                'cpu': 80,
217|                'memory': 85,
218|                'disk': 90
219|            }
220|   208|        # Ajustar para manejar la estructura correcta del perfil
221|   209|        if 'settings' in config and 'alert_thresholds' in config['settings']:
222|   210|            thresholds = config['settings']['alert_thresholds']
223|   211|        elif 'alert_thresholds' in config:
224|   212|            thresholds = config['alert_thresholds']
225|   213|        else:
226|   214|            # Configuración por defecto
227|   215|            thresholds = {
228|   216|                'cpu': 80,
229|   217|                'memory': 85,
230|   218|                'disk': 90
231|   219|            }
232|   220|        if 'settings' in config and 'alert_thresholds' in config['settings']:
233|   221|            thresholds = config['settings']['alert_thresholds']
234|   222|        elif 'alert_thresholds' in config:
235|   223|            thresholds = config['alert_thresholds']
236|   224|        else:
237|   225|            # Configuración por defecto
238|   226|            thresholds = {
239|   227|                'cpu': 80,
240|   228|                'memory': 85,
241|   229|                'disk': 90
242|   230|            }
243|   231|            
244|   232|            # Obtener métricas actuales
245|   233|            metrics = self.get_system_metrics()
246|   234|            logger.info(f"Métricas actuales: {metrics}")
247|   235|            
248|   236|            # Verificar alertas
249|   237|            alerts = self.check_alerts(metrics, thresholds)
250|   238|            
251|   239|            # Cargar historial para análisis predictivo
252|   240|            history = []
253|   241|            try:
254|   242|                if os.path.exists(self.history_file):
255|   243|                    with open(self.history_file, 'r') as f:
256|   244|                        history = json.load(f)
257|   245|            except Exception as e:
258|   246|                logger.warning(f"No se pudo cargar historial: {e}")
259|   247|            
260|   248|            # Analizar tendencias
261|   249|            trends = self.predict_trends([item['metrics'] for item in history])
262|   250|            logger.info(f"Tendencias detectadas: {trends}")
263|   251|            
264|   252|            # Generar alertas contextuales
265|   253|            contextual_alerts = self.generate_contextual_alerts(metrics, trends)
266|   254|            
267|   255|            # Combinar todas las alertas
268|   256|            all_alerts = alerts + contextual_alerts
269|   257|            
270|   258|            # Registrar alertas
271|   259|            if all_alerts:
272|   260|                logger.warning(f"Alertas detectadas: {len(all_alerts)}")
273|   261|                for alert in all_alerts:
274|   262|                    logger.warning(f"ALERTA: {alert['message']}")
275|   263|            else:
276|   264|                logger.info("No se detectaron alertas críticas")
277|   265|            
278|   266|            # Guardar historial
279|   267|            self.save_metrics_history(metrics)
280|   268|            
281|   269|            logger.info("Ciclo de monitoreo completado")
282|   270|            return {'metrics': metrics, 'alerts': all_alerts, 'trends': trends}
283|   271|            
284|   272|        except Exception as e:
285|   273|            logger.error(f"Error durante el ciclo de monitoreo: {e}")
286|   274|            logger.debug(f"Detalles del error: {traceback.format_exc()}")
287|   275|            raise
288|   276|
289|   277|def main():
290|   278|    """Función principal"""
291|   279|    try:
292|   280|        monitor = ProactiveMonitor()
293|   281|        
294|   282|        # Ejecutar monitoreo
295|   283|        result = monitor.run_monitoring_cycle()
296|   284|        
297|   285|        # Si hay alertas críticas, podemos realizar acciones automáticamente
298|   286|        if result['alerts']:
299|   287|            logger.info("Ejecutando acciones preventivas por alertas")
300|   288|            # Aquí podríamos integrar acciones automáticas
301|   289|            pass
302|   290|            
303|   291|        logger.info("Monitoreo proactivo completado exitosamente")
304|   292|        
305|   293|    except Exception as e:
306|   294|        logger.error(f"Fallo en monitoreo proactivo: {e}")
307|   295|        logger.debug(f"Detalles del error: {traceback.format_exc()}")
308|   296|        sys.exit(1)
309|   297|
310|   298|if __name__ == "__main__":
311|   299|    main()