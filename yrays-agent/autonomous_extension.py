#!/usr/bin/env python3
"""
Módulo de Extensión Autónoma para YrYs-Agent
Integra sistemas de tareas, eventos y perfiles de comportamiento
"""

import os
import sys
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

# Importar módulos del sistema de autonomía
try:
    from .autonomous_task_manager import AutonomousTaskManager, Task
    from .event_system import get_event_system, EventType
    from .behavior_profiles import get_profile_manager, BehaviorMode
    AUTONOMY_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Módulos de autonomía no disponibles: {e}")
    AUTONOMY_AVAILABLE = False

class AutonomousExtension:
    """Extensión de autonomía para YrYs-Agent"""
    
    def __init__(self, agent_config: Dict[str, Any]):
        if not AUTONOMY_AVAILABLE:
            raise RuntimeError("Módulos de autonomía no disponibles")
        
        self.config = agent_config
        self.task_manager = AutonomousTaskManager()
        self.event_system = get_event_system()
        self.profile_manager = get_profile_manager()
        
        # Estado de la extensión
        self.enabled = False
        self.started = False
        
        logging.info("Extensión autónoma inicializada")
    
    def enable(self):
        """Habilita la extensión autónoma"""
        self.enabled = True
        logging.info("Extensión autónoma habilitada")
    
    def disable(self):
        """Deshabilita la extensión autónoma"""
        if self.started:
            self.stop()
        self.enabled = False
        logging.info("Extensión autónoma deshabilitada")
    
    def start(self):
        """Inicia los sistemas autónomos"""
        if not self.enabled:
            raise RuntimeError("La extensión debe estar habilitada primero")
        
        if self.started:
            logging.warning("Los sistemas autónomos ya están iniciados")
            return
        
        # Iniciar gestor de tareas
        self.task_manager.start()
        
        # Activar perfil predeterminado si no hay ninguno activo
        if not self.profile_manager.get_active_profile():
            self.profile_manager.activate_profile("Equilibrado")
        
        self.started = True
        logging.info("Sistemas autónomos iniciados")
        
        # Emitir evento de inicio
        self.event_system.emit(EventType.AGENT_STARTED, {
            "component": "autonomous_extension",
            "message": "Sistemas autónomos iniciados"
        })
    
    def stop(self):
        """Detiene los sistemas autónomos"""
        if not self.started:
            return
        
        # Detener gestor de tareas
        self.task_manager.stop()
        
        self.started = False
        logging.info("Sistemas autónomos detenidos")
        
        # Emitir evento de detención
        self.event_system.emit(EventType.AGENT_STOPPED, {
            "component": "autonomous_extension",
            "message": "Sistemas autónomos detenidos"
        })
    
    def schedule_autonomous_scan(self, target: str, scan_type: str = "quick", 
                               schedule_type: str = "once", interval: int = 3600) -> str:
        """
        Programa un escaneo autónomo
        Retorna el ID de la tarea programada
        """
        if not self.started:
            raise RuntimeError("Los sistemas autónomos deben estar iniciados")
        
        # Crear función de escaneo
        def scan_function():
            # Esta sería la implementación real usando las herramientas del agente
            # Por ahora simulamos un escaneo
            import time
            import random
            
            logging.info(f"Iniciando escaneo autónomo de {target} ({scan_type})")
            time.sleep(random.randint(2, 5))  # Simular tiempo de escaneo
            
            # Generar resultados simulados
            open_ports = random.sample([22, 80, 443, 3306, 5432, 8080], random.randint(1, 4))
            result = f"Escaneo completado. Puertos abiertos: {open_ports}"
            
            # Emitir evento de escaneo completado
            self.event_system.emit(EventType.SCAN_COMPLETED, {
                "target": target,
                "scan_type": scan_type,
                "result": result
            })
            
            return result
        
        # Programar la tarea
        task_id = self.task_manager.schedule_task(
            name=f"Escaneo Autónomo - {target}",
            description=f"Escaneo {scan_type} de {target}",
            function=scan_function,
            schedule_type=schedule_type,
            interval=interval
        )
        
        logging.info(f"Escaneo autónomo programado para {target} (ID: {task_id})")
        
        # Emitir evento de inicio de escaneo
        self.event_system.emit(EventType.SCAN_STARTED, {
            "target": target,
            "scan_type": scan_type,
            "task_id": task_id
        })
        
        return task_id
    
    def schedule_vulnerability_monitor(self, target: str, frequency: str = "daily") -> str:
        """
        Programa un monitor de vulnerabilidades
        Retorna el ID de la tarea programada
        """
        if not self.started:
            raise RuntimeError("Los sistemas autónomos deben estar iniciados")
        
        # Crear función de monitoreo
        def monitor_function():
            # Esta sería la implementación real
            # Por ahora simulamos un monitoreo
            import random
            
            logging.info(f"Monitoreando vulnerabilidades en {target}")
            
            # Simular detección de vulnerabilidades aleatoria
            vulnerabilities = []
            if random.random() > 0.7:  # 30% de probabilidad
                vulns = [
                    "Servidor web sin parches de seguridad",
                    "Versión desactualizada de OpenSSL",
                    "Configuración débil de SSH",
                    "Fallo de inyección SQL potencial"
                ]
                vulnerabilities = random.sample(vulns, random.randint(1, 2))
            
            if vulnerabilities:
                # Emitir eventos por cada vulnerabilidad encontrada
                for vuln in vulnerabilities:
                    self.event_system.emit(EventType.VULNERABILITY_FOUND, {
                        "target": target,
                        "vulnerability": vuln,
                        "severity": random.choice(["baja", "media", "alta"]),
                        "confidence": random.choice(["baja", "media", "alta"])
                    })
                
                result = f"Vulnerabilidades encontradas: {len(vulnerabilities)}"
            else:
                result = "No se encontraron vulnerabilidades críticas"
            
            return result
        
        # Programar la tarea
        schedule_map = {
            "hourly": ("interval", 3600),
            "daily": ("daily", 0),
            "weekly": ("weekly", 0)
        }
        
        schedule_type, interval = schedule_map.get(frequency, ("daily", 0))
        
        task_id = self.task_manager.schedule_task(
            name=f"Monitor de Vulnerabilidades - {target}",
            description=f"Monitoreo continuo de vulnerabilidades en {target}",
            function=monitor_function,
            schedule_type=schedule_type,
            interval=interval
        )
        
        logging.info(f"Monitor de vulnerabilidades programado para {target} (ID: {task_id})")
        return task_id
    
    def get_autonomous_status(self) -> Dict[str, Any]:
        """Obtiene el estado de los sistemas autónomos"""
        if not self.started:
            return {"status": "stopped", "message": "Sistemas autónomos detenidos"}
        
        # Obtener estado de tareas
        tasks = self.task_manager.list_tasks()
        active_tasks = [t for t in tasks if t["status"] in ["scheduled", "running"]]
        completed_tasks = [t for t in tasks if t["status"] == "completed"]
        failed_tasks = [t for t in tasks if t["status"] == "failed"]
        
        # Obtener perfil activo
        active_profile = self.profile_manager.get_active_profile()
        
        # Obtener últimos eventos
        recent_events = self.event_system.get_events(limit=10)
        
        return {
            "status": "running",
            "active_tasks": len(active_tasks),
            "completed_tasks": len(completed_tasks),
            "failed_tasks": len(failed_tasks),
            "active_profile": active_profile.name if active_profile else "ninguno",
            "recent_events": len(recent_events),
            "message": "Sistemas autónomos operativos"
        }
    
    def get_recent_events(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Obtiene eventos recientes"""
        events = self.event_system.get_events(limit=limit)
        return [event.to_dict() for event in events]
    
    def get_active_tasks(self) -> List[Dict[str, Any]]:
        """Obtiene tareas activas"""
        return self.task_manager.get_tasks_by_status("scheduled") + \
               self.task_manager.get_tasks_by_status("running")
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancela una tarea programada"""
        return self.task_manager.cancel_task(task_id)
    
    def set_behavior_profile(self, profile_name: str) -> bool:
        """Establece un perfil de comportamiento"""
        return self.profile_manager.activate_profile(profile_name)
    
    def get_behavior_profiles(self) -> List[Dict[str, str]]:
        """Obtiene lista de perfiles de comportamiento"""
        return self.profile_manager.list_profiles()

# Función para crear la extensión autónoma
def create_autonomous_extension(agent_config: Dict[str, Any]) -> Optional[AutonomousExtension]:
    """Crea una instancia de la extensión autónoma"""
    try:
        if AUTONOMY_AVAILABLE:
            return AutonomousExtension(agent_config)
        else:
            logging.warning("Módulos de autonomía no disponibles, extensión no creada")
            return None
    except Exception as e:
        logging.error(f"Error al crear extensión autónoma: {e}")
        return None

# Ejemplo de uso
if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Simular configuración del agente
    agent_config = {
        "autonomy": {
            "enabled": True,
            "default_profile": "balanced"
        }
    }
    
    try:
        # Crear extensión autónoma
        extension = create_autonomous_extension(agent_config)
        if extension:
            # Habilitar y empezar
            extension.enable()
            extension.start()
            
            # Programar algunas tareas
            task1 = extension.schedule_autonomous_scan("192.168.1.1", "quick", "interval", 60)
            task2 = extension.schedule_vulnerability_monitor("192.168.1.1", "daily")
            
            print(f"Tareas programadas: {task1}, {task2}")
            
            # Obtener estado
            status = extension.get_autonomous_status()
            print(f"Estado: {status}")
            
            # Listar perfiles
            profiles = extension.get_behavior_profiles()
            print("Perfiles disponibles:")
            for profile in profiles:
                print(f"  • {profile['name']} ({profile['mode']})")
            
            # Esperar un momento para ver algunos eventos
            import time
            time.sleep(10)
            
            # Obtener eventos recientes
            events = extension.get_recent_events(5)
            print(f"Últimos {len(events)} eventos:")
            for event in events:
                print(f"  • [{event['timestamp']}] {event['type']}: {event['data']}")
            
            # Detener la extensión
            extension.stop()
            extension.disable()
            
        else:
            print("❌ No se pudo crear la extensión autónoma")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()