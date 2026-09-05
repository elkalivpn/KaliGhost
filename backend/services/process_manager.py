"""
Process Manager Module
Manages background processes, Docker containers, and micro-VMs
"""

import os
import signal
import subprocess
from typing import Dict, List, Optional, Any
from pathlib import Path
import docker


class ProcessManager:
    """
    Manages all processes in KaliGhost IDE
    Handles system processes, Docker containers, and isolated VMs
    """
    
    def __init__(self):
        self.processes: Dict[int, Dict[str, Any]] = {}
        self.containers: Dict[str, Any] = {}
        self.docker_client = None
        
        # Initialize Docker client if available
        try:
            self.docker_client = docker.from_env()
        except Exception:
            pass
    
    def start_process(self, command: List[str], name: str = None,
                      background: bool = True, **kwargs) -> Optional[int]:
        """
        Start a new process
        
        Args:
            command: Command to execute
            name: Process name for tracking
            background: Run in background
            
        Returns:
            Process ID or None
        """
        try:
            if background:
                proc = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    **kwargs
                )
            else:
                proc = subprocess.run(command, capture_output=True, **kwargs)
                return None
            
            pid = proc.pid
            self.processes[pid] = {
                'name': name or command[0],
                'command': command,
                'process': proc,
                'status': 'running'
            }
            
            return pid
            
        except Exception as e:
            return None
    
    def stop_process(self, pid: int, force: bool = False) -> bool:
        """
        Stop a process
        
        Args:
            pid: Process ID
            force: Use SIGKILL instead of SIGTERM
            
        Returns:
            Success status
        """
        if pid not in self.processes:
            return False
        
        try:
            proc_info = self.processes[pid]
            sig = signal.SIGKILL if force else signal.SIGTERM
            
            proc_info['process'].send_signal(sig)
            proc_info['process'].wait(timeout=5)
            
            del self.processes[pid]
            return True
            
        except Exception:
            # Force kill if normal termination fails
            try:
                os.kill(pid, signal.SIGKILL)
                del self.processes[pid]
                return True
            except:
                return False
    
    def get_process_status(self, pid: int) -> Optional[Dict]:
        """Get process status"""
        if pid not in self.processes:
            return None
        
        proc = self.processes[pid]['process']
        return {
            'pid': pid,
            'name': self.processes[pid]['name'],
            'status': 'running' if proc.poll() is None else 'stopped',
            'return_code': proc.poll()
        }
    
    def list_processes(self) -> List[Dict]:
        """List all managed processes"""
        return [
            {
                'pid': pid,
                'name': info['name'],
                'command': info['command'],
                'status': 'running' if info['process'].poll() is None else 'stopped'
            }
            for pid, info in self.processes.items()
        ]
    
    def start_container(self, image: str, name: str = None,
                        volumes: Dict = None, network: str = None,
                        command: List[str] = None, **kwargs) -> Optional[str]:
        """
        Start a Docker container
        
        Args:
            image: Docker image name
            name: Container name
            volumes: Volume mounts
            network: Network mode
            command: Command to run
            
        Returns:
            Container ID or None
        """
        if not self.docker_client:
            return None
        
        try:
            container = self.docker_client.containers.run(
                image,
                command=command,
                name=name,
                volumes=volumes,
                network_mode=network,
                detach=True,
                **kwargs
            )
            
            self.containers[container.id] = {
                'name': name or container.name,
                'image': image,
                'container': container
            }
            
            return container.id
            
        except Exception as e:
            return None
    
    def stop_container(self, container_id: str, force: bool = False) -> bool:
        """
        Stop a Docker container
        
        Args:
            container_id: Container ID
            force: Force stop
            
        Returns:
            Success status
        """
        if container_id not in self.containers:
            return False
        
        try:
            container = self.containers[container_id]['container']
            container.stop(timeout=5 if not force else 0)
            container.remove(force=force)
            
            del self.containers[container_id]
            return True
            
        except Exception:
            return False
    
    def list_containers(self) -> List[Dict]:
        """List all managed containers"""
        return [
            {
                'id': cid,
                'name': info['name'],
                'image': info['image'],
                'status': info['container'].status
            }
            for cid, info in self.containers.items()
        ]
    
    def start_sandbox_vm(self, name: str, image: str = None,
                         isolate_network: bool = True) -> Optional[str]:
        """
        Start an isolated sandbox VM for malware analysis
        
        Args:
            name: VM name
            image: Base image (qcow2 path)
            isolate_network: Enable network isolation
            
        Returns:
            VM identifier or None
        """
        # This would integrate with QEMU/KVM or similar
        # For now, use Docker with heavy restrictions
        return self.start_container(
            image='kalilinux/kali-rolling',
            name=f"sandbox_{name}",
            volumes={'/tmp/sandbox': {'bind': '/sandbox', 'mode': 'rw'}},
            network_mode='none' if isolate_network else 'bridge',
            cap_drop=['ALL'],
            security_opt=['no-new-privileges:true']
        )
    
    def cleanup_all(self):
        """Stop all managed processes and containers"""
        # Stop processes
        for pid in list(self.processes.keys()):
            self.stop_process(pid, force=True)
        
        # Stop containers
        for cid in list(self.containers.keys()):
            self.stop_container(cid, force=True)
    
    def __del__(self):
        self.cleanup_all()
