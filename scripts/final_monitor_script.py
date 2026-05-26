import json
import subprocess
import os
from datetime import datetime
import re

def get_system_metrics():
    # CPU usage using top command
    try:
        cpu_result = subprocess.run(['top', '-bn1'], capture_output=True, text=True, timeout=10)
        cpu_line = [line for line in cpu_result.stdout.split('\n') if 'Cpu(s)' in line][0]
        cpu_percent = float(cpu_line.split(',')[0].split()[-1].rstrip('%'))
    except:
        cpu_percent = 0.0
        
    # Memory usage using vm_stat - improved parsing
    mem_percent = 0.0
    try:
        mem_result = subprocess.run(['vm_stat'], capture_output=True, text=True, timeout=10)
        lines = mem_result.stdout.split('\n')
        free_pages = 0
        active_pages = 0
        inactive_pages = 0
        wired_pages = 0
        
        for line in lines:
            if 'Pages free:' in line:
                # Fix for decimal number parsing
                free_match = re.search(r'Pages free:\s+([0-9]+\.?)', line)
                if free_match:
                    free_pages = int(float(free_match.group(1)))
            elif 'Pages active:' in line:
                active_match = re.search(r'Pages active:\s+([0-9]+\.?)', line)
                if active_match:
                    active_pages = int(float(active_match.group(1)))
            elif 'Pages inactive:' in line:
                inactive_match = re.search(r'Pages inactive:\s+([0-9]+\.?)', line)
                if inactive_match:
                    inactive_pages = int(float(inactive_match.group(1)))
            elif 'Pages wired down:' in line:
                wired_match = re.search(r'Pages wired down:\s+([0-9]+\.?)', line)
                if wired_match:
                    wired_pages = int(float(wired_match.group(1)))

        # Calculate approximate memory percentage
        # This is a rough approximation only
        # On macOS the command output isn't reliable enough for precise percentage
        # But we'll at least attempt to show an estimate
        if free_pages + active_pages + inactive_pages + wired_pages > 0:
            mem_percent = 100.0 * (active_pages + inactive_pages + wired_pages) / (free_pages + active_pages + inactive_pages + wired_pages)
    except Exception as e:
        print(f"Memory parsing error: {e}")
        
    # Disk usage using df
    try:
        disk_result = subprocess.run(['df', '/'], capture_output=True, text=True, timeout=10)
        disk_line = disk_result.stdout.strip().split('\n')[1]
        disk_percent = float(disk_line.split()[4].rstrip('%'))
    except:
        disk_percent = 0.0
    
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

if __name__ == '__main__':
    get_system_metrics()