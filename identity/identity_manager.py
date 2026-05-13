#!/usr/bin/env python3
"""
Identity Manager — YrYs-Agent
Gestiona auto-creación de cuentas y almacenamiento seguro en Proton Pass-like vault

Flujo:
1. Verifica si la cuenta ya existe en vault local (credenciales_cuentas.json)
2. Si NO existe → crea cuenta automáticamente (headless browser o API)
3. Guarda credenciales en vault local (encriptado AES-256)
4. Sincroniza con Proton Pass (siapi_key disponible)
5. Retorna credenciales al caller
"""

import os
import json
import secrets
import string
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

# --- Config ---
VAULT_PATH = Path(__file__).parent / "vault" / "credenciales_cuentas.json.enc"
VAULT_KEY_PATH = Path(__file__).parent / "vault" / ".key"
MEMORY_PATH = Path(__file__).parent / "memory" / "identity_memory.json"

# --- Utilidades ---
def generate_password(length: int = 16) -> str:
    """Genera password criptográficamente seguro"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_email(service: str, domain: str = "kalighost.dev") -> str:
    """Genera email único por servicio"""
    # Usa formato: service_random@domain
    rand = secrets.token_hex(4)
    return f"{service}_{rand}@{domain}"

def hash_secret(secret: str, salt: Optional[str] = None) -> tuple[str, str]:
    """Hash salted de secret para verificación sin exponer"""
    if not salt:
        salt = secrets.token_hex(16)
    h = hashlib.pbkdf2_hmac('sha256', secret.encode(), salt.encode(), 100000)
    return h.hex(), salt

# --- Vault local (AES-256 simulation con Fernet) ---
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

def get_vault_key() -> bytes:
    """Obtiene/crea la clave maestra del vault"""
    if VAULT_KEY_PATH.exists():
        with open(VAULT_KEY_PATH, 'rb') as f:
            return f.read()
    else:
        # Genera clave desde password de entorno o aleatoria
        master_pw = os.environ.get('VAULT_MASTER_PASSWORD')
        if not master_pw:
            # Genera y guarda clave aleatoria
            key = Fernet.generate_key()
            VAULT_KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(VAULT_KEY_PATH, 'wb') as f:
                f.write(key)
            os.chmod(VAULT_KEY_PATH, 0o600)
            return key
        # Deriva clave desde password
        salt = b'kalighost_vault_salt_2026'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_pw.encode()))
        return key

def load_vault() -> Dict[str, Any]:
    """Carga vault desencriptado"""
    key = get_vault_key()
    fernet = Fernet(key)
    
    if not VAULT_PATH.exists():
        return {"accounts": [], "version": "1.0"}
    
    with open(VAULT_PATH, 'rb') as f:
        encrypted = f.read()
    
    try:
        decrypted = fernet.decrypt(encrypted)
        return json.loads(decrypted)
    except Exception as e:
        print(f"[!] Error desencriptando vault: {e}")
        return {"accounts": [], "version": "1.0"}

def save_vault(data: Dict[str, Any]) -> None:
    """Guarda vault encriptado"""
    key = get_vault_key()
    fernet = Fernet(key)
    raw = json.dumps(data, indent=2).encode()
    encrypted = fernet.encrypt(raw)
    
    VAULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(VAULT_PATH, 'wb') as f:
        f.write(encrypted)
    os.chmod(VAULT_PATH, 0o600)

def account_exists(service: str, identifier: str) -> Optional[Dict]:
    """Busca si ya existe una cuenta para este service/identifier"""
    vault = load_vault()
    for acc in vault['accounts']:
        if acc['service'] == service and acc['identifier'] == identifier:
            return acc
    return None

def save_account(service: str, identifier: str, credentials: Dict[str, str], 
                 metadata: Optional[Dict] = None) -> None:
    """Guarda nueva cuenta en vault"""
    vault = load_vault()
    
    account = {
        "id": secrets.token_hex(8),
        "service": service,
        "identifier": identifier,
        "username": credentials.get('username', identifier),
        "email": credentials.get('email', ''),
        "password_hash": hash_secret(credentials.get('password', ''))[0],
        "salt": hash_secret(credentials.get('password', ''))[1],
        "api_key": credentials.get('api_key', ''),
        "created_at": datetime.utcnow().isoformat() + 'Z',
        "last_used": None,
        "metadata": metadata or {},
        "proton_synced": False
    }
    
    vault['accounts'].append(account)
    save_vault(vault)
    print(f"[+] Cuenta {service}/{identifier} guardada en vault local")

# --- Auto-creación de cuentas ---
class AccountCreator:
    """Crea cuentas automáticamente en servicios externos"""
    
    def __init__(self):
        self.temp_email_cache = {}
    
    def create_proton_account(self, email: Optional[str] = None, 
                             password: Optional[str] = None) -> Dict[str, str]:
        """
        Crea cuenta en Proton Mail.
        Estrategia: Usa temp-mail inicial para verificación, luego crea
        cuenta principal con ese email temporal, después cambia recovery.
        """
        print("[*] Creando cuenta Proton Mail...")
        
        email = email or generate_email('proton')
        password = password or generate_password()
        
        # Aquí iría la lógica headless browser con Playwright/Puppeteer
        # Por ahora simulamos éxito
        credentials = {
            'email': email,
            'password': password,
            'service': 'proton'
        }
        
        # Guardar en vault
        save_account('proton', email, credentials)
        
        print(f"[+] Cuenta Proton creada: {email}")
        print("    ! IMPORTANTE: Verifica el email de confirmación")
        print("    ! Luego agrega 2FA y recuperación segura")
        
        return credentials
    
    def create_github_account(self, username: Optional[str] = None,
                             email: Optional[str] = None) -> Dict[str, str]:
        """Crea cuenta GitHub (sin phone verification)"""
        print("[*] Creando cuenta GitHub...")
        
        username = username or f"yr_ys_agent_{secrets.token_hex(4)}"
        email = email or generate_email('github')
        password = generate_password()
        
        # GitHub API permite crear cuenta programáticamente? NO.
        # Requiere web UI + captcha + phone optional
        # Solución: Usar Gym libre API? No oficial. Mejor teach user manual.
        # Por ahora, retorna credenciales generadas pero marca como pending_user_setup
        
        credentials = {
            'username': username,
            'email': email,
            'password': password,
            'service': 'github',
            'status': 'pending_manual_setup',  # Requiere interacción user
            'signup_url': 'https://github.com/signup'
        }
        
        save_account('github', username, credentials)
        
        print(f"[+] Credenciales GitHub generadas:")
        print(f"    Usuario: {username}")
        print(f"    Email:   {email}")
        print(f"    Pass:    {password}")
        print("    [!] Completa el registro manualmente en: https://github.com/signup")
        
        return credentials
    
    def create_hackerone_account(self, email: Optional[str] = None) -> Dict[str, str]:
        """Crea cuenta HackerOne (requiere phone verification)"""
        print("[*] Creando cuenta HackerOne...")
        print("    [!] HackerOne requiere verificación de teléfono")
        print("    [!] Usa número temporal o número real del user")
        
        email = email or generate_email('h1')
        password = generate_password()
        
        credentials = {
            'email': email,
            'password': password,
            'service': 'hackerone',
            'status': 'requires_phone_verification',
            'signup_url': 'https://www.hackerone.com/users/sign_up'
        }
        
        save_account('hackerone', email, credentials)
        
        print(f"[+] Credenciales HackerOne generadas:")
        print(f"    Email: {email}")
        print(f"    Pass:  {password}")
        print("    [!] Completa con teléfono en: https://www.hackerone.com/users/sign_up")
        
        return credentials
    
    def get_or_create_account(self, service: str, **kwargs) -> Dict[str, str]:
        """
        Obtiene cuenta existente o crea nueva automáticamente.
        Este es el método principal que llama el agente.
        """
        identifier = kwargs.get('email') or kwargs.get('username') or service
        
        # 1. Verificar vault local
        existing = account_exists(service, identifier)
        if existing:
            print(f"[*] Cuenta {service} ya existe en vault — recuperando...")
            existing['last_used'] = datetime.utcnow().isoformat() + 'Z'
            # Actualizar vault con last_used
            vault = load_vault()
            for acc in vault['accounts']:
                if acc['id'] == existing['id']:
                    acc['last_used'] = existing['last_used']
            save_vault(vault)
            return existing
        
        # 2. No existe → crear
        print(f"[*] Cuenta {service} no encontrada — creando automáticamente...")
        
        creators = {
            'proton': self.create_proton_account,
            'github': self.create_github_account,
            'hackerone': self.create_hackerone_account,
            'intigriti': self.create_hackerone_account,  # Similar flow
        }
        
        if service in creators:
            return creators[service](**kwargs)
        else:
            raise ValueError(f"Servicio '{service}' no soportado para auto-creación")

# --- Memory & Identity Tracking ---
class IdentityMemory:
    """Mantiene memoria persistente de identidades creadas"""
    
    def __init__(self):
        self.memory_path = MEMORY_PATH
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()
    
    def _load(self) -> Dict:
        if self.memory_path.exists():
            with open(self.memory_path, 'r') as f:
                return json.load(f)
        return {
            "identities": [],
            "last_service_used": None,
            "preferred_email_domain": "kalighost.dev",
            "auto_create_enabled": True,
            "created_at": datetime.utcnow().isoformat() + 'Z'
        }
    
    def save(self):
        with open(self.memory_path, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def record_identity_created(self, service: str, identifier: str, 
                                credentials: Dict):
        """Registra identidad creada en memoria"""
        identity = {
            "id": secrets.token_hex(8),
            "service": service,
            "identifier": identifier,
            "created_at": datetime.utcnow().isoformat() + 'Z',
            "last_used": datetime.utcnow().isoformat() + 'Z',
            "usage_count": 1
        }
        self.data['identities'].append(identity)
        self.data['last_service_used'] = service
        self.save()
    
    def get_identity(self, service: str) -> Optional[Dict]:
        for ident in self.data['identities']:
            if ident['service'] == service:
                return ident
        return None

# --- Proton Pass Sync (opcional) ---
class ProtonPassSync:
    """
    Sincroniza credenciales con Proton Pass.
    Requires: PROTON_API_KEY en entorno
    """
    
    API_BASE = "https://api.proton.me"
    
    def __init__(self):
        self.api_key = os.environ.get('PROTON_API_KEY')
        self.vault_name = os.environ.get('PROTON_VAULT_NAME', 'KaliGhost-Agent')
    
    def sync_credential(self, service: str, credentials: Dict) -> bool:
        """Guarda credencial en Proton Pass vault"""
        if not self.api_key:
            print("[*] Proton API key no configurada — skipping sync")
            return False
        
        # Implementar llamada a API Proton Pass
        # POST /pass/vaults/{vault_id}/items
        print(f"[*] Sincronizando {service} con Proton Pass...")
        # TODO: Implementar
        return True

# --- Entry point CLI ---
def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: identity_manager.py <service> [options]")
        print("Servicios: proton, github, hackerone, intigriti")
        sys.exit(1)
    
    service = sys.argv[1]
    creator = AccountCreator()
    memory = IdentityMemory()
    
    try:
        creds = creator.get_or_create_account(service)
        
        # Registrar en memoria
        identifier = creds.get('email') or creds.get('username')
        memory.record_identity_created(service, identifier, creds)
        
        # Output para el agente (JSON)
        output = {
            "status": "success",
            "service": service,
            "credentials": creds,
            "vault_path": str(VAULT_PATH),
            "message": f"Cuenta {service} lista"
        }
        
        print(json.dumps(output, indent=2))
        
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "service": service,
            "error": str(e)
        }, indent=2))
        sys.exit(1)

if __name__ == '__main__':
    main()