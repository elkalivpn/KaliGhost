
def scan_host(host="localhost"):
    """Escanea un host específico"""
    return f"Escaneando host: {host}"

def list_ports():
    """Lista los puertos comunes"""
    common_ports = [22, 80, 443, 3306, 5432]
    return f"Puertos comunes: {common_ports}"
