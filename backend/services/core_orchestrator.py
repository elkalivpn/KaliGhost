"""
KaliGhost 4.0 ULTIMATE - Core Orchestrator
Orquestador central de todos los módulos del sistema
Nivel: Elite - Multi-agente, autónomo, auto-aprendizaje
"""

import os
import json
import hashlib
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
import logging
import sqlite3
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SystemStatus:
    """Estado del sistema"""
    status: str  # active, standby, emergency, maintenance
    active_modules: List[str]
    memory_usage: float
    cpu_usage: float
    active_operations: int
    timestamp: str


@dataclass
class OperationResult:
    """Resultado de operación"""
    success: bool
    operation_id: str
    module: str
    action: str
    result: Any
    duration: float
    timestamp: str


class CoreOrchestrator:
    """
    Orquestador Central de KaliGhost 4.0 ULTIMATE
    - Coordina todos los módulos del sistema
    - Gestión de memoria y aprendizaje persistente
    - Planificación de operaciones multi-agente
    - Respuesta automática a eventos
    """
    
    def __init__(self, db_path: str = "kalighost_core.db"):
        self.db_path = db_path
        self.modules: Dict[str, Any] = {}
        self.active_operations: Dict[str, OperationResult] = {}
        self.operation_history: List[Dict] = []
        self.system_status = SystemStatus(
            status="active",
            active_modules=[],
            memory_usage=0.0,
            cpu_usage=0.0,
            active_operations=0,
            timestamp=datetime.now().isoformat()
        )
        
        # Inicializar base de datos
        self._init_database()
        
        # Registrar módulos disponibles
        self._register_modules()
    
    def _init_database(self):
        """Inicializa base de datos SQLite para memoria persistente"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de operaciones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS operations (
                id TEXT PRIMARY KEY,
                module TEXT,
                action TEXT,
                result TEXT,
                duration REAL,
                timestamp TEXT
            )
        ''')
        
        # Tabla de aprendizaje
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern TEXT,
                response TEXT,
                success_rate REAL,
                created_at TEXT
            )
        ''')
        
        # Tabla de configuración
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Base de datos inicializada")
    
    def _register_modules(self):
        """Registra todos los módulos disponibles"""
        available_modules = {
            'red_team': 'Red Team Operations',
            'purple_team': 'Purple Team Simulation',
            'blue_team': 'Blue Team Defense',
            'grey_team': 'Grey Team Covert Ops',
            'sandbox': 'Sandbox Engine',
            'payload_generator': 'Payload Generator',
            'ram_execution': 'RAM Execution',
            'steganography': 'Steganography Engine',
            'forensics': 'Digital Forensics',
            'network_routing': 'Network Routing',
            'emergency_response': 'Emergency Response'
        }
        
        for module_id, description in available_modules.items():
            try:
                module = self._load_module(module_id)
                if module:
                    self.modules[module_id] = {
                        'instance': module,
                        'description': description,
                        'status': 'ready'
                    }
                    logger.info(f"Módulo registrado: {module_id}")
            except Exception as e:
                logger.warning(f"No se pudo cargar módulo {module_id}: {e}")
        
        self.system_status.active_modules = list(self.modules.keys())
    
    def _load_module(self, module_id: str) -> Optional[Any]:
        """Carga dinámicamente un módulo"""
        try:
            module_name = f"backend.services.{module_id}"
            if module_id == 'sandbox':
                module_name = "backend.services.sandbox_engine"
            elif module_id == 'payload_generator':
                module_name = "backend.services.payload_generator"
            elif module_id == 'ram_execution':
                module_name = "backend.services.ram_execution"
            elif module_id == 'steganography':
                module_name = "backend.services.steganography"
            
            # Importar función getter del módulo
            parts = module_name.split('.')
            module = __import__(module_name, fromlist=[parts[-1]])
            getter_func = getattr(module, f'get_{module_id.replace("_", "_")}_engine', None)
            
            if getter_func:
                return getter_func()
            else:
                # Intentar con nombre alternativo
                getter_func = getattr(module, f'get_{parts[-1]}', None)
                if getter_func:
                    return getter_func()
                
        except ImportError as e:
            logger.debug(f"ImportError para {module_id}: {e}")
        except Exception as e:
            logger.debug(f"Error cargando {module_id}: {e}")
        
        return None
    
    def execute_operation(self, 
                       module_id: str,
                       action: str,
                       params: Dict[str, Any]) -> OperationResult:
        """Ejecuta una operación en un módulo específico"""
        
        if module_id not in self.modules:
            raise ValueError(f"Módulo {module_id} no disponible")
        
        operation_id = hashlib.sha256(
            f"{datetime.now().isoformat()}{os.urandom(8).hex()}".encode()
        ).hexdigest()[:16]
        
        start_time = datetime.now()
        
        try:
            module = self.modules[module_id]['instance']
            
            # Ejecutar acción según módulo
            if hasattr(module, action):
                method = getattr(module, action)
                result = method(**params)
            else:
                raise AttributeError(f"Acción {action} no disponible en {module_id}")
            
            duration = (datetime.now() - start_time).total_seconds()
            
            op_result = OperationResult(
                success=True,
                operation_id=operation_id,
                module=module_id,
                action=action,
                result=result,
                duration=duration,
                timestamp=datetime.now().isoformat()
            )
            
            # Guardar en historial
            self._save_operation(op_result)
            self.active_operations[operation_id] = op_result
            
            logger.info(f"Operación completada: {module_id}.{action} ({duration:.2f}s)")
            return op_result
            
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            
            op_result = OperationResult(
                success=False,
                operation_id=operation_id,
                module=module_id,
                action=action,
                result=str(e),
                duration=duration,
                timestamp=datetime.now().isoformat()
            )
            
            self._save_operation(op_result)
            logger.error(f"Operación fallida: {module_id}.{action} - {e}")
            return op_result
    
    def _save_operation(self, result: OperationResult):
        """Guarda operación en base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO operations (id, module, action, result, duration, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            result.operation_id,
            result.module,
            result.action,
            json.dumps(result.result) if not isinstance(result.result, str) else result.result,
            result.duration,
            result.timestamp
        ))
        
        conn.commit()
        conn.close()
        
        self.operation_history.append(asdict(result))
    
    def get_system_status(self) -> SystemStatus:
        """Obtiene estado actual del sistema"""
        self.system_status.active_operations = len(self.active_operations)
        self.system_status.timestamp = datetime.now().isoformat()
        self.system_status.status = "active"
        return self.system_status
    
    def learn_pattern(self, pattern: str, response: str, success: bool):
        """Registra patrón de aprendizaje"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Obtener tasa de éxito anterior
        cursor.execute('SELECT success_rate FROM learning WHERE pattern = ?', (pattern,))
        row = cursor.fetchone()
        
        if row:
            old_rate = row[0]
            new_rate = old_rate * 0.9 + (1.0 if success else 0.0) * 0.1
            cursor.execute('UPDATE learning SET success_rate = ? WHERE pattern = ?', 
                          (new_rate, pattern))
        else:
            cursor.execute('''
                INSERT INTO learning (pattern, response, success_rate, created_at)
                VALUES (?, ?, ?, ?)
            ''', (pattern, response, 1.0 if success else 0.0, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def query_learning(self, pattern: str) -> Optional[str]:
        """Consulta patrón aprendido"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT response FROM learning 
            WHERE pattern LIKE ? 
            ORDER BY success_rate DESC 
            LIMIT 1
        ''', (f'%{pattern}%',))
        
        row = cursor.fetchone()
        conn.close()
        
        return row[0] if row else None
    
    def get_module_info(self, module_id: str) -> Optional[Dict]:
        """Obtiene información de un módulo"""
        if module_id not in self.modules:
            return None
        
        return {
            'id': module_id,
            'description': self.modules[module_id]['description'],
            'status': self.modules[module_id]['status'],
            'available_actions': self._get_module_actions(module_id)
        }
    
    def _get_module_actions(self, module_id: str) -> List[str]:
        """Obtiene acciones disponibles de un módulo"""
        if module_id not in self.modules:
            return []
        
        module = self.modules[module_id]['instance']
        actions = [m for m in dir(module) if not m.startswith('_') and callable(getattr(module, m))]
        return actions[:20]  # Limitar a 20 acciones
    
    def cleanup(self):
        """Limpieza de recursos"""
        logger.info("Limpiando recursos del orquestador...")
        self.active_operations.clear()
        logger.info("Orquestador limpiado")


# Singleton instance
_orchestrator_instance: Optional[CoreOrchestrator] = None

def get_orchestrator(db_path: str = "kalighost_core.db") -> CoreOrchestrator:
    """Obtiene instancia singleton del Core Orchestrator"""
    global _orchestrator_instance
    if _orchestrator_instance is None:
        _orchestrator_instance = CoreOrchestrator(db_path)
    return _orchestrator_instance


if __name__ == "__main__":
    print("🔮 KaliGhost 4.0 ULTIMATE - Core Orchestrator")
    print("=" * 50)
    
    orchestrator = get_orchestrator()
    
    # Mostrar estado del sistema
    status = orchestrator.get_system_status()
    print(f"\n📊 Estado del Sistema:")
    print(f"   Status: {status.status}")
    print(f"   Módulos activos: {len(status.active_modules)}")
    print(f"   Operaciones activas: {status.active_operations}")
    
    # Listar módulos
    print(f"\n📦 Módulos Disponibles:")
    for module_id in status.active_modules:
        info = orchestrator.get_module_info(module_id)
        if info:
            print(f"   ✓ {module_id}: {info['description']}")
    
    # Demo: ejecutar operación en payload generator
    print(f"\n🚀 Ejecutando operación de prueba...")
    try:
        result = orchestrator.execute_operation(
            module_id='payload_generator',
            action='get_payload_stats',
            params={}
        )
        print(f"   Resultado: {result.success}")
        print(f"   Duración: {result.duration:.4f}s")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n✅ Core Orchestrator listo para operaciones")
