#!/usr/bin/env python3
"""
Script para crear skills seguras de ejemplo para KaliGhost
"""

import sys
import os
from pathlib import Path

# Añadir el directorio del agente al path
sys.path.insert(0, str(Path(__file__).parent / "yrays-agent"))

def create_safe_kalighost_skills():
    """Crea skills seguras de ejemplo para KaliGhost"""
    try:
        # Importar el sistema de skills directamente
        from skill_system import SkillManager
        
        # Directorio de skills
        skills_dir = Path(__file__).parent / "yrays-agent" / "skills"
        
        # Crear un gestor de skills
        skill_manager = SkillManager(str(skills_dir))
        print("✅ Gestor de skills creado correctamente")
        print(f"📁 Directorio de skills: {skills_dir}")
        
        # Crear skill de escaneo de red (versión segura)
        network_scan_code = '''
def analyze_scan_results(nmap_output):
    """Analiza los resultados de un escaneo de nmap"""
    if not nmap_output:
        return "❌ No hay resultados para analizar"
    
    lines = nmap_output.split("\\n")
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
    
    return "\\n".join(analysis)

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
'''
        
        # Crear la skill de escaneo de red
        result = skill_manager.create_skill(
            "safe_network_scanner", 
            "Herramientas seguras de análisis de escaneos de red", 
            network_scan_code
        )
        if result:
            print("✅ Skill 'safe_network_scanner' creada correctamente")
        else:
            print("❌ Fallo al crear la skill 'safe_network_scanner'")
        
        # Crear skill de análisis web (versión segura)
        web_analysis_code = '''
def analyze_web_technologies(whatweb_output):
    """Analiza los resultados de whatweb"""
    if not whatweb_output:
        return "❌ No hay resultados para analizar"
    
    lines = whatweb_output.split("\\n")
    technologies = []
    
    for line in lines:
        if line.strip():
            # Extraer tecnologías del formato de whatweb
            parts = line.split(" ")
            if len(parts) > 1:
                url = parts[0]
                techs = [part.strip("[]") for part in parts[1:] if part.startswith("[") and part.endswith("]")]
                if techs:
                    technologies.append(f"📱 {url}: {', '.join(techs)}")
    
    if technologies:
        return "\\n".join(technologies)
    else:
        return "🔍 No se detectaron tecnologías específicas"

def check_http_headers(headers_dict):
    """Analiza headers HTTP para seguridad"""
    security_issues = []
    
    # Verificar headers de seguridad
    if "x-frame-options" not in headers_dict:
        security_issues.append("⚠️ Falta X-Frame-Options (posible riesgo de clickjacking)")
    
    if "x-content-type-options" not in headers_dict:
        security_issues.append("⚠️ Falta X-Content-Type-Options (posible riesgo de MIME-sniffing)")
    
    if "x-xss-protection" not in headers_dict:
        security_issues.append("⚠️ Falta X-XSS-Protection (posible riesgo de XSS)")
    
    if "strict-transport-security" not in headers_dict:
        security_issues.append("⚠️ Falta Strict-Transport-Security (posible riesgo de downgrade attacks)")
    
    if "content-security-policy" not in headers_dict:
        security_issues.append("⚠️ Falta Content-Security-Policy (posible riesgo de XSS)")
    
    if security_issues:
        return "\\n".join(security_issues)
    else:
        return "✅ Todos los headers de seguridad presentes"
'''
        
        # Crear la skill de análisis web
        result = skill_manager.create_skill(
            "safe_web_analyzer", 
            "Herramientas seguras de análisis de tecnologías web", 
            web_analysis_code
        )
        if result:
            print("✅ Skill 'safe_web_analyzer' creada correctamente")
        else:
            print("❌ Fallo al crear la skill 'safe_web_analyzer'")
        
        # Crear skill de reporte
        reporting_code = '''
def generate_summary(scan_results):
    """Genera un resumen de los resultados de escaneo"""
    lines = scan_results.split("\\n")
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
    
    return "\\n".join(summary)

def format_report(title, findings):
    """Formatea un reporte profesional"""
    separator = "=" * 50
    report = f"{separator}\\n{title.upper()}\\n{separator}\\n\\n"
    report += f"📅 Fecha: {{}}\\n"
    report += f"🤖 Generado por: YrYs-Agent\\n\\n"
    report += "📋 RESULTADOS:\\n"
    report += f"{{findings}}\\n\\n"
    report += f"{{separator}}\\n"
    
    # Añadir timestamp
    from datetime import datetime
    return report.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), findings=findings, separator=separator[:-1])

def extract_key_findings(scan_output):
    """Extrae hallazgos clave de un escaneo"""
    lines = scan_output.split("\\n")
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
        key_findings.append("\\n⚡ SERVICIOS POTENCIALMENTE PELIGROSOS:")
        key_findings.extend([f"  • {service}" for service in set(dangerous_services)])
    
    return "\\n".join(key_findings) if key_findings else "✅ No se encontraron hallazgos críticos"
'''
        
        # Crear la skill de reporte
        result = skill_manager.create_skill(
            "security_reporter", 
            "Herramientas para generar reportes de seguridad profesionales", 
            reporting_code
        )
        if result:
            print("✅ Skill 'security_reporter' creada correctamente")
        else:
            print("❌ Fallo al crear la skill 'security_reporter'")
        
        # Listar todas las skills
        skills_info = skill_manager.list_skills()
        print(f"\n📚 Skills disponibles: {len(skills_info)}")
        for skill in skills_info:
            print(f"  • {skill['name']}: {skill['description']} ({skill['status']})")
            if skill['functions']:
                print(f"    Funciones: {', '.join(skill['functions'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al crear skills: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🛡️ Creando skills seguras de ejemplo para KaliGhost...")
    success = create_safe_kalighost_skills()
    if success:
        print("\n🎉 Skills seguras creadas correctamente")
        sys.exit(0)
    else:
        print("\n💥 Fallo al crear skills seguras")
        sys.exit(1)