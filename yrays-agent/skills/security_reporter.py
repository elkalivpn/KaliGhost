# Skill: security_reporter
# Descripción: Herramientas para generar reportes de seguridad profesionales
# Generado automáticamente por YrYs-Agent


def generate_summary(scan_results):
    """Genera un resumen de los resultados de escaneo"""
    lines = scan_results.split("\n")
    summary = []
    
    # Contar hosts encontrados
    hosts_found = [line for line in lines if "Nmap scan report" in line]
    summary.append(f"🖥️ Hosts encontrados: {len(hosts_found)}")
    
    # Contar puertos abiertos
    open_ports = [line for line in lines if "/tcp" in line and "open" in line]
    summary.append(f"🔌 Puertos abiertos: {len(open_ports)}")
    
    # Buscar servicios comunes
    http_services = [line for line in open_ports if "http" in line.lower()]
    ssh_services = [line for line in open_ports if "ssh" in line.lower()]
    https_services = [line for line in open_ports if "https" in line.lower()]
    
    if http_services:
        summary.append(f"🌐 Servicios HTTP: {len(http_services)}")
    if ssh_services:
        summary.append(f"🔐 Servicios SSH: {len(ssh_services)}")
    if https_services:
        summary.append(f"🔒 Servicios HTTPS: {len(https_services)}")
    
    return "\n".join(summary)

def format_report(title, findings):
    """Formatea un reporte profesional"""
    separator = "=" * 50
    report = f"{separator}\n{title.upper()}\n{separator}\n\n"
    report += f"📅 Fecha: {{}}\n"
    report += f"🤖 Generado por: YrYs-Agent\n\n"
    report += "📋 RESULTADOS:\n"
    report += f"{{findings}}\n\n"
    report += f"{{separator}}\n"
    
    # Añadir timestamp
    from datetime import datetime
    return report.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), findings=findings, separator=separator[:-1])

def extract_key_findings(scan_output):
    """Extrae hallazgos clave de un escaneo"""
    lines = scan_output.split("\n")
    key_findings = []
    
    # Buscar puertos críticos
    critical_ports = []
    for line in lines:
        if "/tcp" in line and "open" in line:
            if any(port in line for port in ["21/", "22/", "23/", "25/", "53/", "80/", "110/", "143/", "443/", "993/", "995/"]):
                critical_ports.append(line.strip())
    
    if critical_ports:
        key_findings.append("🚩 PUERTOS CRÍTICOS DETECTADOS:")
        key_findings.extend([f"  • {port}" for port in critical_ports[:5]])
    
    # Buscar servicios potencialmente peligrosos
    dangerous_services = []
    for line in lines:
        if "http" in line.lower() and "open" in line:
            dangerous_services.append("Web Server (posible superficie de ataque)")
        elif "ftp" in line.lower() and "open" in line:
            dangerous_services.append("FTP Server (posible transferencia insegura)")
        elif "telnet" in line.lower() and "open" in line:
            dangerous_services.append("Telnet (comunicación no cifrada)")
    
    if dangerous_services:
        key_findings.append("\n⚡ SERVICIOS POTENCIALMENTE PELIGROSOS:")
        key_findings.extend([f"  • {service}" for service in set(dangerous_services)])
    
    return "\n".join(key_findings) if key_findings else "✅ No se encontraron hallazgos críticos"
