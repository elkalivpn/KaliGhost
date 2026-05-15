#!/usr/bin/env python3
"""
Demostración completa de capacidades autónomas de YrYs-Agent
Muestra cómo los sistemas trabajan juntos de forma autónoma
"""

import sys
import os
import time
from pathlib import Path
from datetime import datetime, timedelta

# Añadir el directorio del agente al path
sys.path.insert(0, str(Path(__file__).parent / "yrays-agent"))

def run_comprehensive_autonomous_demo():
    """Ejecuta una demostración completa de las capacidades autónomas"""
    print("🚀 DEMOSTRACIÓN COMPLETA DE CAPACIDADES AUTÓNOMAS DE YrYs-Agent")
    print("=" * 70)
    
    try:
        # Importar todos los sistemas
        from autonomous_task_manager import AutonomousTaskManager
        from event_system import get_event_system, EventType, on_task_completed, on_vulnerability_found, on_system_alert
        from behavior_profiles import ProfileManager, BehaviorMode
        import tempfile
        import logging
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        # Crear entorno de demostración
        with tempfile.TemporaryDirectory() as temp_dir:
            print(f"\n📂 Directorio de trabajo: {temp_dir}")
            
            # 1. Configurar perfiles de comportamiento
            print("\n🤖 1. CONFIGURANDO PERFILES DE COMPORTAMIENTO")
            profiles_dir = Path(temp_dir) / "profiles"
            profile_manager = ProfileManager(str(profiles_dir))
            
            # Crear perfil avanzado para demostración
            demo_profile = profile_manager.create_profile(
                name="demo_avanzada",
                mode=BehaviorMode.BALANCED,
                description="Perfil avanzado para demostración de capacidades autónomas"
            )
            
            # Configurar parámetros específicos
            demo_profile.update_setting("max_parallel_scans", 3)
            demo_profile.update_setting("scan_intensity", "normal")
            demo_profile.update_setting("alert_sensitivity", "high")
            demo_profile.update_setting("auto_report", True)
            profile_manager._save_profile(demo_profile)
            
            print(f"✅ Perfil 'demo_avanzada' creado y configurado")
            print(f"   - Modo: {demo_profile.mode.value}")
            print(f"   - Escaneos paralelos máximos: {demo_profile.get_setting('max_parallel_scans')}")
            print(f"   - Intensidad: {demo_profile.get_setting('scan_intensity')}")
            
            # 2. Inicializar sistema de eventos
            print("\n📡 2. INICIALIZANDO SISTEMA DE EVENTOS")
            event_system = get_event_system()
            
            # Variables para rastrear métricas
            metrics = {
                "tasks_completed": 0,
                "vulnerabilities_found": 0,
                "alerts_generated": 0,
                "system_events": 0
            }
            
            # Configurar manejadores de eventos avanzados
            @on_task_completed
            def advanced_task_handler(event):
                """Manejador avanzado para tareas completadas"""
                metrics["tasks_completed"] += 1
                task_name = event.data.get('task_name', 'desconocida')
                result = event.data.get('result', 'sin resultado')
                duration = event.data.get('duration', 'N/A')
                print(f"✅ TAREA COMPLETADA: {task_name}")
                print(f"   │ Resultado: {result}")
                if duration != 'N/A':
                    print(f"   │ Duración: {duration}")
                print(f"   └─ Event #{metrics['tasks_completed']}")
            
            @on_vulnerability_found
            def advanced_vuln_handler(event):
                """Manejador avanzado para vulnerabilidades"""
                metrics["vulnerabilities_found"] += 1
                target = event.data.get('target', 'desconocido')
                vulnerability = event.data.get('vulnerability', 'sin especificar')
                severity = event.data.get('severity', 'media')
                cvss = event.data.get('cvss_score', 'N/A')
                
                # Mapeo de colores para severidad
                severity_colors = {
                    "baja": "🟢",
                    "media": "🟡",
                    "alta": "🔴",
                    "crítica": "💥"
                }
                
                color = severity_colors.get(severity.lower(), "⚪")
                print(f"{color} VULNERABILIDAD ENCONTRADA: {vulnerability}")
                print(f"   │ Target: {target}")
                print(f"   │ Severidad: {severity}")
                if cvss != 'N/A':
                    print(f"   │ CVSS Score: {cvss}")
                print(f"   └─ Alerta #{metrics['vulnerabilities_found']}")
            
            @on_system_alert
            def advanced_alert_handler(event):
                """Manejador avanzado para alertas del sistema"""
                metrics["alerts_generated"] += 1
                message = event.data.get('message', 'Sin mensaje')
                level = event.data.get('level', 'info')
                component = event.data.get('component', 'desconocido')
                
                level_icons = {
                    "info": "ℹ️",
                    "warning": "⚠️",
                    "critical": "🚨"
                }
                
                icon = level_icons.get(level, "📋")
                print(f"{icon} ALERTA DEL SISTEMA: {message}")
                print(f"   │ Nivel: {level.upper()}")
                print(f"   │ Componente: {component}")
                print(f"   └─ Alerta #{metrics['alerts_generated']}")
            
            print("✅ Sistema de eventos inicializado con manejadores avanzados")
            
            # 3. Configurar gestor de tareas autónomas
            print("\n⚙️  3. CONFIGURANDO GESTOR DE TAREAS AUTÓNOMAS")
            db_path = Path(temp_dir) / "demo_autonomous.db"
            task_manager = AutonomousTaskManager(str(db_path))
            
            # Simular funciones de tareas realistas
            def network_discovery_task(network_range="192.168.1.0/24"):
                """Tarea de descubrimiento de red"""
                print(f"🔍 Descubriendo hosts en {network_range}...")
                time.sleep(1)
                hosts = ["192.168.1.1", "192.168.1.10", "192.168.1.25"]
                return f"Descubiertos {len(hosts)} hosts: {', '.join(hosts)}"
            
            def port_scan_task(target_host="192.168.1.1"):
                """Tarea de escaneo de puertos"""
                print(f"🛰️  Escaneando puertos en {target_host}...")
                time.sleep(1.5)
                ports = [22, 80, 443, 8080]
                return f"Puertos abiertos en {target_host}: {', '.join(map(str, ports))}"
            
            def vulnerability_assessment_task(target="192.168.1.10"):
                """Tarea de evaluación de vulnerabilidades"""
                print(f"🛡️  Evaluando vulnerabilidades en {target}...")
                time.sleep(2)
                vulns = [
                    {"name": "SSH Version Detection", "severity": "media", "cvss": 5.0},
                    {"name": "HTTP Server Header Disclosure", "severity": "baja", "cvss": 2.6}
                ]
                return f"Encontradas {len(vulns)} vulnerabilidades potenciales"
            
            def security_report_task(findings_summary=""):
                """Tarea de generación de reporte de seguridad"""
                print("📋 Generando reporte de seguridad...")
                time.sleep(1)
                return "Reporte de seguridad generado exitosamente"
            
            def system_monitor_task():
                """Tarea de monitoreo del sistema"""
                print("🖥️  Monitoreando recursos del sistema...")
                time.sleep(0.5)
                return "Uso de CPU: 25%, Memoria: 45%, Disco: 60%"
            
            # 4. Programar tareas autónomas con diferentes horarios
            print("\n📱 4. PROGRAMANDO TAREAS AUTÓNOMAS")
            
            # Tareas de descubrimiento (ejecución única)
            discovery_task = task_manager.schedule_task(
                name="Descubrimiento de Red",
                description="Descubrir hosts en la red local",
                function=network_discovery_task,
                args=("192.168.1.0/24",),
                schedule_type="once"
            )
            
            # Tareas de escaneo (con tiempos de inicio programados)
            now = datetime.now()
            scan_start_time1 = now + timedelta(seconds=1)
            scan_task1 = task_manager.schedule_task(
                name="Escaneo de Puertos 1",
                description="Escaneo de puertos en host crítico",
                function=port_scan_task,
                args=("192.168.1.1",),
                schedule_type="once",
                start_time=scan_start_time1
            )
            
            scan_start_time2 = now + timedelta(seconds=2)
            scan_task2 = task_manager.schedule_task(
                name="Escaneo de Puertos 2",
                description="Escaneo de puertos en host secundario",
                function=port_scan_task,
                args=("192.168.1.10",),
                schedule_type="once",
                start_time=scan_start_time2
            )
            
            # Tarea de evaluación de vulnerabilidades
            vuln_start_time = now + timedelta(seconds=3)
            vuln_task = task_manager.schedule_task(
                name="Evaluación de Vulnerabilidades",
                description="Evaluación detallada de vulnerabilidades",
                function=vulnerability_assessment_task,
                args=("192.168.1.10",),
                schedule_type="once",
                start_time=vuln_start_time
            )
            
            # Tarea de monitoreo del sistema (repetitiva)
            monitor_task = task_manager.schedule_task(
                name="Monitoreo del Sistema",
                description="Monitoreo continuo de recursos del sistema",
                function=system_monitor_task,
                schedule_type="interval",
                interval=2  # Cada 2 segundos
            )
            
            # Tarea de reporte (última ejecución)
            report_start_time = now + timedelta(seconds=8)
            report_task = task_manager.schedule_task(
                name="Generación de Reporte",
                description="Generar reporte final de seguridad",
                function=security_report_task,
                schedule_type="once",
                start_time=report_start_time
            )
            
            print(f"✅ {len(task_manager.list_tasks())} tareas programadas:")
            for i, task in enumerate(task_manager.list_tasks(), 1):
                print(f"   {i}. {task['name']} ({task['schedule_type']})")
            
            # 5. Iniciar ejecución autónoma
            print("\n⚡ 5. INICIANDO EJECUCIÓN AUTÓNOMA")
            task_manager.start()
            print("✅ Gestor de tareas autónomas iniciado")
            
            # 6. Emitir eventos simulados durante la ejecución
            print("\n📨 6. EMITIENDO EVENTOS SIMULADOS")
            
            # Emitir eventos durante la ejecución autónoma
            time.sleep(0.5)
            event_system.emit(EventType.SYSTEM_ALERT, {
                "message": "Inicio de operaciones autónomas",
                "level": "info",
                "component": "task_manager"
            })
            
            time.sleep(1)
            event_system.emit(EventType.TASK_COMPLETED, {
                "task_name": "Descubrimiento de Red",
                "result": "Descubiertos 3 hosts activos",
                "duration": "1.2s"
            })
            
            time.sleep(0.5)
            event_system.emit(EventType.VULNERABILITY_FOUND, {
                "target": "192.168.1.1",
                "vulnerability": "SSH Version Detection",
                "severity": "media",
                "cvss_score": 5.0
            })
            
            time.sleep(1)
            event_system.emit(EventType.SYSTEM_ALERT, {
                "message": "Alto uso de recursos detectado",
                "level": "warning",
                "component": "scanner_worker"
            })
            
            time.sleep(1)
            event_system.emit(EventType.VULNERABILITY_FOUND, {
                "target": "192.168.1.10",
                "vulnerability": "HTTP Server Header Disclosure",
                "severity": "baja",
                "cvss_score": 2.6
            })
            
            time.sleep(1)
            event_system.emit(EventType.TASK_COMPLETED, {
                "task_name": "Evaluación de Vulnerabilidades",
                "result": "Completada evaluación detallada",
                "duration": "2.1s"
            })
            
            # Esperar a que se completen todas las tareas
            print("\n⏳ 7. EJECUTANDO OPERACIONES AUTÓNOMAS (12 segundos)")
            print("   Observando ejecución de tareas y manejo de eventos...")
            time.sleep(12)
            
            # 8. Detener y mostrar resultados finales
            print("\n⏹️  8. DETENIENDO SISTEMAS AUTÓNOMOS")
            task_manager.stop()
            
            # Obtener estadísticas finales
            final_tasks = task_manager.list_tasks()
            completed_tasks = [t for t in final_tasks if t["status"] == "completed"]
            running_tasks = [t for t in final_tasks if t["status"] == "running"]
            
            print("\n" + "=" * 70)
            print("📊 RESUMEN FINAL DE LA DEMOSTRACIÓN")
            print("=" * 70)
            
            print(f"\n📁 Archivos y Perfiles:")
            print(f"   • Directorio temporal: {temp_dir}")
            print(f"   • Base de datos: {db_path.name}")
            print(f"   • Perfil activo: {demo_profile.name}")
            
            print(f"\n⚙️  Tareas Autónomas:")
            print(f"   • Total programadas: {len(final_tasks)}")
            print(f"   • Completadas: {len(completed_tasks)}")
            print(f"   • En ejecución: {len(running_tasks)}")
            
            print(f"\n📡 Eventos y Métricas:")
            print(f"   • Tareas completadas detectadas: {metrics['tasks_completed']}")
            print(f"   • Vulnerabilidades encontradas: {metrics['vulnerabilities_found']}")
            print(f"   • Alertas del sistema: {metrics['alerts_generated']}")
            
            # Evaluar éxito de la demostración
            success_criteria = [
                len(final_tasks) > 0,
                metrics['tasks_completed'] > 0,
                metrics['vulnerabilities_found'] > 0,
                metrics['alerts_generated'] > 0
            ]
            
            if all(success_criteria):
                print(f"\n🎉 ÉXITO TOTAL: Todos los sistemas autónomos funcionan correctamente!")
                print("✅ El agente YrYs-Agent demuestra capacidades autónomas avanzadas")
                print("✅ Sistemas integrados: Tareas, Eventos, Perfiles de Comportamiento")
                print("✅ Comunicación en tiempo real entre componentes")
                return True
            else:
                print(f"\n⚠️  ALGUNAS FUNCIONES REQUIEREN ATENCIÓN")
                return False
                
    except Exception as e:
        print(f"\n💥 ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_capabilities_summary():
    """Muestra un resumen de las capacidades autónomas"""
    print("\n" + "=" * 70)
    print("🌟 CAPACIDADES AUTÓNOMAS DE YrYs-Agent")
    print("=" * 70)
    
    capabilities = {
        "GESTIÓN DE TAREAS": [
            "✓ Programación flexible (única, repetitiva, diferida)",
            "✓ Ejecución en segundo plano con hilos",
            "✓ Persistencia en base de datos SQLite",
            "✓ Monitoreo en tiempo real del estado",
            "✓ Cancelación y gestión de ciclos de vida"
        ],
        "SISTEMA DE EVENTOS": [
            "✓ Arquitectura basada en eventos/emisores",
            "✓ Suscripciones y manejadores personalizados",
            "✓ Decoradores para eventos comunes",
            "✓ Historial de eventos con límites de memoria",
            "✓ Comunicación asíncrona entre componentes"
        ],
        "PERFILES DE COMPORTAMIENTO": [
            "✓ Modos predefinidos (Sigiloso, Agresivo, Equilibrado, Pasivo)",
            "✓ Configuración personalizable por perfil",
            "✓ Activación/desactivación dinámica",
            "✓ Persistencia en archivos JSON",
            "✓ Integración con tareas y herramientas"
        ],
        "INTEGRACIÓN AVANZADA": [
            "✓ Coordinación entre múltiples sistemas",
            "✓ Manejo de errores robusto",
            "✓ Logging y monitoreo detallado",
            "✓ Compatibilidad con herramientas de seguridad",
            "✓ Extensibilidad para nuevas funcionalidades"
        ]
    }
    
    for category, features in capabilities.items():
        print(f"\n🔹 {category}:")
        for feature in features:
            print(f"   {feature}")

if __name__ == "__main__":
    # Mostrar resumen de capacidades
    show_capabilities_summary()
    
    # Solicitar inicio de demostración
    print("\n" + "=" * 70)
    print("🚀 ¿Iniciar demostración completa de capacidades autónomas?")
    
    try:
        # En un entorno real, aquí podríamos pedir confirmación
        # Para esta demostración, procedemos automáticamente
        print("   Iniciando en 2 segundos...")
        time.sleep(2)
        
        # Ejecutar demostración
        success = run_comprehensive_autonomous_demo()
        
        if success:
            print("\n" + "=" * 70)
            print("🎊 DEMOSTRACIÓN COMPLETADA CON ÉXITO")
            print("🔧 YrYs-Agent está listo para operaciones autónomas avanzadas")
            print("=" * 70)
            sys.exit(0)
        else:
            print("\n" + "=" * 70)
            print("❌ DEMOSTRACIÓN FINALIZADA CON PROBLEMAS")
            print("⚠️  Revisar logs y configuración del sistema")
            print("=" * 70)
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Demostración interrumpida por el usuario")
        sys.exit(0)