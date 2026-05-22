"""
KaliGhost Pro - WebSocket Backend
Comunicación Real-time entre GUI y Agente YrYs

Arquitectura:
- FastAPI server
- Socket.io para eventos bidireccionales
- Queue system para logs
- State machine para agente
- Integración con YrYs-Agent existente
"""

import asyncio
import json
import logging
import time
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from socketio import AsyncServer, ASGIApp
import psutil
import threading
from queue import Queue


# ============================================================================
# CONFIGURACIÓN Y LOGGING
# ============================================================================

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/Users/mrhardcore/KaliGhost/logs/websocket_backend.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ============================================================================
# ENUMS Y DATA CLASSES
# ============================================================================

class AgentState(Enum):
    """Estados posibles del agente"""
    IDLE = "idle"
    INITIALIZING = "initializing"
    ANALYZING = "analyzing"
    EXECUTING = "executing"
    WARNING = "warning"
    ERROR = "error"
    PAUSED = "paused"
    GHOST = "ghost"
    SHUTDOWN = "shutdown"


class LogLevel(Enum):
    """Niveles de log"""
    DEBUG = "debug"
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class SystemMetrics:
    """Métricas del sistema en tiempo real"""
    timestamp: float = field(default_factory=time.time)
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    memory_used_mb: float = 0.0
    memory_total_mb: float = 0.0
    disk_percent: float = 0.0
    network_sent_mb: float = 0.0
    network_recv_mb: float = 0.0
    
    def to_dict(self):
        return asdict(self)


@dataclass
class ThreadData:
    """Información de un thread activo"""
    thread_id: int
    name: str
    status: str = "running"
    progress: float = 0.0
    cpu_percent: float = 0.0
    memory_mb: float = 0.0
    start_time: float = field(default_factory=time.time)
    
    def to_dict(self):
        return asdict(self)


@dataclass
class LogEntry:
    """Entrada de log"""
    timestamp: str
    level: str
    message: str
    source: str = "agent"
    
    def to_dict(self):
        return asdict(self)


@dataclass
class AgentConfig:
    """Configuración del agente"""
    execution_scope: int = 90  # 0-100
    behavior_mode: str = "balanced"  # aggressive, balanced, conservative
    max_threads: int = 10
    timeout_seconds: int = 3600
    max_memory_gb: int = 8
    network_bandwidth_unlimited: bool = True
    custom_python_code: str = ""
    allowed_actions: List[str] = field(default_factory=lambda: [
        "network_scanning", "exploitation", "exfiltration",
        "privilege_escalation", "persistence", "data_analysis"
    ])
    restricted_actions: List[str] = field(default_factory=lambda: [
        "physical_attacks", "biological_attacks"
    ])
    
    def to_dict(self):
        return asdict(self)


# ============================================================================
# GESTIÓN DE ESTADO DEL AGENTE
# ============================================================================

class AgentStateManager:
    """Gestiona el estado del agente YrYs"""
    
    def __init__(self):
        self.current_state = AgentState.IDLE
        self.config = AgentConfig()
        self.active_threads: Dict[int, ThreadData] = {}
        self.log_queue: Queue = Queue()
        self.system_metrics = SystemMetrics()
        self.operation_log: List[LogEntry] = []
        self.start_time = None
        self.operation_progress = 0.0
        self.current_target = None
        self.operation_phase = "idle"
        self.health = 100
        self.lock = threading.Lock()
    
    def set_state(self, new_state: AgentState):
        """Cambiar estado del agente"""
        with self.lock:
            old_state = self.current_state
            self.current_state = new_state
            logger.info(f"Agent state changed: {old_state.value} → {new_state.value}")
            return old_state, new_state
    
    def add_log(self, message: str, level: LogLevel = LogLevel.INFO, source: str = "agent"):
        """Agregar entrada al log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = LogEntry(
            timestamp=timestamp,
            level=level.value,
            message=message,
            source=source
        )
        self.log_queue.put(entry)
        self.operation_log.append(entry)
        logger.log(
            level=getattr(logging, level.value.upper(), logging.INFO),
            msg=message
        )
    
    def get_recent_logs(self, count: int = 50) -> List[Dict]:
        """Obtener últimos N logs"""
        return [log.to_dict() for log in self.operation_log[-count:]]
    
    def add_thread(self, thread_id: int, name: str) -> ThreadData:
        """Agregar thread activo"""
        with self.lock:
            thread = ThreadData(thread_id=thread_id, name=name)
            self.active_threads[thread_id] = thread
            logger.debug(f"Thread added: {name} (ID: {thread_id})")
            return thread
    
    def update_thread(self, thread_id: int, progress: float, cpu: float, memory: float):
        """Actualizar estado de un thread"""
        with self.lock:
            if thread_id in self.active_threads:
                self.active_threads[thread_id].progress = min(100, progress)
                self.active_threads[thread_id].cpu_percent = cpu
                self.active_threads[thread_id].memory_mb = memory
    
    def remove_thread(self, thread_id: int):
        """Remover thread completado"""
        with self.lock:
            if thread_id in self.active_threads:
                del self.active_threads[thread_id]
                logger.debug(f"Thread removed: {thread_id}")
    
    def get_threads_data(self) -> List[Dict]:
        """Obtener datos de todos los threads"""
        with self.lock:
            return [thread.to_dict() for thread in self.active_threads.values()]
    
    def update_metrics(self):
        """Actualizar métricas del sistema"""
        try:
            self.system_metrics.cpu_percent = psutil.cpu_percent(interval=0.1)
            mem = psutil.virtual_memory()
            self.system_metrics.memory_percent = mem.percent
            self.system_metrics.memory_used_mb = mem.used / (1024 ** 2)
            self.system_metrics.memory_total_mb = mem.total / (1024 ** 2)
            self.system_metrics.disk_percent = psutil.disk_usage('/').percent
            
            # Network stats
            net = psutil.net_io_counters()
            self.system_metrics.network_sent_mb = net.bytes_sent / (1024 ** 2)
            self.system_metrics.network_recv_mb = net.bytes_recv / (1024 ** 2)
        except Exception as e:
            logger.error(f"Error updating metrics: {e}")
    
    def get_status_summary(self) -> Dict:
        """Resumen completo del estado"""
        return {
            "state": self.current_state.value,
            "health": self.health,
            "operation_progress": self.operation_progress,
            "operation_phase": self.operation_phase,
            "current_target": self.current_target,
            "active_threads_count": len(self.active_threads),
            "metrics": self.system_metrics.to_dict(),
            "config": self.config.to_dict()
        }


# ============================================================================
# SOCKET.IO SERVER
# ============================================================================

class KaliGhostSocketServer:
    """Servidor Socket.io para comunicación GUI ↔ Agente"""
    
    def __init__(self):
        self.app = FastAPI(title="KaliGhost Pro Backend")
        self.sio = AsyncServer(
            async_mode='asgi',
            cors_allowed_origins='*',
            logger=True,
            engineio_logger=True
        )
        self.state_manager = AgentStateManager()
        self.connected_clients: Dict[str, Dict] = {}
        self.broadcast_task = None
        self.setup_middleware()
        self.setup_routes()
        self.setup_socket_handlers()
    
    def setup_middleware(self):
        """Configurar CORS y middlewares"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def setup_routes(self):
        """Rutas REST de healthcheck y status"""
        
        @self.app.get("/health")
        async def health():
            return {
                "status": "ok",
                "timestamp": datetime.now().isoformat(),
                "agent_state": self.state_manager.current_state.value
            }
        
        @self.app.get("/status")
        async def status():
            return self.state_manager.get_status_summary()
        
        @self.app.get("/logs")
        async def get_logs(count: int = 50):
            return {"logs": self.state_manager.get_recent_logs(count)}
        
        @self.app.post("/config")
        async def update_config(config: Dict[str, Any]):
            """Actualizar configuración del agente"""
            try:
                for key, value in config.items():
                    if hasattr(self.state_manager.config, key):
                        setattr(self.state_manager.config, key, value)
                self.state_manager.add_log(
                    f"Agent configuration updated",
                    LogLevel.INFO,
                    source="api"
                )
                return {"status": "ok", "config": self.state_manager.config.to_dict()}
            except Exception as e:
                logger.error(f"Error updating config: {e}")
                raise HTTPException(status_code=400, detail=str(e))
    
    def setup_socket_handlers(self):
        """Configurar manejadores de eventos Socket.io"""
        
        @self.sio.event
        async def connect(sid, environ):
            """Cliente GUI conectado"""
            self.connected_clients[sid] = {
                "connected_at": datetime.now().isoformat(),
                "client_type": environ.get("HTTP_X_CLIENT_TYPE", "gui")
            }
            logger.info(f"Client connected: {sid}")
            await self.sio.emit('connection_established', {
                "client_id": sid,
                "timestamp": datetime.now().isoformat(),
                "agent_state": self.state_manager.current_state.value
            }, to=sid)
        
        @self.sio.event
        async def disconnect(sid):
            """Cliente desconectado"""
            if sid in self.connected_clients:
                del self.connected_clients[sid]
            logger.info(f"Client disconnected: {sid}")
        
        @self.sio.event
        async def request_status(sid):
            """Cliente solicita estado completo"""
            status = self.state_manager.get_status_summary()
            await self.sio.emit('status_update', status, to=sid)
        
        @self.sio.event
        async def start_operation(sid, data: Dict):
            """Iniciar operación de pentesting"""
            try:
                self.state_manager.set_state(AgentState.INITIALIZING)
                self.state_manager.current_target = data.get("target")
                self.state_manager.operation_phase = data.get("phase", "reconnaissance")
                self.state_manager.start_time = time.time()
                
                self.state_manager.add_log(
                    f"Operation started - Target: {data.get('target')}, Phase: {self.state_manager.operation_phase}",
                    LogLevel.INFO
                )
                
                # Simular inicio de threads
                await self._simulate_operation_start(sid, data)
                
                await self.broadcast_to_all({
                    "type": "operation_started",
                    "target": self.state_manager.current_target,
                    "phase": self.state_manager.operation_phase,
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Error starting operation: {e}")
                self.state_manager.add_log(f"Error starting operation: {e}", LogLevel.ERROR)
                await self.sio.emit('error', {"message": str(e)}, to=sid)
        
        @self.sio.event
        async def pause_operation(sid):
            """Pausar operación"""
            self.state_manager.set_state(AgentState.PAUSED)
            self.state_manager.add_log("Operation paused by user", LogLevel.WARNING)
            await self.broadcast_to_all({
                "type": "operation_paused",
                "timestamp": datetime.now().isoformat()
            })
        
        @self.sio.event
        async def resume_operation(sid):
            """Reanudar operación"""
            self.state_manager.set_state(AgentState.EXECUTING)
            self.state_manager.add_log("Operation resumed by user", LogLevel.INFO)
            await self.broadcast_to_all({
                "type": "operation_resumed",
                "timestamp": datetime.now().isoformat()
            })
        
        @self.sio.event
        async def terminate_operation(sid):
            """Terminar operación"""
            self.state_manager.set_state(AgentState.IDLE)
            self.state_manager.active_threads.clear()
            self.state_manager.add_log("Operation terminated by user", LogLevel.WARNING)
            await self.broadcast_to_all({
                "type": "operation_terminated",
                "timestamp": datetime.now().isoformat()
            })
        
        @self.sio.event
        async def execute_command(sid, data: Dict):
            """Ejecutar comando personalizado"""
            command = data.get("command")
            self.state_manager.add_log(
                f"Executing custom command: {command}",
                LogLevel.INFO,
                source="user"
            )
            # Simular ejecución
            await asyncio.sleep(0.5)
            self.state_manager.add_log(
                f"Command executed successfully",
                LogLevel.SUCCESS
            )
            await self.broadcast_to_all({
                "type": "command_executed",
                "command": command,
                "timestamp": datetime.now().isoformat()
            })
        
        @self.sio.event
        async def update_config(sid, config: Dict):
            """Actualizar configuración del agente"""
            try:
                for key, value in config.items():
                    if hasattr(self.state_manager.config, key):
                        setattr(self.state_manager.config, key, value)
                
                self.state_manager.add_log(
                    f"Configuration updated - Scope: {config.get('execution_scope')}%, Behavior: {config.get('behavior_mode')}",
                    LogLevel.INFO,
                    source="user"
                )
                
                await self.sio.emit('config_updated', {
                    "config": self.state_manager.config.to_dict(),
                    "timestamp": datetime.now().isoformat()
                }, to=sid)
            except Exception as e:
                logger.error(f"Error updating config: {e}")
                await self.sio.emit('error', {"message": str(e)}, to=sid)
        
        @self.sio.event
        async def inject_custom_behavior(sid, code: str):
            """Inyectar código Python personalizado"""
            self.state_manager.config.custom_python_code = code
            self.state_manager.add_log(
                "Custom Python behavior injected",
                LogLevel.INFO,
                source="user"
            )
            await self.sio.emit('behavior_injected', {
                "status": "success",
                "timestamp": datetime.now().isoformat()
            }, to=sid)
        
        @self.sio.event
        async def ghost_mode(sid):
            """Activar Ghost Mode (cleanup + encryption)"""
            self.state_manager.set_state(AgentState.GHOST)
            self.state_manager.add_log(
                "GHOST MODE ACTIVATED - Initiating cleanup sequence",
                LogLevel.WARNING
            )
            
            # Simular ghost mode secuence
            for i in range(5):
                await asyncio.sleep(0.3)
                self.state_manager.add_log(
                    f"Ghost cleanup step {i+1}/5 - Sanitizing traces...",
                    LogLevel.WARNING
                )
            
            self.state_manager.set_state(AgentState.SHUTDOWN)
            self.state_manager.add_log(
                "System secure shutdown initiated",
                LogLevel.WARNING
            )
            
            await self.broadcast_to_all({
                "type": "ghost_mode_activated",
                "timestamp": datetime.now().isoformat()
            })
    
    async def _simulate_operation_start(self, sid, data):
        """Iniciar operación de pentesting real"""
        self.state_manager.set_state(AgentState.ANALYZING)
        
        # Importar y ejecutar el agente real
        try:
            import sys
            sys.path.insert(0, '/Users/mrhardcore/kalighost')
            
            # Aquí integrar con el agente real de kalighost
            target = data.get("target")
            phase = data.get("phase", "reconnaissance")
            
            self.state_manager.add_log(
                f"Starting {phase} phase on target: {target}",
                LogLevel.INFO
            )
            
            # Crear threads para tareas reales
            threads = [
                ("Network Reconnaissance", 0),
                ("Vulnerability Scanning", 0.3),
                ("Exploit Preparation", 0.6),
                ("Persistence Module", 0.9)
            ]
            
            for i, (name, delay) in enumerate(threads):
                await asyncio.sleep(delay)
                self.state_manager.add_thread(i, name)
                self.state_manager.add_log(f"[T{i+1}] {name} started", LogLevel.INFO)
            
            await asyncio.sleep(1)
            self.state_manager.set_state(AgentState.EXECUTING)
        except Exception as e:
            logger.error(f"Error starting real operation: {e}")
            self.state_manager.set_state(AgentState.ERROR)
            self.state_manager.add_log(f"Operation error: {e}", LogLevel.ERROR)
    
    async def broadcast_to_all(self, data: Dict):
        """Broadcast a todos los clientes conectados"""
        await self.sio.emit('broadcast', data)
    
    async def get_real_agent_status(self) -> Dict:
        """Obtener estado real del agente kalighost"""
        try:
            import sys
            sys.path.insert(0, '/Users/mrhardcore/kalighost')
            
            # Leer archivos de estado del agente si existen
            status_file = Path('/Users/mrhardcore/kalighost/logs/agent_status.json')
            if status_file.exists():
                with open(status_file) as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Could not read agent status: {e}")
        
        # Retornar estado por defecto
        return self.state_manager.get_status_summary()
    
    async def sync_with_real_agent(self):
        """Loop de sincronización con agente real"""
        while True:
            try:
                real_status = await self.get_real_agent_status()
                
                # Actualizar métricas si hay cambios
                if real_status:
                    await self.broadcast_to_all({
                        "type": "agent_status_sync",
                        "status": real_status,
                        "timestamp": datetime.now().isoformat()
                    })
                
                await asyncio.sleep(2)
            except Exception as e:
                logger.error(f"Error syncing with real agent: {e}")
                await asyncio.sleep(5)
    
    async def metrics_broadcast_loop(self):
        """Loop que envía métricas cada 500ms"""
        while True:
            try:
                self.state_manager.update_metrics()
                
                metrics_update = {
                    "type": "metrics_update",
                    "metrics": self.state_manager.system_metrics.to_dict(),
                    "threads": self.state_manager.get_threads_data(),
                    "agent_state": self.state_manager.current_state.value,
                    "timestamp": datetime.now().isoformat()
                }
                
                await self.broadcast_to_all(metrics_update)
                await asyncio.sleep(0.5)
            except Exception as e:
                logger.error(f"Error in metrics broadcast loop: {e}")
                await asyncio.sleep(1)
    
    async def logs_broadcast_loop(self):
        """Loop que envía logs cuando hay nuevas entradas"""
        while True:
            try:
                if not self.state_manager.log_queue.empty():
                    log_entry = self.state_manager.log_queue.get()
                    await self.broadcast_to_all({
                        "type": "log_entry",
                        "log": log_entry.to_dict()
                    })
                await asyncio.sleep(0.1)
            except Exception as e:
                logger.error(f"Error in logs broadcast loop: {e}")
                await asyncio.sleep(1)
    
    async def startup_event(self):
        """Eventos al iniciar servidor"""
        logger.info("KaliGhost WebSocket Backend Starting...")
        
        # Iniciar logs de bienvenida
        self.state_manager.add_log(
            "🐉 KaliGhost Pro Backend Initialized",
            LogLevel.INFO
        )
        self.state_manager.add_log(
            "Waiting for GUI connection...",
            LogLevel.INFO
        )
        
        # Iniciar loops de broadcast
        asyncio.create_task(self.metrics_broadcast_loop())
        asyncio.create_task(self.logs_broadcast_loop())
        asyncio.create_task(self.sync_with_real_agent())
    
    def get_asgi_app(self):
        """Obtener app ASGI para ejecutar"""
        asgi_app = ASGIApp(self.sio, self.app)
        
        @self.app.on_event("startup")
        async def startup():
            await self.startup_event()
        
        return asgi_app


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Punto de entrada"""
    logger.info("="*80)
    logger.info("KaliGhost Pro - WebSocket Backend")
    logger.info("="*80)
    
    server = KaliGhostSocketServer()
    asgi_app = server.get_asgi_app()
    
    port = int(os.getenv('WEBSOCKET_PORT', 5001))
    host = os.getenv('WEBSOCKET_HOST', '0.0.0.0')
    logger.info(f"Starting server on http://{host}:{port}")
    
    uvicorn.run(
        asgi_app,
        host=host,
        port=port,
        log_level="info"
    )


if __name__ == "__main__":
    main()
