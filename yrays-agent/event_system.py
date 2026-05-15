#!/usr/bin/env python3
"""
Sistema de Eventos y Notificaciones para YrYs-Agent
Permite la comunicación entre componentes y notificaciones de eventos importantes
"""

import logging
import json
import threading
from typing import Dict, List, Callable, Any
from datetime import datetime
from enum import Enum

class EventType(Enum):
    """Tipos de eventos del sistema"""
    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"
    SCAN_STARTED = "scan_started"
    SCAN_COMPLETED = "scan_completed"
    VULNERABILITY_FOUND = "vulnerability_found"
    SYSTEM_ALERT = "system_alert"
    TOOL_EXECUTION = "tool_execution"
    SKILL_CREATED = "skill_created"
    AGENT_STARTED = "agent_started"
    AGENT_STOPPED = "agent_stopped"

class Event:
    """Representa un evento del sistema"""
    
    def __init__(self, event_type: EventType, data: Dict[str, Any] = None, timestamp: datetime = None):
        self.id = f"evt_{int(datetime.now().timestamp() * 1000000)}"
        self.type = event_type
        self.data = data or {}
        self.timestamp = timestamp or datetime.now()
        self.handled = False
    
    def to_dict(self) -> Dict:
        """Convierte el evento a diccionario"""
        return {
            "id": self.id,
            "type": self.type.value,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
            "handled": self.handled
        }

class EventHandler:
    """Manejador de eventos"""
    
    def __init__(self, name: str, callback: Callable[[Event], None]):
        self.name = name
        self.callback = callback
        self.active = True
    
    def handle(self, event: Event):
        """Maneja un evento"""
        if self.active:
            try:
                self.callback(event)
            except Exception as e:
                logging.error(f"Error en manejador {self.name}: {e}")

class EventSystem:
    """Sistema central de eventos y notificaciones"""
    
    def __init__(self):
        self.handlers: Dict[EventType, List[EventHandler]] = {}
        self.event_history: List[Event] = []
        self.max_history = 1000
        self.lock = threading.Lock()
        
        logging.info("Sistema de eventos inicializado")
    
    def subscribe(self, event_type: EventType, handler_name: str, 
                  callback: Callable[[Event], None]) -> EventHandler:
        """Suscribe un manejador a un tipo de evento"""
        with self.lock:
            if event_type not in self.handlers:
                self.handlers[event_type] = []
            
            handler = EventHandler(handler_name, callback)
            self.handlers[event_type].append(handler)
            logging.debug(f"Suscriptor añadido: {handler_name} para {event_type.value}")
            return handler
    
    def unsubscribe(self, event_type: EventType, handler: EventHandler):
        """Desuscribe un manejador de un tipo de evento"""
        with self.lock:
            if event_type in self.handlers:
                if handler in self.handlers[event_type]:
                    self.handlers[event_type].remove(handler)
                    logging.debug(f"Suscriptor eliminado: {handler.name} para {event_type.value}")
    
    def emit(self, event_type: EventType, data: Dict[str, Any] = None) -> Event:
        """Emite un evento"""
        event = Event(event_type, data)
        
        # Añadir al historial
        with self.lock:
            self.event_history.append(event)
            if len(self.event_history) > self.max_history:
                self.event_history.pop(0)
        
        # Notificar a los manejadores
        if event_type in self.handlers:
            for handler in self.handlers[event_type]:
                try:
                    handler.handle(event)
                except Exception as e:
                    logging.error(f"Error notificando a {handler.name}: {e}")
        
        logging.debug(f"Evento emitido: {event_type.value}")
        return event
    
    def get_events(self, event_type: EventType = None, limit: int = 50) -> List[Event]:
        """Obtiene eventos del historial"""
        with self.lock:
            if event_type:
                events = [e for e in self.event_history if e.type == event_type]
            else:
                events = self.event_history[:]
            
            return events[-limit:]  # Últimos N eventos
    
    def get_event_count(self, event_type: EventType = None) -> int:
        """Obtiene el conteo de eventos"""
        with self.lock:
            if event_type:
                return len([e for e in self.event_history if e.type == event_type])
            else:
                return len(self.event_history)

# Sistema global de eventos
global_event_system = EventSystem()

def get_event_system() -> EventSystem:
    """Obtiene el sistema de eventos global"""
    return global_event_system

# Decoradores para eventos comunes
def on_task_completed(callback: Callable[[Event], None]):
    """Decorador para suscribirse a eventos de tarea completada"""
    return global_event_system.subscribe(EventType.TASK_COMPLETED, callback.__name__, callback)

def on_vulnerability_found(callback: Callable[[Event], None]):
    """Decorador para suscribirse a eventos de vulnerabilidad encontrada"""
    return global_event_system.subscribe(EventType.VULNERABILITY_FOUND, callback.__name__, callback)

def on_system_alert(callback: Callable[[Event], None]):
    """Decorador para suscribirse a eventos de alerta del sistema"""
    return global_event_system.subscribe(EventType.SYSTEM_ALERT, callback.__name__, callback)

# Manejadores de eventos predeterminados
def default_task_completion_handler(event: Event):
    """Manejador predeterminado para tareas completadas"""
    task_name = event.data.get("task_name", "desconocida")
    result = event.data.get("result", "sin resultado")
    logging.info(f"✅ Tarea completada: {task_name}")
    logging.debug(f"   Resultado: {result}")

def default_vulnerability_handler(event: Event):
    """Manejador predeterminado para vulnerabilidades encontradas"""
    target = event.data.get("target", "desconocido")
    vulnerability = event.data.get("vulnerability", "sin especificar")
    severity = event.data.get("severity", "media")
    
    logging.warning(f"⚠️ Vulnerabilidad encontrada en {target}: {vulnerability} (Gravedad: {severity})")

def default_system_alert_handler(event: Event):
    """Manejador predeterminado para alertas del sistema"""
    message = event.data.get("message", "Alerta sin mensaje")
    level = event.data.get("level", "info")
    
    if level == "critical":
        logging.critical(f"🚨 ALERTA CRÍTICA: {message}")
    elif level == "warning":
        logging.warning(f"⚠️ ALERTA: {message}")
    else:
        logging.info(f"ℹ️  Alerta: {message}")

# Registrar manejadores predeterminados
global_event_system.subscribe(EventType.TASK_COMPLETED, "default_task_handler", default_task_completion_handler)
global_event_system.subscribe(EventType.VULNERABILITY_FOUND, "default_vuln_handler", default_vulnerability_handler)
global_event_system.subscribe(EventType.SYSTEM_ALERT, "default_alert_handler", default_system_alert_handler)

# Ejemplo de uso
if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Emitir algunos eventos de ejemplo
    event_system = get_event_system()
    
    # Emitir evento de tarea completada
    event_system.emit(EventType.TASK_COMPLETED, {
        "task_name": "Escaneo de Red",
        "result": "8 puertos abiertos encontrados",
        "duration": "45 segundos"
    })
    
    # Emitir evento de vulnerabilidad
    event_system.emit(EventType.VULNERABILITY_FOUND, {
        "target": "192.168.1.100",
        "vulnerability": "Servidor SSH con versión desactualizada",
        "severity": "alta",
        "details": "OpenSSH 7.2p2"
    })
    
    # Emitir alerta del sistema
    event_system.emit(EventType.SYSTEM_ALERT, {
        "message": "Uso de CPU alto detectado",
        "level": "warning",
        "component": "scanner_worker"
    })
    
    # Mostrar historial de eventos
    events = event_system.get_events(limit=10)
    print(f"\n📊 Historial de eventos ({len(events)} eventos):")
    for event in events:
        print(f"  • [{event.timestamp.strftime('%H:%M:%S')}] {event.type.value}: {event.data}")