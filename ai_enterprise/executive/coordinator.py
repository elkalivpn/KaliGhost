"""
KaliGhost AI Enterprise - Executive Coordinator
El coordinador ejecutivo que organiza y asigna tareas a los agentes
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any

# Importamos los agentes
from agents.research_analyst.analyzer import ResearchAnalyst
from agents.content_creator.writer import ContentCreator
from agents.sales_strategist.optimizer import SalesStrategist
from agents.product_manager.planner import ProductManager
from agents.financial_analyst.analyst import FinancialAnalyst
from agents.customer_support.responder import CustomerSupport
from agents.security_specialist.protector import SecuritySpecialist

class KaliGhostExecutive:
    """
    Sistema de coordinación ejecutiva que asigna tareas y supervisa agentes
    """
    
    def __init__(self):
        self.name = "KaliGhost Executive"
        self.agents = {}
        self.task_queue = []
        self.execution_history = []
        self.setup_agents()
        
    def setup_agents(self):
        """Configurar y registrar todos los agentes"""
        self.agents = {
            "research_analyst": ResearchAnalyst(),
            "content_creator": ContentCreator(),
            "sales_strategist": SalesStrategist(),
            "product_manager": ProductManager(),
            "financial_analyst": FinancialAnalyst(), 
            "customer_support": CustomerSupport(),
            "security_specialist": SecuritySpecialist()
        }
        
        print("🤖 Agentes registrados y listos para ejecutar")
        for agent_name, agent in self.agents.items():
            print(f"   - {agent_name}: {agent.__class__.__name__}")
        
    def assign_task(self, agent_name: str, task: Dict[str, Any]) -> bool:
        """Asignar tarea a un agente específico"""
        if agent_name in self.agents:
            agent = self.agents[agent_name]
            try:
                # Ejecutar tarea
                result = agent.execute_task(task)
                
                # Registrar ejecución
                execution_record = {
                    "task_id": len(self.execution_history) + 1,
                    "timestamp": datetime.now().isoformat(),
                    "agent": agent_name,
                    "task": task,
                    "result": result,
                    "status": "completed"
                }
                
                self.execution_history.append(execution_record)
                print(f"✅ Tarea asignada a {agent_name}: {task['description'][:50]}...")
                return True
                
            except Exception as e:
                print(f"❌ Error en asignación de tarea: {str(e)}")
                return False
        else:
            print(f"⚠️ Agente {agent_name} no encontrado")
            return False
            
    def coordinate_workflows(self, workflow: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Coordinar flujo de trabajo multi-agente"""
        results = []
        for step in workflow:
            agent_name = step["agent"]
            task = step["task"]
            success = self.assign_task(agent_name, task)
            
            if success:
                results.append({
                    "step": step,
                    "status": "completed"
                })
            else:
                results.append({
                    "step": step,
                    "status": "failed"
                })
                
        return {
            "workflow_id": len(self.execution_history) + 1,
            "timestamp": datetime.now().isoformat(),
            "steps_completed": len([r for r in results if r["status"] == "completed"]),
            "total_steps": len(workflow),
            "results": results
        }
        
    def get_agent_status(self) -> Dict[str, Any]:
        """Obtener estado de todos los agentes"""
        status_report = {
            "executive": self.name,
            "timestamp": datetime.now().isoformat(),
            "agents_count": len(self.agents),
            "active_tasks": len(self.task_queue),
            "execution_history_count": len(self.execution_history),
            "agents_status": {}
        }
        
        for agent_name, agent in self.agents.items():
            status_report["agents_status"][agent_name] = {
                "name": agent_name,
                "type": agent.__class__.__name__,
                "status": "active"
            }
            
        return status_report
        
    def generate_daily_report(self) -> Dict[str, Any]:
        """Generar reporte diario de actividad"""
        report = {
            "report_date": datetime.now().isoformat(),
            "executive": self.name,
            "total_executions": len(self.execution_history),
            "agents_active": len(self.agents),
            "last_execution": self.execution_history[-1]["timestamp"] if self.execution_history else None,
            "task_summary": self.get_task_summary()
        }
        return report
        
    def get_task_summary(self) -> Dict[str, int]:
        """Resumen de tareas ejecutadas"""
        summary = {}
        for record in self.execution_history:
            agent = record["agent"]
            summary[agent] = summary.get(agent, 0) + 1
        return summary

# Ejemplo de uso
if __name__ == "__main__":
    coordinator = KaliGhostExecutive()
    
    # Obtener estado de agentes
    status = coordinator.get_agent_status()
    print("📋 Estado de agentes:")
    print(json.dumps(status, indent=2, ensure_ascii=False))
    
    # Ejecutar tarea específica
    task = {
        "description": "Analizar mercado de ciberseguridad",
        "priority": "high",
        "deadline": "24h"
    }
    coordinator.assign_task("research_analyst", task)
    
    # Generar reporte diario
    report = coordinator.generate_daily_report()
    print("\n📊 Reporte diario:")
    print(json.dumps(report, indent=2, ensure_ascii=False))