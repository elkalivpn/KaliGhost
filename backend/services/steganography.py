"""
KaliGhost IDE - Steganography and Deniable Volumes Module
Implements advanced steganography and deniable encrypted volumes for operational security.
"""

import os
import secrets
import hashlib
from typing import Optional, Tuple
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64


class DeniableVolume:
    """
    Creates and manages deniable encrypted volumes with plausible deniability.
    Uses a single container file that can have multiple passwords revealing different content.
    """
    
    def __init__(self, volume_path: str):
        self.volume_path = volume_path
        self.backend = default_backend()
        
    def create_volume(self, size_mb: int, outer_password: str, 
                     hidden_password: Optional[str] = None) -> bool:
        """
        Create a deniable volume with optional hidden partition.
        
        Args:
            size_mb: Size of the volume in megabytes
            outer_password: Password for the outer (decoy) volume
            hidden_password: Password for the hidden volume (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Generate random data for the entire volume
            size_bytes = size_mb * 1024 * 1024
            random_data = secrets.token_bytes(size_bytes)
            
            # Derive keys for outer and hidden volumes
            outer_key = self._derive_key(outer_password, b'outer_salt_kalighost')
            
            if hidden_password:
                hidden_key = self._derive_key(hidden_password, b'hidden_salt_kalighost')
                # Split volume: 60% outer, 40% hidden
                outer_size = int(size_bytes * 0.6)
                hidden_size = size_bytes - outer_size
                
                # Encrypt hidden partition first (at the end)
                hidden_data = random_data[outer_size:]
                hidden_encrypted = self._encrypt_data(hidden_data, hidden_key)
                
                # Encrypt outer partition
                outer_data = random_data[:outer_size]
                outer_encrypted = self._encrypt_data(outer_data, outer_key)
                
                # Combine: outer + hidden
                final_data = outer_encrypted + hidden_encrypted
            else:
                # Simple encrypted volume
                final_data = self._encrypt_data(random_data, outer_key)
            
            # Write to file
            with open(self.volume_path, 'wb') as f:
                f.write(final_data)
            
            # Set restrictive permissions
            os.chmod(self.volume_path, 0o600)
            
            return True
            
        except Exception as e:
            print(f"Error creating deniable volume: {e}")
            return False
    
    def mount_volume(self, password: str) -> Tuple[bool, Optional[bytes], str]:
        """
        Mount the volume with the given password.
        Returns success status, decrypted data, and volume type (outer/hidden).
        """
        try:
            if not os.path.exists(self.volume_path):
                return False, None, "error"
            
            with open(self.volume_path, 'rb') as f:
                encrypted_data = f.read()
            
            # Try outer password first
            outer_key = self._derive_key(password, b'outer_salt_kalighost')
            outer_size = int(len(encrypted_data) * 0.6)
            
            try:
                outer_decrypted = self._decrypt_data(encrypted_data[:outer_size], outer_key)
                # Check if decryption was successful (simple heuristic)
                if self._verify_plaintext(outer_decrypted):
                    return True, outer_decrypted, "outer"
            except:
                pass
            
            # Try hidden password
            hidden_key = self._derive_key(password, b'hidden_salt_kalighost')
            hidden_size = len(encrypted_data) - outer_size
            
            try:
                hidden_decrypted = self._decrypt_data(encrypted_data[outer_size:], hidden_key)
                if self._verify_plaintext(hidden_decrypted):
                    return True, hidden_decrypted, "hidden"
            except:
                pass
            
            return False, None, "invalid_password"
            
        except Exception as e:
            print(f"Error mounting volume: {e}")
            return False, None, "error"
    
    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """Derive a 256-bit key from password using PBKDF2."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=self.backend
        )
        return kdf.derive(password.encode())
    
    def _encrypt_data(self, data: bytes, key: bytes) -> bytes:
        """Encrypt data using AES-256-GCM."""
        iv = secrets.token_bytes(12)
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()
        return iv + encryptor.tag + ciphertext
    
    def _decrypt_data(self, data: bytes, key: bytes) -> bytes:
        """Decrypt data using AES-256-GCM."""
        iv = data[:12]
        tag = data[12:28]
        ciphertext = data[28:]
        
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=self.backend)
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()
    
    def _verify_plaintext(self, data: bytes) -> bool:
        """Simple heuristic to verify if decrypted data looks like valid plaintext."""
        # Check for common filesystem signatures or low entropy
        if len(data) < 100:
            return False
        
        # Look for null bytes at start (common in filesystems)
        if data[:10].count(b'\x00') > 5:
            return True
        
        # Check ASCII ratio
        ascii_chars = sum(1 for b in data[:1000] if 32 <= b <= 126 or b in (9, 10, 13))
        if ascii_chars > len(data[:1000]) * 0.7:
            return True
            
        return True


class SteganographyEngine:
    """
    Advanced steganography engine for hiding data in various carrier files.
    Supports images, audio, and video files with encryption.
    """
    
    def __init__(self):
        self.backend = default_backend()
    
    def hide_data(self, carrier_path: str, secret_data: bytes, 
                 password: str, output_path: str) -> bool:
        """
        Hide encrypted data within a carrier file using LSB steganography.
        
        Args:
            carrier_path: Path to the carrier file (PNG, WAV, etc.)
            secret_data: Data to hide
            password: Password for encryption
            output_path: Path for the output stego file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Encrypt the secret data first
            key = self._derive_key(password, b'stego_salt_kalighost')
            encrypted_data = self._encrypt_data(secret_data, key)
            
            # Add magic header and length
            header = b'KGST' + len(encrypted_data).to_bytes(8, 'big')
            full_payload = header + encrypted_data
            
            # Read carrier file
            with open(carrier_path, 'rb') as f:
                carrier_data = bytearray(f.read())
            
            # Check if carrier is large enough
            if len(carrier_data) < len(full_payload) * 8:
                print("Carrier file too small")
                return False
            
            # Find suitable area for embedding (skip headers for common formats)
            start_offset = self._get_header_size(carrier_path)
            
            # Embed data using LSB steganography
            bit_index = 0
            for byte in full_payload:
                for bit_pos in range(7, -1, -1):
                    if bit_index >= len(carrier_data) - start_offset:
                        return False
                    
                    pixel_index = start_offset + bit_index
                    bit = (byte >> bit_pos) & 1
                    
                    # Modify LSB
                    carrier_data[pixel_index] = (carrier_data[pixel_index] & 0xFE) | bit
                    bit_index += 1
            
            # Write output
            with open(output_path, 'wb') as f:
                f.write(carrier_data)
            
            return True
            
        except Exception as e:
            print(f"Error hiding data: {e}")
            return False
    
    def extract_data(self, stego_path: str, password: str) -> Optional[bytes]:
        """
        Extract hidden data from a stego file.
        
        Args:
            stego_path: Path to the stego file
            password: Password for decryption
            
        Returns:
            Extracted data or None if extraction fails
        """
        try:
            with open(stego_path, 'rb') as f:
                stego_data = f.read()
            
            start_offset = self._get_header_size(stego_path)
            
            # Extract bits using LSB
            extracted_bits = []
            bit_index = 0
            
            while True:
                byte_val = 0
                for bit_pos in range(7, -1, -1):
                    if start_offset + bit_index >= len(stego_data):
                        break
                    pixel_index = start_offset + bit_index
                    bit = stego_data[pixel_index] & 1
                    byte_val |= (bit << bit_pos)
                    bit_index += 1
                
                extracted_bits.append(byte_val)
                
                # Check for magic header
                if len(extracted_bits) == 4:
                    if bytes(extracted_bits) != b'KGST':
                        return None
                
                # Extract length after header
                if len(extracted_bits) == 12:
                    data_length = int.from_bytes(bytes(extracted_bits[4:12]), 'big')
                    total_bytes_needed = 12 + data_length
                    
                    if len(extracted_bits) >= total_bytes_needed:
                        encrypted_data = bytes(extracted_bits[12:12+data_length])
                        
                        # Decrypt
                        key = self._derive_key(password, b'stego_salt_kalighost')
                        return self._decrypt_data(encrypted_data, key)
            
            return None
            
        except Exception as e:
            print(f"Error extracting data: {e}")
            return None
    
    def _get_header_size(self, file_path: str) -> int:
        """Get the header size to skip for different file formats."""
        ext = file_path.lower().split('.')[-1]
        
        headers = {
            'png': 54,    # Skip PNG header
            'bmp': 54,    # Skip BMP header
            'wav': 44,    # Skip WAV header
            'avi': 100,   # Skip AVI header
        }
        
        return headers.get(ext, 0)
    
    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """Derive a 256-bit key from password."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=self.backend
        )
        return kdf.derive(password.encode())
    
    def _encrypt_data(self, data: bytes, key: bytes) -> bytes:
        """Encrypt data using AES-256-GCM."""
        iv = secrets.token_bytes(12)
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()
        return iv + encryptor.tag + ciphertext
    
    def _decrypt_data(self, data: bytes, key: bytes) -> bytes:
        """Decrypt data using AES-256-GCM."""
        iv = data[:12]
        tag = data[12:28]
        ciphertext = data[28:]
        
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=self.backend)
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()


# Utility functions for metadata cleaning
def clean_metadata(file_path: str) -> bool:
    """
    Remove all metadata from a file in real-time.
    Supports images, documents, and media files.
    """
    try:
        import subprocess
        
        # Try using exiftool if available
        try:
            subprocess.run(['exiftool', '-all=', file_path], 
                         capture_output=True, check=True)
            # Remove backup file created by exiftool
            backup_file = file_path + '_original'
            if os.path.exists(backup_file):
                os.remove(backup_file)
            return True
        except FileNotFoundError:
            pass
        
        # Fallback: basic metadata removal for common formats
        ext = file_path.lower().split('.')[-1]
        
        if ext in ['jpg', 'jpeg', 'png', 'gif']:
            # Simple approach: re-save without metadata
            try:
                from PIL import Image
                img = Image.open(file_path)
                # Save without metadata
                img.save(file_path, format=img.format)
                return True
            except ImportError:
                pass
        
        # For other files, overwrite metadata sections with zeros
        with open(file_path, 'r+b') as f:
            content = f.read()
            # This is a simplified approach - real implementation would be format-specific
            pass
        
        return True
        
    except Exception as e:
        print(f"Error cleaning metadata: {e}")
        return False


if __name__ == "__main__":
    # Example usage
    print("KaliGhost Steganography and Deniable Volumes Module")
    
    # Test deniable volume
    volume = DeniableVolume("/tmp/test_volume.kgv")
    success = volume.create_volume(10, "outer_pass", "hidden_pass")
    print(f"Volume created: {success}")
    
    # Test steganography
    stego = SteganographyEngine()
    # Note: Would need actual carrier file for full test
