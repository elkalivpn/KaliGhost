#!/usr/bin/env python3
"""
Script de prueba para verificar psutil
"""

try:
    import psutil
    print("psutil is available")
    
    # Probar algunas funciones básicas
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    print(f"CPU: {cpu_percent}%")
    print(f"Memory: {memory.percent}%")
    print(f"Disk: {(disk.used/disk.total)*100:.1f}%")
    
except ImportError:
    print("psutil is not available")
except Exception as e:
    print(f"Error: {e}")