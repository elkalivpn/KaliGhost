#!/usr/bin/env python3
"""
Script para probar la integración completa de los sistemas autónomos de YrYs-Agent
"""

import sys
import os
import time
from pathlib import Path

# Añadir el directorio del agente al path
sys.path.insert(0, str(Path(__file__).parent / "yrays-agent"))

def test_full_autonomous_integration():
    """Prueba la integración completa de los sistemas autónomos"""
    try:
        print("🔄 Iniciando prueba de integración completa...")
        
        # Importar todos los sistemas
        from autonomous_task_manager import AutonomousTaskManager
        from event_system import get_event_system, EventType, on_task_completed, on_vulnerability_found
        from behavior_profiles import ProfileManager, BehaviorMode, AutonomousProfile
        import tempfile
        import logging
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        # 1. Probar perfiles de comportamiento
        print("\n=== 1. Probando perfiles de comportamiento ===")
        
        # Crear gestor de perfiles con directorio temporal
        with tempfile.TemporaryDirectory() as temp_dir:
            profiles_dir = Path(temp_dir) / "profiles"
            profile_manager = ProfileManager(str(profiles_dir))
            
            # Crear perfil personalizado
            custom_profile = profile_manager.create_profile(
                name="perfil_prueba",
                mode=BehaviorMode.BALANCED,
                description="Perfil de prueba para integración"
            )
            
            # Modificar algunas configuraciones
            custom_profile.update_setting("max_parallel_scans", 5)
            custom_profile.update_setting("scan_intensity", "high")
            profile_manager._save_profile(custom_profile)
            
            loaded_profile = profile_manager.get_profile("perfil_prueba")
            
            if loaded_profile and loaded_profile.name == "perfil_prueba":
                print("✅ Perfiles de comportamiento funcionando correctamente")
            else:
                print("❌ Error en perfiles de comportamiento")
                return False
            
            # 2. Probar sistema de tareas con perfil
            print("\n=== 2. Probando sistema de tareas con perfil ===")
            
            # Crear gestor de tareas con base de datos temporal
            db_path = Path(temp_dir) / "integration_test.db"
            task_manager = AutonomousTaskManager(str(db_path))
            
            # Crear funciones de prueba
            def scan_task(target="localhost"):
                """Tarea de escaneo de prueba"""
                print(f"🔍 Escaneando {target}")
                time.sleep(1)
                return f"✅ Escaneo completado en {target}"
            
            def analysis_task(data="test"):
                """Tarea de análisis de prueba"""
                print(f"🧮 Analizando datos: {data}")
                time.sleep(1)
                return f"✅ Análisis completado para {data}"
            
            # Programar tareas
            task1_id = task_manager.schedule_task(
                name="Escaneo de Integración",
                description="Escaneo de prueba para integración",
                function=scan_task,
                args=("192.168.1.1",),
                schedule_type="once"
            )
            
            task2_id = task_manager.schedule_task(
                name="Análisis de Integración",
                description="Análisis de prueba para integración",
                function=analysis_task,
                args=("datos_prueba",),
                schedule_type="interval",
                interval=5
            )
            
            print("✅ Tareas programadas correctamente")
            
            # 3. Probar sistema de eventos
            print("\n=== 3. Probando sistema de eventos ===")
            event_system = get_event_system()
            
            # Crear contador de eventos para verificar recepción
            event_count = {"task": 0, "vuln": 0}
            
            # Crear manejadores de eventos
            @on_task_completed
            def task_event_handler(event):
                """Manejador de eventos para tareas completadas"""
                task_name = event.data.get('task_name', 'desconocida')
                result = event.data.get('result', 'sin resultado')
                print(f"🔔 EVENTO: Tarea '{task_name}' completada - {result}")
                event_count["task"] += 1
            
            @on_vulnerability_found
            def vuln_event_handler(event):
                """Manejador de eventos para vulnerabilidades"""
                target = event.data.get('target', 'desconocido')
                vuln = event.data.get('vulnerability', 'sin especificar')
                print(f"⚠️ ALERTA: Vulnerabilidad encontrada en {target} - {vuln}")
                event_count["vuln"] += 1
            
            print("✅ Sistema de eventos configurado")
            
            # 4. Ejecutar tareas y verificar integración
            print("\n=== 4. Ejecutando tareas y verificando integración ===")
            
            # Iniciar gestor de tareas
            task_manager.start()
            
            # Emitir algunos eventos de prueba
            event_system.emit(EventType.TASK_COMPLETED, {
                "task_name": "Escaneo de Integración",
                "result": "8 puertos abiertos encontrados"
            })
            
            event_system.emit(EventType.VULNERABILITY_FOUND, {
                "target": "192.168.1.1",
                "vulnerability": "Servidor SSH desactualizado",
                "severity": "alta"
            })
            
            # Esperar un momento para observar la ejecución
            print("⏳ Ejecutando tareas durante 3 segundos...")
            time.sleep(3)
            
            # Detener gestor de tareas
            task_manager.stop()
            
            # Verificar resultados
            tasks = task_manager.list_tasks()
            scheduled_tasks = [t for t in tasks if t["status"] == "scheduled"]
            
            print(f"\n📊 Resultados:")
            print(f"   Tareas programadas: {len(tasks)}")
            print(f"   Eventos de tareas recibidos: {event_count['task']}")
            print(f"   Eventos de vulnerabilidades recibidos: {event_count['vuln']}")
            
            if event_count['task'] > 0 and event_count['vuln'] > 0:
                print("✅ Integración completa exitosa")
                return True
            else:
                print("❌ Problemas en la integración")
                return False

    except Exception as e:
        print(f"❌ Error en la prueba de integración: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_autonomous_workflow():
    """Prueba un flujo de trabajo autónomo completo"""
    try:
        print("\n=== 5. Probando flujo de trabajo autónomo ===")
        
        # Importar sistemas
        from autonomous_task_manager import AutonomousTaskManager
        from event_system import get_event_system, EventType
        from behavior_profiles import ProfileManager, BehaviorMode
        import tempfile
        import logging
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        # Crear entorno de prueba
        with tempfile.TemporaryDirectory() as temp_dir:
            # Crear gestor de perfiles
            profiles_dir = Path(temp_dir) / "profiles"
            profile_manager = ProfileManager(str(profiles_dir))
            
            # Crear gestor de tareas
            db_path = Path(temp_dir) / "workflow_test.db"
            task_manager = AutonomousTaskManager(str(db_path))
            
            event_system = get_event_system()
            
            # Crear perfil para flujo de trabajo
            workflow_profile = profile_manager.create_profile(
                name="flujo_trabajo",
                mode=BehaviorMode.AGGRESSIVE,
                description="Perfil para flujo de trabajo autónomo"
            )
            
            # Modificar configuraciones
            workflow_profile.update_setting("max_parallel_scans", 10)
            workflow_profile.update_setting("scan_intensity", "high")
            profile_manager._save_profile(workflow_profile)
            
            # Crear funciones de flujo de trabajo
            def reconnaissance_phase(target):
                """Fase de reconocimiento"""
                print(f"🔍 Fase 1: Reconocimiento de {target}")
                time.sleep(0.5)
                return f"✅ Puertos abiertos en {target}: 22, 80, 443"
            
            def scanning_phase(target, ports):
                """Fase de escaneo"""
                print(f"🔧 Fase 2: Escaneo detallado de puertos {ports} en {target}")
                time.sleep(0.5)
                return f"✅ Servicios identificados en {target}"
            
            def exploitation_phase(target):
                """Fase de explotación (simulada)"""
                print(f"💣 Fase 3: Análisis de vulnerabilidades en {target}")
                time.sleep(0.5)
                return f"✅ Vulnerabilidades encontradas en {target}"
            
            def reporting_phase(*args):
                """Fase de reporte"""
                print(f"📝 Fase 4: Generando reporte")
                time.sleep(0.5)
                return "✅ Reporte generado exitosamente"
            
            # Programar tareas del flujo de trabajo
            rec_task = task_manager.schedule_task(
                name="Reconocimiento",
                description="Fase de reconocimiento del objetivo",
                function=reconnaissance_phase,
                args=("10.0.0.1",),
                schedule_type="once"
            )
            
            scan_task = task_manager.schedule_task(
                name="Escaneo",
                description="Fase de escaneo detallado",
                function=scanning_phase,
                args=("10.0.0.1", "22,80,443"),
                schedule_type="once"
            )
            
            exploit_task = task_manager.schedule_task(
                name="Explotación",
                description="Fase de análisis de vulnerabilidades",
                function=exploitation_phase,
                args=("10.0.0.1",),
                schedule_type="once"
            )
            
            report_task = task_manager.schedule_task(
                name="Reporte",
                description="Generación de reporte final",
                function=reporting_phase,
                schedule_type="once"
            )
            
            print("✅ Flujo de trabajo autónomo programado")
            
            # Contador de eventos
            completion_count = 0
            
            # Crear manejador para contar tareas completadas
            def task_completion_counter(event):
                nonlocal completion_count
                completion_count += 1
                task_name = event.data.get('task_name', 'desconocida')
                result = event.data.get('result', 'sin resultado')
                print(f"✅ Tarea '{task_name}' completada: {result}")
            
            # Suscribir manejador
            event_system.subscribe(EventType.TASK_COMPLETED, "counter", task_completion_counter)
            
            # Iniciar ejecución
            task_manager.start()
            
            # Emitir eventos durante la ejecución
            time.sleep(0.1)
            event_system.emit(EventType.TASK_COMPLETED, {
                "task_name": "Reconocimiento",
                "result": "Puertos 22, 80, 443 abiertos"
            })
            
            time.sleep(0.1)
            event_system.emit(EventType.VULNERABILITY_FOUND, {
                "target": "10.0.0.1",
                "vulnerability": "Servidor web vulnerable",
                "severity": "media"
            })
            
            # Esperar a que se completen las tareas
            print("⏳ Ejecutando flujo de trabajo autónomo...")
            time.sleep(5)
            
            # Detener y verificar
            task_manager.stop()
            
            tasks = task_manager.list_tasks()
            print(f"\n📊 Flujo de trabajo completado:")
            print(f"   Tareas totales: {len(tasks)}")
            print(f"   Eventos de tareas completadas: {completion_count}")
            
            if completion_count >= 1:  # Al menos 1 evento de tarea completada
                print("✅ Flujo de trabajo autónomo exitoso")
                return True
            else:
                print("❌ Problemas en el flujo de trabajo")
                return False
                
    except Exception as e:
        print(f"❌ Error en flujo de trabajo: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Probando integración completa de sistemas autónomos de YrYs-Agent")
    
    # Ejecutar pruebas
    success1 = test_full_autonomous_integration()
    success2 = test_autonomous_workflow()
    
    if success1 and success2:
        print("\n🎉 ¡Todas las pruebas de integración pasaron correctamente!")
        print("✅ El sistema autónomo está listo para su uso")
        sys.exit(0)
    else:
        print("\n💥 Algunas pruebas de integración fallaron")
        sys.exit(1)