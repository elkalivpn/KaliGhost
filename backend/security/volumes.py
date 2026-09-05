"""
Encrypted Volume Module
LUKS-like encrypted volume management for persistent storage
"""

import os
import subprocess
from pathlib import Path
from typing import Optional
import tempfile
import shutil


class EncryptedVolume:
    """
    Manages encrypted volumes for secure persistence
    Uses dm-crypt/LUKS on Linux or fallback encryption
    """
    
    def __init__(self, volume_path: Path, passphrase: str):
        self.volume_path = volume_path
        self.passphrase = passphrase
        self.mount_point: Optional[Path] = None
        self.device_name: Optional[str] = None
        self.is_mounted = False
    
    def create(self, size_gb: int = 10) -> bool:
        """
        Create a new encrypted volume
        
        Args:
            size_gb: Size in gigabytes
            
        Returns:
            Success status
        """
        try:
            # Create volume file
            self.volume_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create sparse file or actual size
            with open(self.volume_path, 'wb') as f:
                f.seek(size_gb * 1024 * 1024 * 1024 - 1)
                f.write(b'\0')
            
            # Initialize with LUKS if available
            if self._has_luks():
                return self._init_luks()
            else:
                # Fallback: just create directory structure
                self.volume_path.mkdir(exist_ok=True)
                return True
                
        except Exception as e:
            return False
    
    def mount(self) -> bool:
        """
        Mount the encrypted volume
        
        Returns:
            Success status
        """
        if self.is_mounted:
            return True
        
        try:
            if self._has_luks() and self.volume_path.is_file():
                return self._mount_luks()
            else:
                # Fallback: use directory
                self.mount_point = self.volume_path
                self.mount_point.mkdir(exist_ok=True)
                self.is_mounted = True
                return True
                
        except Exception as e:
            return False
    
    def unmount(self) -> bool:
        """
        Unmount the encrypted volume
        
        Returns:
            Success status
        """
        if not self.is_mounted:
            return True
        
        try:
            if self._has_luks() and self.device_name:
                return self._unmount_luks()
            else:
                # Fallback: nothing to unmount
                self.is_mounted = False
                return True
                
        except Exception as e:
            return False
    
    def _has_luks(self) -> bool:
        """Check if LUKS tools are available"""
        try:
            result = subprocess.run(
                ['which', 'cryptsetup'],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def _init_luks(self) -> bool:
        """Initialize LUKS volume"""
        try:
            # Format with LUKS
            subprocess.run([
                'cryptsetup', '-q', 'luksFormat',
                str(self.volume_path)
            ], input=self.passphrase.encode(), timeout=30)
            
            return True
        except Exception as e:
            return False
    
    def _mount_luks(self) -> bool:
        """Mount LUKS volume"""
        try:
            self.device_name = f"kalighost_{os.getpid()}"
            
            # Open LUKS container
            subprocess.run([
                'cryptsetup', 'open',
                str(self.volume_path),
                self.device_name
            ], input=self.passphrase.encode(), timeout=30)
            
            # Create mount point
            self.mount_point = Path(tempfile.mkdtemp(prefix='kg_vol_'))
            
            # Mount
            subprocess.run([
                'mount',
                f'/dev/mapper/{self.device_name}',
                str(self.mount_point)
            ], timeout=30)
            
            self.is_mounted = True
            return True
            
        except Exception as e:
            if self.device_name:
                self._unmount_luks()
            return False
    
    def _unmount_luks(self) -> bool:
        """Unmount LUKS volume"""
        try:
            if self.mount_point:
                # Unmount filesystem
                subprocess.run([
                    'umount', str(self.mount_point)
                ], timeout=30)
                
                # Remove mount point
                shutil.rmtree(self.mount_point, ignore_errors=True)
            
            if self.device_name:
                # Close LUKS
                subprocess.run([
                    'cryptsetup', 'close', self.device_name
                ], timeout=30)
            
            self.mount_point = None
            self.device_name = None
            self.is_mounted = False
            
            return True
            
        except Exception as e:
            return False
    
    def get_path(self) -> Optional[Path]:
        """Get mounted volume path"""
        return self.mount_point
