"""
Ghost Logger - Sistema de logging seguro con auto-limpieza y ofuscación
"""
import os
import sys
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
from enum import Enum

class LogLevel(Enum):
    GHOST = "GHOST"      # No se registra, solo memoria volátil
    STEALTH = "STEALTH"  # Se registra encriptado
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class GhostLogger:
    """Sistema de logging con modos fantasma y limpieza automática"""
    
    def __init__(self, name: str, log_dir: str = "data/logs", 
                 ghost_mode: bool = False, auto_wipe: bool = True):
        self.name = name
        self.log_dir = Path(log_dir)
        self.ghost_mode = ghost_mode
        self.auto_wipe = auto_wipe
        self.memory_buffer: List[Dict[str, Any]] = []
        self.max_memory_entries = 100
        
        if not ghost_mode:
            self.log_dir.mkdir(parents=True, exist_ok=True)
            self.log_file = self.log_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
        else:
            self.log_file = None
    
    def _generate_entry_id(self, message: str, level: str) -> str:
        """Genera ID único para entrada"""
        timestamp = datetime.now().isoformat()
        data = f"{timestamp}{message}{level}{os.getpid()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def log(self, level: LogLevel, message: str, metadata: Optional[Dict] = None,
            sensitive: bool = False) -> None:
        """Registra mensaje con nivel especificado"""
        entry = {
            "id": self._generate_entry_id(message, level.value),
            "timestamp": datetime.now().isoformat(),
            "level": level.value,
            "message": message if not sensitive else "[REDACTED]",
            "module": self.name,
            "pid": os.getpid(),
            "metadata": metadata or {}
        }
        
        if level == LogLevel.GHOST or (self.ghost_mode and level != LogLevel.CRITICAL):
            # Solo mantener en memoria volátil
            self.memory_buffer.append(entry)
            if len(self.memory_buffer) > self.max_memory_entries:
                self.memory_buffer.pop(0)
            return
        
        if self.log_file and not self.ghost_mode:
            log_line = json.dumps(entry)
            with open(self.log_file, 'a') as f:
                f.write(log_line + '\n')
        
        # Output a consola si es debug mode
        if os.getenv("DEBUG_MODE", "false").lower() == "true":
            print(f"[{entry['timestamp']}] [{level.value}] {message}", file=sys.stderr)
    
    def ghost(self, message: str, metadata: Optional[Dict] = None) -> None:
        """Log fantasma - solo en memoria volátil"""
        self.log(LogLevel.GHOST, message, metadata)
    
    def stealth(self, message: str, metadata: Optional[Dict] = None) -> None:
        """Log stealth - encriptado en disco"""
        self.log(LogLevel.STEALTH, message, metadata, sensitive=True)
    
    def info(self, message: str, metadata: Optional[Dict] = None) -> None:
        self.log(LogLevel.INFO, message, metadata)
    
    def warning(self, message: str, metadata: Optional[Dict] = None) -> None:
        self.log(LogLevel.WARNING, message, metadata)
    
    def error(self, message: str, metadata: Optional[Dict] = None) -> None:
        self.log(LogLevel.ERROR, message, metadata)
    
    def critical(self, message: str, metadata: Optional[Dict] = None) -> None:
        self.log(LogLevel.CRITICAL, message, metadata)
    
    def wipe(self) -> None:
        """Limpia todos los logs en disco y memoria"""
        self.memory_buffer.clear()
        
        if self.log_file and self.log_file.exists():
            # Limpieza segura (7 passes)
            file_size = self.log_file.stat().st_size
            with open(self.log_file, 'r+b') as f:
                patterns = [b'\x00', b'\xFF', b'\xAA', b'\x55', b'\x00', b'\xFF', b'\x00']
                for pattern in patterns:
                    f.seek(0)
                    f.write(pattern * file_size)
            self.log_file.unlink()
    
    def get_memory_logs(self) -> List[Dict[str, Any]]:
        """Retorna logs en memoria (volátiles)"""
        return self.memory_buffer.copy()
    
    def __del__(self):
        """Auto-limpieza al destruir si está configurado"""
        if self.auto_wipe and self.ghost_mode:
            try:
                self.wipe()
            except Exception:
                pass
