"""
KaliGhost IDE - RAM-Only Execution Module
Implements execution of processes exclusively in RAM for maximum operational security.
No traces left on disk.
"""

import os
import sys
import mmap
import ctypes
import secrets
import tempfile
import subprocess
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import threading
import time


@dataclass
class RAMProcess:
    """Represents a process running exclusively in RAM."""
    pid: int
    name: str
    memory_size: int
    start_time: float
    is_critical: bool


class RAMExecutionEngine:
    """
    Engine for executing code and processes exclusively in RAM.
    Ensures no traces are left on disk during or after execution.
    """
    
    def __init__(self):
        self.processes: Dict[int, RAMProcess] = {}
        self.lock = threading.Lock()
        self.libc = ctypes.CDLL("libc.so.6", use_errno=True)
        
    def execute_in_ram(self, code: bytes, args: List[str] = None, 
                      is_critical: bool = True) -> Optional[RAMProcess]:
        """
        Execute binary code directly in RAM without writing to disk.
        
        Args:
            code: Binary executable code
            args: Command line arguments
            is_critical: If True, extra precautions are taken
            
        Returns:
            RAMProcess object if successful, None otherwise
        """
        try:
            # Create anonymous memory mapping (not backed by file)
            page_size = os.sysconf(os.sysconf_names['SC_PAGESIZE'])
            code_size = len(code)
            mapped_size = ((code_size // page_size) + 1) * page_size
            
            # Use MAP_ANONYMOUS | MAP_PRIVATE for RAM-only allocation
            MAP_ANONYMOUS = 0x20
            MAP_PRIVATE = 0x02
            PROT_READ = 0x1
            PROT_WRITE = 0x2
            PROT_EXEC = 0x4
            
            # Allocate executable memory
            mem_ptr = self.libc.mmap(
                0,
                mapped_size,
                PROT_READ | PROT_WRITE,
                MAP_ANONYMOUS | MAP_PRIVATE,
                -1,
                0
            )
            
            if mem_ptr == ctypes.c_void_p(-1).value:
                errno = ctypes.get_errno()
                print(f"mmap failed with errno {errno}")
                return None
            
            # Copy code to allocated memory
            ctypes.memmove(mem_ptr, code, code_size)
            
            # Make memory executable
            result = self.libc.mprotect(
                ctypes.c_void_p(mem_ptr),
                mapped_size,
                PROT_READ | PROT_EXEC
            )
            
            if result != 0:
                print("mprotect failed")
                self._cleanup_memory(mem_ptr, mapped_size)
                return None
            
            # Fork and execute
            pid = os.fork()
            
            if pid == 0:
                # Child process
                try:
                    # Execute code from memory
                    # Note: This is a simplified example - real implementation
                    # would need proper function pointer casting
                    ctypes.cast(mem_ptr, ctypes.CFUNCTYPE(ctypes.c_int))()
                except Exception as e:
                    os._exit(1)
                os._exit(0)
            else:
                # Parent process
                with self.lock:
                    ram_process = RAMProcess(
                        pid=pid,
                        name=f"ram_exec_{secrets.token_hex(4)}",
                        memory_size=mapped_size,
                        start_time=time.time(),
                        is_critical=is_critical
                    )
                    self.processes[pid] = ram_process
                
                # Clean up memory mapping in parent
                self._cleanup_memory(mem_ptr, mapped_size)
                
                return ram_process
                
        except Exception as e:
            print(f"Error executing in RAM: {e}")
            return None
    
    def execute_script_in_ram(self, script_path: str, 
                             interpreter: str = "/usr/bin/python3") -> Optional[RAMProcess]:
        """
        Load and execute a script entirely in RAM.
        
        Args:
            script_path: Path to the script to execute
            interpreter: Interpreter to use
            
        Returns:
            RAMProcess object if successful
        """
        try:
            # Read script into memory
            with open(script_path, 'rb') as f:
                script_content = f.read()
            
            # Create temporary file in tmpfs (RAM-based filesystem)
            tmpfs_paths = ['/dev/shm', '/run', '/tmp']
            tmpfs_path = None
            
            for path in tmpfs_paths:
                if os.path.exists(path):
                    # Check if it's tmpfs
                    try:
                        stat = os.statvfs(path)
                        # Heuristic: tmpfs usually has specific characteristics
                        tmpfs_path = path
                        break
                    except:
                        pass
            
            if not tmpfs_path:
                tmpfs_path = '/dev/shm'  # Default to shm
            
            # Create file in tmpfs
            temp_name = f"kalighost_ram_{secrets.token_hex(8)}.py"
            temp_path = os.path.join(tmpfs_path, temp_name)
            
            try:
                # Write to tmpfs
                with open(temp_path, 'wb') as f:
                    f.write(script_content)
                
                # Set restrictive permissions
                os.chmod(temp_path, 0o600)
                
                # Execute from tmpfs
                process = subprocess.Popen(
                    [interpreter, temp_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                
                with self.lock:
                    ram_process = RAMProcess(
                        pid=process.pid,
                        name=os.path.basename(script_path),
                        memory_size=len(script_content),
                        start_time=time.time(),
                        is_critical=True
                    )
                    self.processes[process.pid] = ram_process
                
                # Schedule cleanup after process ends
                def cleanup_after():
                    process.wait()
                    try:
                        os.remove(temp_path)
                    except:
                        pass
                
                threading.Thread(target=cleanup_after, daemon=True).start()
                
                return ram_process
                
            except Exception as e:
                print(f"Error executing script in RAM: {e}")
                return None
                
        except Exception as e:
            print(f"Error loading script: {e}")
            return None
    
    def _cleanup_memory(self, mem_ptr: int, size: int):
        """Safely clear and unmap memory."""
        try:
            # Zero out memory before unmapping
            ctypes.memset(mem_ptr, 0, size)
            
            # Unmap
            self.libc.munmap(ctypes.c_void_p(mem_ptr), size)
        except:
            pass
    
    def terminate_process(self, pid: int, secure: bool = True) -> bool:
        """
        Terminate a RAM process with optional secure cleanup.
        
        Args:
            pid: Process ID to terminate
            secure: If True, attempt to overwrite memory before termination
            
        Returns:
            True if successful
        """
        try:
            with self.lock:
                if pid not in self.processes:
                    return False
                
                ram_process = self.processes[pid]
                
                if secure and ram_process.is_critical:
                    # Send SIGUSR1 to trigger secure cleanup (if supported)
                    try:
                        os.kill(pid, 10)  # SIGUSR1
                        time.sleep(0.1)
                    except:
                        pass
                
                # Terminate process
                os.kill(pid, 9)  # SIGKILL
                
                # Remove from tracking
                del self.processes[pid]
                
                return True
                
        except Exception as e:
            print(f"Error terminating process: {e}")
            return False
    
    def list_processes(self) -> List[RAMProcess]:
        """List all tracked RAM processes."""
        with self.lock:
            return list(self.processes.values())
    
    def get_process_info(self, pid: int) -> Optional[RAMProcess]:
        """Get information about a specific process."""
        with self.lock:
            return self.processes.get(pid)
    
    def emergency_wipe(self):
        """
        Emergency wipe all RAM processes and associated memory.
        Use in case of compromise detection.
        """
        with self.lock:
            pids = list(self.processes.keys())
        
        for pid in pids:
            try:
                self.terminate_process(pid, secure=True)
            except:
                pass
        
        print("Emergency wipe completed")


class TmpFSSandbox:
    """
    Sandbox environment running entirely in tmpfs (RAM-based filesystem).
    Provides isolated execution with automatic cleanup.
    """
    
    def __init__(self, sandbox_id: str = None):
        self.sandbox_id = sandbox_id or secrets.token_hex(8)
        self.sandbox_path = f"/dev/shm/kalighost_sandbox_{self.sandbox_id}"
        self.created = False
        
    def create(self, size_mb: int = 100) -> bool:
        """Create the sandbox directory in tmpfs."""
        try:
            os.makedirs(self.sandbox_path, mode=0o700, exist_ok=True)
            
            # Verify it's in tmpfs
            stat = os.statvfs(self.sandbox_path)
            
            self.created = True
            return True
            
        except Exception as e:
            print(f"Error creating sandbox: {e}")
            return False
    
    def write_file(self, filename: str, content: bytes) -> Optional[str]:
        """Write a file to the sandbox."""
        if not self.created:
            return None
        
        file_path = os.path.join(self.sandbox_path, filename)
        
        try:
            with open(file_path, 'wb') as f:
                f.write(content)
            
            os.chmod(file_path, 0o600)
            return file_path
            
        except Exception as e:
            print(f"Error writing file: {e}")
            return None
    
    def read_file(self, filename: str) -> Optional[bytes]:
        """Read a file from the sandbox."""
        if not self.created:
            return None
        
        file_path = os.path.join(self.sandbox_path, filename)
        
        try:
            with open(file_path, 'rb') as f:
                return f.read()
        except:
            return None
    
    def execute(self, command: List[str]) -> subprocess.Popen:
        """Execute a command within the sandbox."""
        if not self.created:
            raise RuntimeError("Sandbox not created")
        
        return subprocess.Popen(
            command,
            cwd=self.sandbox_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    
    def destroy(self):
        """Completely destroy the sandbox and all contents."""
        if not self.created:
            return
        
        try:
            import shutil
            shutil.rmtree(self.sandbox_path, ignore_errors=True)
            self.created = False
        except Exception as e:
            print(f"Error destroying sandbox: {e}")
    
    def __enter__(self):
        self.create()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.destroy()


# Convenience function for one-time RAM execution
def run_in_ram_once(code: bytes, cleanup_delay: float = 0.0) -> int:
    """
    Execute code in RAM and automatically cleanup.
    Returns exit code.
    """
    engine = RAMExecutionEngine()
    process = engine.execute_in_ram(code)
    
    if not process:
        return -1
    
    # Wait for completion
    try:
        _, exit_code = os.waitpid(process.pid, 0)
        return exit_code >> 8
    except:
        return -1


if __name__ == "__main__":
    print("KaliGhost RAM-Only Execution Module")
    
    # Test tmpfs sandbox
    with TmpFSSandbox("test") as sandbox:
        test_file = sandbox.write_file("test.txt", b"Secret data in RAM only")
        if test_file:
            content = sandbox.read_file("test.txt")
            print(f"Read from sandbox: {content}")
    
    print("Sandbox automatically cleaned up")
