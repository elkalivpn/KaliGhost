#!/usr/bin/env python3
import json
import subprocess
import os
import time

def get_cpu_usage():
    """Get CPU usage percentage using macOS top command"""
    try:
        # Run top command and get CPU usage data
        result = subprocess.run(['top', '-l', '1', '-n', '0'], capture_output=True, text=True)
        cpu_percent = 0
        
        # Parse the output to find CPU usage
        for line in result.stdout.split('\n'):
            if 'CPU usage' in line:
                parts = line.split()
                if len(parts) >= 4:
                    try:
                        cpu_percent = 100 - float(parts[3].rstrip('%'))
                        break
                    except ValueError:
                        # Handle case where conversion fails
                        cpu_percent = 0
                        break
        
        return cpu_percent
    except Exception as e:
        print(f"Error getting CPU usage: {e}")
        return 0

def get_memory_usage():
    """Get memory usage percentage using vm_stat command"""
    try:
        result = subprocess.run(['vm_stat'], capture_output=True, text=True)
        memory_used = 0
        memory_total = 0
        
        # Parse vm_stat output to calculate memory usage
        active = 0
        wired = 0
        free = 0
        
        for line in result.stdout.split('\n'):
            if 'Pages active' in line:
                try:
                    active = int(float(line.split(':')[1].strip().split()[0]))
                except:
                    active = 0
            elif 'Pages wired' in line:
                try:
                    wired = int(float(line.split(':')[1].strip().split()[0]))
                except:
                    wired = 0
            elif 'Pages free' in line:
                try:
                    free = int(float(line.split(':')[1].strip().split()[0]))
                except:
                    free = 0
        
        # Calculate memory usage in MB
        memory_used = (active + wired) * 4096 / (1024*1024)
        memory_total = (active + wired + free) * 4096 / (1024*1024)
        
        if memory_total > 0:
            memory_percent = (memory_used / memory_total) * 100
        else:
            memory_percent = 0
            
        return memory_percent
    except Exception as e:
        print(f"Error getting memory usage: {e}")
        return 0

def get_disk_usage():
    """Get disk usage percentage using df command"""
    try:
        result = subprocess.run(['df', '/'], capture_output=True, text=True)
        # Parse df output to get disk usage
        disk_output = result.stdout.split('\n')[1]
        disk_parts = disk_output.split()
        disk_percent = int(disk_parts[4].rstrip('%'))
        
        # Return usage as percentage (we need 100 - used %)
        return 100 - disk_percent
    except Exception as e:
        print(f"Error getting disk usage: {e}")
        return 0

def main():
    # Get system metrics
    cpu_percent = get_cpu_usage()
    memory_percent = get_memory_usage()
    disk_percent = get_disk_usage()
    
    # Create dashboard data structure
    dashboard_data = {
        'timestamp': time.time(),
        'cpu': {
            'percent': round(cpu_percent, 2)
        },
        'memory': {
            'percent': round(memory_percent, 2)
        },
        'disk': {
            'percent': disk_percent
        }
    }
    
    # Write to dashboard data file
    dashboard_data_path = os.path.expanduser('~/KaliGhost/gui/frontend/dashboard_data.json')
    with open(dashboard_data_path, 'w') as f:
        json.dump(dashboard_data, f)
    
    # Print the data for logging purposes
    print(json.dumps(dashboard_data))

if __name__ == '__main__':
    main()