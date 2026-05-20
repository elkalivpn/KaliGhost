#!/usr/bin/env python3
"""
Script para crear skills de ejemplo para KaliGhost usando el sistema avanzado
"""

import sys
import os
from pathlib import Path

# Añadir el directorio del agente al path
sys.path.insert(0, str(Path(__file__).parent / "yrays-agent"))

def create_kalighost_skills():
    """Crea skills de ejemplo para KaliGhost"""
    try:
        # Importar el sistema de skills directamente
        from skill_system import SkillManager
        
        # Directorio de skills
        skills_dir = Path(__file__).parent / "yrays-agent" / "skills"
        
        # Crear un gestor de skills
        skill_manager = SkillManager(str(skills_dir))
        print("✅ Gestor de skills creado correctamente")
        print(f"📁 Directorio de skills: {skills_dir}")
        
        # Crear skill de escaneo de red
        network_scan_code = '''
def quick_scan(target):
    """Realiza un escaneo rápido de puertos abiertos"""
    import subprocess
    try:
        # Usar nmap con opción de escaneo rápido
        result = subprocess.run(["nmap", "-F", target], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return f"✅ Escaneo completado:\\n{result.stdout}"
        else:
            return f"❌ Error en escaneo:\\n{result.stderr}"
    except subprocess.TimeoutExpired:
        return "⏰ Escaneo excedió el tiempo límite"
    except Exception as e:
        return f"💥 Error: {e}"

def service_detection(target):
    """Detecta servicios en puertos abiertos"""
    import subprocess
    try:
        # Usar nmap con detección de servicios
        result = subprocess.run(["nmap", "-sV", target], capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            return f"✅ Detección de servicios completada:\\n{result.stdout}"
        else:
            return f"❌ Error en detección:\\n{result.stderr}"
    except subprocess.TimeoutExpired:
        return "⏰ Detección excedió el tiempo límite"
    except Exception as e:
        return f"💥 Error: {e}"
'''
        
        # Crear la skill de escaneo de red
        result = skill_manager.create_skill(
            "network_scanner", 
            "Herramientas de escaneo de red y detección de servicios", 
            network_scan_code
        )
        if result:
            print("✅ Skill 'network_scanner' creada correctamente")
        else:
            print("❌ Fallo al crear la skill 'network_scanner'")
        
        # Crear skill de análisis web
        web_analysis_code = '''
def analyze_web_server(url):
    """Analiza un servidor web buscando tecnologías comunes"""
    import subprocess
    try:
        # Usar whatweb para identificar tecnologías
        result = subprocess.run(["whatweb", url], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return f"✅ Análisis web completado:\\n{result.stdout}"
        else:
            return f"❌ Error en análisis:\\n{result.stderr}"
    except FileNotFoundError:
        return "❌ whatweb no está instalado"
    except subprocess.TimeoutExpired:
        return "⏰ Análisis excedió el tiempo límite"
    except Exception as e:
        return f"💥 Error: {e}"

def check_robots_txt(base_url):
    """Verifica el archivo robots.txt de un sitio"""
    import requests
    try:
        response = requests.get(f"{base_url}/robots.txt", timeout=10)
        if response.status_code == 200:
            return f"✅ Contenido de robots.txt:\\n{response.text}"
        else:
            return f"❌ No se encontró robots.txt (Status: {response.status_code})"
    except Exception as e:
        return f"💥 Error: {e}"
'''
        
        # Crear la skill de análisis web
        result = skill_manager.create_skill(
            "web_analyzer", 
            "Herramientas de análisis de servidores web", 
            web_analysis_code
        )
        if result:
            print("✅ Skill 'web_analyzer' creada correctamente")
        else:
            print("❌ Fallo al crear la skill 'web_analyzer'")
        
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
'''
        
        # Crear la skill de reporte
        result = skill_manager.create_skill(
            "report_generator", 
            "Herramientas para generar reportes profesionales", 
            reporting_code
        )
        if result:
            print("✅ Skill 'report_generator' creada correctamente")
        else:
            print("❌ Fallo al crear la skill 'report_generator'")
        
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
    print("🔨 Creando skills de ejemplo para KaliGhost...")
    success = create_kalighost_skills()
    if success:
        print("\n🎉 Skills creadas correctamente")
        sys.exit(0)
    else:
        print("\n💥 Fallo al crear skills")
        sys.exit(1)