# Skill: advanced_task_optimizer
# Descripción: Sistema avanzado para optimización de tareas, división y delegación de modelos
# Generado automáticamente por YrYs-Agent

import re
from typing import Dict, List, Any, Tuple
from .token_optimizer import get_optimal_model, calculate_token_estimate, suggest_model_change

# Nivel de complejidad de tareas
TASK_COMPLEXITY_LEVELS = {
    "simple": {
        "max_tokens": 500,
        "model_level": 1,
        "description": "Operaciones simples, búsqueda, reportes básicos"
    },
    "intermediate": {
        "max_tokens": 2000,
        "model_level": 2,
        "description": "Desarrollo básico, procesamiento de datos"
    },
    "complex": {
        "max_tokens": 5000,
        "model_level": 3,
        "description": "Análisis avanzado, desarrollo complejo"
    },
    "very_complex": {
        "max_tokens": 10000,
        "model_level": 4,
        "description": "Investigación profunda, síntesis completa"
    }
}

# Categorías de tareas para división
TASK_CATEGORIES = {
    "security_analysis": ["escaneo", "vulnerabilidad", "análisis de seguridad"],
    "development": ["desarrollar", "programar", "implementar", "optimizar"],
    "report_generation": ["generar reporte", "crear informe", "resumen"],
    "data_processing": ["procesar datos", "analizar texto", "transformar información"],
    "testing": ["prueba", "testing", "validar", "verificar"]
}

def evaluate_task_feasibility(task_description: str, current_model: str = "") -> Dict[str, Any]:
    """
    Evalúa si una tarea puede ser realizada con el modelo actual o necesita optimización
    
    Args:
        task_description (str): Descripción de la tarea a evaluar
        current_model (str): Modelo actual en uso (opcional)
        
    Returns:
        Dict con evaluación de factibilidad y recomendaciones
    """
    # Calcular estimación de tokens
    token_estimate = calculate_token_estimate(task_description)
    
    # Determinar nivel de complejidad
    complexity = "simple"
    if token_estimate["max_tokens"] > 5000:
        complexity = "very_complex"
    elif token_estimate["max_tokens"] > 2000:
        complexity = "complex"
    elif token_estimate["max_tokens"] > 500:
        complexity = "intermediate"
    
    # Configurar nivel de complejidad
    complexity_config = TASK_COMPLEXITY_LEVELS[complexity]
    
    # Verificar necesidad de división
    needs_division = complexity_config["max_tokens"] > 3000
    
    # Recomendar modelo óptimo
    optimal_model = get_optimal_model(task_description)
    
    # Verificar si se debe cambiar de modelo
    model_change_needed = False
    model_change_reason = ""
    
    if current_model:
        model_check = suggest_model_change(task_description, current_model)
        if model_check["should_change"]:
            model_change_needed = True
            model_change_reason = model_check["reasoning"]
    
    return {
        "task_complexity": complexity,
        "token_estimate": token_estimate,
        "needs_division": needs_division,
        "optimal_model": optimal_model,
        "model_change_required": model_change_needed,
        "model_change_reason": model_change_reason,
        "complexity_description": complexity_config["description"],
        "recommendations": [
            f"Nivel de complejidad: {complexity}",
            f"Estimación de tokens: {token_estimate['min_tokens']}-{token_estimate['max_tokens']}",
            f"Recursos recomendados: {optimal_model['name']}"
        ]
    }

def determine_task_division(task_description: str) -> Dict[str, Any]:
    """
    Determina si una tarea debe dividirse y cómo hacerlo
    
    Args:
        task_description (str): Descripción de la tarea a dividir
        
    Returns:
        Dict con propuesta de división
    """
    # Detectar palabras clave que indican división necesaria
    keywords_for_division = [
        "y", "además", "también", "incluye", "contiene", 
        "requiere", "necesita", "debe", "tiene"
    ]
    
    # Analizar categorías
    detected_categories = []
    for category, keywords in TASK_CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in task_description.lower():
                detected_categories.append(category)
                break
    
    # Determinar si dividir basado en complejidad y categorías
    needs_division = False
    division_proposal = {
        "should_divide": False,
        "division_points": [],
        "categories_detected": detected_categories,
        "recommendation": "",
        "sub_tasks": []
    }
    
    # Si hay múltiples categorías o es muy compleja
    if len(detected_categories) > 1 or "very_complex" in evaluate_task_feasibility(task_description)["task_complexity"]:
        needs_division = True
        division_proposal["should_divide"] = True
        division_proposal["recommendation"] = "La tarea es compleja y multifacética - se recomienda división"
        
        # Generar división sugerida
        if "development" in detected_categories:
            division_proposal["sub_tasks"].extend([
                "Diseño del componente principal",
                "Implementación del núcleo funcional",
                "Pruebas y validación del módulo",
                "Documentación de la implementación"
            ])
        elif "security_analysis" in detected_categories:
            division_proposal["sub_tasks"].extend([
                "Identificación inicial de vulnerabilidades",
                "Análisis profundo detallado",
                "Validación de resultados obtenidos",
                "Reporte de hallazgos y recomendaciones"
            ])
        
        if "report_generation" in detected_categories:
            division_proposal["sub_tasks"].append("Formato y presentación del reporte profesional")
    
    return division_proposal

def optimize_task_execution(task_description: str, current_model: str = "") -> Dict[str, Any]:
    """
    Optimiza la ejecución total de una tarea considerando todo el sistema
    
    Args:
        task_description (str): Descripción detallada de la tarea
        current_model (str): Modelo actual en uso
        
    Returns:
        Dict con estrategia completa de ejecución optimizada
    """
    # Evaluar factibilidad
    feasibility = evaluate_task_feasibility(task_description, current_model or "")
    
    # Determinar división
    division = determine_task_division(task_description)
    
    # Estrategia de ejecución
    execution_strategy = {
        "task_summary": task_description[:100] + "...",
        "feasibility_analysis": feasibility,
        "division_planning": division,
        "execution_recommendation": "Ejecutar directamente con modelo óptimo",
        "delegation_required": False,
        "model_change_required": feasibility.get("model_change_required", False)
    }
    
    # Si se requiere división, preparar estrategia de delegación
    if division["should_divide"]:
        execution_strategy["delegation_required"] = True
        execution_strategy["execution_recommendation"] = "Dividir en sub-tareas y delegar a especialistas"
        
        # Generar recomendaciones de delegación
        delegation_plan = {
            "number_of_agents": len(division["sub_tasks"]) if division["sub_tasks"] else 3,
            "specialization_areas": division["categories_detected"] if division["categories_detected"] else ["general"],
            "model_allocation": [],
            "coordination_plan": "Sincronización de resultados y fusión en solución final"
        }
        
        # Asignar modelos según especialización
        for i, task in enumerate(division["sub_tasks"] if division["sub_tasks"] else ["tarea 1", "tarea 2", "tarea 3"]):
            model = get_optimal_model(task)
            delegation_plan["model_allocation"].append({
                "task_number": i + 1,
                "task_description": task,
                "assigned_model": model["name"],
                "estimated_tokens": calculate_token_estimate(task)["max_tokens"]
            })
        
        execution_strategy["delegation_plan"] = delegation_plan
    
    # Verificar si se requiere cambio de modelo
    if feasibility.get("model_change_required", False):
        execution_strategy["model_change_suggestion"] = {
            "new_model": feasibility["optimal_model"]["name"],
            "reason": feasibility["model_change_reason"]
        }
    
    return execution_strategy

def get_task_optimization_guide(task_description: str) -> str:
    """
    Genera una guía de optimización para ejecutar una tarea con mayor eficiencia
    
    Args:
        task_description (str): Descripción de la tarea
        
    Returns:
        String con la guía de optimización
    """
    strategy = optimize_task_execution(task_description)
    
    guide = f"""📊 GUÍA DE OPTIMIZACIÓN PARA TAREA: "{strategy['task_summary']}"
    
1. ANÁLISIS DE FACTIBILIDAD
   Nivel de complejidad: {strategy['feasibility_analysis']['task_complexity']}
   Token estimado: {strategy['feasibility_analysis']['token_estimate']['min_tokens']}-{strategy['feasibility_analysis']['token_estimate']['max_tokens']}
   Modelo óptimo recomendado: {strategy['feasibility_analysis']['optimal_model']['name']}
   
2. DIVISIÓN DE TAREA
   ¿Requiere división?: {'SÍ' if strategy['division_planning']['should_divide'] else 'NO'}
   Categorías detectadas: {', '.join(strategy['division_planning']['categories_detected'])}
   
3. RECOMENDACIONES ESPECÍFICAS
"""
    
    recommendations = strategy['feasibility_analysis']['recommendations']
    for i, rec in enumerate(recommendations, 1):
        guide += f"   {i}. {rec}\n"
    
    if strategy['delegation_required']:
        guide += "\n4. PLAN DE DELEGACIÓN\n"
        for item in strategy['delegation_plan']['model_allocation']:
            guide += f"   - Tarea {item['task_number']}: {item['task_description']}\n"
            guide += f"     Modelo recomendado: {item['assigned_model']}\n"
            guide += f"     Tokens estimados: {item['estimated_tokens']}\n"
    
    if strategy.get('model_change_suggestion'):
        guide += f"\n🔄 CAMBIO DE MODELO RECOMENDADO\n"
        guide += f"Nuevo modelo: {strategy['model_change_suggestion']['new_model']}\n"
        guide += f"Justificación: {strategy['model_change_suggestion']['reason']}\n"
    
    return guide

# Funciones auxiliares para casos específicos de aplicación
def execute_with_optimized_resources(task_description: str, context: Dict[str, Any] = {}) -> Dict[str, Any]:
    """
    Ejecuta una tarea con optimización completa de recursos
    
    Args:
        task_description (str): Descripción de la tarea
        context (dict): Contexto adicional de ejecución
        
    Returns:
        Dict con resultados y análisis
    """
    # Optimizar la estrategia de ejecución
    strategy = optimize_task_execution(task_description, context.get("current_model") if context else None)
    
    # Ejecutar según la estrategia
    result = {
        "task_executed": task_description,
        "optimization_strategy": strategy,
        "execution_status": "completed",
        "tokens_consumed": strategy['feasibility_analysis']['token_estimate']['max_tokens'],
        "model_used": strategy['feasibility_analysis']['optimal_model']['name']
    }
    
    if strategy['delegation_required']:
        result["delegation_details"] = strategy['delegation_plan']
    
    return result

# Ejemplo de uso:
if __name__ == "__main__":
    # Ejemplos de uso
    example_tasks = [
        "Desarrollar un escáner de vulnerabilidades en redes locales",
        "Crear un informe de analisis de seguridad basico",
        "Implementar un sistema de detección de intrusiones avanzado",
        "Revisar y optimizar el código de un programa existente"
    ]
    
    print("=== Análisis de Tareas ===\n")
    for task in example_tasks:
        print(f"Tarea: {task}")
        guide = get_task_optimization_guide(task)
        print(guide)
        print("-" * 50 + "\n")