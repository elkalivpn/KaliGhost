# Skill: hermes_token_optimizer
# Descripción: Sistema de optimización de tokens para Hermes y KaliGhost
# Generado automáticamente por YrYs-Agent

import re
from typing import Dict, List, Any
from .token_optimizer import get_optimal_model, calculate_token_estimate
from .advanced_task_optimizer import evaluate_task_feasibility, determine_task_division

# Definición de niveles de valor técnico
TECHNICAL_VALUE_LEVELS = {
    "minimal": {
        "score": 1,
        "description": "Valor técnico mínimo - repetición o información obvia",
        "tokens_limit": 200
    },
    "low": {
        "score": 3,
        "description": "Valor técnico bajo - simple tarea sin impacto",
        "tokens_limit": 500
    },
    "medium": {
        "score": 6,
        "description": "Valor técnico medio - tarea importante pero no crítica",
        "tokens_limit": 1500
    },
    "high": {
        "score": 8,
        "description": "Valor técnico alto - desarrollo significativo",
        "tokens_limit": 3000
    },
    "critical": {
        "score": 10,
        "description": "Valor técnico crítico - función fundamental del sistema",
        "tokens_limit": 5000
    }
}

# Clasificación de tareas por valor técnico
TASK_VALUE_CATEGORIES = {
    # Tareas de valor mínimo
    "minimal": [
        r"repetir\s+(?:información|dato)",
        r"explicar\s+(?:algo|concepto)",
        r"dar\s+(?:ejemplo|ejemplos)",
        r"repetir\s+(?:instrucción|comando)"
    ],
    
    # Tareas de valor bajo
    "low": [
        r"formatear\s+(?:texto|código)",
        r"organizar\s+(?:información|archivos)",
        r"revisar\s+(?:estructura|formato)",
        r"crear\s+(?:plantilla|estructura)" 
    ],
    
    # Tareas de valor medio
    "medium": [
        r"analizar\s+(?:código|funcionalidad)",
        r"mejorar\s+(?:rendimiento|función)",
        r"documentar\s+(?:componente|función)",
        r"corregir\s+(?:error|problema)"
    ],
    
    # Tareas de valor alto
    "high": [
        r"desarrollar\s+(?:nueva funcionalidad|característica)",
        r"integrar\s+(?:módulo|componente)",
        r"optimizar\s+(?:sistema|proceso)",
        r"implementar\s+(?:algoritmo|función)"
    ],
    
    # Tareas de valor crítico
    "critical": [
        r"construir\s+(?:sistema|plataforma)",
        r"desarrollar\s+(?:componente central|núcleo)",
        r"resolver\s+(?:problema|bug crítico)",
        r"diseñar\s+(?:arquitectura|estructura fundamental)"
    ]
}

def assess_task_technical_value(task_description: str) -> Dict[str, Any]:
    """
    Evalúa el valor técnico de una tarea
    
    Args:
        task_description (str): Descripción de la tarea
        
    Returns:
        Dict con valor técnico y recomendaciones
    """
    normalized_desc = task_description.lower().strip()
    
    # Determinar nivel de valor técnico
    value_level = "medium"  # Por defecto
    value_score = 6
    
    # Verificar categorías por nivel de valor
    for level, patterns in TASK_VALUE_CATEGORIES.items():
        for pattern in patterns:
            if re.search(pattern, normalized_desc, re.IGNORECASE):
                # Obtener el score correspondiente
                score_info = TECHNICAL_VALUE_LEVELS[level]
                if score_info["score"] > value_score:
                    value_level = level
                    value_score = score_info["score"]
    
    # Obtener información del nivel
    level_info = TECHNICAL_VALUE_LEVELS[value_level]
    
    return {
        "value_level": value_level,
        "value_score": value_score,
        "description": level_info["description"],
        "tokens_limit": level_info["tokens_limit"],
        "recommendation": f"Nivel de valor técnico: {value_level} ({value_score}/10)"
    }

def optimize_task_execution_for_hermes(task_description: str, current_context: Dict[str, Any] = {}) -> Dict[str, Any]:
    """
    Optimiza la ejecución de tareas específicamente para Hermes
    
    Args:
        task_description (str): Descripción de la tarea
        current_context (Dict): Contexto actual de ejecución
        
    Returns:
        Dict con estrategia de ejecución optimizada para Hermes
    """
    # Evaluar valor técnico de la tarea
    technical_value = assess_task_technical_value(task_description)
    
    # Calcular estimación de tokens
    token_estimate = calculate_token_estimate(task_description)
    
    # Evaluar factibilidad
    feasibility = evaluate_task_feasibility(task_description)
    
    # Determinar si se requiere división
    division = determine_task_division(task_description)
    
    # Evaluar necesidad de cambio de modelo
    model_suggestion = get_optimal_model(task_description)
    
    # Estrategia de ejecución
    execution_strategy = {
        "task_description": task_description,
        "technical_value": technical_value,
        "token_estimate": token_estimate,
        "feasibility": feasibility,
        "requires_division": division["should_divide"],
        "recommended_model": model_suggestion,
        "optimized_approach": {
            "priority": "high" if technical_value["value_score"] >= 8 else "medium",
            "token_consideration": True,
            "value_consideration": True,
            "division_recommendation": division["should_divide"] if division["should_divide"] else "no division needed"
        }
    }
    
    # Si la tarea tiene valor técnico bajo, recomendar evitarla o optimizarla
    if technical_value["value_score"] <= 4:
        execution_strategy["optimization_suggestion"] = {
            "action": "reconsider",
            "reason": "Valor técnico bajo, reconsiderar prioridad",
            "alternative_actions": [
                "Buscar tareas de mayor valor técnico",
                "Unir con otra tarea similar para mayor impacto",
                "Deferir hasta etapa posterior"
            ]
        }
    elif technical_value["value_score"] <= 6 and token_estimate["max_tokens"] > 2000:
        # Tarea media pero consume muchos tokens
        execution_strategy["optimization_suggestion"] = {
            "action": "divide",
            "reason": "Valor técnico medio pero alto consumo de tokens",
            "recommendation": "Dividir en subtareas o reducir scope"
        }
    
    # Si se requiere división
    if division["should_divide"]:
        execution_strategy["division_plan"] = {
            "sub_tasks": division["sub_tasks"] if division["sub_tasks"] else [
                "Componente principal",
                "Implementación secundaria", 
                "Pruebas y validación"
            ],
            "model_assignment": [],
            "coordinated_execution": True
        }
        
        # Asignar modelos a cada sub-tarea
        for i, sub_task in enumerate(execution_strategy["division_plan"]["sub_tasks"]):
            model = get_optimal_model(sub_task)
            execution_strategy["division_plan"]["model_assignment"].append({
                "task_number": i + 1,
                "sub_task": sub_task,
                "model": model["name"]
            })
    
    return execution_strategy

def get_hermes_execution_guide(task_description: str) -> str:
    """
    Genera una guía específica para ejecución optimizada por Hermes
    
    Args:
        task_description (str): Descripción de la tarea
        
    Returns:
        String con guía de ejecución optimizada para Hermes
    """
    strategy = optimize_task_execution_for_hermes(task_description)
    
    guide = f"""🎯 DIRECTRICES DE EJECUCIÓN OPTIMIZADA PARA HERMES
    
Tarea: "{strategy['task_description'][:100]}..."
===

1. VALOR TÉCNICO
   Nivel: {strategy['technical_value']['value_level']}
   Puntuación: {strategy['technical_value']['value_score']}/10
   Descripción: {strategy['technical_value']['description']}
   Límite de tokens: {strategy['technical_value']['tokens_limit']}

2. ESTIMACIÓN DE TOKENS
   Mínimo estimado: {strategy['token_estimate']['min_tokens']}
   Máximo estimado: {strategy['token_estimate']['max_tokens']}
   Complejidad: {strategy['token_estimate']['complexity_score']}/10

3. ENFOQUE RECOMENDADO
   {strategy['optimized_approach']['priority'].upper()} PRIORIDAD
   Modelo recomendado: {strategy['recommended_model']['name']}

4. ACCIONES ESPECÍFICAS
"""
    
    # Agregar consejos según el valor técnico
    if strategy['technical_value']['value_score'] <= 4:
        guide += "   ⚠️ BAJA PRIORIDAD - Reconsiderar esta tarea\n"
    elif 5 <= strategy['technical_value']['value_score'] <= 6:
        guide += "   👀 VALOR MEDIO - Revisar si puede dividirse\n"
    elif strategy['technical_value']['value_score'] >= 7:
        guide += "   ✅ ALTA PRIORIDAD - Ejecutar con enfoque técnico\n"
    
    if strategy['requires_division']:
        guide += "   🔄 REQUERIDAS SUB-TAREAS - Dividir para mayor eficiencia\n"
    
    # Recomendaciones adicionales
    if strategy.get('optimization_suggestion'):
        guide += f"\n📝 RECOMENDACIÓN DE OPTIMIZACIÓN:\n"
        guide += f"   {strategy['optimization_suggestion']['reason']}\n"
        if 'alternative_actions' in strategy['optimization_suggestion']:
            for action in strategy['optimization_suggestion']['alternative_actions']:
                guide += f"   • {action}\n"
    
    return guide

# Funciones de monitoreo y control de ejecución
def monitor_execution_progress(task_id: str, tokens_used: int, value_score: int) -> Dict[str, Any]:
    """
    Monitoriza el progreso de ejecución de una tarea
    
    Args:
        task_id (str): ID de la tarea
        tokens_used (int): Tokens utilizados
        value_score (int): Puntuación de valor técnico
        
    Returns:
        Dict con métricas de control
    """
    efficiency_score = tokens_used / value_score if value_score > 0 else 0
    
    return {
        "task_id": task_id,
        "tokens_used": tokens_used,
        "value_score": value_score,
        "efficiency_ratio": efficiency_score,
        "recommendation": "continue" if efficiency_score < 2000 else "review",
        "performance_alert": efficiency_score > 3000
    }

# Ejemplo de uso:
if __name__ == "__main__":
    # Prueba de la nueva habilidad
    test_tasks = [
        "Crear un informe de análisis de seguridad básico",
        "Desarrollar un escáner de vulnerabilidades en redes locales",
        "Repetir la información sobre cómo funciona la función",
        "Implementar un sistema de detección de intrusiones avanzado"
    ]
    
    print("=== Análisis de Tareas para Hermes ===\n")
    for task in test_tasks:
        print(f"Tarea: {task}")
        guide = get_hermes_execution_guide(task)
        print(guide[:300] + "...\n")
        print("-" * 50 + "\n")