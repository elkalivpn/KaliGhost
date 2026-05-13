"""
Bucle Autónomo del Agente — YrYs-Agent
Implementa: plan → execute → adapt → retry hasta completar tarea al 100%
"""

import os
import json
import time
import asyncio
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

# --- Configuración y Rutas ---
AGENT_ROOT = Path(__file__).parent.parent
CONFIG_PATH = AGENT_ROOT / "yrays_config.yaml"
MEMORY_PATH = AGENT_ROOT / "memory" / "agent_memory.json"
LOGS_DIR = AGENT_ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# --- Logger ---
def log(message: str, level: str = "INFO") -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {level} | {message}"
    
    with open(LOGS_DIR / "agent.log", "a") as f:
        f.write(log_entry + "\n")
        
    print(f"\033[94m{log_entry}\033[0m")

class AutonomousAgent:
    """
    Agent Core para KaliGhost
    - Recibe órdenes en lenguaje natural
    - Crea un plan detallado
    - Ejecuta tareas
    - Se adapta si falla
    - Reintenta hasta completar 100%
    """
    
    def __init__(self):
        self.config = self.load_config()
        self.memory = self.load_memory()
        self.autonomy_level = self.config['agent']['autonomy_level']
        self.auto_confirm = self.config['agent']['auto_confirm']
        self.retry_on_failure = self.config['self_healing']['max_retry_chain']
        self.adaptive_timeout = self.config['self_healing']['adaptive_timeout']
        
        # Fallback chain de IA
        self.llm_chain = self.config['fallback_chain']  # ['bedrock', 'ollama', 'openai', 'anthropic', 'local']
        
        # Fallback tools
        self.fallback_tools = self.config['self_healing']['fallback_tools']
        
        log("YrYs-Agent iniciado en modo autónomo", "INFO")
    
    def load_config(self) -> Dict[str, Any]:
        """Carga configuración completa"""
        try:
            with open(CONFIG_PATH, 'r') as f:
                import yaml
                return yaml.safe_load(f)
        except Exception as e:
            log(f"Error cargando configuración: {e}", "ERROR")
            # Config mínima
            return {
                "agent": {
                    "autonomy_level": 100,
                    "auto_confirm": True
                },
                "self_healing": {
                    "retry_on_failure": 5,
                    "adaptive_timeout": True,
                    "fallback_tools": {}
                },
                "fallback_chain": ["local"],
                "tools": {"enabled": {}}
            }
    
    def load_memory(self) -> Dict[str, Any]:
        """Carga memoria persistente del agente"""
        if MEMORY_PATH.exists():
            with open(MEMORY_PATH, 'r') as f:
                return json.load(f)
        return {
            "sessions": [],
            "skills": {},
            "last_failure": None,
            "success_rate": 0.0,
            "total_tasks": 0,
            "current_task_id": None
        }
    
    def save_memory(self) -> None:
        """Guarda memoria actualizada"""
        MEMORY_PATH.parent.mkdir(exist_ok=True)
        with open(MEMORY_PATH, 'w') as f:
            json.dump(self.memory, f, indent=2)
    
    def understand_task(self, user_input: str) -> Dict[str, Any]:
        """Interpreta la tarea del usuario y la estructura"""
        log(f"Entendiendo tarea: {user_input}", "INFO")
        
        # Ejemplo de análisis estructurado
        # En producción, usaría LLM para parsear
        task_types = {
            "escaneo": ["nmap", "masscan", "rustscan"],
            "vulnerabilidad": ["nuclei", "ffuf", "gobuster"],
            "exploit": ["metasploit", "custom"],
            "red": ["mitm", "arp poisoning", "dns spoofing"]
        }
        
        # Simple keyword matching para PoC
        detected_type = "unknown"
        for t_type, tools in task_types.items():
            if t_type in user_input.lower():
                detected_type = t_type
                break
        
        return {
            "original": user_input,
            "type": detected_type,
            "keywords": user_input.split(),
            "priority": "high",  # Podría inferirse
            "estimated_difficulty": 5,  # 1-10
            "requires_privilege": "sudo" in user_input.lower()
        }
    
    def generate_plan(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Genera plan detallado para ejecutar la tarea"""
        log("Generando plan...", "INFO")
        
        plan = []
        
        if task['type'] == "escaneo":
            plan = [
                {
                    "id": "nmap_scan",
                    "tool": "nmap",
                    "args": ["-sV", "-sC", "-O", task['keywords'][-1]],  # Última palabra como target
                    "description": "Escaneo de servicios y OS",
                    "retry_with": ["masscan", "rustscan"]
                },
                {
                    "id": "masscan_fast",
                    "tool": "masscan",
                    "args": ["--rate=1000", task['keywords'][-1], "-p0-65535"],
                    "description": "Escaneo rápido de puertos",
                    "retry_with": ["nmap", "rustscan"]
                }
            ]
        
        elif task['type'] == "vulnerabilidad":
            plan = [
                {
                    "id": "nuclei_template",
                    "tool": "nuclei",
                    "args": ["-u", task['keywords'][-1], "-t", "cves/", "-severity", "high,critical"],
                    "description": "Búsqueda de CVEs conocidos",
                    "retry_with": ["ffuf", "gobuster"]
                }
            ]
        
        else:
            log("Tipo de tarea no reconocido, usando plan genérico", "WARNING")
            plan = [
                {
                    "id": "manual_mode",
                    "tool": "custom",
                    "args": [task['original']],
                    "description": "Tarea manual o desconocida",
                    "retry_with": []
                }
            ]
        
        return plan
    
    async def execute_step(self, step: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta un paso del plan"""
        tool = step['tool']
        args = step['args']
        target = args[-1] if args else "localhost"
        
        log(f"Ejecutando {tool} en {target}...", "ACTION")
        
        # Simula tools disponibles
        available_tools = [k for k, v in self.config.get('tools', {}).get('enabled', {}).items() if v]
        available_tools += [k for k in self.config.get('local_tools', {}).get('enabled', [])]
        
        if tool not in available_tools:
            return {
                "step_id": step['id'],
                "success": False,
                "error": f"Tool '{tool}' no disponible",
                "output": "",
                "retryable": True
            }
        
        # Simular ejecución (en producción, ejecutaría el comando real)
        cmd = [tool] + args
        
        try:
            # En producción: subprocess.run o terminal
            log(f"Comando simulado: {' '.join(cmd)}", "DEBUG")
            
            # Simulación de salida
            simulated_output = f"[SIMULATED OUTPUT] {tool} completado en {target}\nService: SSH 2.0 OpenSSH\nPort: 22\nOS: Linux\n[END {tool} OUTPUT]"
            
            # Simular fallo ocasional para probar retry
            import random
            if random.random() < 0.3 and step.get('retry_with'):
                raise Exception("Simulated failure for testing retry")
            
            time.sleep(1)  # Simular tiempo de ejecución
            
            return {
                "step_id": step['id'],
                "success": True,
                "error": None,
                "output": simulated_output,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            log(f"Error en {tool}: {e}", "ERROR")
            return {
                "step_id": step['id'],
                "success": False,
                "error": str(e),
                "output": "",
                "retryable": True
            }
    
    def adapt_plan(self, failed_step: Dict[str, Any], plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Adapta el plan usando fallback tools si un paso falla"""
        step_id = failed_step['step_id']
        
        # Buscar el paso que falló
        for i, step in enumerate(plan):
            if step['id'] == step_id:
                # Buscar el siguiente tool de fallback disponible
                current_tool = step['tool']
                fallback_options = step.get('retry_with', [])
                
                for fallback_tool in fallback_options:
                    if fallback_tool in [k for k, v in self.config.get('tools', {}).get('enabled', {}).items() if v]:
                        log(f"Adaptando: usando '{fallback_tool}' en lugar de '{current_tool}'", "ADAPT")
                        plan[i]['tool'] = fallback_tool
                        return plan  # Plan adaptado
                
                # Si no hay fallback directo, usar sistema general
                generic_fallback = self.fallback_tools.get(current_tool, [])
                for tool in generic_fallback:
                    if tool in [k for k, v in self.config.get('tools', {}).get('enabled', {}).items() if v]:
                        log(f"Fallback genérico: usando '{tool}' para '{current_tool}'", "ADAPT")
                        plan[i]['tool'] = tool
                        return plan
                
                # Sin fallback posible
                log(f"No hay fallback para '{current_tool}'", "ERROR")
                plan[i]['retryable'] = False
                
        return plan
    
    async def execute_plan(self, plan: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Ejecuta el plan con retry y adaptación"""
        results = []
        success_count = 0
        total_steps = len(plan)
        
        for step in plan:
            step_id = step['id']
            max_retries = self.retry_on_failure
            attempted_retries = 0
            success = False
            last_result = None
            
            while not success and attempted_retries <= max_retries:
                # Marca como en progreso
                log(f"Paso {step_id} (reintento {attempted_retries + 1}/{max_retries + 1})", "PROGRESS")
                
                result = await self.execute_step(step, {"plan": plan, "results": results})
                last_result = result
                
                if result['success']:
                    success = True
                    success_count += 1
                    log(f"✅ Paso {step_id} completado", "SUCCESS")
                    break
                
                # Si falló y hay más intentos
                if attempted_retries < max_retries:
                    log(f"🔁 {step_id} falló: {result.get('error', 'Unknown')}", "RETRY")
                    
                    # Adaptar plan
                    if result.get('retryable', False):
                        plan = self.adapt_plan(result, plan)
                    
                    # Esperar antes de reintentar (exponential backoff)
                    wait_time = 2 ** attempted_retries
                    log(f"Esperando {wait_time}s antes de reintento...", "WAIT")
                    time.sleep(wait_time)
                
                attempted_retries += 1
            
            # Si tras todos los reintentos sigue fallando
            if not success:
                log(f"❌ Paso {step_id} falló después de {max_retries + 1} intentos", "FAILURE")
                if last_result:
                    results.append(last_result)
                # Continuar con siguiente paso si es posible
            else:
                results.append(result)
        
        # Resultado final
        final_success = success_count == total_steps
        
        summary = {
            "success": final_success,
            "completed_steps": success_count,
            "total_steps": total_steps,
            "results": results,
            "plan": plan,
            "timestamp": datetime.now().isoformat()
        }
        
        if final_success:
            log("\033[92m✅ TAREA COMPLETADA AL 100%\033[0m", "SUCCESS")
        else:
            log("\033[91m❌ TAREA INCOMPLETA\033[0m", "FAILURE")
            
        return summary
    
    async def run_task(self, user_input: str) -> Dict[str, Any]:
        """Ejecuta una tarea completa del usuario con autonomía total"""
        task_id = f"task_{int(time.time())}"
        
        # Inicializar memoria de tarea
        self.memory['current_task_id'] = task_id
        self.memory['total_tasks'] += 1
        
        log(f"\033[1mNueva tarea recibida: {user_input}\033[0m", "USER")
        
        # 1. Entender tarea
        task_data = self.understand_task(user_input)
        log(f"Tipo detectado: {task_data['type']}", "INFO")
        
        # 2. Generar plan
        plan = self.generate_plan(task_data)
        log(f"Plan generado: {len(plan)} pasos", "PLAN")
        
        for i, step in enumerate(plan, 1):
            log(f"  {i}. {step['tool']} {step['description']}", "PLAN")
        
        # En modo AUTO, no pedir confirmación
        if not self.auto_confirm:
            confirm = input("¿Ejecutar plan? (s/n): ").lower()
            if confirm not in ['s', 'y', 'si', 'yes']:
                return {"success": False, "error": "Usuario canceló"}
        
        # 3. Ejecutar plan con retry y adaptación
        result = await self.execute_plan(plan)
        
        # 4. Guardar en memoria
        self.memory['sessions'].append({
            "task_id": task_id,
            "user_input": user_input,
            "task_data": task_data,
            "plan": plan,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
        
        self.save_memory()
        
        return result

def main():
    """Entry point para testing"""
    agent = AutonomousAgent()
    
    test_tasks = [
        "Escanea la red local 192.168.1.1 y encuentra servicios",
        "Busca vulnerabilidades en https://example.com",
        "Realiza un pentest completo en mi servidor"
    ]
    
    for task in test_tasks:
        print("\n" + "=" * 60)
        result = asyncio.run(agent.run_task(task))
        
        if result['success']:
            print("\033[92mTarea completada con éxito\033[0m")
        else:
            print("\033[91mTarea no completada\033[0m")
        
        time.sleep(2)
    
    log("Test completado", "INFO")

if __name__ == "__main__":
    main()