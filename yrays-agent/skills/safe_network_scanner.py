# Skill: safe_network_scanner
# Descripción: Herramientas seguras de análisis de escaneos de red
# Generado automáticamente por YrYs-Agent


def analyze_scan_results(nmap_output):
    """Analiza los resultados de un escaneo de nmap"""
    if not nmap_output:
        return "❌ No hay resultados para analizar"
    
    lines = nmap_output.split("\n")
    analysis = []
    
    # Contar hosts encontrados
    hosts_found = [line for line in lines if "Nmap scan report" in line]
    analysis.append(f"🖥️ Hosts encontrados: {len(hosts_found)}")
    
    # Contar puertos abiertos
    open_ports = [line for line in lines if "/tcp" in line and "open" in line]
    analysis.append(f"🔌 Puertos abiertos: {len(open_ports)}")
    
    # Buscar servicios comunes
    http_services = [line for line in open_ports if "http" in line.lower() or "80/tcp" in line]
    ssh_services = [line for line in open_ports if "ssh" in line.lower() or "22/tcp" in line]
    https_services = [line for line in open_ports if "https" in line.lower() or "443/tcp" in line]
    
    if http_services:
        analysis.append(f"🌐 Servicios HTTP: {len(http_services)}")
    if ssh_services:
        analysis.append(f"🔐 Servicios SSH: {len(ssh_services)}")
    if https_services:
        analysis.append(f"🔒 Servicios HTTPS: {len(https_services)}")
    
    return "\n".join(analysis)

def prepare_nmap_scan(target, scan_type="quick"):
    """Prepara los parámetros para un escaneo de nmap"""
    if scan_type == "quick":
        return {
            "tool": "nmap",
            "args": ["-F", target],
            "description": f"Escaneo rápido de {target}"
        }
    elif scan_type == "service":
        return {
            "tool": "nmap",
            "args": ["-sV", target],
            "description": f"Detección de servicios en {target}"
        }
    elif scan_type == "os":
        return {
            "tool": "nmap",
            "args": ["-O", target],
            "description": f"Detección de sistema operativo en {target}"
        }
    else:
        return {
            "tool": "nmap",
            "args": [target],
            "description": f"Escaneo estándar de {target}"
        }
