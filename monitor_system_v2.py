import json
import subprocess
from datetime import datetime, timezone

def get_system_metrics():
    metrics = {}
    
    # Obtener uso de CPU (comando diferente para macOS)
    try:
        # Usar ps aux para obtener datos de CPU
        ps_output = subprocess.check_output(['ps', 'aux', '-n', '1'], stderr=subprocess.STDOUT, text=True)
        # Obtener la línea promedio de CPU de todos los procesos
        ps_lines = ps_output.split('\n')[1:]  # Saltar encabezado
        cpu_total = 0
        count = 0
        for line in ps_lines:
            if line.strip():
                parts = line.split()
                if len(parts) > 2:
                    try:
                        cpu_val = float(parts[2])
                        cpu_total += cpu_val
                        count += 1
                    except ValueError:
                        continue
        cpu_avg = cpu_total / count if count > 0 else 0
        metrics['cpu'] = {
            'user': cpu_avg,
            'system': 0,
            'idle': 100 - cpu_avg
        }
    except Exception:
        metrics['cpu'] = {'user': 0, 'system': 0, 'idle': 0}
    
    # Obtener uso de memoria
    try:
        vmstat_output = subprocess.check_output(['vm_stat'], stderr=subprocess.STDOUT, text=True)
        import re
        # Extraemos información más precisa de la salida de vm_stat
        total_match = re.search(r'Mach Virtual Memory Statistics: \(page size of (\d+) bytes\)', vmstat_output)
        pages_free_match = re.search(r'Pages free: (\d+)', vmstat_output)
        pages_inactive_match = re.search(r'Pages inactive: (\d+)', vmstat_output)
        pages_wired_match = re.search(r'Pages wired down: (\d+)', vmstat_output)
        pages_active_match = re.search(r'Pages active: (\d+)', vmstat_output)
        
        page_size = int(total_match.group(1)) if total_match else 4096
        pages_free = int(pages_free_match.group(1)) if pages_free_match else 0
        pages_inactive = int(pages_inactive_match.group(1)) if pages_inactive_match else 0
        pages_wired = int(pages_wired_match.group(1)) if pages_wired_match else 0
        pages_active = int(pages_active_match.group(1)) if pages_active_match else 0
        
        # Calcular en MB
        page_size_mb = page_size // 1024 // 1024
        total_mb = (pages_free + pages_inactive + pages_wired + pages_active) * page_size_mb
        free_mb = pages_free * page_size_mb
        inactive_mb = pages_inactive * page_size_mb
        wired_mb = pages_wired * page_size_mb
        active_mb = pages_active * page_size_mb
        used_mb = total_mb - free_mb
        
        metrics['memory'] = {
            'total': total_mb,
            'used': used_mb,
            'free': free_mb,
            'inactive': inactive_mb,
            'wired': wired_mb,
            'active': active_mb
        }
    except Exception:
        metrics['memory'] = {'total': 0, 'used': 0, 'free': 0, 'inactive': 0, 'wired': 0, 'active': 0}
    
    # Obtener uso de disco con df -h
    try:
        df_output = subprocess.check_output(['df', '-h'], stderr=subprocess.STDOUT, text=True)
        lines = df_output.split('\n')[1:]
        for line in lines:
            parts = line.split()
            if len(parts) >= 5 and parts[0].startswith('/dev/'):
                capacity_str = parts[4].rstrip('%')
                capacity = int(capacity_str) if capacity_str.isdigit() else 0
                # Convertir '12Gi' a número
                if 'Gi' in parts[2]:
                    used_value = float(parts[2].rstrip('Gi'))
                    used_gb = used_value
                elif 'Mi' in parts[2]:
                    used_value = float(parts[2].rstrip('Mi'))
                    used_gb = used_value / 1024
                else:
                    used_gb = 0
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
    'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'system': metrics
}

with open('gui/frontend/dashboard_data.json', 'w') as f:
    json.dump(report, f, indent=2)
print('Datos del dashboard actualizados correctamente')