"""
Emergency Response System - Dead Man's Switch, Shamir Secret Sharing, Wipe Seguro
"""
import os
import time
import threading
import secrets
from pathlib import Path
from typing import Optional, Dict, Any, List, Callable
from datetime import datetime, timedelta
import hashlib
import json

class ShamirSecretSharing:
    """Implementación de Shamir's Secret Sharing Scheme"""
    
    def __init__(self, field_size: int = 256):
        self.field_size = field_size
    
    def split_secret(self, secret: bytes, n_parts: int, k_threshold: int) -> List[bytes]:
        """Divide secreto en N partes, requiere K para reconstruir"""
        if k_threshold > n_parts:
            raise ValueError("K threshold no puede ser mayor que N parts")
        
        shares = []
        secret_int = int.from_bytes(secret, 'big')
        
        for i in range(n_parts):
            # Generar polinomio aleatorio de grado k-1
            coefficients = [secret_int] + [secrets.randbelow(self.field_size) for _ in range(k_threshold - 1)]
            
            # Evaluar polinomio en x = i+1
            share_value = sum(coef * pow(i + 1, j, self.field_size) 
                            for j, coef in enumerate(coefficients)) % self.field_size
            
            shares.append(bytes([i + 1, share_value]))
        
        return shares
    
    def reconstruct_secret(self, shares: List[bytes]) -> bytes:
        """Reconstruye secreto desde K o más partes"""
        if len(shares) < 2:
            raise ValueError("Se necesitan al menos 2 shares")
        
        # Implementación simplificada de interpolación de Lagrange
        x_values = [share[0] for share in shares]
        y_values = [share[1] for share in shares]
        
        secret = 0
        for i in range(len(shares)):
            numerator = 1
            denominator = 1
            
            for j in range(len(shares)):
                if i != j:
                    numerator = (numerator * (-x_values[j])) % self.field_size
                    denominator = (denominator * (x_values[i] - x_values[j])) % self.field_size
            
            lagrange_coef = (numerator * pow(denominator, -1, self.field_size)) % self.field_size
            secret = (secret + y_values[i] * lagrange_coef) % self.field_size
        
        return bytes([secret])


class DeadMansSwitch:
    """Dead Man's Switch con múltiples triggers"""
    
    def __init__(self, timeout_minutes: int = 30):
        self.timeout_seconds = timeout_minutes * 60
        self.last_heartbeat = time.time()
        self.triggers: List[Callable] = []
        self.active = False
        self._thread: Optional[threading.Thread] = None
    
    def start(self, callback: Callable[[], None]) -> None:
        """Inicia el watchdog timer"""
        self.active = True
        self.callback = callback
        
        self._thread = threading.Thread(target=self._monitor, daemon=True)
        self._thread.start()
    
    def stop(self) -> None:
        """Detiene el watchdog"""
        self.active = False
        if self._thread:
            self._thread.join(timeout=5)
    
    def heartbeat(self) -> None:
        """Resetea el timer"""
        self.last_heartbeat = time.time()
    
    def add_trigger(self, trigger: Callable[[], bool]) -> None:
        """Añade trigger personalizado"""
        self.triggers.append(trigger)
    
    def _monitor(self) -> None:
        """Monitoriza triggers en hilo separado"""
        while self.active:
            elapsed = time.time() - self.last_heartbeat
            
            # Verificar timeout
            if elapsed > self.timeout_seconds:
                self.callback()
                break
            
            # Verificar triggers personalizados
            for trigger in self.triggers:
                try:
                    if trigger():
                        self.callback()
                        self.active = False
                        return
                except Exception:
                    pass
            
            time.sleep(10)  # Chequear cada 10 segundos


class EmergencyResponseSystem:
    """Sistema completo de respuesta a emergencias"""
    
    def __init__(self, wipe_method: str = "secure_delete_7pass"):
        self.wipe_method = wipe_method
        self.shamir = ShamirSecretSharing()
        self.dead_man_switch: Optional[DeadMansSwitch] = None
        self.secrets_to_protect: List[Path] = []
        self.notification_callbacks: List[Callable[[str], None]] = []
    
    def configure_dead_man_switch(self, timeout_minutes: int = 30, 
                                  callback: Optional[Callable] = None) -> None:
        """Configura Dead Man's Switch"""
        final_callback = callback or self._emergency_action
        
        self.dead_man_switch = DeadMansSwitch(timeout_minutes)
        self.dead_man_switch.start(final_callback)
    
    def reset_dead_man_timer(self) -> None:
        """Resetea el timer del Dead Man's Switch"""
        if self.dead_man_switch:
            self.dead_man_switch.heartbeat()
    
    def split_master_key(self, master_key: bytes, n_parts: int = 5, 
                         k_threshold: int = 3) -> List[bytes]:
        """Divide clave maestra usando Shamir"""
        return self.shamir.split_secret(master_key, n_parts, k_threshold)
    
    def reconstruct_master_key(self, shares: List[bytes]) -> bytes:
        """Reconstruye clave maestra desde shares"""
        return self.shamir.reconstruct_secret(shares)
    
    def register_secret(self, secret_path: Union[str, Path]) -> None:
        """Registra archivo secreto para protección"""
        self.secrets_to_protect.append(Path(secret_path))
    
    def add_notification(self, callback: Callable[[str], None]) -> None:
        """Añade callback de notificación"""
        self.notification_callbacks.append(callback)
    
    def _notify(self, message: str) -> None:
        """Envía notificaciones a todos los callbacks"""
        for callback in self.notification_callbacks:
            try:
                callback(message)
            except Exception:
                pass
    
    def _emergency_action(self) -> None:
        """Acción de emergencia: notificar y limpiar"""
        timestamp = datetime.now().isoformat()
        message = f"EMERGENCY ACTIVATED at {timestamp}"
        
        self._notify(message)
        self.wipe_all_secrets()
    
    def wipe_all_secrets(self) -> Dict[str, Any]:
        """Limpia todos los secretos registrados"""
        results = []
        
        for secret_path in self.secrets_to_protect:
            result = self.secure_wipe_file(secret_path)
            results.append(result)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "files_processed": len(results),
            "results": results
        }
    
    def secure_wipe_file(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Limpieza segura de archivo con múltiples passes"""
        path = Path(file_path)
        
        if not path.exists():
            return {"success": False, "error": "File not found", "path": str(path)}
        
        try:
            file_size = path.stat().st_size
            
            # Patrones para diferentes métodos
            patterns_map = {
                "single_pass": [b'\x00'],
                "3pass": [b'\x00', b'\xFF', b'\x00'],
                "7pass": [b'\x00', b'\xFF', b'\xAA', b'\x55', b'\x00', b'\xFF', b'\x00'],
                "secure_delete_7pass": [b'\x00', b'\xFF', b'\xAA', b'\x55', b'\x00', b'\xFF', b'\x00'],
                "dod_5220": [b'\x00', b'\xFF', b'\x00', b'\xFF', b'\xAA', b'\x55', b'\x00']
            }
            
            patterns = patterns_map.get(self.wipe_method, patterns_map["7pass"])
            
            with open(path, 'r+b') as f:
                for pattern in patterns:
                    f.seek(0)
                    f.write(pattern * file_size)
                    f.flush()
                    os.fsync(f.fileno())
            
            # Eliminar archivo
            path.unlink()
            
            return {"success": True, "path": str(path), "method": self.wipe_method}
        
        except Exception as e:
            return {"success": False, "error": str(e), "path": str(path)}
    
    def secure_wipe_directory(self, dir_path: Union[str, Path], 
                              recursive: bool = True) -> Dict[str, Any]:
        """Limpieza segura de directorio completo"""
        path = Path(dir_path)
        results = []
        
        files = path.rglob("*") if recursive else path.glob("*")
        
        for file in files:
            if file.is_file():
                result = self.secure_wipe_file(file)
                results.append(result)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "directory": str(path),
            "files_processed": len(results),
            "results": results
        }
    
    def panic_button(self) -> Dict[str, Any]:
        """Botón de pánico: activa todas las medidas de emergencia"""
        timestamp = datetime.now().isoformat()
        
        # Activar limpieza
        wipe_result = self.wipe_all_secrets()
        
        # Detener Dead Man's Switch si está activo
        if self.dead_man_switch:
            self.dead_man_switch.stop()
        
        return {
            "activated": True,
            "timestamp": timestamp,
            "wipe_result": wipe_result
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna estado del sistema de emergencia"""
        return {
            "dead_man_switch_active": self.dead_man_switch.active if self.dead_man_switch else False,
            "timeout_seconds": self.dead_man_switch.timeout_seconds if self.dead_man_switch else 0,
            "last_heartbeat": datetime.fromtimestamp(self.dead_man_switch.last_heartbeat).isoformat() 
                           if self.dead_man_switch else None,
            "registered_secrets": len(self.secrets_to_protect),
            "wipe_method": self.wipe_method,
            "notification_handlers": len(self.notification_callbacks)
        }
