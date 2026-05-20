#!/usr/bin/env python3
"""
Script de prueba para las habilidades de optimización de tokens y delegación
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'yrays-agent'))

# Importar las funciones principales
try:
    from skills.advanced_task_optimizer import (
        get_task_optimization_guide,
        execute_with_optimized_resources,
        evaluate_task_feasibility,
        determine_task_division
    )
    
    print("✅ Importación exitosa de habilidades de optimización")
    
    # Ejemplo de tareas para prueba
    test_tasks = [
        "Desarrollar un escáner de vulnerabilidades en redes locales",
        "Crear un informe de análisis de seguridad básico",
        "Implementar un sistema de detección de intrusiones avanzado",
        "Revisar y optimizar el código de un programa existente"
    ]
    
    print("\n🔍 Análisis de Tareas:")
    print("=" * 50)
    
    for i, task in enumerate(test_tasks, 1):
        print(f"\n{i}. Tarea: {task}")
        try:
            # Generar guía de optimización
            guide = get_task_optimization_guide(task)
            print("   ✅ Guía generada correctamente")
            
            # Análisis básico
            feasibility = evaluate_task_feasibility(task)
            print(f"   📊 Complejidad: {feasibility['task_complexity']}")
            print(f"   🧠 Modelo recomendado: {feasibility['optimal_model']['name']}")
            
            # División de tarea
            division = determine_task_division(task)
            if division['should_divide']:
                print("   ⚠️  Requiere división")
            else:
                print("   ✅ No requiere división")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n🎯 Ejecución Optimizada:")
    print("=" * 50)
    
    # Testeo de ejecución optimizada
    result = execute_with_optimized_resources("Revisar y optimizar el código de un programa existente")
    print("✅ Ejecución completada")
    print(f"   Tarea ejecutada: {result['task_executed']}")
    print(f"   Modelo usado: {result['model_used']}")
    print(f"   Tokens consumidos: {result['tokens_consumed']}")
    
except ImportError as e:
    print(f"❌ Error al importar: {e}")
    import traceback
    traceback.print_exc()