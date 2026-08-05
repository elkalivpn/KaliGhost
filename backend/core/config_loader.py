"""
Config Loader - Carga configuración segura con encriptación
"""
import os
import json
from pathlib import Path
from typing import Any, Dict, Optional
from cryptography.fernet import Fernet
from dotenv import load_dotenv

class ConfigLoader:
    """Carga y gestiona configuración con soporte para valores encriptados"""
    
    def __init__(self, env_file: str = ".env"):
        self.env_file = Path(env_file)
        self._config: Dict[str, Any] = {}
        self._cipher: Optional[Fernet] = None
        self.load()
    
    def load(self) -> None:
        """Carga variables de entorno y configuración"""
        if self.env_file.exists():
            load_dotenv(self.env_file)
        
        # Cargar configuración desde variables de entorno
        self._config = {
            "version": os.getenv("KALIGHOST_VERSION", "4.0-ULTIMATE"),
            "mode": os.getenv("MODE", "hybrid"),
            "master_key": os.getenv("MASTER_KEY"),
            "encryption_algorithm": os.getenv("ENCRYPTION_ALGORITHM", "AES-256-GCM"),
            "database_url": os.getenv("DATABASE_URL", "sqlite+aiosqlite:///data/kalighost.db"),
            "redis_url": os.getenv("REDIS_URL", "redis://localhost:6379/0"),
            "cve_db_path": os.getenv("CVE_DB_PATH", "data/cve_db/cve_database.sqlite"),
            "ram_disk_size": os.getenv("RAM_DISK_SIZE", "2G"),
            "ram_execution_enabled": os.getenv("RAM_EXECUTION_ENABLED", "true").lower() == "true",
            "auto_wipe": os.getenv("AUTO_WIPE", "true").lower() == "true",
            "default_routing_mode": os.getenv("DEFAULT_ROUTING_MODE", "isolated"),
            "tor_enabled": os.getenv("TOR_ENABLED", "false").lower() == "true",
            "proxy_chain_enabled": os.getenv("PROXY_CHAIN_ENABLED", "false").lower() == "true",
            "steganography_algorithm": os.getenv("STEGANOGRAPHY_ALGORITHM", "lsb_advanced"),
            "dead_man_switch_enabled": os.getenv("DEAD_MAN_SWITCH_ENABLED", "true").lower() == "true",
            "dead_man_timeout_minutes": int(os.getenv("DEAD_MAN_TIMEOUT_MINUTES", "30")),
            "shamir_n_parts": int(os.getenv("SHAMIR_N_PARTS", "5")),
            "shamir_k_threshold": int(os.getenv("SHAMIR_K_THRESHOLD", "3")),
            "ai_model_endpoint": os.getenv("AI_MODEL_ENDPOINT", "http://localhost:11434"),
            "ai_model_name": os.getenv("AI_MODEL_NAME", "mistral-large"),
            "rag_enabled": os.getenv("RAG_ENABLED", "true").lower() == "true",
            "sandbox_type": os.getenv("SANDBOX_TYPE", "docker_kubernetes_hybrid"),
            "sandbox_timeout_seconds": int(os.getenv("SANDBOX_TIMEOUT_SECONDS", "300")),
            "api_host": os.getenv("API_HOST", "0.0.0.0"),
            "api_port": int(os.getenv("API_PORT", "8000")),
            "webchat_port": int(os.getenv("WEBCHAT_PORT", "8001")),
            "debug_mode": os.getenv("DEBUG_MODE", "false").lower() == "true",
            "secret_key": os.getenv("SECRET_KEY"),
        }
        
        # Inicializar cipher si existe master key
        if self._config["master_key"]:
            self._cipher = Fernet(self._config["master_key"].encode())
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obtiene valor de configuración"""
        return self._config.get(key, default)
    
    def get_encrypted(self, key: str) -> Optional[str]:
        """Obtiene y desencripta valor"""
        if not self._cipher:
            raise ValueError("No hay clave maestra configurada")
        
        encrypted_value = os.getenv(f"ENC_{key}")
        if encrypted_value:
            return self._cipher.decrypt(encrypted_value.encode()).decode()
        return None
    
    def is_ghost_mode(self) -> bool:
        """Verifica si está en modo fantasma puro"""
        return self._config["mode"] == "ghost"
    
    def is_hybrid_mode(self) -> bool:
        """Verifica si está en modo híbrido"""
        return self._config["mode"] == "hybrid"
    
    def to_dict(self) -> Dict[str, Any]:
        """Retorna configuración como diccionario (sin datos sensibles)"""
        safe_config = self._config.copy()
        safe_config.pop("master_key", None)
        safe_config.pop("secret_key", None)
        return safe_config
