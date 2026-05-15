#!/usr/bin/env python3
"""
Script de prueba para la extensión autónoma de YrYs-Agent
"""

import sys
import os
from pathlib import Path

# Añadir el directorio del agente al path
sys.path.insert(0, str(Path(__file__).parent / "yrays-agent"))

def test_autonomous_extension():
    """Prueba la extensión autónoma del agente"""
    try:
        # Importar clases necesarias
        from yrays import Agent
        import yaml
        import time
        
        # Crear un agente de prueba
        config_path = Path(__file__).parent / "yrays-agent" / "config" / "config.yaml"
        agent = Agent(str(config_path))
        
        print("✅ Agente creado correctamente")
        
        # Verificar si la extensión autónoma está disponible
        if hasattr(agent, 'autonomous_extension') and agent.autonomous_extension:
            print("🤖 Extensión autónoma disponible")
            
            # Iniciar la extensión autónoma
            try:
                agent.autonomous_extension.start()
                print("✅ Extensión autónoma iniciada")
            except Exception as e:
                print(f"❌ Error al iniciar extensión autónoma: {e}")
                return False
            
            # Obtener estado de la extensión
            status = agent.autonomous_extension.get_autonomous_status()
            print(f"📊 Estado de la extensión: {status}")
            
            # Listar perfiles de comportamiento
            profiles = agent.autonomous_extension.get_behavior_profiles()
            print(f"📚 Perfiles de comportamiento disponibles: {len(profiles)}")
            for profile in profiles:
                status_text = "✓ ACTIVO" if profile["is_active"] else "○ INACTIVO"
                print(f"  • {profile['name']} ({profile['mode']}) - {status_text}")
            
            # Programar una tarea autónoma de ejemplo
            print("\n⏰ Programando tareas autónomas...")
            
            # Programar un escaneo repetitivo
            scan_task_id = agent.autonomous_extension.schedule_autonomous_scan(
                target="localhost",
                scan_type="quick",
                schedule_type="interval",
                interval=30  # Cada 30 segundos
            )
            print(f"✅ Escaneo programado (ID: {scan_task_id})")
            
            # Programar un monitor de vulnerabilidades
            monitor_task_id = agent.autonomous_extension.schedule_vulnerability_monitor(
                target="localhost",
                frequency="daily"
            )
            print(f"✅ Monitor de vulnerabilidades programado (ID: {monitor_task_id})")
            
            # Obtener tareas activas
            active_tasks = agent.autonomous_extension.get_active_tasks()
            print(f"🔄 Tareas activas: {len(active_tasks)}")
            for task in active_tasks:
                print(f"  • {task['name']}: {task['status']} (Próxima: {task['next_run']})")
            
            # Esperar unos segundos para observar eventos
            print("\n⏳ Observando eventos durante 15 segundos...")
            time.sleep(15)
            
            # Obtener eventos recientes
            recent_events = agent.autonomous_extension.get_recent_events(10)
            print(f"🔔 Eventos recientes: {len(recent_events)}")
            for event in recent_events:
                print(f"  • [{event['timestamp']}] {event['type']}: {event['data']}")
            
            # Detener la extensión autónoma
            agent.autonomous_extension.stop()
            print("🛑 Extensión autónoma detenida")
            
            return True
        else:
            print("⚠️ Extensión autónoma no disponible")
            return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔬 Probando extensión autónoma de YrYs-Agent...")
    success = test_autonomous_extension()
    if success:
        print("\n🎉 Prueba completada correctamente")
        sys.exit(0)
    else:
        print("\n💥 La prueba falló")
        sys.exit(1)