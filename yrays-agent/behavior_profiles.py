#!/usr/bin/env python3
"""
Sistema de Perfiles de Comportamiento Autónomo para YrYs-Agent
Define y gestiona diferentes perfiles de comportamiento para el agente
"""

import json
import logging
from typing import Dict, List, Any, Optional
from enum import Enum
from pathlib import Path

class BehaviorMode(Enum):
    """Modos de comportamiento del agente"""
    STEALTH = "stealth"          # Modo sigiloso, mínimo impacto
    AGGRESSIVE = "aggressive"    # Modo agresivo, exploración exhaustiva
    BALANCED = "balanced"        # Modo equilibrado
    PASSIVE = "passive"          # Modo pasivo, solo monitoreo
    CUSTOM = "custom"            # Modo personalizado

class AutonomousProfile:
    """Perfil de comportamiento autónomo"""
    
    def __init__(self, name: str, mode: BehaviorMode, description: str = ""):
        self.name = name
        self.mode = mode
        self.description = description
        self.settings = self._get_default_settings(mode)
        self.created_at = None  # Se establece al guardar
        self.is_active = False
    
    def _get_default_settings(self, mode: BehaviorMode) -> Dict[str, Any]:
        """Obtiene la configuración predeterminada para un modo"""
        base_settings = {
            "scan_intensity": "normal",      # low, normal, high
            "execution_speed": "normal",     # slow, normal, fast
            "resource_usage": "moderate",    # low, moderate, high
            "alert_sensitivity": "medium",   # low, medium, high
            "auto_report": True,
            "persistent_monitoring": False,
            "network_activity": "normal",    # low, normal, high
            "tool_timeout": 300,             # segundos
            "max_parallel_scans": 3,
            "retry_attempts": 3,
            "log_level": "INFO"
        }
        
        # Ajustar configuración según el modo
        if mode == BehaviorMode.STEALTH:
            base_settings.update({
                "scan_intensity": "low",
                "execution_speed": "slow",
                "resource_usage": "low",
                "alert_sensitivity": "high",
                "network_activity": "low",
                "tool_timeout": 600,
                "max_parallel_scans": 1,
                "retry_attempts": 5,
                "log_level": "DEBUG"
            })
        elif mode == BehaviorMode.AGGRESSIVE:
            base_settings.update({
                "scan_intensity": "high",
                "execution_speed": "fast",
                "resource_usage": "high",
                "alert_sensitivity": "low",
                "network_activity": "high",
                "tool_timeout": 180,
                "max_parallel_scans": 10,
                "retry_attempts": 1,
                "log_level": "WARNING"
            })
        elif mode == BehaviorMode.BALANCED:
            base_settings.update({
                "scan_intensity": "normal",
                "execution_speed": "normal",
                "resource_usage": "moderate",
                "alert_sensitivity": "medium",
                "network_activity": "normal",
                "tool_timeout": 300,
                "max_parallel_scans": 3,
                "retry_attempts": 3,
                "log_level": "INFO"
            })
        elif mode == BehaviorMode.PASSIVE:
            base_settings.update({
                "scan_intensity": "low",
                "execution_speed": "slow",
                "resource_usage": "low",
                "alert_sensitivity": "high",
                "network_activity": "low",
                "tool_timeout": 900,
                "max_parallel_scans": 1,
                "retry_attempts": 10,
                "log_level": "INFO",
                "persistent_monitoring": True
            })
        
        return base_settings
    
    def update_setting(self, key: str, value: Any) -> bool:
        """Actualiza una configuración específica"""
        if key in self.settings:
            self.settings[key] = value
            return True
        return False
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Obtiene una configuración específica"""
        return self.settings.get(key, default)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el perfil a diccionario"""
        return {
            "name": self.name,
            "mode": self.mode.value,
            "description": self.description,
            "settings": self.settings,
            "created_at": self.created_at,
            "is_active": self.is_active
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AutonomousProfile':
        """Crea un perfil desde un diccionario"""
        profile = cls(data["name"], BehaviorMode(data["mode"]), data.get("description", ""))
        profile.settings = data.get("settings", {})
        profile.created_at = data.get("created_at")
        profile.is_active = data.get("is_active", False)
        return profile

class ProfileManager:
    """Gestiona perfiles de comportamiento autónomo"""
    
    def __init__(self, profiles_dir: str = "profiles"):
        self.profiles_dir = Path(profiles_dir)
        self.profiles_dir.mkdir(exist_ok=True)
        self.profiles: Dict[str, AutonomousProfile] = {}
        self.active_profile: Optional[AutonomousProfile] = None
        
        # Crear perfiles predeterminados
        self._create_default_profiles()
        self._load_profiles()
        
        logging.info("Gestor de perfiles autónomos inicializado")
    
    def _create_default_profiles(self):
        """Crea perfiles predeterminados"""
        default_profiles = [
            AutonomousProfile("Sigiloso", BehaviorMode.STEALTH, "Modo de bajo impacto y sigilo"),
            AutonomousProfile("Agresivo", BehaviorMode.AGGRESSIVE, "Modo de exploración exhaustiva"),
            AutonomousProfile("Equilibrado", BehaviorMode.BALANCED, "Modo de comportamiento equilibrado"),
            AutonomousProfile("Pasivo", BehaviorMode.PASSIVE, "Modo de monitoreo continuo")
        ]
        
        for profile in default_profiles:
            if profile.name not in self.profiles:
                self.profiles[profile.name] = profile
                self._save_profile(profile)
    
    def _load_profiles(self):
        """Carga perfiles desde archivos"""
        for profile_file in self.profiles_dir.glob("*.json"):
            try:
                with open(profile_file, 'r') as f:
                    data = json.load(f)
                    profile = AutonomousProfile.from_dict(data)
                    self.profiles[profile.name] = profile
                    
                    # Activar perfil si estaba activo
                    if profile.is_active:
                        self.active_profile = profile
                        
            except Exception as e:
                logging.error(f"Error cargando perfil {profile_file}: {e}")
    
    def _save_profile(self, profile: AutonomousProfile):
        """Guarda un perfil en archivo"""
        try:
            profile_file = self.profiles_dir / f"{profile.name.lower().replace(' ', '_')}.json"
            with open(profile_file, 'w') as f:
                json.dump(profile.to_dict(), f, indent=2)
        except Exception as e:
            logging.error(f"Error guardando perfil {profile.name}: {e}")
    
    def create_profile(self, name: str, mode: BehaviorMode, description: str = "") -> AutonomousProfile:
        """Crea un nuevo perfil"""
        if name in self.profiles:
            raise ValueError(f"El perfil '{name}' ya existe")
        
        profile = AutonomousProfile(name, mode, description)
        self.profiles[name] = profile
        self._save_profile(profile)
        return profile
    
    def get_profile(self, name: str) -> Optional[AutonomousProfile]:
        """Obtiene un perfil por nombre"""
        return self.profiles.get(name)
    
    def list_profiles(self) -> List[Dict[str, str]]:
        """Lista todos los perfiles"""
        return [
            {
                "name": profile.name,
                "mode": profile.mode.value,
                "description": profile.description,
                "is_active": profile.is_active
            }
            for profile in self.profiles.values()
        ]
    
    def activate_profile(self, name: str) -> bool:
        """Activa un perfil"""
        profile = self.get_profile(name)
        if not profile:
            return False
        
        # Desactivar perfil actual
        if self.active_profile:
            self.active_profile.is_active = False
            self._save_profile(self.active_profile)
        
        # Activar nuevo perfil
        profile.is_active = True
        self.active_profile = profile
        self._save_profile(profile)
        
        logging.info(f"Perfil activado: {name}")
        return True
    
    def deactivate_profile(self) -> bool:
        """Desactiva el perfil actual"""
        if self.active_profile:
            self.active_profile.is_active = False
            self._save_profile(self.active_profile)
            self.active_profile = None
            logging.info("Perfil desactivado")
            return True
        return False
    
    def delete_profile(self, name: str) -> bool:
        """Elimina un perfil"""
        if name in self.profiles:
            profile = self.profiles[name]
            
            # No permitir eliminar perfil activo
            if profile.is_active:
                logging.warning("No se puede eliminar el perfil activo")
                return False
            
            # Eliminar archivo
            profile_file = self.profiles_dir / f"{name.lower().replace(' ', '_')}.json"
            if profile_file.exists():
                profile_file.unlink()
            
            # Eliminar de memoria
            del self.profiles[name]
            logging.info(f"Perfil eliminado: {name}")
            return True
        return False
    
    def get_active_profile(self) -> Optional[AutonomousProfile]:
        """Obtiene el perfil activo"""
        return self.active_profile
    
    def get_profile_setting(self, key: str, default: Any = None) -> Any:
        """Obtiene una configuración del perfil activo"""
        if self.active_profile:
            return self.active_profile.get_setting(key, default)
        return default

# Instancia global del gestor de perfiles
_global_profile_manager = None

def get_profile_manager() -> ProfileManager:
    """Obtiene el gestor de perfiles global"""
    global _global_profile_manager
    if _global_profile_manager is None:
        _global_profile_manager = ProfileManager()
    return _global_profile_manager

# Ejemplo de uso
if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Obtener gestor de perfiles
    profile_manager = get_profile_manager()
    
    # Listar perfiles disponibles
    profiles = profile_manager.list_profiles()
    print("📚 Perfiles disponibles:")
    for profile in profiles:
        status = "✓ ACTIVO" if profile["is_active"] else "○ INACTIVO"
        print(f"  • {profile['name']} ({profile['mode']}) - {status}")
        print(f"    {profile['description']}")
    
    # Activar perfil equilibrado
    if profile_manager.activate_profile("Equilibrado"):
        print("\n✅ Perfil 'Equilibrado' activado")
        
        # Obtener configuración del perfil activo
        active_profile = profile_manager.get_active_profile()
        if active_profile:
            print(f"\n🔧 Configuración del perfil '{active_profile.name}':")
            for key, value in active_profile.settings.items():
                print(f"  {key}: {value}")
    
    # Crear perfil personalizado
    try:
        custom_profile = profile_manager.create_profile(
            "Personalizado", 
            BehaviorMode.CUSTOM, 
            "Perfil con configuración personalizada"
        )
        
        # Modificar algunas configuraciones
        custom_profile.update_setting("scan_intensity", "high")
        custom_profile.update_setting("max_parallel_scans", 5)
        profile_manager._save_profile(custom_profile)
        
        print(f"\n🆕 Perfil personalizado creado: {custom_profile.name}")
        
    except ValueError as e:
        print(f"\n❌ Error: {e}")