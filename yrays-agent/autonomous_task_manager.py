#!/usr/bin/env python3
"""
Sistema de Gestión de Tareas Autónomas para YrYs-Agent
Permite programar tareas, ejecutarlas en segundo plano y gestionar su ciclo de vida
"""

import os
import sys
import time
import threading
import json
import logging
import traceback
from typing import Dict, List, Callable, Any, Optional
from pathlib import Path
from datetime import datetime, timedelta
import sqlite3
import queue
import uuid

class Task:
    """Representa una tarea programada"""
    
    def __init__(self, name: str, description: str, function: Callable, args: tuple = (), kwargs: dict = None, 
                 schedule_type: str = "once", interval: int = 0, start_time: datetime = None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.function = function
        self.args = args
        self.kwargs = kwargs or {}
        self.schedule_type = schedule_type  # "once", "interval", "daily", "weekly"
        self.interval = interval  # segundos para tareas repetitivas
        self.start_time = start_time or datetime.now()
        self.created_at = datetime.now()
        self.last_run = None
        self.next_run = self.start_time
        self.status = "scheduled"  # "scheduled", "running", "completed", "failed", "cancelled"
        self.result = None
        self.error = None
        self.run_count = 0
        
    def should_run(self) -> bool:
        """Determina si la tarea debe ejecutarse"""
        if self.status in ["cancelled", "completed"] and self.schedule_type == "once":
            return False
        
        now = datetime.now()
        return now >= self.next_run
    
    def execute(self) -> bool:
        """Ejecuta la tarea"""
        try:
            self.status = "running"
            self.last_run = datetime.now()
            logging.info(f"Iniciando ejecución de tarea: {self.name}")
            
            # Ejecutar la función
            self.result = self.function(*self.args, **self.kwargs)
            self.status = "completed"
            self.run_count += 1
            
            # Calcular próxima ejecución si es repetitiva
            if self.schedule_type == "interval":
                self.next_run = datetime.now() + timedelta(seconds=self.interval)
            elif self.schedule_type == "daily":
                self.next_run = datetime.now() + timedelta(days=1)
            elif self.schedule_type == "weekly":
                self.next_run = datetime.now() + timedelta(weeks=1)
            else:
                # Tarea única completada
                self.status = "completed"
            
            logging.info(f"Tarea completada: {self.name}")
            return True
            
        except Exception as e:
            self.status = "failed"
            self.error = str(e)
            logging.error(f"Error en tarea {self.name}: {e}")
            logging.error(traceback.format_exc())
            return False
    
    def cancel(self):
        """Cancela la tarea"""
        self.status = "cancelled"
    
    def to_dict(self) -> Dict:
        """Convierte la tarea a diccionario para serialización"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "schedule_type": self.schedule_type,
            "interval": self.interval,
            "start_time": self.start_time.isoformat(),
            "created_at": self.created_at.isoformat(),
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "next_run": self.next_run.isoformat(),
            "status": self.status,
            "result": str(self.result) if self.result else None,
            "error": self.error,
            "run_count": self.run_count
        }

class AutonomousTaskManager:
    """Gestiona tareas autónomas en segundo plano"""
    
    def __init__(self, db_path: str = "autonomous_tasks.db"):
        self.db_path = Path(db_path)
        self.tasks: Dict[str, Task] = {}
        self.running = False
        self.worker_thread = None
        self.task_queue = queue.Queue()
        
        # Inicializar base de datos
        self._init_database()
        self._load_tasks()
        
        logging.info("Gestor de tareas autónomas inicializado")
    
    def _init_database(self):
        """Inicializa la base de datos SQLite para persistencia de tareas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                schedule_type TEXT NOT NULL,
                interval INTEGER,
                start_time TEXT,
                created_at TEXT,
                last_run TEXT,
                next_run TEXT,
                status TEXT,
                result TEXT,
                error TEXT,
                run_count INTEGER
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _load_tasks(self):
        """Carga tareas desde la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM tasks WHERE status IN ('scheduled', 'running')")
            rows = cursor.fetchall()
            
            for row in rows:
                task_data = {
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "schedule_type": row[3],
                    "interval": row[4],
                    "start_time": datetime.fromisoformat(row[5]),
                    "created_at": datetime.fromisoformat(row[6]),
                    "last_run": datetime.fromisoformat(row[7]) if row[7] else None,
                    "next_run": datetime.fromisoformat(row[8]),
                    "status": row[9],
                    "result": row[10],
                    "error": row[11],
                    "run_count": row[12]
                }
                
                # Crear tarea dummy (sin función real, solo para seguimiento)
                task = Task(
                    name=task_data["name"],
                    description=task_data["description"],
                    function=lambda: None,
                    schedule_type=task_data["schedule_type"],
                    interval=task_data["interval"],
                    start_time=task_data["start_time"]
                )
                
                task.id = task_data["id"]
                task.created_at = task_data["created_at"]
                task.last_run = task_data["last_run"]
                task.next_run = task_data["next_run"]
                task.status = task_data["status"]
                task.result = task_data["result"]
                task.error = task_data["error"]
                task.run_count = task_data["run_count"]
                
                self.tasks[task.id] = task
            
            conn.close()
            logging.info(f"Cargadas {len(self.tasks)} tareas desde la base de datos")
            
        except Exception as e:
            logging.error(f"Error al cargar tareas: {e}")
    
    def _save_task(self, task: Task):
        """Guarda una tarea en la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO tasks 
                (id, name, description, schedule_type, interval, start_time, created_at, 
                 last_run, next_run, status, result, error, run_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                task.id, task.name, task.description, task.schedule_type, task.interval,
                task.start_time.isoformat(), task.created_at.isoformat(),
                task.last_run.isoformat() if task.last_run else None,
                task.next_run.isoformat(), task.status, str(task.result) if task.result else None,
                task.error, task.run_count
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logging.error(f"Error al guardar tarea {task.name}: {e}")
    
    def add_task(self, task: Task) -> str:
        """
        Añade una tarea al gestor
        Retorna el ID de la tarea
        """
        self.tasks[task.id] = task
        self._save_task(task)
        logging.info(f"Tarea añadida: {task.name} (ID: {task.id})")
        return task.id
    
    def schedule_task(self, name: str, description: str, function: Callable, 
                     args: tuple = (), kwargs: dict = None, schedule_type: str = "once",
                     interval: int = 0, start_time: datetime = None) -> str:
        """
        Programa una nueva tarea
        Retorna el ID de la tarea
        """
        task = Task(
            name=name,
            description=description,
            function=function,
            args=args,
            kwargs=kwargs,
            schedule_type=schedule_type,
            interval=interval,
            start_time=start_time
        )
        
        return self.add_task(task)
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Obtiene una tarea por su ID"""
        return self.tasks.get(task_id)
    
    def get_tasks_by_status(self, status: str) -> List[Task]:
        """Obtiene todas las tareas con un estado específico"""
        return [task for task in self.tasks.values() if task.status == status]
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancela una tarea"""
        task = self.get_task(task_id)
        if task:
            task.cancel()
            self._save_task(task)
            logging.info(f"Tarea cancelada: {task.name}")
            return True
        return False
    
    def remove_task(self, task_id: str) -> bool:
        """Elimina una tarea permanentemente"""
        task = self.get_task(task_id)
        if task:
            # Eliminar de la base de datos
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
                conn.commit()
                conn.close()
            except Exception as e:
                logging.error(f"Error al eliminar tarea de BD: {e}")
            
            # Eliminar de memoria
            del self.tasks[task_id]
            logging.info(f"Tarea eliminada: {task.name}")
            return True
        return False
    
    def list_tasks(self) -> List[Dict]:
        """Lista todas las tareas"""
        return [task.to_dict() for task in self.tasks.values()]
    
    def start(self):
        """Inicia el gestor de tareas"""
        if self.running:
            logging.warning("El gestor de tareas ya está en ejecución")
            return
        
        self.running = True
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()
        logging.info("Gestor de tareas autónomas iniciado")
    
    def stop(self):
        """Detiene el gestor de tareas"""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
        logging.info("Gestor de tareas autónomas detenido")
    
    def _worker_loop(self):
        """Bucle principal del worker de tareas"""
        while self.running:
            try:
                # Verificar tareas programadas
                now = datetime.now()
                for task in self.tasks.values():
                    if task.should_run():
                        # Añadir tarea a la cola de ejecución
                        self.task_queue.put(task)
                        logging.debug(f"Tarea añadida a cola: {task.name}")
                
                # Ejecutar tareas en la cola (con timeout para evitar bloqueos)
                try:
                    task = self.task_queue.get(timeout=1)
                    if task.status != "cancelled":
                        success = task.execute()
                        self._save_task(task)
                        if success:
                            logging.info(f"Tarea ejecutada correctamente: {task.name}")
                        else:
                            logging.error(f"Tarea fallida: {task.name}")
                except queue.Empty:
                    # No hay tareas en la cola, continuar
                    pass
                
                # Pequeña pausa para evitar consumo excesivo de CPU
                time.sleep(0.1)
                
            except Exception as e:
                logging.error(f"Error en el bucle de tareas: {e}")
                time.sleep(1)  # Pausa más larga en caso de error

# Funciones de ejemplo para tareas autónomas
def example_network_monitor(target: str = "localhost") -> str:
    """Ejemplo de tarea de monitoreo de red"""
    import subprocess
    try:
        result = subprocess.run(["ping", "-c", "1", target], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return f"✅ {target} está accesible"
        else:
            return f"❌ {target} no responde"
    except Exception as e:
        return f"💥 Error al monitorear {target}: {e}"

def example_system_health_check() -> str:
    """Ejemplo de tarea de chequeo de salud del sistema"""
    import psutil
    
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    
    report = f"""
📊 Informe de Salud del Sistema:
  CPU: {cpu_percent:.1f}%
  Memoria: {memory.percent:.1f}% usado ({memory.available // (1024*1024)} MB disponible)
  Disco: {(disk.used / disk.total) * 100:.1f}% usado ({disk.free // (1024*1024*1024)} GB disponible)
"""
    return report

def example_security_scan(target: str = "localhost") -> str:
    """Ejemplo de tarea de escaneo de seguridad"""
    # Simular un escaneo de seguridad
    time.sleep(2)  # Simular tiempo de procesamiento
    
    vulnerabilities = ["Puerto 22 abierto (SSH)", "Servidor web sin HTTPS"]
    if vulnerabilities:
        return f"⚠️ Vulnerabilidades encontradas en {target}:\n" + "\n".join(f"  • {v}" for v in vulnerabilities)
    else:
        return f"✅ No se encontraron vulnerabilidades en {target}"

# Ejemplo de uso
if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Crear gestor de tareas
    task_manager = AutonomousTaskManager()
    
    # Programar algunas tareas de ejemplo
    task_manager.schedule_task(
        name="Monitor de Red",
        description="Monitorea la conectividad de red",
        function=example_network_monitor,
        args=("google.com",),
        schedule_type="interval",
        interval=30  # Cada 30 segundos
    )
    
    task_manager.schedule_task(
        name="Chequeo de Salud",
        description="Verifica el estado del sistema",
        function=example_system_health_check,
        schedule_type="interval",
        interval=60  # Cada minuto
    )
    
    # Iniciar el gestor
    task_manager.start()
    
    # Listar tareas
    tasks = task_manager.list_tasks()
    print(f"📚 Tareas programadas: {len(tasks)}")
    for task in tasks:
        print(f"  • {task['name']}: {task['status']} (Próxima: {task['next_run']})")
    
    # Mantener el programa en ejecución por 5 minutos
    try:
        time.sleep(300)
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo gestor de tareas...")
    
    # Detener el gestor
    task_manager.stop()
    print("👋 Gestor de tareas detenido")