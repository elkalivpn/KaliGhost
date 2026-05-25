import subprocess
import json
import os
from datetime import datetime

def diagnose_memory():
    # Get the raw vm_stat output
    result = subprocess.run(['vm_stat'], capture_output=True, text=True, timeout=10)
    lines = result.stdout.split('\n')
    
    # Parse vm_stat
    free_pages = 0
    active_pages = 0
    inactive_pages = 0
    wired_pages = 0
    
    for line in lines:
        if 'Pages free:' in line:
            parts = line.split()
            if len(parts) > 3:
                try:
                    free_pages = int(parts[2])
                except ValueError:
                    pass
        elif 'Pages active:' in line:
            parts = line.split()
            if len(parts) > 3:
                try:
                    active_pages = int(parts[2])
                except ValueError:
                    pass
        elif 'Pages inactive:' in line:
            parts = line.split()
            if len(parts) > 3:
                try:
                    inactive_pages = int(parts[2])
                except ValueError:
                    pass
        elif 'Pages wired down:' in line:
            parts = line.split()
            if len(parts) > 3:
                try:
                    wired_pages = int(parts[2])
                except ValueError:
                    pass
    
    # Calculate total physical memory (approximate)
    # We need to get page size - assume 16384 bytes (16KB) based on standard macOS
    page_size = 16384  # bytes
    
    total_memory_pages = free_pages + active_pages + inactive_pages + wired_pages
    if total_memory_pages > 0:
        # Calculate memory usage percentage (active + inactive + wired pages)
        memory_used_pages = active_pages + inactive_pages + wired_pages
        memory_percentage = 100.0 * float(memory_used_pages) / float(total_memory_pages)
        print(f"Calculated memory usage: {memory_percentage:.2f}%")
    else:
        # Fallback: Get system memory info
        try:
            mem_info = subprocess.run(['sysctl', 'hw.memsize'], capture_output=True, text=True, timeout=10)
            if 'hw.memsize' in mem_info.stdout:
                total_mem_bytes = int(mem_info.stdout.split()[1])
                total_mem_mb = total_mem_bytes / (1024 * 1024)
                print(f"Total system memory: {total_mem_mb:.2f} MB")
        except Exception as e:
            print(f"Could not determine total memory: {e}")

if __name__ == "__main__":
    diagnose_memory()