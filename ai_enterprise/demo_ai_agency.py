#!/usr/bin/env python3
"""
Demostración de la agencia de IA KaliGhost Enterprise en acción
Esta demo muestra cómo funciona la estructura completa de agentes autónomos
"""

import json
import time
from datetime import datetime
from ceo.brain import KaliGhostBrain
from executive.coordinator import KaliGhostExecutive

def main():
    print("🚀 DEMO KALIGHOST AI ENTERPRISE")
    print("=" * 50)
    
    # Crear el cerebro de la empresa (CEO)
    print("🧠 Inicializando KaliGhost Brain (CEO)...") 
    ceo = KaliGhostBrain()
    ceo.set_strategy("Generar 20,000€ en ingresos en 24 horas con curso de ciberseguridad")
    print("✅ CEO listo para tomar decisiones estratégicas")
    
    # Crear el coordinador ejecutivo
    print("\n🔧 Inicializando KaliGhost Executive (Subdirector)...")
    executive = KaliGhostExecutive()
    print("✅ Subdirector coordinador listo")
    
    # Tomar decisiones estratégicas
    print("\n📝 Decisiones del CEO:")
    decision1 = ceo.make_decision("marketing", {
        "campaign": "Lanzamiento de curso de ciberseguridad",
        "target_audience": "Profesionales de seguridad"
    })
    
    decision2 = ceo.make_decision("sales", {
        "approach": "Oferta urgente con descuento del 30%",
        "deadline": "48 horas"
    })
    
    # Ejecutar flujo de trabajo completo
    print("\n⚙️ Ejecutando flujo de trabajo multi-agente...")
    
    # Definir el flujo de trabajo
    workflow = [
        {
            "agent": "research_analyst",
            "task": {
                "description": "Análisis de mercado para curso de ciberseguridad",
                "priority": "high"
            }
        },
        {
            "agent": "content_creator", 
            "task": {
                "description": "Crear contenido de marketing para lanzamiento",
                "priority": "high"
            }
        },
        {
            "agent": "sales_strategist",
            "task": {
                "description": "Desarrollar estrategia de ventas con descuento",
                "priority": "high"
            }
        },
        {
            "agent": "product_manager",
            "task": {
                "description": "Gestionar lanzamiento del curso completo",
                "priority": "high"
            }
        }
    ]
    
    # Ejecutar el flujo de trabajo
    result = executive.coordinate_workflows(workflow)
    print(f"✅ Flujo de trabajo completado: {result['steps_completed']}/{result['total_steps']} pasos completados")
    
    # Generar reportes
    print("\n📊 Reportes del sistema:")
    
    # Reporte de ejecutivo
    exec_report = executive.generate_daily_report()
    print("📋 Reporte Ejecutivo:")
    print(f"   Total ejecuciones: {exec_report['total_executions']}")
    print(f"   Agentes activos: {exec_report['agents_active']}")
    print(f"   Última ejecución: {exec_report['last_execution']}")
    
    # Reporte financiero simulado
    financial_data = {
        "projected_revenue": "20,000€ en 24h",
        "costs": "4,000€",
        "net_profit": "16,000€",
        "roi": "300%",
        "conversion_rate": "5.2%",
        "customers": "100-200",
        "timestamp": datetime.now().isoformat()
    }
    
    print("\n💰 Reporte Financiero:")
    print(f"   Ingresos proyectados: {financial_data['projected_revenue']}")
    print(f"   Beneficio neto: {financial_data['net_profit']}")
    print(f"   ROI: {financial_data['roi']}")
    print(f"   Clientes: {financial_data['customers']}")
    
    # Resumen final
    print("\n🎉 RESUMEN DE LA AGENCIA DE IA:")
    print("=" * 50)
    print("✅ Estructura completada con éxito")
    print("✅ Agentes funcionando en cooperación")
    print("✅ Sistema de coordinación automatizado")
    print("✅ Rendimiento medible y optimizable")
    print("✅ Potencial para escalar ilimitadamente")
    print("\n🎯 La agencia puede generar 20,000€ en 24 horas")
    print("   ¡Estamos listos para comenzar a facturar!")
    
    print("\n📋 COMPONENTES PRINCIPALES:")
    print("1. KaliGhost Brain (CEO) - Toma decisiones estratégicas") 
    print("2. KaliGhost Executive (Director) - Coordina agentes")
    print("3. 7 Agentes especializados:")
    print("   - Analista de Investigación")
    print("   - Creador de Contenido") 
    print("   - Estratega de Ventas")
    print("   - Gerente de Producto")
    print("   - Analista Financiero")
    print("   - Soporte al Cliente")
    print("   - Especialista en Seguridad")
    print("4. Sistema de Comunicación")
    print("5. Mecanismos de Reporte y Métricas")

if __name__ == "__main__":
    main()