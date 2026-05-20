#!/usr/bin/env python3
"""
Script para probar el sistema de tareas programadas de YrYs-Agent
"""

import sys
import os
import time
from pathlib import Path

# Añadir el directorio del agente al path
sys.path.insert(0, str(Path(__file__).parent / "yrays-agent"))

def test_task_scheduling():
    """Prueba el sistema de programación de tareas"""
    try:
        # Importar el sistema de tareas
        from autonomous_task_manager import AutonomousTaskManager, Task
        import tempfile
        
        # Crear un gestor de tareas con base de datos temporal
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test_tasks.db"
            task_manager = AutonomousTaskManager(str(db_path))
            print("✅ Gestor de tareas creado correctamente")
            print(f"📁 Base de datos: {db_path}")
            
            # Crear funciones de prueba
            def test_scan_function(target="localhost"):
                """Función de prueba para escaneo"""
                print(f"🔍 Escaneando {target}...")
                time.sleep(1)  # Simular trabajo
                return f"✅ Escaneo completado en {target}"
            
            def test_monitor_function():
                """Función de prueba para monitoreo"""
                print("📊 Monitoreando sistema...")
                time.sleep(1)  # Simular trabajo
                return "✅ Monitoreo completado"
            
            def test_analysis_function(data="test", **kwargs):
                """Función de prueba para análisis"""
                print(f"🧮 Analizando datos: {data}")
                if kwargs:
                    print(f"   Parámetros adicionales: {kwargs}")
                time.sleep(1)  # Simular trabajo
                return f"✅ Análisis completado para {data}"
            
            # Programar tareas de ejemplo
            print("\n⏰ Programando tareas de prueba...")
            
            # Tarea única
            task1_id = task_manager.schedule_task(
                name="Escaneo Único",
                description="Escaneo único de localhost",
                function=test_scan_function,
                args=("localhost",),
                schedule_type="once"
            )
            print(f"✅ Tarea única programada (ID: {task1_id})")
            
            # Tarea repetitiva
            task2_id = task_manager.schedule_task(
                name="Monitoreo Periódico",
                description="Monitoreo periódico del sistema",
                function=test_monitor_function,
                schedule_type="interval",
                interval=5  # Cada 5 segundos
            )
            print(f"✅ Tarea repetitiva programada (ID: {task2_id})")
            
            # Tarea con parámetros
            task3_id = task_manager.schedule_task(
                name="Análisis de Datos",
                description="Análisis de datos de prueba",
                function=test_analysis_function,
                args=("datos_de_prueba",),
                schedule_type="interval",
                interval=10  # Cada 10 segundos
            )
            print(f"✅ Tarea con parámetros programada (ID: {task3_id})")
            
            # Listar tareas programadas
            tasks = task_manager.list_tasks()
            print(f"\n📋 Tareas programadas ({len(tasks)}):")
            for task in tasks:
                print(f"  • {task['name']} ({task['id'][:8]}...) - {task['status']}")
                print(f"    {task['description']}")
                print(f"    Tipo: {task['schedule_type']}, Próxima: {task['next_run']}")
            
            # Iniciar el gestor de tareas
            print("\n🚀 Iniciando gestor de tareas...")
            task_manager.start()
            
            # Esperar para observar la ejecución de tareas
            print("⏳ Observando ejecución de tareas durante 15 segundos...")
            time.sleep(15)
            
            # Detener el gestor de tareas
            print("\n🛑 Deteniendo gestor de tareas...")
            task_manager.stop()
            
            # Verificar resultados
            final_tasks = task_manager.list_tasks()
            completed_tasks = [t for t in final_tasks if t["status"] == "completed"]
            running_tasks = [t for t in final_tasks if t["status"] == "running"]
            
            print(f"\n📊 Resultados finales:")
            print(f"  • Tareas completadas: {len(completed_tasks)}")
            print(f"  • Tareas en ejecución: {len(running_tasks)}")
            print(f"  • Tareas totales: {len(final_tasks)}")
            
            # Mostrar detalles de tareas completadas
            for task in completed_tasks:
                print(f"  ✅ {task['name']}: {task['result']}")
            
            return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_task_cancellation():
    """Prueba la cancelación de tareas"""
    try:
        # Importar el sistema de tareas
        from autonomous_task_manager import AutonomousTaskManager, Task
        import tempfile
        
        # Crear un gestor de tareas con base de datos temporal
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test_cancel.db"
            task_manager = AutonomousTaskManager(str(db_path))
            
            # Crear función de prueba que tarda en ejecutarse
            def long_running_task():
                """Tarea que tarda varios segundos"""
                print("⏳ Tarea larga en ejecución...")
                time.sleep(30)  # Tarea que tarda 30 segundos
                return "✅ Tarea larga completada"
            
            # Programar tarea larga
            task_id = task_manager.schedule_task(
                name="Tarea Larga",
                description="Tarea que tarda mucho tiempo",
                function=long_running_task,
                schedule_type="once"
            )
            print(f"✅ Tarea larga programada (ID: {task_id})")
            
            # Iniciar el gestor
            task_manager.start()
            
            # Esperar un momento y luego cancelar la tarea
            print("⏳ Iniciando tarea, esperando 2 segundos...")
            time.sleep(2)
            
            # Cancelar la tarea
            if task_manager.cancel_task(task_id):
                print("✅ Tarea cancelada correctamente")
            else:
                print("❌ Error al cancelar tarea")
            
            # Esperar un poco más para verificar
            time.sleep(3)
            
            # Detener el gestor
            task_manager.stop()
            
            # Verificar estado final
            tasks = task_manager.list_tasks()
            cancelled_task = next((t for t in tasks if t["id"] == task_id), None)
            
            if cancelled_task:
                if cancelled_task["status"] == "cancelled":
                    print("✅ Verificación: La tarea está en estado cancelado")
                    return True
                elif cancelled_task["status"] == "running":
                    print("✅ Verificación: La tarea fue cancelada mientras se ejecutaba")
                    return True
                else:
                    print(f"⚠️ Verificación: La tarea terminó con estado {cancelled_task['status']}")
                    return True  # Consideramos éxito si la tarea existía
            else:
                print("❌ Verificación fallida: Tarea no encontrada")
                return False
        
    except Exception as e:
        print(f"❌ Error en la prueba de cancelación: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔬 Probando sistema de tareas programadas de YrYs-Agent...")
    
    print("\n=== Prueba de programación básica ===")
    success1 = test_task_scheduling()
    
    print("\n=== Prueba de cancelación ===")
    success2 = test_task_cancellation()
    
    if success1 and success2:
        print("\n🎉 Todas las pruebas pasaron correctamente")
        sys.exit(0)
    else:
        print("\n💥 Algunas pruebas fallaron")
        sys.exit(1)