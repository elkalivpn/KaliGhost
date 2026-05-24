#!/usr/bin/env python3
"""
Enhanced memory analysis tool for KaliGhost monitoring.
"""

import subprocess
import sys
import os

def enhanced_memory_analysis():
    """
    Perform enhanced memory analysis using vm_stat for more accurate percentage.
    """
    try:
        # Get memory stats using vm_stat
        mem_result = subprocess.run(['vm_stat'], capture_output=True, text=True, timeout=10)
        lines = mem_result.stdout.split('\n')
        
        # Parse vm_stat output for more accurate memory usage
        free_pages = 0
        active_pages = 0
        inactive_pages = 0
        wired_pages = 0
        
        for line in lines:
            if 'Pages free:' in line:
                free_pages = int(line.split(':')[1].strip().split()[0])
            elif 'Pages active:' in line:
                active_pages = int(line.split(':')[1].strip().split()[0])
            elif 'Pages inactive:' in line:
                inactive_pages = int(line.split(':')[1].strip().split()[0])
            elif 'Pages wired down:' in line:
                wired_pages = int(line.split(':')[1].strip().split()[0])
        
        # Calculate approximate memory percentage (simple estimation based on macOS memory model)
        # Total physical memory estimation (based on typical macOS systems)
        memory_page_size = 16384  # Default page size in bytes for macOS
        total_memory_pages = free_pages + active_pages + inactive_pages + wired_pages
        total_memory_mb = (total_memory_pages * memory_page_size) / (1024 * 1024)
        used_memory_mb = ((active_pages + inactive_pages + wired_pages) * memory_page_size) / (1024 * 1024)
        mem_percent = (used_memory_mb / total_memory_mb) * 100 if total_memory_mb > 0 else 0.0
        
        return mem_percent
        
    except Exception as e:
        print(f'Memory analysis error: {e}')
        return None

def get_top_memory_processes():
    """
    Get top memory-consuming processes.
    """
    try:
        # Get process list sorted by memory usage
        ps_result = subprocess.run(['ps', 'aux'], capture_output=True, text=True, timeout=10)
        lines = ps_result.stdout.split('\n')[1:]  # Skip header
        
        # Extract and sort by memory usage
        processes = []
        for line in lines:
            parts = line.split(None, 10)
            if len(parts) >= 4:
                try:
                    mem_pct = float(parts[3])
                    cmd = parts[10] if len(parts) > 10 else parts[4] if len(parts) > 4 else ''
                    processes.append((mem_pct, cmd))
                except ValueError:
                    continue
        
        # Sort by memory usage descending and show top 5
        processes.sort(reverse=True)
        return processes[:5]
        
    except Exception as e:
        print(f'Error getting process list: {e}')
        return []

def main():
    print('=== Enhanced Memory Analysis ===')
    mem_percent = enhanced_memory_analysis()
    if mem_percent is not None:
        print(f'Estimated memory usage: {mem_percent:.2f}%')
        
        # Check if memory usage is critical (over 90%)
        if mem_percent > 90:
            print(f'[CRITICAL] High memory usage detected: {mem_percent:.2f}%')
            
    else:
        print('Could not determine memory usage')
    
    print('\n=== Top Memory Consumers ===')
    top_processes = get_top_memory_processes() 
    if top_processes:
        for i, (mem_pct, cmd) in enumerate(top_processes, 1):
            print(f'{i}. {mem_pct:.2f}% - {cmd[:100]}')
    else:
        print('Could not retrieve process list')

if __name__ == '__main__':
    main()