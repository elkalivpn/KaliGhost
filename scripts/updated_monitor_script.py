#!/usr/bin/env python3

import json
import subprocess
import os
from datetime import datetime

def get_system_metrics():
    # CPU usage using top command
    cpu_percent = 0.0
    try:
        cpu_result = subprocess.run(['top', '-bn1'], capture_output=True, text=True, timeout=10)
        cpu_line = [line for line in cpu_result.stdout.split('\n') if 'Cpu(s)' in line][0]
        cpu_percent = float(cpu_line.split(',')[0].split()[-1].rstrip('%'))
    except Exception as e:
        print(f"CPU parsing error: {e}")
        
    # Memory parsing with enhanced accuracy for macOS
    mem_percent = 0.0
    try:
        # Get memory information using sysctl for more reliable reading
        mem_info = subprocess.run(['sysctl', 'hw.memsize'], capture_output=True, text=True, timeout=10)
        total_mem_bytes = 0
        if 'hw.memsize' in mem_info.stdout:
            total_mem_bytes = int(mem_info.stdout.split()[1])
            
        # Parse vm_stat for active memory usage
        vm_stat_result = subprocess.run(['vm_stat'], capture_output=True, text=True, timeout=10)
        
        active_pages = 0
        wired_pages = 0
        
        # Extract page information from vm_stat output
        for line in vm_stat_result.stdout.split('\n'):
            if 'Pages active:' in line:
                # Extract the numeric value for active pages
                try:
                    active_pages = int(line.split()[2])  # Get second column after 'Pages active:'
                except:
                    pass
            elif 'Pages wired down:' in line:
                # Extract the numeric value for wired pages  
                try:
                    wired_pages = int(line.split()[2])  # Get second column after 'Pages wired down:'
                except:
                    pass
        
        # Convert pages to bytes (assuming 16KB pages, which is standard on macOS)
        page_size = 16384  # bytes
        total_active_wired_bytes = (active_pages + wired_pages) * page_size
        
        if total_mem_bytes > 0:
            mem_percent = (total_active_wired_bytes / total_mem_bytes) * 100
    except Exception as e:
        print(f"Memory parsing error: {e}")
        
    # Disk usage using df
    disk_percent = 0.0
    try:
        disk_result = subprocess.run(['df', '/'], capture_output=True, text=True, timeout=10)
        disk_line = disk_result.stdout.strip().split('\n')[1]
        disk_percent = float(disk_line.split()[4].rstrip('%'))
    except Exception as e:
        print(f"Disk parsing error: {e}")
    
    # Create data structure
    data = {
        'timestamp': datetime.now().timestamp(),
        'cpu': {
            'percent': round(cpu_percent, 2)
        },
        'memory': {
            'percent': round(mem_percent, 2)
        },
        'disk': {
            'percent': round(disk_percent, 2)
        }
    }
    
    # Write to file
    filename = os.path.expanduser('~/KaliGhost/gui/frontend/dashboard_data.json')
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
        
    print(f'Updated dashboard data with: {data}')
    return data

if __name__ == '__main__':
    get_system_metrics()