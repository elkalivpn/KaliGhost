#!/usr/bin/env python3
"""
Script para probar el sistema de eventos de YrYs-Agent
"""

import sys
import os
import time
from pathlib import Path

# Añadir el directorio del agente al path
sys.path.insert(0, str(Path(__file__).parent / "yrays-agent"))

def test_event_system():
    """Prueba el sistema de eventos"""
    try:
        # Importar el sistema de eventos
        from event_system import get_event_system, EventType, on_task_completed, on_vulnerability_found
        
        # Obtener el sistema de eventos
        event_system = get_event_system()
        print("✅ Sistema de eventos creado correctamente")
        
        # Crear manejadores de eventos de prueba
        def task_completed_handler(event):
            """Manejador para tareas completadas"""
            print(f"✅ EVENTO: Tarea completada - {event.data.get('task_name', 'desconocida')}")
            print(f"   Resultado: {event.data.get('result', 'sin resultado')}")
        
        def vulnerability_handler(event):
            """Manejador para vulnerabilidades encontradas"""
            target = event.data.get('target', 'desconocido')
            vuln = event.data.get('vulnerability', 'sin especificar')
            severity = event.data.get('severity', 'media')
            print(f"⚠️ EVENTO: Vulnerabilidad encontrada en {target}")
            print(f"   Descripción: {vuln}")
            print(f"   Gravedad: {severity}")
        
        def system_alert_handler(event):
            """Manejador para alertas del sistema"""
            message = event.data.get('message', 'Alerta sin mensaje')
            level = event.data.get('level', 'info')
            print(f"🔔 EVENTO: Alerta del sistema ({level.upper()}) - {message}")
        
        # Suscribir manejadores a eventos
        print("\n📢 Suscribiendo manejadores de eventos...")
        
        handler1 = event_system.subscribe(EventType.TASK_COMPLETED, "task_handler", task_completed_handler)
        handler2 = event_system.subscribe(EventType.VULNERABILITY_FOUND, "vuln_handler", vulnerability_handler)
        handler3 = event_system.subscribe(EventType.SYSTEM_ALERT, "alert_handler", system_alert_handler)
        
        print("✅ Manejadores suscritos correctamente")
        
        # Emitir algunos eventos de prueba
        print("\n🔔 Emitiendo eventos de prueba...")
        
        # Evento de tarea completada
        event_system.emit(EventType.TASK_COMPLETED, {
            "task_name": "Escaneo de Red",
            "result": "8 puertos abiertos encontrados",
            "duration": "45 segundos"
        })
        
        # Evento de vulnerabilidad
        event_system.emit(EventType.VULNERABILITY_FOUND, {
            "target": "192.168.1.100",
            "vulnerability": "Servidor SSH con versión desactualizada",
            "severity": "alta",
            "details": "OpenSSH 7.2p2"
        })
        
        # Evento de alerta del sistema
        event_system.emit(EventType.SYSTEM_ALERT, {
            "message": "Uso de CPU alto detectado",
            "level": "warning",
            "component": "scanner_worker"
        })
        
        # Evento adicional de vulnerabilidad
        event_system.emit(EventType.VULNERABILITY_FOUND, {
            "target": "192.168.1.101",
            "vulnerability": "Servidor web sin HTTPS",
            "severity": "media",
            "details": "HTTP en puerto 80"
        })
        
        # Mostrar historial de eventos
        print(f"\n📋 Historial de eventos:")
        events = event_system.get_events(limit=10)
        print(f"   Total de eventos: {len(events)}")
        
        for event in events:
            timestamp = event.timestamp.strftime("%H:%M:%S")
            print(f"   [{timestamp}] {event.type.value}: {event.data}")
        
        # Obtener conteo de eventos por tipo
        print(f"\n📊 Estadísticas de eventos:")
        total_events = event_system.get_event_count()
        task_events = event_system.get_event_count(EventType.TASK_COMPLETED)
        vuln_events = event_system.get_event_count(EventType.VULNERABILITY_FOUND)
        alert_events = event_system.get_event_count(EventType.SYSTEM_ALERT)
        
        print(f"   Eventos totales: {total_events}")
        print(f"   Tareas completadas: {task_events}")
        print(f"   Vulnerabilidades: {vuln_events}")
        print(f"   Alertas del sistema: {alert_events}")
        
        # Probar decoradores
        print(f"\n🎨 Probando decoradores de eventos...")
        
        @on_task_completed
        def decorated_task_handler(event):
            """Manejador decorado para tareas completadas"""
            print(f"✨ MANEJADOR DECORADO: Tarea '{event.data.get('task_name')}' completada")
        
        @on_vulnerability_found
        def decorated_vuln_handler(event):
            """Manejador decorado para vulnerabilidades"""
            print(f"✨ MANEJADOR DECORADO: Vulnerabilidad en {event.data.get('target')}")
        
        # Emitir otro evento para probar los manejadores decorados
        event_system.emit(EventType.TASK_COMPLETED, {
            "task_name": "Análisis de Vulnerabilidades",
            "result": "Análisis completado",
            "findings": "2 vulnerabilidades críticas identificadas"
        })
        
        event_system.emit(EventType.VULNERABILITY_FOUND, {
            "target": "192.168.1.102",
            "vulnerability": "Base de datos expuesta",
            "severity": "crítica",
            "details": "MongoDB sin autenticación"
        })
        
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_event_performance():
    """Prueba el rendimiento del sistema de eventos"""
    try:
        # Importar el sistema de events
        from event_system import get_event_system, EventType
        
        event_system = get_event_system()
        
        # Crear manejador de prueba
        def performance_handler(event):
            """Manejador simple para pruebas de rendimiento"""
            pass  # No hacer nada, solo medir tiempo
        
        # Suscribir manejador
        handler = event_system.subscribe(EventType.TASK_COMPLETED, "perf_handler", performance_handler)
        
        # Emitir muchos eventos rápidamente
        print("\n⚡ Probando rendimiento del sistema de eventos...")
        import time
        
        start_time = time.time()
        num_events = 1000
        
        for i in range(num_events):
            event_system.emit(EventType.TASK_COMPLETED, {
                "task_name": f"Tarea_{i}",
                "result": f"Resultado de tarea {i}"
            })
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"✅ {num_events} eventos emitidos en {elapsed_time:.4f} segundos")
        print(f"   Velocidad: {num_events/elapsed_time:.0f} eventos/segundo")
        
        # Verificar que todos los eventos se registraron
        total_events = event_system.get_event_count()
        print(f"   Eventos en historial: {total_events}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba de rendimiento: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔬 Probando sistema de eventos de YrYs-Agent...")
    
    print("\n=== Prueba de funcionalidad básica ===")
    success1 = test_event_system()
    
    print("\n=== Prueba de rendimiento ===")
    success2 = test_event_performance()
    
    if success1 and success2:
        print("\n🎉 Todas las pruebas pasaron correctamente")
        sys.exit(0)
    else:
        print("\n💥 Algunas pruebas fallaron")
        sys.exit(1)