# KaliGhost Security Best Practices

This document outlines essential security practices for safely operating and extending the KaliGhost platform. Following these guidelines ensures the confidentiality, integrity, and availability of both the KaliGhost system and the environments it assesses.

## Table of Contents

1. [Operational Security](#operational-security)
2. [Network Security](#network-security)
3. [Data Protection](#data-protection)
4. [Authentication and Authorization](#authentication-and-authorization)
5. [System Hardening](#system-hardening)
6. [Secure Coding Practices](#secure-coding-practices)
7. [Incident Response](#incident-response)
8. [Compliance Considerations](#compliance-considerations)
9. [Third-Party Integrations](#third-party-integrations)

## Operational Security

### Environment Isolation

Always maintain separate environments for different security domains:

```yaml
# Example environment separation in docker-compose.yml
version: '3.8'
services:
  kalighost-core:
    # Production environment
    networks:
      - prod-network
      
  kalighost-testing:
    # Testing environment
    networks:
      - test-network
      
  kalighost-client-a:
    # Client-specific environment
    networks:
      - client-a-network

networks:
  prod-network:
    driver: bridge
    internal: true
    
  test-network:
    driver: bridge
    internal: true
    
  client-a-network:
    driver: bridge
    internal: true
```

### Secure Communication

Ensure all communications are encrypted:

```python
import ssl
import socket
from OpenSSL import SSL

def create_secure_socket_connection(hostname: str, port: int) -> socket.socket:
    """
    Create a securely configured socket connection.
    
    Args:
        hostname: Target hostname
        port: Target port
        
    Returns:
        Secure socket connection
    """
    # Create SSL context with strong security settings
    context = ssl.create_default_context()
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    context.set_ciphers('HIGH:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!SRP:!CAMELLIA')
    
    # Establish secure connection
    sock = socket.create_connection((hostname, port))
    secure_sock = context.wrap_socket(sock, server_hostname=hostname)
    
    return secure_sock
```

### Credential Management

Never hardcode credentials; always use secure storage:

```python
import os
from cryptography.fernet import Fernet

class SecureCredentialManager:
    """Manage credentials securely using encryption."""
    
    def __init__(self):
        # Get encryption key from secure environment
        self.key = os.environ.get('CREDENTIAL_ENCRYPTION_KEY')
        if not self.key:
            raise ValueError("Encryption key not found in environment")
        self.cipher_suite = Fernet(self.key.encode())
    
    def store_credential(self, service: str, credential: str) -> None:
        """
        Store credential securely.
        
        Args:
            service: Service name
            credential: Credential to store
        """
        # Encrypt credential
        encrypted_cred = self.cipher_suite.encrypt(credential.encode())
        
        # Store in secure location (e.g., encrypted file, secure vault)
        with open(f'/secure/vault/{service}.enc', 'wb') as f:
            f.write(encrypted_cred)
    
    def retrieve_credential(self, service: str) -> str:
        """
        Retrieve credential securely.
        
        Args:
            service: Service name
            
        Returns:
            Decrypted credential
        """
        # Read encrypted credential
        with open(f'/secure/vault/{service}.enc', 'rb') as f:
            encrypted_cred = f.read()
        
        # Decrypt credential
        decrypted_cred = self.cipher_suite.decrypt(encrypted_cred)
        return decrypted_cred.decode()
```

## Network Security

### Network Segmentation

Implement proper network segmentation:

```python
import subprocess
import iptables

class NetworkSecurityManager:
    """Manage network security policies."""
    
    def __init__(self):
        self.base_rules = [
            "-P INPUT DROP",
            "-P FORWARD DROP",
            "-P OUTPUT ACCEPT",
            "-A INPUT -i lo -j ACCEPT",
            "-A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT"
        ]
    
    def apply_assessment_isolation(self, target_network: str) -> None:
        """
        Apply isolation rules for security assessment.
        
        Args:
            target_network: Network being assessed
        """
        # Block all outbound traffic except to target network
        rules = self.base_rules.copy()
        rules.append(f"-A OUTPUT -d {target_network} -j ACCEPT")
        rules.append("-A OUTPUT -o lo -j ACCEPT")
        
        # Apply rules
        for rule in rules:
            subprocess.run(["iptables", rule.split()])
    
    def remove_isolation(self) -> None:
        """Remove isolation rules."""
        subprocess.run(["iptables", "-F"])
        subprocess.run(["iptables", "-P", "INPUT", "ACCEPT"])
        subprocess.run(["iptables", "-P", "FORWARD", "ACCEPT"])
        subprocess.run(["iptables", "-P", "OUTPUT", "ACCEPT"])
```

### Traffic Monitoring

Monitor network traffic for anomalies:

```python
import pyshark
from collections import defaultdict
import time

class NetworkTrafficMonitor:
    """Monitor network traffic for suspicious activity."""
    
    def __init__(self, interface: str = "eth0"):
        self.interface = interface
        self.connection_stats = defaultdict(int)
        self.alert_threshold = 100  # connections per minute
    
    def start_monitoring(self, duration_minutes: int = 60) -> None:
        """
        Start monitoring network traffic.
        
        Args:
            duration_minutes: Duration to monitor (default: 60 minutes)
        """
        capture = pyshark.LiveCapture(interface=self.interface)
        start_time = time.time()
        
        for packet in capture.sniff_continuously():
            if time.time() - start_time > duration_minutes * 60:
                break
                
            # Track connection attempts
            if hasattr(packet, 'tcp'):
                conn_key = f"{packet.ip.src}:{packet.tcp.srcport}-{packet.ip.dst}:{packet.tcp.dstport}"
                self.connection_stats[conn_key] += 1
                
                # Check for potential scanning activity
                if self.connection_stats[conn_key] > self.alert_threshold:
                    self._alert_potential_scan(conn_key)
    
    def _alert_potential_scan(self, connection: str) -> None:
        """
        Alert on potential scanning activity.
        
        Args:
            connection: Connection identifier
        """
        print(f"WARN: Potential scanning detected: {connection}")
        # Additional alerting logic here (email, syslog, etc.)
```

### Secure Tunneling

Use secure tunnels for remote access:

```bash
# SSH tunnel for secure remote KaliGhost access
ssh -L 8080:localhost:8080 -N user@remote-host

# VPN setup for assessment
sudo openvpn --config assessment.ovpn --auth-user-pass vpn-credentials.txt

# Tor for anonymous operations
torsocks python3 agent.py --task "anonymous assessment"
```

## Data Protection

### Encryption at Rest

Encrypt sensitive data stored on disk:

```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

class DataEncryptionService:
    """Provide encryption for data at rest."""
    
    def __init__(self):
        self.backend = default_backend()
    
    def encrypt_file(self, input_path: str, output_path: str, key: bytes) -> None:
        """
        Encrypt file using AES-256-GCM.
        
        Args:
            input_path: Path to input file
            output_path: Path to output encrypted file
            key: 32-byte encryption key
        """
        # Generate random IV
        iv = os.urandom(12)
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(iv),
            backend=self.backend
        )
        encryptor = cipher.encryptor()
        
        # Process file in chunks
        with open(input_path, 'rb') as infile, \
             open(output_path, 'wb') as outfile:
            
            # Write IV to beginning of file
            outfile.write(iv)
            
            # Encrypt and write data
            while chunk := infile.read(65536):  # 64KB chunks
                ciphertext = encryptor.update(chunk)
                outfile.write(ciphertext)
            
            # Finalize encryption
            finalize_cipher = encryptor.finalize()
            outfile.write(finalize_cipher)
            
            # Write authentication tag
            outfile.write(encryptor.tag)
    
    def decrypt_file(self, input_path: str, output_path: str, key: bytes) -> None:
        """
        Decrypt file using AES-256-GCM.
        
        Args:
            input_path: Path to encrypted input file
            output_path: Path to output decrypted file
            key: 32-byte decryption key
        """
        with open(input_path, 'rb') as infile:
            # Read IV from beginning of file
            iv = infile.read(12)
            
            # Create cipher
            cipher = Cipher(
                algorithms.AES(key),
                modes.GCM(iv),
                backend=self.backend
            )
            decryptor = cipher.decryptor()
            
            # Process file in chunks
            with open(output_path, 'wb') as outfile:
                # Read file content (excluding IV and auth tag)
                file_content = infile.read()
                ciphertext = file_content[:-16]  # Last 16 bytes are auth tag
                auth_tag = file_content[-16:]
                
                # Set authentication tag
                decryptor.authenticate_additional_data(auth_tag)
                
                # Decrypt and write data
                while chunk := ciphertext[65536:]:
                    plaintext = decryptor.update(chunk)
                    outfile.write(plaintext)
                
                # Finalize decryption
                outfile.write(decryptor.finalize())
```

### Data Loss Prevention

Implement data loss prevention measures:

```python
import re
import hashlib
from typing import List, Pattern

class DataLossPrevention:
    """Prevent accidental exposure of sensitive data."""
    
    def __init__(self):
        self.sensitive_patterns: List[Pattern] = [
            re.compile(r'\b\d{16}\b'),  # Credit card numbers
            re.compile(r'\b[A-Z0-9]{10,30}\b'),  # API keys
            re.compile(r'\b\d{3}-?\d{2}-?\d{4}\b'),  # SSNs
            re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')  # Email addresses
        ]
        self.exclusion_patterns: List[Pattern] = [
            re.compile(r'version|copyright|license', re.IGNORECASE)
        ]
    
    def scan_for_sensitive_data(self, text: str) -> List[str]:
        """
        Scan text for potentially sensitive data.
        
        Args:
            text: Text to scan
            
        Returns:
            List of sensitive data matches
        """
        findings = []
        
        # Skip excluded content
        if any(pattern.search(text) for pattern in self.exclusion_patterns):
            return findings
        
        # Check for sensitive patterns
        for pattern in self.sensitive_patterns:
            matches = pattern.findall(text)
            findings.extend(matches)
        
        return findings
    
    def sanitize_output(self, text: str) -> str:
        """
        Remove sensitive data from text.
        
        Args:
            text: Text to sanitize
            
        Returns:
            Sanitized text
        """
        sanitized = text
        
        for pattern in self.sensitive_patterns:
            # Replace matches with masked versions
            sanitized = pattern.sub('[REDACTED]', sanitized)
        
        return sanitized
```

### Secure File Handling

Handle files securely to prevent leaks:

```python
import os
import stat
import tempfile
from pathlib import Path

class SecureFileManager:
    """Manage file operations securely."""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix='kalighost_')
        # Set restrictive permissions
        os.chmod(self.temp_dir, stat.S_IRWXU)  # 700 - owner only
    
    def create_secure_temp_file(self, suffix: str = '') -> str:
        """
        Create temporary file with secure permissions.
        
        Args:
            suffix: File suffix
            
        Returns:
            Path to temporary file
        """
        temp_file = tempfile.NamedTemporaryFile(
            dir=self.temp_dir,
            suffix=suffix,
            delete=False
        )
        temp_file.close()
        
        # Set restrictive permissions (600 - owner read/write only)
        os.chmod(temp_file.name, stat.S_IRUSR | stat.S_IWUSR)
        
        return temp_file.name
    
    def secure_delete(self, file_path: str) -> None:
        """
        Securely delete file by overwriting before removal.
        
        Args:
            file_path: Path to file to delete
        """
        if not os.path.exists(file_path):
            return
            
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Overwrite with random data multiple times
        with open(file_path, 'r+b') as f:
            for _ in range(3):  # 3 passes
                f.seek(0)
                f.write(os.urandom(file_size))
                f.flush()
                os.fsync(f.fileno())
        
        # Remove file
        os.remove(file_path)
```

## Authentication and Authorization

### Multi-Factor Authentication

Implement multi-factor authentication for administrative access:

```python
import pyotp
import qrcode
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class MultiFactorAuth:
    """Handle multi-factor authentication."""
    
    def __init__(self):
        self.totp = pyotp.TOTP(pyotp.random_base32())
    
    def generate_qr_code(self, username: str) -> str:
        """
        Generate QR code for TOTP setup.
        
        Args:
            username: User identifier
            
        Returns:
            Path to QR code image
        """
        uri = self.totp.provisioning_uri(
            name=username,
            issuer_name="KaliGhost"
        )
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        qr_path = f"/tmp/mfa_{username}.png"
        img.save(qr_path)
        
        return qr_path
    
    def verify_totp(self, token: str) -> bool:
        """
        Verify TOTP token.
        
        Args:
            token: 6-digit TOTP token
            
        Returns:
            True if valid, False otherwise
        """
        return self.totp.verify(token)
    
    def derive_key_from_password(self, password: str, salt: bytes) -> bytes:
        """
        Derive encryption key from password using PBKDF2.
        
        Args:
            password: User password
            salt: Random salt
            
        Returns:
            Derived key
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return kdf.derive(password.encode())
```

### Role-Based Access Control

Implement fine-grained access control:

```python
from enum import Enum
from typing import Set, Dict

class Permission(Enum):
    """Permission levels."""
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"
    AUDIT = "audit"

class Role(Enum):
    """User roles."""
    ANALYST = "analyst"
    SENIOR_ANALYST = "senior_analyst"
    ADMIN = "admin"
    AUDITOR = "auditor"

class AccessControl:
    """Manage role-based access control."""
    
    def __init__(self):
        self.role_permissions: Dict[Role, Set[Permission]] = {
            Role.ANALYST: {Permission.READ, Permission.EXECUTE},
            Role.SENIOR_ANALYST: {Permission.READ, Permission.WRITE, Permission.EXECUTE},
            Role.ADMIN: {Permission.READ, Permission.WRITE, Permission.EXECUTE, Permission.ADMIN},
            Role.AUDITOR: {Permission.READ, Permission.AUDIT}
        }
        
        self.user_roles: Dict[str, Set[Role]] = {}
    
    def assign_role(self, user_id: str, role: Role) -> None:
        """
        Assign role to user.
        
        Args:
            user_id: User identifier
            role: Role to assign
        """
        if user_id not in self.user_roles:
            self.user_roles[user_id] = set()
        self.user_roles[user_id].add(role)
    
    def check_permission(self, user_id: str, permission: Permission) -> bool:
        """
        Check if user has permission.
        
        Args:
            user_id: User identifier
            permission: Permission to check
            
        Returns:
            True if user has permission, False otherwise
        """
        if user_id not in self.user_roles:
            return False
            
        user_roles = self.user_roles[user_id]
        for role in user_roles:
            if permission in self.role_permissions[role]:
                return True
            if Role.ADMIN in user_roles:
                return True  # Admins have all permissions
                
        return False
    
    def require_permission(self, user_id: str, permission: Permission) -> None:
        """
        Require permission (raises exception if not granted).
        
        Args:
            user_id: User identifier
            permission: Required permission
            
        Raises:
            PermissionError: If user lacks required permission
        """
        if not self.check_permission(user_id, permission):
            raise PermissionError(
                f"User {user_id} lacks required permission: {permission.value}"
            )
```

## System Hardening

### Container Security

Secure container configurations:

```dockerfile
# Multi-stage build for security and size optimization
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage with minimal attack surface
FROM python:3.11-alpine

# Add non-root user
RUN addgroup -g 1001 -S kalighost &&\
    adduser -u 1001 -S kalighost -G kalighost

# Install minimal runtime dependencies
RUN apk add --no-cache \
    libgl \
    libglib \
    curl

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy application
COPY . /app
WORKDIR /app

# Change ownership to non-root user
RUN chown -R kalighost:kalighost /app

# Drop privileges
USER kalighost

# Expose only necessary ports
EXPOSE 8080

# Health check with limited scope
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Prevent privilege escalation
RUN chmod 755 /app

# Set secure environment defaults
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Run application
ENTRYPOINT ["python3"]
CMD ["main.py"]
```

### Kernel Security

Implement Linux kernel security enhancements:

```python
import subprocess
import os

class KernelSecurityManager:
    """Manage kernel-level security settings."""
    
    def __init__(self):
        self.security_modules = {
            'selinux': self._configure_selinux,
            'apparmor': self._configure_apparmor
        }
    
    def enable_aslr(self) -> None:
        """Enable Address Space Layout Randomization."""
        with open('/proc/sys/kernel/randomize_va_space', 'w') as f:
            f.write('2')  # Full randomization
    
    def disable_core_dumps(self) -> None:
        """Disable core dumps to prevent memory inspection."""
        with open('/proc/sys/fs/suid_dumpable', 'w') as f:
            f.write('0')
        
        # Set ulimits
        subprocess.run(['ulimit', '-c', '0'])
    
    def configure_kernel_parameters(self) -> None:
        """Configure additional security parameters."""
        security_params = {
            'kernel.exec-shield': '1',
            'kernel.kptr_restrict': '1',
            'kernel.dmesg_restrict': '1',
            'net.ipv4.conf.all.rp_filter': '1',
            'net.ipv4.conf.default.rp_filter': '1',
            'net.ipv4.icmp_echo_ignore_broadcasts': '1'
        }
        
        for param, value in security_params.items():
            try:
                with open(f'/proc/sys/{param.replace(".", "/")}', 'w') as f:
                    f.write(value)
            except IOError:
                print(f"Warning: Could not set {param}")
    
    def apply_sysctl_hardening(self) -> None:
        """Apply system-wide security hardening."""
        sysctl_config = """
# Network security
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv4.conf.all.secure_redirects = 0
net.ipv4.conf.default.secure_redirects = 0
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0
net.ipv6.conf.all.accept_redirects = 0
net.ipv6.conf.default.accept_redirects = 0
net.ipv6.conf.all.accept_source_route = 0
net.ipv6.conf.default.accept_source_route = 0

# TCP hardening
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 4096

# Hide kernel pointers
kernel.kptr_restrict = 1
kernel.dmesg_restrict = 1

# Disable unprivileged bpf
kernel.unprivileged_bpf_disabled = 1
"""
        
        with open('/etc/sysctl.d/99-kalighost-security.conf', 'w') as f:
            f.write(sysctl_config)
        
        subprocess.run(['sysctl', '--system'])
```

## Secure Coding Practices

### Input Validation

Validate all inputs rigorously:

```python
import re
from typing import Union, List
from urllib.parse import urlparse

class InputValidator:
    """Validate all user inputs."""
    
    def __init__(self):
        self.patterns = {
            'ip_address': re.compile(r'^(\d{1,3}\.){3}\d{1,3}$'),
            'hostname': re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'),
            'port_range': re.compile(r'^\d{1,5}(-\d{1,5})?$'),
            'url': re.compile(r'^https?://'),
            'filename': re.compile(r'^[\w\-.]+$')
        }
    
    def validate_ip_address(self, ip: str) -> bool:
        """Validate IP address format and values."""
        if not self.patterns['ip_address'].match(ip):
            return False
            
        parts = ip.split('.')
        return all(0 <= int(part) <= 255 for part in parts)
    
    def validate_hostname(self, hostname: str) -> bool:
        """Validate hostname format."""
        if not self.patterns['hostname'].match(hostname):
            return False
            
        if len(hostname) > 253:
            return False
            
        # Check label lengths
        labels = hostname.split('.')
        return all(1 <= len(label) <= 63 for label in labels)
    
    def validate_port_range(self, port_range: str) -> bool:
        """Validate port range specification."""
        if not self.patterns['port_range'].match(port_range):
            return False
            
        if '-' in port_range:
            start, end = map(int, port_range.split('-'))
            return 1 <= start <= 65535 and 1 <= end <= 65535 and start <= end
        else:
            port = int(port_range)
            return 1 <= port <= 65535
    
    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to prevent path traversal."""
        # Remove dangerous characters
        safe_chars = self.patterns['filename']
        sanitized = ''.join(c for c in filename if safe_chars.match(c) or c in '.-_')
        
        # Prevent directory traversal
        while '../' in sanitized:
            sanitized = sanitized.replace('../', '')
        
        # Remove leading dots to prevent hidden files
        sanitized = sanitized.lstrip('.')
        
        return sanitized if sanitized else 'unnamed_file'
```

### Safe Command Execution

Execute system commands safely:

```python
import subprocess
import shlex
from typing import List, Optional

class SafeCommandExecutor:
    """Execute system commands with security safeguards."""
    
    def __init__(self):
        self.allowed_commands = {
            'nmap', 'masscan', 'sqlmap', 'nikto', 'ffuf', 'gobuster'
        }
        self.dangerous_patterns = [
            ';', '&&', '||', '|', '`', '$(', '${', '>', '<', '>>', '<<'
        ]
    
    def execute_safe_command(self, 
                           command: str, 
                           args: List[str], 
                           timeout: int = 300,
                           check_allowed: bool = True) -> subprocess.CompletedProcess:
        """
        Execute command safely with input validation.
        
        Args:
            command: Command to execute
            args: Command arguments
            timeout: Execution timeout in seconds
            check_allowed: Whether to check against allowed command list
            
        Returns:
            Command execution result
            
        Raises:
            ValueError: If command is not allowed or contains dangerous patterns
            subprocess.TimeoutExpired: If command exceeds timeout
        """
        # Check if command is allowed
        if check_allowed and command not in self.allowed_commands:
            raise ValueError(f"Command not allowed: {command}")
        
        # Validate arguments for dangerous patterns
        full_command = ' '.join([command] + args)
        for pattern in self.dangerous_patterns:
            if pattern in full_command:
                raise ValueError(f"Dangerous pattern detected: {pattern}")
        
        # Validate individual arguments
        validated_args = []
        for arg in args:
            # Check for dangerous patterns in each argument
            for pattern in self.dangerous_patterns:
                if pattern in arg:
                    raise ValueError(f"Dangerous pattern in argument: {pattern}")
            
            # Quote arguments properly
            validated_args.append(shlex.quote(arg))
        
        # Construct final command
        cmd = [command] + validated_args
        
        # Execute with timeout and security constraints
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,  # Don't raise on non-zero exit codes
                cwd='/tmp',  # Restrict to safe directory
                env={'PATH': '/usr/local/bin:/usr/bin:/bin'}  # Limited PATH
            )
            return result
        except subprocess.TimeoutExpired as e:
            raise subprocess.TimeoutExpired(cmd, timeout) from e
    
    def execute_nmap_safely(self, 
                          targets: List[str], 
                          options: List[str] = None,
                          timeout: int = 600) -> subprocess.CompletedProcess:
        """
        Execute nmap with additional safety checks.
        
        Args:
            targets: Target hosts to scan
            options: Nmap options
            timeout: Execution timeout
            
        Returns:
            Nmap execution result
        """
        if options is None:
            options = ['-sV', '-sC']
        
        # Validate targets
        for target in targets:
            if not (self.validate_ip_address(target) or 
                   self.validate_hostname(target)):
                raise ValueError(f"Invalid target: {target}")
        
        # Restrict dangerous nmap options
        dangerous_nmap_options = [
            '--script', '--script-trace', '--script-updatedb',
            '--resume', '--stylesheet'
        ]
        for option in options:
            if option in dangerous_nmap_options:
                raise ValueError(f"Dangerous nmap option: {option}")
        
        # Construct command
        cmd = ['nmap'] + options + targets
        
        # Execute safely
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
            cwd='/tmp'
        )
```

### Error Handling Without Information Leakage

Handle errors securely:

```python
import logging
import traceback
from typing import Optional

class SecureErrorHandler:
    """Handle errors without leaking sensitive information."""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.sensitive_keywords = [
            'password', 'secret', 'key', 'token', 'credential',
            'private', 'ssh', 'api_key', 'auth'
        ]
    
    def handle_exception(self, 
                        exception: Exception, 
                        context: str = "",
                        user_message: Optional[str] = None) -> str:
        """
        Handle exception securely.
        
        Args:
            exception: Exception to handle
            context: Context where error occurred
            user_message: Message to show to user
            
        Returns:
            Sanitized user message
        """
        # Log full error details securely (not shown to user)
        self.logger.error(
            f"Error in {context}: {str(exception)}", 
            exc_info=True
        )
        
        # Sanitize error message for user display
        error_msg = str(exception)
        sanitized_msg = self._sanitize_error_message(error_msg)
        
        # Return generic message to prevent information leakage
        if user_message:
            return user_message
        else:
            return "An error occurred while processing your request. Please try again."
    
    def _sanitize_error_message(self, message: str) -> str:
        """
        Remove sensitive information from error message.
        
        Args:
            message: Error message to sanitize
            
        Returns:
            Sanitized message
        """
        sanitized = message
        
        # Remove sensitive keywords and their values
        for keyword in self.sensitive_keywords:
            # Simple pattern matching (in practice, use more sophisticated regex)
            if keyword in sanitized.lower():
                # Replace with generic placeholder
                sanitized = re.sub(
                    rf'{keyword}[^,\.\s]*', 
                    f'{keyword}_[REDACTED]', 
                    sanitized, 
                    flags=re.IGNORECASE
                )
        
        # Remove stack traces from user-facing messages
        if 'Traceback' in sanitized:
            sanitized = sanitized.split('Traceback')[0].strip()
        
        return sanitized
```

## Incident Response

### Security Event Monitoring

Monitor for security events:

```python
import time
from datetime import datetime
from typing import Dict, List
import json

class SecurityEventMonitor:
    """Monitor for security-related events."""
    
    def __init__(self, log_file: str = "/var/log/kalighost/security.log"):
        self.log_file = log_file
        self.alert_thresholds = {
            'failed_logins': 5,  # Failed logins per hour
            'suspicious_commands': 10,  # Suspicious commands per hour
            'large_data_exports': 3,  # Large data exports per hour
            'unauthorized_access': 1  # Any unauthorized access attempts
        }
        self.event_buffer: List[Dict] = []
    
    def log_security_event(self, 
                          event_type: str, 
                          severity: str, 
                          details: Dict) -> None:
        """
        Log security event.
        
        Args:
            event_type: Type of security event
            severity: Severity level (low, medium, high, critical)
            details: Event details
        """
        event = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'type': event_type,
            'severity': severity,
            'details': details
        }
        
        # Write to security log
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(event) + '\n')
        
        # Add to buffer for analysis
        self.event_buffer.append(event)
        
        # Check for alert conditions
        self._check_alert_conditions(event)
    
    def _check_alert_conditions(self, new_event: Dict) -> None:
        """
        Check if event triggers alert conditions.
        
        Args:
            new_event: New event to evaluate
        """
        # Analyze recent events for patterns
        recent_events = self._get_recent_events(hours=1)
        
        # Check for excessive failed logins
        failed_logins = [
            e for e in recent_events 
            if e['type'] == 'failed_login'
        ]
        if len(failed_logins) >= self.alert_thresholds['failed_logins']:
            self._trigger_alert('excessive_failed_logins', len(failed_logins))
        
        # Check for suspicious command execution
        suspicious_commands = [
            e for e in recent_events
            if e['type'] == 'suspicious_command'
        ]
        if len(suspicious_commands) >= self.alert_thresholds['suspicious_commands']:
            self._trigger_alert('suspicious_activity', len(suspicious_commands))
    
    def _get_recent_events(self, hours: int = 1) -> List[Dict]:
        """
        Get events from recent time period.
        
        Args:
            hours: Number of hours to look back
            
        Returns:
            List of recent events
        """
        cutoff_time = time.time() - (hours * 3600)
        recent_events = []
        
        for event in self.event_buffer:
            event_timestamp = datetime.fromisoformat(
                event['timestamp'].rstrip('Z')
            ).timestamp()
            if event_timestamp >= cutoff_time:
                recent_events.append(event)
        
        return recent_events
    
    def _trigger_alert(self, alert_type: str, count: int) -> None:
        """
        Trigger security alert.
        
        Args:
            alert_type: Type of alert
            count: Number of triggering events
        """
        alert_message = f"SECURITY ALERT: {alert_type} ({count} events)"
        
        # Log alert
        self.logger.critical(alert_message)
        
        # Send alert to security team (implementation depends on alerting system)
        self._send_security_alert(alert_message)
    
    def _send_security_alert(self, message: str) -> None:
        """
        Send alert to security team.
        
        Args:
            message: Alert message
        """
        # This would integrate with your alerting system
        # Examples: email, SMS, Slack webhook, SIEM integration
        print(f"SENDING ALERT: {message}")
```

### Emergency Response Procedures

Establish emergency response procedures:

```python
import os
import signal
import sys
from typing import Callable

class EmergencyResponseSystem:
    """Handle emergency situations."""
    
    def __init__(self):
        self.emergency_callbacks: List[Callable] = []
        self.graceful_shutdown_enabled = True
        
        # Register signal handlers
        signal.signal(signal.SIGTERM, self._handle_shutdown_signal)
        signal.signal(signal.SIGINT, self._handle_shutdown_signal)
        signal.signal(signal.SIGUSR1, self._handle_emergency_signal)
    
    def register_emergency_callback(self, callback: Callable) -> None:
        """
        Register callback to be called during emergency shutdown.
        
        Args:
            callback: Function to call during emergency
        """
        self.emergency_callbacks.append(callback)
    
    def _handle_shutdown_signal(self, signum: int, frame) -> None:
        """
        Handle graceful shutdown signals.
        
        Args:
            signum: Signal number
            frame: Frame object
        """
        print("Received shutdown signal, initiating graceful shutdown...")
        self.initiate_graceful_shutdown()
    
    def _handle_emergency_signal(self, signum: int, frame) -> None:
        """
        Handle emergency signals.
        
        Args:
            signum: Signal number
            frame: Frame object
        """
        print("Received emergency signal, initiating immediate shutdown...")
        self.initiate_emergency_shutdown()
    
    def initiate_graceful_shutdown(self) -> None:
        """Initiate graceful shutdown sequence."""
        try:
            # Execute registered callbacks
            for callback in self.emergency_callbacks:
                try:
                    callback()
                except Exception as e:
                    print(f"Error in emergency callback: {e}")
            
            # Perform cleanup
            self._cleanup_resources()
            
            print("Graceful shutdown completed.")
            sys.exit(0)
            
        except Exception as e:
            print(f"Error during graceful shutdown: {e}")
            self.initiate_emergency_shutdown()
    
    def initiate_emergency_shutdown(self) -> None:
        """Initiate immediate emergency shutdown."""
        print("Emergency shutdown initiated!")
        
        # Immediate resource cleanup
        self._emergency_cleanup()
        
        # Force exit
        os._exit(1)
    
    def _cleanup_resources(self) -> None:
        """Perform normal resource cleanup."""
        # Close open files
        # Terminate child processes
        # Flush logs
        # Clear temporary files
        pass
    
    def _emergency_cleanup(self) -> None:
        """Perform immediate emergency cleanup."""
        # Kill all child processes
        # Clear sensitive memory
        # Flush critical logs immediately
        # Wipe temporary sensitive data
        pass
    
    def activate_ghost_mode(self) -> None:
        """Activate maximum security cleanup procedures."""
        print("Activating Ghost Mode - securing all traces...")
        
        # Clear volatile memory
        # Encrypt/wipe logs
        # Clean temporary files
        # Reset network state
        # Shutdown system
        self.initiate_graceful_shutdown()

# Global instance
emergency_system = EmergencyResponseSystem()
```

## Compliance Considerations

### Data Privacy Regulations

Ensure compliance with privacy regulations:

```python
from enum import Enum
from datetime import datetime, timedelta
from typing import Dict, List

class PrivacyRegulation(Enum):
    """Privacy regulations."""
    GDPR = "gdpr"
    CCPA = "ccpa"
    HIPAA = "hipaa"
    PCI_DSS = "pci_dss"

class ComplianceManager:
    """Manage compliance with privacy regulations."""
    
    def __init__(self):
        self.regulations = {
            PrivacyRegulation.GDPR: self._check_gdpr_compliance,
            PrivacyRegulation.CCPA: self._check_ccpa_compliance,
            PrivacyRegulation.HIPAA: self._check_hipaa_compliance,
            PrivacyRegulation.PCI_DSS: self._check_pci_compliance
        }
        self.data_retention_policies = {
            PrivacyRegulation.GDPR: timedelta(days=2555),  # ~7 years
            PrivacyRegulation.CCPA: timedelta(days=365),   # 1 year
            PrivacyRegulation.HIPAA: timedelta(days=2555), # 7 years
            PrivacyRegulation.PCI_DSS: timedelta(days=365) # 1 year
        }
    
    def check_compliance(self, 
                        regulation: PrivacyRegulation, 
                        data_category: str) -> Dict:
        """
        Check compliance for specific regulation and data category.
        
        Args:
            regulation: Regulation to check
            data_category: Category of data being processed
            
        Returns:
            Compliance status and recommendations
        """
        checker = self.regulations.get(regulation)
        if not checker:
            raise ValueError(f"Unknown regulation: {regulation}")
            
        return checker(data_category)
    
    def _check_gdpr_compliance(self, data_category: str) -> Dict:
        """Check GDPR compliance."""
        requirements = {
            'consent': False,
            'data_minimization': True,
            'purpose_limitation': True,
            'storage_limitation': True,
            'integrity_confidentiality': True,
            'accountability': True
        }
        
        # Specific checks based on data category
        if data_category == 'personal':
            requirements['consent'] = True
            requirements['right_to_erasure'] = True
            requirements['data_portability'] = True
        
        return {
            'regulation': 'GDPR',
            'compliant': all(requirements.values()),
            'requirements': requirements,
            'recommendations': self._get_gdpr_recommendations(requirements)
        }
    
    def _get_gdpr_recommendations(self, requirements: Dict) -> List[str]:
        """Get GDPR compliance recommendations."""
        recommendations = []
        
        if not requirements.get('consent'):
            recommendations.append(
                "Implement explicit consent mechanism for personal data processing"
            )
        
        if not requirements.get('right_to_erasure'):
            recommendations.append(
                "Implement data deletion capability upon user request"
            )
        
        if not requirements.get('data_portability'):
            recommendations.append(
                "Provide data export functionality in standard format"
            )
        
        return recommendations
    
    def apply_data_retention_policy(self, 
                                  regulation: PrivacyRegulation, 
                                  data_age: timedelta) -> bool:
        """
        Apply data retention policy.
        
        Args:
            regulation: Regulation governing data retention
            data_age: Age of data
            
        Returns:
            True if data should be retained, False if it should be deleted
        """
        max_retention = self.data_retention_policies.get(regulation)
        if not max_retention:
            return True  # Keep if no specific policy
            
        return data_age <= max_retention
```

### Audit Logging

Maintain comprehensive audit logs:

```python
import json
import hashlib
from datetime import datetime
from typing import Dict, Any

class AuditLogger:
    """Maintain secure audit logs."""
    
    def __init__(self, log_file: str = "/var/log/kalighost/audit.log"):
        self.log_file = log_file
        self.audit_events = [
            'user_login', 'user_logout', 'permission_change',
            'tool_execution', 'config_change', 'data_access',
            'report_generation', 'file_operation'
        ]
    
    def log_audit_event(self, 
                       event_type: str, 
                       user_id: str, 
                       details: Dict[str, Any],
                       sensitive: bool = False) -> None:
        """
        Log audit event securely.
        
        Args:
            event_type: Type of audit event
            user_id: User who triggered event
            details: Event details
            sensitive: Whether event contains sensitive information
        """
        if event_type not in self.audit_events:
            raise ValueError(f"Unknown audit event type: {event_type}")
        
        # Create audit record
        audit_record = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'event_type': event_type,
            'user_id': user_id,
            'session_id': self._get_current_session_id(),
            'details_hash': self._hash_details(details) if sensitive else None,
            'details': details if not sensitive else {},
            'ip_address': self._get_client_ip(),
            'user_agent': self._get_user_agent()
        }
        
        # Write to audit log
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(audit_record) + '\n')
    
    def _hash_details(self, details: Dict) -> str:
        """
        Create hash of sensitive details for verification.
        
        Args:
            details: Details to hash
            
        Returns:
            SHA-256 hash of details
        """
        details_str = json.dumps(details, sort_keys=True)
        return hashlib.sha256(details_str.encode()).hexdigest()
    
    def _get_current_session_id(self) -> str:
        """Get current session identifier."""
        # Implementation depends on session management system
        return "session_placeholder"
    
    def _get_client_ip(self) -> str:
        """Get client IP address."""
        # Implementation depends on web framework
        return "127.0.0.1"
    
    def _get_user_agent(self) -> str:
        """Get user agent string."""
        # Implementation depends on web framework
        return "KaliGhost-Agent/1.0"
    
    def export_audit_log(self, 
                        start_time: datetime, 
                        end_time: datetime,
                        format: str = 'json') -> str:
        """
        Export audit log for specified time period.
        
        Args:
            start_time: Start of export period
            end_time: End of export period
            format: Export format (json, csv)
            
        Returns:
            Path to exported file
        """
        # Implementation for exporting audit trails
        return "/tmp/audit_export.json"
```

## Third-Party Integrations

### Secure API Integration

Securely integrate with external APIs:

```python
import requests
import jwt
import time
from cryptography.hazmat.primitives import serialization
from typing import Optional, Dict, Any

class SecureAPIIntegration:
    """Securely integrate with third-party APIs."""
    
    def __init__(self, 
                 api_base_url: str, 
                 api_key: Optional[str] = None,
                 jwt_private_key: Optional[str] = None):
        self.api_base_url = api_base_url.rstrip('/')
        self.api_key = api_key
        self.jwt_private_key = jwt_private_key
        self.session = requests.Session()
        
        # Configure session with security settings
        self.session.headers.update({
            'User-Agent': 'KaliGhost-Security-Scanner/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    
    def make_authenticated_request(self, 
                                 endpoint: str, 
                                 method: str = 'GET',
                                 data: Optional[Dict] = None,
                                 params: Optional[Dict] = None) -> requests.Response:
        """
        Make authenticated API request.
        
        Args:
            endpoint: API endpoint
            method: HTTP method
            data: Request payload
            params: Query parameters
            
        Returns:
            API response
        """
        url = f"{self.api_base_url}/{endpoint.lstrip('/')}"
        
        # Add authentication headers
        headers = self._get_auth_headers()
        
        # Make request with timeout and security settings
        try:
            response = self.session.request(
                method=method.upper(),
                url=url,
                headers=headers,
                json=data,
                params=params,
                timeout=30,
                verify=True  # Ensure SSL verification
            )
            
            # Validate response
            self._validate_response(response)
            
            return response
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """
        Generate appropriate authentication headers.
        
        Returns:
            Authentication headers
        """
        headers = {}
        
        if self.jwt_private_key:
            # Generate JWT token
            token = self._generate_jwt_token()
            headers['Authorization'] = f"Bearer {token}"
        elif self.api_key:
            # Use API key
            headers['X-API-Key'] = self.api_key
        else:
            # No authentication (public API)
            pass
        
        return headers
    
    def _generate_jwt_token(self) -> str:
        """
        Generate JWT token for authentication.
        
        Returns:
            JWT token
        """
        # Load private key
        private_key = serialization.load_pem_private_key(
            self.jwt_private_key.encode(),
            password=None
        )
        
        # Create payload
        payload = {
            'iss': 'KaliGhost',
            'exp': int(time.time()) + 3600,  # 1 hour expiration
            'iat': int(time.time()),
            'sub': 'api-access'
        }
        
        # Generate token
        token = jwt.encode(payload, private_key, algorithm='RS256')
        return token
    
    def _validate_response(self, response: requests.Response) -> None:
        """
        Validate API response for security issues.
        
        Args:
            response: API response to validate
        """
        # Check for suspicious headers
        suspicious_headers = [
            'server', 'x-powered-by', 'x-aspnet-version'
        ]
        for header in suspicious_headers:
            if header in response.headers:
                print(f"Warning: Server exposed via header: {header}")
        
        # Validate content type
        content_type = response.headers.get('content-type', '')
        if not content_type.startswith('application/json'):
            raise Exception("Unexpected response content type")
        
        # Check response size (prevent resource exhaustion)
        if len(response.content) > 10 * 1024 * 1024:  # 10MB limit
            raise Exception("Response too large")

```

Following these security best practices will help ensure that KaliGhost operates as a secure, compliant, and trustworthy penetration testing platform. Remember that security is an ongoing process that requires continuous attention and adaptation to new threats and technologies.

---
© 2026 KaliGhost Project. All rights reserved.