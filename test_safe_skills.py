#!/usr/bin/env python3
"""
Script para probar las skills seguras de KaliGhost
"""

import sys
import os
from pathlib import Path

# Añadir el directorio del agente al path
sys.path.insert(0, str(Path(__file__).parent / "yrays-agent"))

def test_safe_skills():
    """Prueba las skills seguras creadas"""
    try:
        # Importar el sistema de skills directamente
        from skill_system import SkillManager
        
        # Directorio de skills
        skills_dir = Path(__file__).parent / "yrays-agent" / "skills"
        
        # Crear un gestor de skills
        skill_manager = SkillManager(str(skills_dir))
        print("✅ Gestor de skills creado correctamente")
        
        # Probar la skill de análisis de red
        print("\n=== Probando safe_network_scanner ===")
        
        # Simular salida de nmap
        nmap_output = """Starting Nmap 7.99 ( https://nmap.org ) at 2026-05-15 21:13 +0200
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000050s latency).
Other addresses for localhost (not scanned): ::1
Not shown: 93 closed tcp ports (conn-refused)
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
443/tcp  open  https
3000/tcp open  ppp
5000/tcp open  upnp
8080/tcp open  http-proxy
8081/tcp open  blackice-icecap

Nmap done: 1 IP address (1 host up) scanned in 0.04 seconds"""
        
        # Analizar resultados
        analysis = skill_manager.execute_skill_function("safe_network_scanner", "analyze_scan_results", nmap_output)
        print(f"📊 Análisis de escaneo:")
        print(analysis)
        
        # Preparar escaneo
        scan_params = skill_manager.execute_skill_function("safe_network_scanner", "prepare_nmap_scan", "192.168.1.1", "service")
        print(f"⚙️ Parámetros de escaneo: {scan_params}")
        
        # Probar la skill de análisis web
        print("\n=== Probando safe_web_analyzer ===")
        
        # Simular salida de whatweb
        whatweb_output = """http://example.com [200 OK] Country[UNITED STATES][US] HTML5 X-UA-Compatible[IE=edge] http-server-header[nginx] nginx[1.18.0]"""
        
        # Analizar tecnologías web
        tech_analysis = skill_manager.execute_skill_function("safe_web_analyzer", "analyze_web_technologies", whatweb_output)
        print(f"📱 Análisis de tecnologías:")
        print(tech_analysis)
        
        # Analizar headers HTTP
        headers = {
            "server": "nginx/1.18.0",
            "date": "Mon, 15 May 2026 19:13:00 GMT",
            "content-type": "text/html",
            "content-length": "1234"
        }
        
        header_analysis = skill_manager.execute_skill_function("safe_web_analyzer", "check_http_headers", headers)
        print(f"🔒 Análisis de headers:")
        print(header_analysis)
        
        # Probar la skill de reportería
        print("\n=== Probando security_reporter ===")
        
        # Generar resumen
        summary = skill_manager.execute_skill_function("security_reporter", "generate_summary", nmap_output)
        print(f"📋 Resumen:")
        print(summary)
        
        # Extraer hallazgos clave
        key_findings = skill_manager.execute_skill_function("security_reporter", "extract_key_findings", nmap_output)
        print(f"🚩 Hallazgos clave:")
        print(key_findings)
        
        # Formatear reporte
        report = skill_manager.execute_skill_function("security_reporter", "format_report", "Análisis de Red", summary)
        print(f"📄 Reporte formateado (primeras 3 líneas):")
        print("\\n".join(report.split("\\n")[:3]))
        
        print("\n✅ Todas las skills probadas correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error al probar skills: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Probando skills seguras de KaliGhost...")
    success = test_safe_skills()
    if success:
        print("\n🎉 Todas las pruebas pasaron correctamente")
        sys.exit(0)
    else:
        print("\n💥 Algunas pruebas fallaron")
        sys.exit(1)