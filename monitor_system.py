import json
import subprocess
from datetime import datetime

def get_system_metrics():
    metrics = {}
    
    # Obtener uso de CPU
    try:
        top_output = subprocess.check_output(['top', '-l', '1', '-n', '0'], stderr=subprocess.STDOUT, text=True)
        for line in top_output.split('\n'):
            if 'CPU usage:' in line:
                cpu_line = line.strip()
                import re
                cpu_match = re.search(r'(\d+\.\d+)% user, (\d+\.\d+)% system, (\d+\.\d+)% idle', cpu_line)
                if cpu_match:
                    metrics['cpu'] = {
                        'user': float(cpu_match.group(1)),
                        'system': float(cpu_match.group(2)),
                        'idle': float(cpu_match.group(3))
                    }
                break
    except Exception:
        metrics['cpu'] = {'user': 0, 'system': 0, 'idle': 0}
    
    # Obtener uso de memoria
    try:
        vmstat_output = subprocess.check_output(['vm_stat'], stderr=subprocess.STDOUT, text=True)
        import re
        total_match = re.search(r'Total number of mach_factor.*?(\d+)', vmstat_output)
        free_match = re.search(r'Pages free.*?(\d+)', vmstat_output)
        inactive_match = re.search(r'Pages inactive.*?(\d+)', vmstat_output)
        wired_match = re.search(r'Pages wired down.*?(\d+)', vmstat_output)
        
        total = int(total_match.group(1)) if total_match else 0
        free = int(free_match.group(1)) if free_match else 0
        inactive = int(inactive_match.group(1)) if inactive_match else 0
        wired = int(wired_match.group(1)) if wired_match else 0
        
        page_size_kb = 4
        total_mb = total * page_size_kb // 1024
        free_mb = free * page_size_kb // 1024
        inactive_mb = inactive * page_size_kb // 1024
        wired_mb = wired * page_size_kb // 1024
        
        used_mb = total_mb - free_mb - inactive_mb
        metrics['memory'] = {
            'total': total_mb,
            'used': used_mb,
            'free': free_mb,
            'inactive': inactive_mb,
            'wired': wired_mb
        }
    except Exception:
        metrics['memory'] = {'total': 0, 'used': 0, 'free': 0, 'inactive': 0, 'wired': 0}
    
    # Obtener uso de disco
    try:
        df_output = subprocess.check_output(['df', '-h'], stderr=subprocess.STDOUT, text=True)
        lines = df_output.split('\n')[1:]
        for line in lines:
            parts = line.split()
            if len(parts) >= 5 and parts[0].startswith('/dev/'):
                capacity_str = parts[4].rstrip('%')
                capacity = int(capacity_str) if capacity_str.isdigit() else 0
                metrics['disk'] = {
                    'capacity': capacity,
                    'used': parts[2],
                    'available': parts[3],
                    'mounted': parts[5] if len(parts) > 5 else '/'
                }
                break
    except Exception:
        metrics['disk'] = {'capacity': 0, 'used': '0', 'available': '0', 'mounted': '/'}

    # Tiempo de actividad
    try:
        uptime_output = subprocess.check_output(['uptime'], stderr=subprocess.STDOUT, text=True)
        import re
        uptime_match = re.search(r'load average: (.*)', uptime_output)
        if uptime_match:
            metrics['uptime'] = uptime_match.group(1)
        else:
            metrics['uptime'] = 'unknown'
    except Exception:
        metrics['uptime'] = 'unknown'

    return metrics

metrics = get_system_metrics()
report = {
    'timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
    'system': metrics
}

with open('gui/frontend/dashboard_data.json', 'w') as f:
    json.dump(report, f, indent=2)
print('Datos del dashboard actualizados correctamente')