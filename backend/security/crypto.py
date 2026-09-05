"""
Cryptography Module
AES-256-GCM encryption, key management, and secure operations
"""

import os
import hashlib
from pathlib import Path
from typing import Optional, Tuple
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import secrets


class CryptoManager:
    """
    Manages cryptographic operations for KaliGhost IDE
    Provides AES-256-GCM encryption with PBKDF2 key derivation
    """
    
    def __init__(self):
        self.backend = default_backend()
        self.iterations = 100_000  # PBKDF2 iterations
    
    def derive_key(self, passphrase: str, salt: bytes) -> bytes:
        """
        Derive a 256-bit key from passphrase using PBKDF2
        
        Args:
            passphrase: User passphrase
            salt: Random salt (16 bytes recommended)
            
        Returns:
            32-byte derived key
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.iterations,
            backend=self.backend
        )
        return kdf.derive(passphrase.encode('utf-8'))
    
    def encrypt(self, plaintext: bytes, passphrase: str) -> Tuple[bytes, bytes, bytes]:
        """
        Encrypt data using AES-256-GCM
        
        Args:
            plaintext: Data to encrypt
            passphrase: Encryption passphrase
            
        Returns:
            Tuple of (salt, nonce, ciphertext)
        """
        # Generate random salt and nonce
        salt = secrets.token_bytes(16)
        nonce = secrets.token_bytes(12)  # 96-bit nonce for GCM
        
        # Derive key
        key = self.derive_key(passphrase, salt)
        
        # Encrypt
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(nonce, plaintext, None)
        
        return salt, nonce, ciphertext
    
    def decrypt(self, salt: bytes, nonce: bytes, ciphertext: bytes, 
                passphrase: str) -> bytes:
        """
        Decrypt data using AES-256-GCM
        
        Args:
            salt: Salt used for encryption
            nonce: Nonce used for encryption
            ciphertext: Encrypted data
            passphrase: Decryption passphrase
            
        Returns:
            Decrypted plaintext
            
        Raises:
            cryptography.exceptions.AuthenticationError: If decryption fails
        """
        # Derive key
        key = self.derive_key(passphrase, salt)
        
        # Decrypt
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        
        return plaintext
    
    def encrypt_file(self, input_path: str, output_path: str, passphrase: str) -> bool:
        """
        Encrypt a file
        
        Args:
            input_path: Path to input file
            output_path: Path for encrypted output
            passphrase: Encryption passphrase
            
        Returns:
            Success status
        """
        try:
            # Read input file
            with open(input_path, 'rb') as f:
                plaintext = f.read()
            
            # Encrypt
            salt, nonce, ciphertext = self.encrypt(plaintext, passphrase)
            
            # Write output: salt (16) + nonce (12) + ciphertext
            with open(output_path, 'wb') as f:
                f.write(salt)
                f.write(nonce)
                f.write(ciphertext)
            
            return True
            
        except Exception as e:
            return False
    
    def decrypt_file(self, input_path: str, output_path: str, passphrase: str) -> bool:
        """
        Decrypt a file
        
        Args:
            input_path: Path to encrypted file
            output_path: Path for decrypted output
            passphrase: Decryption passphrase
            
        Returns:
            Success status
        """
        try:
            # Read encrypted file
            with open(input_path, 'rb') as f:
                salt = f.read(16)
                nonce = f.read(12)
                ciphertext = f.read()
            
            # Decrypt
            plaintext = self.decrypt(salt, nonce, ciphertext, passphrase)
            
            # Write output
            with open(output_path, 'wb') as f:
                f.write(plaintext)
            
            return True
            
        except Exception as e:
            return False
    
    def hash_password(self, password: str) -> str:
        """
        Hash a password securely
        
        Args:
            password: Plain text password
            
        Returns:
            Hex-encoded hash with salt
        """
        salt = secrets.token_hex(16)
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            self.iterations
        ).hex()
        
        return f"{salt}${key}"
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """
        Verify a password against its hash
        
        Args:
            password: Plain text password
            hashed: Stored hash (salt$key format)
            
        Returns:
            Verification result
        """
        try:
            salt, key = hashed.split('$')
            new_key = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt.encode('utf-8'),
                self.iterations
            ).hex()
            
            return secrets.compare_digest(key, new_key)
            
        except Exception:
            return False
    
    def generate_key(self) -> str:
        """Generate a random secure key"""
        return secrets.token_hex(32)
    
    def secure_wipe(self, data: bytearray) -> None:
        """
        Securely wipe sensitive data from memory
        
        Args:
            data: Bytearray to wipe
        """
        for i in range(len(data)):
            data[i] = 0
        # Force garbage collection
        import gc
        gc.collect()
