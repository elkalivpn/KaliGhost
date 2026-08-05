"""
Security Manager - Gestión de encriptación, autenticación y seguridad
"""
import os
import hashlib
import secrets
from typing import Optional, Tuple, Dict, Any
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

class SecurityManager:
    """Gestor de seguridad con encriptación AES-256-GCM y hashing seguro"""
    
    def __init__(self, master_key: Optional[str] = None):
        self.master_key = master_key or self._generate_master_key()
        self.backend = default_backend()
    
    def _generate_master_key(self) -> str:
        """Genera clave maestra segura"""
        return secrets.token_hex(32)
    
    def derive_key(self, password: str, salt: bytes, iterations: int = 100000) -> bytes:
        """Deriva clave desde password usando PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=iterations,
            backend=self.backend
        )
        return kdf.derive(password.encode())
    
    def encrypt(self, plaintext: bytes, associated_data: Optional[bytes] = None) -> Tuple[str, str]:
        """Encripta datos con AES-256-GCM"""
        aesgcm = AESGCM(self.master_key.encode()[:32].ljust(32, b'\0'))
        nonce = os.urandom(12)
        ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data)
        return base64.b64encode(nonce).decode(), base64.b64encode(ciphertext).decode()
    
    def decrypt(self, nonce_b64: str, ciphertext_b64: str, 
                associated_data: Optional[bytes] = None) -> bytes:
        """Desencripta datos con AES-256-GCM"""
        aesgcm = AESGCM(self.master_key.encode()[:32].ljust(32, b'\0'))
        nonce = base64.b64decode(nonce_b64)
        ciphertext = base64.b64decode(ciphertext_b64)
        return aesgcm.decrypt(nonce, ciphertext, associated_data)
    
    def hash_password(self, password: str) -> str:
        """Hashea password con SHA-256 y salt"""
        salt = secrets.token_hex(16)
        hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}${hashed.hex()}"
    
    def verify_password(self, password: str, stored_hash: str) -> bool:
        """Verifica password contra hash almacenado"""
        try:
            salt, hash_value = stored_hash.split('$')
            new_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return secrets.compare_digest(new_hash.hex(), hash_value)
        except Exception:
            return False
    
    def generate_api_key(self) -> str:
        """Genera API key segura"""
        return f"kg_{secrets.token_urlsafe(32)}"
    
    def secure_wipe(self, data: bytearray) -> None:
        """Limpieza segura de datos sensibles (7 passes)"""
        patterns = [b'\x00', b'\xFF', b'\xAA', b'\x55', b'\x00', b'\xFF', b'\x00']
        for i, pattern in enumerate(patterns):
            for j in range(len(data)):
                data[j] = pattern[0]
    
    def get_security_info(self) -> Dict[str, Any]:
        """Retorna información de seguridad (sin datos sensibles)"""
        return {
            "algorithm": "AES-256-GCM",
            "hash_algorithm": "PBKDF2-SHA256",
            "hash_rounds": 100000,
            "key_length": 256,
            "nonce_length": 96
        }
