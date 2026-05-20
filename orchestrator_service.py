#!/usr/bin/env python3
"""
Servicio de orquestación de agentes para KaliGhost
"""

import sys
import os
import json
import time
import uuid
import logging
import threading
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('yrays-agent/logs/orchestrator.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class AgentRegistry:
    """Registro de agentes disponibles"""
    
    def __init__(self):
        self.agents = {}
        self.agent_health = {}
        
    def register_agent(self, agent_id, capabilities, address):
        """Registrar un nuevo agente"""
        self.agents[agent_id] = {
            'capabilities': capabilities,
            'address': address,
            'registered_at': datetime.now(),
            'last_seen': datetime.now()
        }
        self.agent_health[agent_id] = {
            'status': 'online',
            'last_check': datetime.now()
        }
        logger.info(f"Agente registrado: {agent_id} con capacidades {capabilities}")
        
    def unregister_agent(self, agent_id):
        """Eliminar registro de agente"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            del self.agent_health[agent_id]
            logger.info(f"Agente eliminado: {agent_id}")
            
    def update_agent_health(self, agent_id, status):
        """Actualizar estado de salud del agente"""
        if agent_id in self.agent_health:
            self.agent_health[agent_id]['status'] = status
            self.agent_health[agent_id]['last_check'] = datetime.now()
            self.agents[agent_id]['last_seen'] = datetime.now()
            
    def get_available_agents(self, capability=None):
        """Obtener agentes disponibles con una capacidad específica"""
        available = []
        for agent_id, info in self.agents.items():
            if self.agent_health[agent_id]['status'] == 'online':
                if capability is None or capability in info['capabilities']:
                    available.append(agent_id)
        return available
        
    def get_agent_info(self, agent_id):
        """Obtener información de un agente"""
        return self.agents.get(agent_id, None)

class WorkflowManager:
    """Gestor de flujos de trabajo"""
    
    def __init__(self, agent_registry):
        self.agent_registry = agent_registry
        self.workflows = {}
        self.workflow_status = {}
        
    def create_workflow(self, name, tasks):
        """Crear un nuevo flujo de trabajo"""
        workflow_id = str(uuid.uuid4())
        self.workflows[workflow_id] = {
            'name': name,
            'tasks': tasks,
            'created_at': datetime.now(),
            'status': 'pending'
        }
        self.workflow_status[workflow_id] = {
            'task_statuses': {task['id']: 'pending' for task in tasks},
            'started_at': None,
            'completed_at': None
        }
        logger.info(f"Workflow creado: {workflow_id} ({name})")
        return workflow_id
        
    def start_workflow(self, workflow_id):
        """Iniciar ejecución de un flujo de trabajo"""
        if workflow_id not in self.workflows:
            logger.error(f"Workflow no encontrado: {workflow_id}")
            return False
            
        workflow = self.workflows[workflow_id]
        workflow['status'] = 'running'
        self.workflow_status[workflow_id]['started_at'] = datetime.now()
        
        logger.info(f"Iniciando workflow: {workflow_id} ({workflow['name']})")
        
        # Ejecutar tareas en orden
        for task in workflow['tasks']:
            task_id = task['id']
            self.workflow_status[workflow_id]['task_statuses'][task_id] = 'running'
            
            # Asignar tarea a un agente apropiado
            agent_id = self.assign_task_to_agent(task)
            if agent_id:
                logger.info(f"Tarea {task_id} asignada a agente {agent_id}")
                # Aquí iría la lógica real de asignación de tareas
                # Por ahora simulamos la ejecución
                time.sleep(1)
                self.workflow_status[workflow_id]['task_statuses'][task_id] = 'completed'
            else:
                logger.error(f"No se encontró agente para tarea {task_id}")
                self.workflow_status[workflow_id]['task_statuses'][task_id] = 'failed'
                
        # Marcar workflow como completado
        workflow['status'] = 'completed'
        self.workflow_status[workflow_id]['completed_at'] = datetime.now()
        logger.info(f"Workflow completado: {workflow_id} ({workflow['name']})")
        return True
        
    def assign_task_to_agent(self, task):
        """Asignar tarea a un agente disponible"""
        # Buscar agentes con la capacidad requerida
        required_capability = task.get('capability', 'general')
        available_agents = self.agent_registry.get_available_agents(required_capability)
        
        if not available_agents:
            return None
            
        # Por ahora seleccionamos el primero disponible
        # En una implementación real, se podría usar un algoritmo más sofisticado
        return available_agents[0]
        
    def get_workflow_status(self, workflow_id):
        """Obtener estado de un workflow"""
        return {
            'workflow': self.workflows.get(workflow_id, None),
            'status': self.workflow_status.get(workflow_id, None)
        }

class MessageQueue:
    """Sistema de mensajería entre agentes"""
    
    def __init__(self):
        self.queues = defaultdict(list)
        self.lock = threading.Lock()
        
    def send_message(self, recipient, message):
        """Enviar mensaje a un destinatario"""
        with self.lock:
            self.queues[recipient].append(message)
            logger.debug(f"Mensaje enviado a {recipient}: {message}")
            
    def receive_messages(self, recipient):
        """Recibir mensajes para un destinatario"""
        with self.lock:
            messages = self.queues[recipient][:]
            self.queues[recipient].clear()
            return messages

class AgentOrchestrator:
    """Orquestador principal de agentes"""
    
    def __init__(self):
        self.agent_registry = AgentRegistry()
        self.workflow_manager = WorkflowManager(self.agent_registry)
        self.message_queue = MessageQueue()
        self.running = False
        
    def start(self):
        """Iniciar el servicio de orquestación"""
        logger.info("🚀 Iniciando servicio de orquestación de agentes...")
        self.running = True
        
        # Crear directorios necesarios
        Path("orchestrator/workflows").mkdir(parents=True, exist_ok=True)
        Path("orchestrator/logs").mkdir(parents=True, exist_ok=True)
        
        # Registrar agentes de ejemplo
        self.register_sample_agents()
        
        # Crear workflows de ejemplo
        self.create_sample_workflows()
        
        logger.info("✅ Servicio de orquestación iniciado")
        logger.info("📊 Dashboard disponible en http://localhost:8080")
        
        # Simular ejecución continua
        try:
            while self.running:
                self.monitor_agents()
                time.sleep(10)
        except KeyboardInterrupt:
            logger.info("\n👋 Servicio de orquestación detenido")
            
    def stop(self):
        """Detener el servicio de orquestación"""
        self.running = False
        
    def register_sample_agents(self):
        """Registrar agentes de ejemplo"""
        self.agent_registry.register_agent(
            "yrays-primary",
            ["pentest", "scanning", "analysis"],
            "localhost:9001"
        )
        
        self.agent_registry.register_agent(
            "yrays-secondary",
            ["pentest", "reporting"],
            "localhost:9002"
        )
        
        self.agent_registry.register_agent(
            "yrays-monitor",
            ["monitoring", "alerting"],
            "localhost:9003"
        )
        
    def create_sample_workflows(self):
        """Crear workflows de ejemplo"""
        # Workflow de escaneo completo
        scan_tasks = [
            {
                "id": "network-discovery",
                "name": "Descubrimiento de red",
                "capability": "scanning",
                "parameters": {"target": "192.168.1.0/24"}
            },
            {
                "id": "vulnerability-assessment",
                "name": "Evaluación de vulnerabilidades",
                "capability": "pentest",
                "parameters": {"target": "discovered_hosts"}
            },
            {
                "id": "report-generation",
                "name": "Generación de informe",
                "capability": "reporting",
                "parameters": {"data": "scan_results"}
            }
        ]
        
        workflow_id = self.workflow_manager.create_workflow(
            "Escaneo de red completo",
            scan_tasks
        )
        
        logger.info(f"Workflow de ejemplo creado: {workflow_id}")
        
    def monitor_agents(self):
        """Monitorear estado de agentes"""
        for agent_id in self.agent_registry.agents:
            # Simular verificación de salud
            import random
            health_status = "online" if random.random() > 0.1 else "offline"
            self.agent_registry.update_agent_health(agent_id, health_status)
            
        logger.debug("Agentes monitoreados")
        
    def get_system_status(self):
        """Obtener estado general del sistema"""
        return {
            "agents": len(self.agent_registry.agents),
            "online_agents": len([
                agent_id for agent_id in self.agent_registry.agent_health 
                if self.agent_registry.agent_health[agent_id]['status'] == 'online'
            ]),
            "workflows": len(self.workflow_manager.workflows),
            "active_workflows": len([
                wf_id for wf_id in self.workflow_manager.workflows
                if self.workflow_manager.workflows[wf_id]['status'] == 'running'
            ])
        }

def main():
    """Función principal del servicio de orquestación"""
    logger.info("🔧 Iniciando sistema de orquestación de agentes para KaliGhost...")
    
    try:
        # Inicializar orquestador
        orchestrator = AgentOrchestrator()
        
        # Iniciar servicio
        orchestrator.start()
        
    except Exception as e:
        logger.error(f"❌ Error grave en el sistema de orquestación: {e}")
        return False
        
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)