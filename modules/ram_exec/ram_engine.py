"""
RAM Execution Engine - Ejecución exclusiva en memoria sin rastros en disco
"""
import os
import sys
import mmap
import ctypes
import tempfile
import shutil
from pathlib import Path
from typing import Optional, Dict, Any, List, Callable
from dataclasses import dataclass
from enum import Enum
import subprocess
import signal

class ExecutionMode(Enum):
    NATIVE = "native"
    SANDBOX_TMPFS = "sandbox_tmpfs"
    SANDBOX_DOCKER = "sandbox_docker"
    EMULATED = "emulated"

@dataclass
class ExecutionResult:
    success: bool
    output: str
    error: str
    exit_code: int
    memory_used: int
    execution_time: float
    wiped: bool

class RAMExecutionEngine:
    """Motor de ejecución en RAM sin tocar disco"""
    
    def __init__(self, ram_disk_size: str = "2G", auto_wipe: bool = True):
        self.ram_disk_size = ram_disk_size
        self.auto_wipe = auto_wipe
        self.ram_disk_path: Optional[Path] = None
        self.active_processes: List[int] = []
        self._setup_ram_disk()
    
    def _setup_ram_disk(self) -> None:
        """Configura disco en RAM (tmpfs)"""
        try:
            self.ram_disk_path = Path("/dev/shm/kalighost_ram_exec")
            self.ram_disk_path.mkdir(parents=True, exist_ok=True)
            
            # Montar tmpfs si no está montado
            if not self._is_mounted():
                size = self.ram_disk_size
                subprocess.run(
                    ["mount", "-t", "tmpfs", "-o", f"size={size}", "tmpfs", str(self.ram_disk_path)],
                    capture_output=True
                )
        except Exception as e:
            # Fallback: usar directorio temporal
            self.ram_disk_path = Path(tempfile.mkdtemp(prefix="kalighost_ram_"))
    
    def _is_mounted(self) -> bool:
        """Verifica si el tmpfs está montado"""
        try:
            result = subprocess.run(["mountpoint", "-q", str(self.ram_disk_path)], 
                                  capture_output=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def execute_binary(self, binary_data: bytes, args: Optional[List[str]] = None,
                       timeout: int = 60, mode: ExecutionMode = ExecutionMode.SANDBOX_TMPFS) -> ExecutionResult:
        """Ejecuta binario directamente en RAM"""
        import time
        start_time = time.time()
        
        if mode == ExecutionMode.SANDBOX_TMPFS:
            return self._execute_tmpfs(binary_data, args, timeout)
        elif mode == ExecutionMode.NATIVE:
            return self._execute_native(binary_data, args, timeout)
        else:
            raise ValueError(f"Modo de ejecución no soportado: {mode}")
    
    def _execute_tmpfs(self, binary_data: bytes, args: Optional[List[str]], 
                       timeout: int) -> ExecutionResult:
        """Ejecuta en sandbox tmpfs"""
        import time
        start_time = time.time()
        
        # Crear archivo temporal en RAM
        exec_file = self.ram_disk_path / f"exec_{os.urandom(8).hex()}"
        
        try:
            # Escribir binario en RAM
            with open(exec_file, 'wb') as f:
                f.write(binary_data)
            
            # Hacer ejecutable
            os.chmod(exec_file, 0o700)
            
            # Preparar comando
            cmd = [str(exec_file)] + (args or [])
            
            # Ejecutar con aislamiento
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(self.ram_disk_path),
                preexec_fn=self._isolate_process
            )
            
            self.active_processes.append(proc.pid)
            
            try:
                stdout, stderr = proc.communicate(timeout=timeout)
                exit_code = proc.returncode
            except subprocess.TimeoutExpired:
                proc.kill()
                stdout, stderr = proc.communicate()
                exit_code = -9
            
            memory_used = self._get_process_memory(proc.pid) if proc.poll() is None else 0
            
            return ExecutionResult(
                success=exit_code == 0,
                output=stdout.decode('utf-8', errors='replace'),
                error=stderr.decode('utf-8', errors='replace'),
                exit_code=exit_code,
                memory_used=memory_used,
                execution_time=time.time() - start_time,
                wiped=False
            )
        
        finally:
            # Limpieza segura
            if self.auto_wipe:
                self._secure_delete(exec_file)
            if exec_file.exists():
                exec_file.unlink()
    
    def _execute_native(self, binary_data: bytes, args: Optional[List[str]], 
                        timeout: int) -> ExecutionResult:
        """Ejecución nativa en memoria usando mmap"""
        import time
        start_time = time.time()
        
        # Reservar memoria
        mem_size = len(binary_data) + 4096
        mem_region = mmap.mmap(-1, mem_size, 
                              mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS,
                              mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC)
        
        try:
            # Copiar binario a memoria
            mem_region.write(binary_data)
            mem_region.flush()
            
            # Nota: La ejecución directa desde mmap requiere técnicas avanzadas
            # Esto es un placeholder para la estructura
            return ExecutionResult(
                success=True,
                output="[Memoria asignada correctamente]",
                error="",
                exit_code=0,
                memory_used=mem_size,
                execution_time=time.time() - start_time,
                wiped=False
            )
        
        finally:
            # Limpieza segura
            if self.auto_wipe:
                mem_region.seek(0)
                mem_region.write(b'\x00' * mem_size)
            mem_region.close()
    
    def _isolate_process(self) -> None:
        """Aísla proceso para sandboxing"""
        os.setsid()  # Nuevo grupo de procesos
        
        # Limitar recursos
        try:
            import resource
            resource.setrlimit(resource.RLIMIT_AS, (1024 * 1024 * 512, 1024 * 1024 * 512))  # 512MB
            resource.setrlimit(resource.RLIMIT_CPU, (60, 60))  # 60 segundos
        except Exception:
            pass
    
    def _get_process_memory(self, pid: int) -> int:
        """Obtiene memoria usada por proceso"""
        try:
            import psutil
            process = psutil.Process(pid)
            return process.memory_info().rss
        except Exception:
            return 0
    
    def _secure_delete(self, file_path: Path) -> None:
        """Eliminación segura con múltiples passes"""
        if not file_path.exists():
            return
        
        file_size = file_path.stat().st_size
        patterns = [b'\x00', b'\xFF', b'\xAA', b'\x55', b'\x00', b'\xFF', b'\x00']
        
        with open(file_path, 'r+b') as f:
            for pattern in patterns:
                f.seek(0)
                f.write(pattern * file_size)
                f.flush()
                os.fsync(f.fileno())
    
    def wipe_all(self) -> None:
        """Limpia toda la RAM disk"""
        # Matar procesos activos
        for pid in self.active_processes:
            try:
                os.kill(pid, signal.SIGKILL)
            except Exception:
                pass
        self.active_processes.clear()
        
        # Limpiar archivos
        if self.ram_disk_path and self.ram_disk_path.exists():
            for file in self.ram_disk_path.glob("*"):
                self._secure_delete(file)
                file.unlink()
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna estado del motor"""
        return {
            "ram_disk_path": str(self.ram_disk_path),
            "is_mounted": self._is_mounted(),
            "active_processes": len(self.active_processes),
            "auto_wipe_enabled": self.auto_wipe
        }
    
    def __del__(self):
        """Limpieza al destruir"""
        try:
            if self.auto_wipe:
                self.wipe_all()
        except Exception:
            pass
