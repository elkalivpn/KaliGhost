import subprocess
import json
import os
from datetime import datetime

# Try to get a more accurate memory measurement with alternative method
try:
    # Use sysctl to get memory information
    result = subprocess.run(['sysctl', 'hw.memsize', 'vm.page_size'], capture_output=True, text=True, timeout=10)
    
    # Parse total memory
    total_mem = 0
    for line in result.stdout.split('\n'):
        if 'hw.memsize' in line:
            total_mem = int(line.split(':')[1].strip())
            break
    
    # Get active memory with vm_stat
    vm_result = subprocess.run(['vm_stat'], capture_output=True, text=True, timeout=10)
    active_pages = 0
    wired_pages = 0
    inactive_pages = 0
    
    for line in vm_result.stdout.split('\n'):
        if 'Pages active:' in line:
            active_pages = int(line.split(':')[1].strip())
        elif 'Pages wired down:' in line:
            wired_pages = int(line.split(':')[1].strip())
        elif 'Pages inactive:' in line:
            inactive_pages = int(line.split(':')[1].strip())
    
    # Convert to MB 
    page_size = 16384  # Usually 16KB pages on macOS
    total_mb = total_mem / (1024 * 1024)
    used_mb = (active_pages + wired_pages + inactive_pages) * page_size / (1024 * 1024)
    mem_percent = (used_mb / total_mb) * 100
    
    print(f'Total memory: {total_mb:.2f} MB')
    print(f'Used memory: {used_mb:.2f} MB')
    print(f'Memory percentage: {mem_percent:.2f}%')
    
    # Check if memory is high
    if mem_percent > 90:
        print('[CRITICAL] High memory usage detected')
    elif mem_percent > 85:
        print('[WARNING] High memory usage approaching threshold')
    
except Exception as e:
    print(f'Error getting memory info: {e}')