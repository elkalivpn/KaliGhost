"""
KaliGhost IDE - Dead Man's Switch and Secret Sharing Module
Implements automatic trigger mechanisms and cryptographic secret sharing.
Provides advanced persistence security and emergency response capabilities.
"""

import os
import sys
import time
import secrets
import hashlib
import threading
import json
import base64
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


@dataclass
class ShareConfig:
    """Configuration for secret sharing."""
    total_shares: int
    threshold: int
    share_data: List[bytes]


class ShamirSecretSharing:
    """
    Implementation of Shamir's Secret Sharing scheme.
    Splits secrets into multiple shares requiring a threshold to reconstruct.
    """
    
    def __init__(self, prime: int = None):
        # Use a large prime for finite field arithmetic
        self.prime = prime or (2**255 - 19)
        self.backend = default_backend()
    
    def split_secret(self, secret: bytes, total_shares: int, 
                    threshold: int) -> ShareConfig:
        """
        Split a secret into multiple shares.
        
        Args:
            secret: The secret to split
            total_shares: Total number of shares to create
            threshold: Minimum shares needed to reconstruct
            
        Returns:
            ShareConfig with all shares
        """
        if threshold > total_shares:
            raise ValueError("Threshold cannot exceed total shares")
        if threshold < 1:
            raise ValueError("Threshold must be at least 1")
        
        # Convert secret to integer (big-endian)
        secret_int = int.from_bytes(secret, 'big')
        
        shares = []
        
        for i in range(1, total_shares + 1):
            # Generate random coefficients for polynomial
            coefficients = [secret_int]
            for _ in range(threshold - 1):
                coefficients.append(secrets.randbelow(self.prime))
            
            # Evaluate polynomial at point i
            share_value = 0
            for j, coef in enumerate(coefficients):
                share_value = (share_value + coef * pow(i, j, self.prime)) % self.prime
            
            shares.append((i, share_value.to_bytes(32, 'big')))
        
        return ShareConfig(
            total_shares=total_shares,
            threshold=threshold,
            share_data=[json.dumps({'index': s[0], 'value': base64.b64encode(s[1]).decode()}).encode() 
                       for s in shares]
        )
    
    def reconstruct_secret(self, shares: List[Tuple[int, bytes]], 
                          threshold: int) -> Optional[bytes]:
        """
        Reconstruct the secret from shares using Lagrange interpolation.
        
        Args:
            shares: List of (index, value) tuples
            threshold: Threshold used when splitting
            
        Returns:
            Reconstructed secret or None if failed
        """
        if len(shares) < threshold:
            print(f"Need at least {threshold} shares, got {len(shares)}")
            return None
        
        # Convert shares to integers
        points = []
        for index, value in shares[:threshold]:
            points.append((index, int.from_bytes(value, 'big')))
        
        # Lagrange interpolation
        secret = 0
        
        for i, (xi, yi) in enumerate(points):
            numerator = 1
            denominator = 1
            
            for j, (xj, _) in enumerate(points):
                if i != j:
                    numerator = (numerator * (-xj)) % self.prime
                    denominator = (denominator * (xi - xj)) % self.prime
            
            # Modular inverse using Fermat's little theorem
            inv_denom = pow(denominator, self.prime - 2, self.prime)
            lagrange_coef = (numerator * inv_denom) % self.prime
            
            secret = (secret + yi * lagrange_coef) % self.prime
        
        # Convert back to bytes
        try:
            byte_length = (secret.bit_length() + 7) // 8
            return secret.to_bytes(byte_length, 'big')
        except:
            return None
    
    def verify_share(self, share: bytes, public_params: Dict) -> bool:
        """Verify if a share is valid (simplified verification)."""
        try:
            data = json.loads(share.decode())
            return 'index' in data and 'value' in data
        except:
            return False


class DeadMansSwitch:
    """
    Dead Man's Switch implementation with multiple trigger conditions.
    Automatically executes actions when triggers are activated.
    """
    
    def __init__(self, switch_id: str = None):
        self.switch_id = switch_id or secrets.token_hex(8)
        self.triggers: Dict[str, Dict[str, Any]] = {}
        self.actions: List[Callable] = []
        self.is_active = False
        self.last_check_time = None
        self.check_interval = 60  # seconds
        self.monitor_thread: Optional[threading.Thread] = None
        self.lock = threading.Lock()
        
    def add_time_trigger(self, max_interval: int, 
                        action: Callable,
                        description: str = "No activity detected") -> str:
        """
        Add a time-based trigger.
        
        Args:
            max_interval: Maximum seconds between checks before triggering
            action: Function to call when triggered
            description: Description of the trigger
            
        Returns:
            Trigger ID
        """
        trigger_id = f"time_{secrets.token_hex(4)}"
        
        self.triggers[trigger_id] = {
            'type': 'time',
            'max_interval': max_interval,
            'last_activity': time.time(),
            'action': action,
            'description': description,
            'enabled': True
        }
        
        return trigger_id
    
    def add_heartbeat_trigger(self, heartbeat_file: str,
                             max_age: int,
                             action: Callable,
                             description: str = "Heartbeat lost") -> str:
        """
        Add a heartbeat file trigger.
        
        Args:
            heartbeat_file: Path to heartbeat file
            max_age: Maximum age in seconds before triggering
            action: Function to call when triggered
            description: Description of the trigger
            
        Returns:
            Trigger ID
        """
        trigger_id = f"heartbeat_{secrets.token_hex(4)}"
        
        self.triggers[trigger_id] = {
            'type': 'heartbeat',
            'file': heartbeat_file,
            'max_age': max_age,
            'action': action,
            'description': description,
            'enabled': True
        }
        
        return trigger_id
    
    def add_process_trigger(self, process_name: str,
                           must_exist: bool = True,
                           action: Callable = None,
                           description: str = None) -> str:
        """
        Add a process existence trigger.
        
        Args:
            process_name: Name of process to monitor
            must_exist: If True, trigger when process disappears
                       If False, trigger when process appears
            action: Function to call when triggered
            description: Description of the trigger
            
        Returns:
            Trigger ID
        """
        trigger_id = f"process_{secrets.token_hex(4)}"
        
        if not description:
            desc_type = "disappeared" if must_exist else "appeared"
            description = f"Process {process_name} {desc_type}"
        
        self.triggers[trigger_id] = {
            'type': 'process',
            'process_name': process_name,
            'must_exist': must_exist,
            'action': action,
            'description': description,
            'enabled': True
        }
        
        return trigger_id
    
    def add_network_trigger(self, host: str, port: int,
                           must_reachable: bool = True,
                           action: Callable = None,
                           description: str = None,
                           timeout: int = 5) -> str:
        """
        Add a network reachability trigger.
        
        Args:
            host: Host to monitor
            port: Port to check
            must_reachable: If True, trigger when unreachable
                           If False, trigger when reachable
            action: Function to call when triggered
            description: Description of the trigger
            timeout: Connection timeout in seconds
            
        Returns:
            Trigger ID
        """
        trigger_id = f"network_{secrets.token_hex(4)}"
        
        if not description:
            desc_type = "unreachable" if must_reachable else "reachable"
            description = f"Host {host}:{port} became {desc_type}"
        
        self.triggers[trigger_id] = {
            'type': 'network',
            'host': host,
            'port': port,
            'must_reachable': must_reachable,
            'timeout': timeout,
            'action': action,
            'description': description,
            'enabled': True
        }
        
        return trigger_id
    
    def register_action(self, action: Callable):
        """Register a global action to execute on any trigger."""
        self.actions.append(action)
    
    def reset_timer(self, trigger_id: str = None):
        """Reset the timer for a time-based trigger."""
        with self.lock:
            if trigger_id:
                if trigger_id in self.triggers:
                    self.triggers[trigger_id]['last_activity'] = time.time()
            else:
                # Reset all time triggers
                for tid, trigger in self.triggers.items():
                    if trigger['type'] == 'time':
                        trigger['last_activity'] = time.time()
    
    def start_monitoring(self):
        """Start the monitoring thread."""
        if self.is_active:
            return
        
        self.is_active = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop the monitoring thread."""
        self.is_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
            self.monitor_thread = None
    
    def _monitor_loop(self):
        """Main monitoring loop."""
        while self.is_active:
            self._check_triggers()
            time.sleep(self.check_interval)
    
    def _check_triggers(self):
        """Check all triggers and execute actions if needed."""
        current_time = time.time()
        triggered = []
        
        with self.lock:
            for trigger_id, trigger in self.triggers.items():
                if not trigger['enabled']:
                    continue
                
                should_trigger = False
                
                if trigger['type'] == 'time':
                    elapsed = current_time - trigger['last_activity']
                    if elapsed > trigger['max_interval']:
                        should_trigger = True
                        
                elif trigger['type'] == 'heartbeat':
                    try:
                        file_mtime = os.path.getmtime(trigger['file'])
                        age = current_time - file_mtime
                        if age > trigger['max_age']:
                            should_trigger = True
                    except FileNotFoundError:
                        should_trigger = True
                        
                elif trigger['type'] == 'process':
                    process_exists = self._check_process_exists(trigger['process_name'])
                    if trigger['must_exist'] and not process_exists:
                        should_trigger = True
                    elif not trigger['must_exist'] and process_exists:
                        should_trigger = True
                        
                elif trigger['type'] == 'network':
                    reachable = self._check_network_reachable(
                        trigger['host'], 
                        trigger['port'],
                        trigger['timeout']
                    )
                    if trigger['must_reachable'] and not reachable:
                        should_trigger = True
                    elif not trigger['must_reachable'] and reachable:
                        should_trigger = True
                
                if should_trigger:
                    triggered.append(trigger)
        
        # Execute actions for triggered conditions
        for trigger in triggered:
            print(f"DMS Trigger activated: {trigger['description']}")
            
            # Execute trigger-specific action
            if trigger.get('action'):
                try:
                    trigger['action']()
                except Exception as e:
                    print(f"Error executing trigger action: {e}")
            
            # Execute global actions
            for action in self.actions:
                try:
                    action()
                except Exception as e:
                    print(f"Error executing global action: {e}")
    
    def _check_process_exists(self, process_name: str) -> bool:
        """Check if a process exists by name."""
        try:
            import subprocess
            result = subprocess.run(
                ['pgrep', '-f', process_name],
                capture_output=True
            )
            return result.returncode == 0
        except:
            return False
    
    def _check_network_reachable(self, host: str, port: int, 
                                timeout: int) -> bool:
        """Check if a host:port is reachable."""
        try:
            socket_conn = __import__('socket').socket()
            socket_conn.settimeout(timeout)
            result = socket_conn.connect_ex((host, port))
            socket_conn.close()
            return result == 0
        except:
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the dead man's switch."""
        with self.lock:
            return {
                'switch_id': self.switch_id,
                'is_active': self.is_active,
                'trigger_count': len(self.triggers),
                'triggers': [
                    {
                        'id': tid,
                        'type': t['type'],
                        'description': t['description'],
                        'enabled': t['enabled']
                    }
                    for tid, t in self.triggers.items()
                ],
                'action_count': len(self.actions)
            }


class EmergencyResponseSystem:
    """
    Coordinates emergency responses including secret destruction,
    data wiping, and alert notifications.
    """
    
    def __init__(self):
        self.dms = DeadMansSwitch()
        self.sss = ShamirSecretSharing()
        self.response_actions: Dict[str, Callable] = {}
        self.secret_shares: Dict[str, ShareConfig] = {}
        
    def setup_standard_protection(self, wipe_paths: List[str] = None,
                                 notification_webhook: str = None) -> DeadMansSwitch:
        """
        Set up standard protection with common triggers.
        
        Args:
            wipe_paths: Paths to wipe on trigger
            notification_webhook: Webhook URL for notifications
            
        Returns:
            Configured DeadMansSwitch
        """
        dms = DeadMansSwitch()
        
        # Time trigger - no activity for 30 minutes
        def emergency_wipe():
            if wipe_paths:
                self._secure_wipe_paths(wipe_paths)
            if notification_webhook:
                self._send_notification(notification_webhook, "Emergency wipe initiated")
        
        dms.add_time_trigger(
            max_interval=1800,  # 30 minutes
            action=emergency_wipe,
            description="No operator activity for 30 minutes"
        )
        
        # Heartbeat trigger
        dms.add_heartbeat_trigger(
            heartbeat_file="/tmp/kalighost_heartbeat",
            max_age=300,  # 5 minutes
            action=emergency_wipe,
            description="Heartbeat signal lost"
        )
        
        # Process trigger - panic if terminal closes
        dms.add_process_trigger(
            process_name="kalighost_session",
            must_exist=True,
            action=emergency_wipe,
            description="KaliGhost session terminated unexpectedly"
        )
        
        self.dms = dms
        return dms
    
    def split_critical_secret(self, secret: bytes, locations: List[str],
                             threshold: int = None) -> ShareConfig:
        """
        Split a critical secret and distribute shares.
        
        Args:
            secret: The secret to split
            locations: Where to store each share
            threshold: Reconstruction threshold (default: len(locations)//2 + 1)
            
        Returns:
            ShareConfig with all shares
        """
        if threshold is None:
            threshold = len(locations) // 2 + 1
        
        shares = self.sss.split_secret(secret, len(locations), threshold)
        
        # Store shares in specified locations
        for i, location in enumerate(locations):
            try:
                with open(location, 'wb') as f:
                    f.write(shares.share_data[i])
                os.chmod(location, 0o600)
            except Exception as e:
                print(f"Error storing share at {location}: {e}")
        
        return shares
    
    def recover_secret(self, share_paths: List[str], 
                      threshold: int) -> Optional[bytes]:
        """
        Recover a secret from stored shares.
        
        Args:
            share_paths: Paths to share files
            threshold: Required threshold
            
        Returns:
            Recovered secret or None
        """
        shares = []
        
        for path in share_paths[:threshold]:
            try:
                with open(path, 'rb') as f:
                    share_data = f.read()
                data = json.loads(share_data.decode())
                index = data['index']
                value = base64.b64decode(data['value'])
                shares.append((index, value))
            except Exception as e:
                print(f"Error reading share from {path}: {e}")
                return None
        
        return self.sss.reconstruct_secret(shares, threshold)
    
    def _secure_wipe_paths(self, paths: List[str]):
        """Securely wipe specified paths."""
        for path in paths:
            try:
                if os.path.isfile(path):
                    self._secure_wipe_file(path)
                elif os.path.isdir(path):
                    import shutil
                    shutil.rmtree(path, ignore_errors=True)
            except Exception as e:
                print(f"Error wiping {path}: {e}")
    
    def _secure_wipe_file(self, filepath: str, passes: int = 3):
        """Securely wipe a file with multiple overwrite passes."""
        try:
            file_size = os.path.getsize(filepath)
            
            with open(filepath, 'r+b') as f:
                # Pass 1: Write zeros
                f.seek(0)
                f.write(b'\x00' * file_size)
                f.flush()
                os.fsync(f.fileno())
                
                # Pass 2: Write ones
                f.seek(0)
                f.write(b'\xFF' * file_size)
                f.flush()
                os.fsync(f.fileno())
                
                # Pass 3: Write random
                if passes >= 3:
                    f.seek(0)
                    f.write(secrets.token_bytes(file_size))
                    f.flush()
                    os.fsync(f.fileno())
            
            # Delete file
            os.remove(filepath)
            
        except Exception as e:
            print(f"Error secure wiping {filepath}: {e}")
    
    def _send_notification(self, webhook_url: str, message: str):
        """Send notification to webhook."""
        try:
            import requests
            requests.post(webhook_url, json={'message': message}, timeout=10)
        except Exception as e:
            print(f"Error sending notification: {e}")


# Singleton instance
_emergency_system: Optional[EmergencyResponseSystem] = None


def get_emergency_system() -> EmergencyResponseSystem:
    """Get or create emergency response system singleton."""
    global _emergency_system
    if _emergency_system is None:
        _emergency_system = EmergencyResponseSystem()
    return _emergency_system


if __name__ == "__main__":
    print("KaliGhost Dead Man's Switch and Secret Sharing Module")
    
    # Test Shamir Secret Sharing
    sss = ShamirSecretSharing()
    secret = b"SuperSecretKey1234567890"
    
    print("\n=== Testing Secret Sharing ===")
    shares = sss.split_secret(secret, 5, 3)
    print(f"Split secret into {shares.total_shares} shares (threshold: {shares.threshold})")
    
    # Reconstruct with 3 shares
    selected_shares = []
    for i in range(3):
        data = json.loads(shares.share_data[i].decode())
        selected_shares.append((data['index'], base64.b64decode(data['value'])))
    
    recovered = sss.reconstruct_secret(selected_shares, 3)
    print(f"Recovered secret: {recovered}")
    print(f"Match: {recovered == secret}")
    
    # Test Dead Man's Switch
    print("\n=== Testing Dead Man's Switch ===")
    dms = DeadMansSwitch()
    
    def test_action():
        print(">>> TRIGGER ACTIVATED! <<<")
    
    dms.add_time_trigger(10, test_action, "Test timer")
    dms.start_monitoring()
    
    print(f"DMS Status: {dms.get_status()}")
    print("Monitoring started (will trigger in 10 seconds without reset)")
    
    # Reset once to demonstrate
    time.sleep(3)
    dms.reset_timer()
    print("Timer reset!")
    
    time.sleep(5)
    dms.stop_monitoring()
    print("Monitoring stopped")
