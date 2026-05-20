# Skill: token_optimizer
# Descripción: Herramientas para optimizar el uso de tokens mediante selección inteligente de modelos
# Generado automáticamente por YrYs-Agent

import re
from typing import Dict, Any

# Mapa de modelos por nivel de complejidad
MODEL_MAPPING = {
    # Nivel 1: Tareas básicas y operaciones simples
    1: {
        "name": "qwen/qwen3-coder-30b-a3b-v1",
        "description": "Modelo eficiente para tareas básicas de programación y análisis"
    },
    # Nivel 2: Tareas intermedias con procesamiento de datos y código simple
    2: {
        "name": "qwen/qwen3-72b",
        "description": "Modelo balanceado para análisis de datos y desarrollo básico"
    },
    # Nivel 3: Tareas complejas y análisis avanzado
    3: {
        "name": "anthropic/claude-sonnet-4",
        "description": "Modelo potente para análisis avanzado y desarrollo complejo"
    },
    # Nivel 4: Tareas muy complejas y síntesis profunda
    4: {
        "name": "openai/gpt-4-turbo",
        "description": "Modelo máximo para investigaciones profundas y análisis exhaustivo"
    }
}

# Patrones clave para determinar complejidad
COMPLEXITY_INDICATORS = {
    # Nivel 1: Operaciones simples
    1: [
        r"buscar\s+(?:en|de)\s+\w+", 
        r"listar\s+\w+", 
        r"analizar\s+(?:simple|básico)",
        r"resumen\s+(?:de|del)",
        r"generar\s+(?:informe|reporte)"
    ],
    # Nivel 2: Procesamiento de datos y desarrollo básico
    2: [
        r"programar\s+\w+", 
        r"desarrollar\s+\w+", 
        r"corregir\s+(?:código|error)",
        r"ejecutar\s+\w+",
        r"analizar\s+(?:datos|texto)"
    ],
    # Nivel 3: Tareas complejas con múltiples pasos
    3: [
        r"implementar\s+\w+",
        r"optimizar\s+\w+",
        r"analizar\s+(?:vulnerabilidades|exploits)",
        r"revisar\s+(?:seguridad|código)",
        r"desarrollar\s+(?:módulo|funcionalidad)",
        r"resolver\s+(?:problema|error)"
    ],
    # Nivel 4: Síntesis profunda y análisis técnico avanzado
    4: [
        r"investigar\s+\w+",
        r"realizar\s+análisis\s+profundo",
        r"sintetizar\s+(?:información|resultados)",
        r"diseñar\s+(?:arquitectura|solución)",
        r"evaluar\s+(?:riesgos|impacto)"
    ]
}

def get_optimal_model(task_description: str) -> Dict[str, Any]:
    """
    Determina el modelo óptimo según la complejidad de la tarea
    
    Args:
        task_description (str): Descripción de la tarea a realizar
        
    Returns:
        Dict con información del modelo seleccionado:
        - name: nombre del modelo
        - description: descripción del modelo
        - complexity_level: nivel de complejidad (1-4)
    """
    # Normalizar la descripción de la tarea
    normalized_desc = task_description.lower().strip()
    
    # Determinar nivel de complejidad
    complexity_level = 1  # Por defecto
    
    # Verificar los patrones por niveles
    for level, patterns in COMPLEXITY_INDICATORS.items():
        for pattern in patterns:
            if re.search(pattern, normalized_desc, re.IGNORECASE):
                complexity_level = max(complexity_level, level)
    
    # Obtener modelo basado en el nivel de complejidad
    model_info = MODEL_MAPPING.get(complexity_level, MODEL_MAPPING[1])
    
    return {
        "name": model_info["name"],
        "description": model_info["description"],
        "complexity_level": complexity_level
    }

def calculate_token_estimate(task_description: str) -> Dict[str, int]:
    """
    Estima el uso de tokens basado en la descripción de la tarea
    
    Args:
        task_description (str): Descripción de la tarea
        
    Returns:
        Dict con estimación de tokens:
        - min_tokens: mínimo estimado
        - max_tokens: máximo estimado
        - complexity_score: puntaje de complejidad (1-10)
    """
    # Calcular longitud aproximada y características
    word_count = len(task_description.split())
    char_count = len(task_description)
    
    # Calcular complejidad basada en características
    complexity_score = 1
    
    # Características que incrementan complejidad
    indicators = [
        (word_count > 15, 2),
        (char_count > 100, 1),
        (r"implementar|desarrollar|optimizar" in task_description.lower(), 3),
        (r"análisis|investigar|síntesis" in task_description.lower(), 2),
        (r"seguridad|vulnerabilidad" in task_description.lower(), 2)
    ]
    
    for indicator, score in indicators:
        if indicator:
            complexity_score += score
    
    # Limitar al rango [1, 10]
    complexity_score = max(1, min(10, complexity_score))
    
    # Estimar tokens (aproximado)
    # Basado en experiencia: 1 palabra ≈ 1.2 tokens para prompts
    # El uso real varía, pero esto da una estimación útil
    
    base_tokens = int(word_count * 1.2)
    
    # Escala de tokens estimados
    min_tokens = max(20, base_tokens // 2)
    max_tokens = base_tokens * 2
    
    return {
        "min_tokens": min_tokens,
        "max_tokens": max_tokens,
        "complexity_score": complexity_score
    }

def optimize_task_execution(task_description: str) -> Dict[str, Any]:
    """
    Optimiza la ejecución de una tarea proporcionando recomendaciones
    
    Args:
        task_description (str): Descripción detallada de la tarea
        
    Returns:
        Recomendaciones combinadas de modelo y token
    """
    # Obtener modelo óptimo
    optimal_model = get_optimal_model(task_description)
    
    # Calcular estimación de tokens
    token_estimate = calculate_token_estimate(task_description)
    
    # Generar recomendaciones de optimización
    recommendations = []
    
    if optimal_model["complexity_level"] <= 2:
        recommendations.append("✅ Tarea suficientemente simple para modelo económico")
    else:
        recommendations.append(f"💡 La complejidad indica que podría usar modelo avanzado")
        
    if token_estimate["complexity_score"] >= 8:
        recommendations.append("⚠️ Alta complejidad estimada - considerar división de tarea")
        
    if token_estimate["max_tokens"] > 2000:
        recommendations.append("⚠️ Alta estimación de tokens - verificar uso eficiente")
        
    return {
        "optimal_model": optimal_model,
        "token_estimate": token_estimate,
        "recommendations": recommendations
    }

def suggest_model_change(task_description: str, current_model: str) -> Dict[str, Any]:
    """
    Sugiere cambio de modelo basado en la complejidad de la tarea
    
    Args:
        task_description (str): Descripción de la tarea
        current_model (str): Modelo actual en uso
        
    Returns:
        Información sobre si se recomienda cambio de modelo
    """
    # Obtener modelo óptimo
    optimal_model = get_optimal_model(task_description)
    
    # Comparar con modelo actual
    should_change_model = optimal_model["name"] != current_model
    
    return {
        "should_change": should_change_model,
        "new_model": optimal_model if should_change_model else None,
        "reasoning": (
            f"Cambio sugerido: Modelo {optimal_model['name']} "
            f"(nivel {optimal_model['complexity_level']}) para "
            f"mejor eficiencia en tarea compleja" if should_change_model else
            "Mantenimiento del modelo actual - suficiente para tarea"
        )
    }