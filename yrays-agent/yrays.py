#!/usr/bin/env python3
"""
YrYs-Agent v1.0.0
Asistente de IA Autónomo para Pentesting dentro de KaliGhost.

Este módulo central coordina todos los aspectos del agente:
- Carga de configuración
- Interfaz con el modelo de IA del host
- Procesamiento de tareas
- Creación dinámica de Habilidades (Skills)
- Aplicación de controles de seguridad (ACL)
"""

import os
import sys
import yaml
import json
import requests
import subprocess
import logging
from typing import Dict, List, Optional
from pathlib import Path
import hashlib
import secrets
import string

def generate_otp(length: int = 16) -> str:
    """Genera una clave OTP (One-Time Password) para autenticación por sesión."""
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))

# --- AI API - SISTEMA DE INTELIGENCIA ARTIFICIAL ---
class AIAPI:
    """Clase para interactuar con el sistema de IA""" 
    def __init__(self, config: Dict):
        # Configuración del sistema de IA
        self.timeout = config.get('timeout', 30)
        
        # Debug
        print(f"🚀 [DEBUG] Sistema de IA inicializado")

    def send_task(self, prompt: str) -> str:
        """Envía una tarea al sistema de IA y devuelve la respuesta."""
        print(f"📡 Enviando solicitud al sistema de IA")
        
        try:
            # Simular respuesta del sistema de IA
            time.sleep(1)  # Simular tiempo de procesamiento
            
            # Respuesta genérica sin revelar detalles de implementación
            response_text = f"✅ [KaliGhost IA] → \n🔍 OBJETIVO RECIBIDO: '{prompt}'\n🔄 PROCESANDO: Aplicando lógica avanzada YrYs-Agent.\n🎯 MODO FANTASMA: Operando en modo seguro y eficiente.\n🛠️ TOOLS: Preparado para ejecutar herramientas autorizadas."
            
            print("✅ Respuesta del sistema de IA recibida")
            return response_text
                
        except Exception as e:
            print(f"❌ ERROR en el sistema de IA: {e}")
            print("------------------------------------------------")
            
            # FALLBACK - Generar respuesta razonable según PRINCIPIOS KALIGHOST
            return f"✅ [KaliGhost FALLBACK] → \n🔍 OBJETIVO RECIBIDO: '{prompt}'\n🔄 PROCESANDO: Aplicando lógica offline YrYs-Agent.\n🎯 MODO FANTASMA: Operando en modo 100% autocontenido.\n🛠️ TOOLS: Preparado para ejecutar herramientas autorizadas."

class SkillManager:
    """Gestiona la creación, carga y ejecución de Skills dinámicas."""
    def __init__(self, skills_dir: str):
        # Detectar si estamos en Docker o entorno local
        if '/root' in skills_dir or 'docker' in os.environ.get('PATH', '').lower():
            # Entorno Docker: usar config original
            self.skills_dir = Path(skills_dir)
        else:
            # Entorno local: usar directorio del proyecto
            self.skills_dir = Path("/Users/mrhardcore/KaliGhost/yrays-agent/skills")
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        self.loaded_skills = {}

    def create_skill(self, name: str, description: str, code: str) -> bool:
        """Crea una nueva habilidad (skill) de forma dinámica."""
        valid_name = ''.join(c for c in name if c.isalnum() or c in '._-').rstrip()
        skill_path = self.skills_dir / f"{valid_name}.py"

        if skill_path.exists():
            logging.warning(f"La habilidad '{name}' ya existe. Sobrescribiendo después de revisión de seguridad.")

        # 1. Aplicar políticas de seguridad (safety_level)
        if not self._review_code(code):
            logging.error(f"Fallo en la revisión de seguridad para la habilidad '{name}'. No se creará.")
            return False

        try:
            # 2. Escribir el código
            with open(skill_path, 'w') as f:
                f.write(code)

            # 3. Dar permisos de solo lectura/escritura al propietario
            skill_path.chmod(0o600)  # chmod 600

            # 4. Cargar la skill en memoria
            self._load_skill(name, skill_path)
            logging.info(f"Habilidad dinámica creada y cargada: {name}")
            return True

        except Exception as e:
            logging.error(f"Error al crear la habilidad '{name}': {e}")
            return False

    def _review_code(self, code: str) -> bool:
        """Revisión de seguridad básica del código de una skill."""
        dangerous_patterns = [
            r'\brm\b', r'\bdelete\b', r'\bformat\b', r'\bxp_cmdshell\b',
            r'\bos\.system\b', r'\bsubprocess\.Popen\b', r'\bsubprocess\.call\b',
            r'\bopen\b.*a', r'\bopen\b.*w', # Solo lectura
            r'\bsocket\b', r'\brequests\.post\b', r'\brequests\.put\b', # Comunicación de red
            r'\bexec\b', r'\beval\b', r'\binput\b', r'\bcompile\b'
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                logging.warning(f"Patrón peligroso detectado en el código: {pattern}")
                return False
        return True

    def _load_skill(self, name: str, path: Path):
        """Carga una skill en el entorno del agente."""
        # Aquí irría la lógica para importar dinámicamente el módulo.
        # Se ha omitido por brevedad, pero en producción se usaría `importlib`.
        self.loaded_skills[name] = str(path)


class Tool:
    """Representa una herramienta del sistema con su política de ACL."""
    def __init__(self, config: Dict):
        self.config = config
        self.allowed_args = set(config.get('args', []))

    def can_execute(self, args: List[str]) -> bool:
        """Verifica si la ejecución con estos argumentos está permitida."""
        # Solo permite los argumentos explícitamente permitidos
        # Simplificación: asume que los argumentos clave (como -p 80) se pasan como ['arg', 'value'] o ['arg=value']
        for arg in args:
            # Extraer solo el nombre del argumento (parte antes del = o el propio arg)
            arg_name = arg.split('=')[0]
            if arg_name.startswith('-') and arg_name not in self.allowed_args:
                return False
        return True

class ACL:
    """Control de acceso a herramientas y red."""
    def __init__(self, config: Dict):
        self.config = config
        self.allowed_tools = {}
        for tool_config in config.get('allowed_tools', []):
            self.allowed_tools[tool_config['name']] = Tool(tool_config)
        self.blocked_tools = set(config.get('blocked_tools', []))
        self.network_policy = config.get('network_policy', 'internal_only')

    def can_use_tool(self, tool_name: str, args: List[str]) -> bool:
        """Determina si una herramienta puede usarse con los argumentos dados."""
        # 1. Verificar si la herramienta está bloqueada
        if tool_name in self.blocked_tools:
            logging.warning(f"Intento de usar herramienta bloqueada: {tool_name}")
            return False

        # 2. Verificar si la herramienta está permitida
        if tool_name not in self.allowed_tools:
            logging.warning(f"Herramienta no autorizada: {tool_name}")
            return False

        # 3. Verificar los argumentos de la herramienta
        tool = self.allowed_tools[tool_name]
        if not tool.can_execute(args):
            logging.warning(f"Argumentos no autorizados para la herramienta '{tool_name}': {args}")
            return False

        return True

    def can_access_network(self, target: str) -> bool:
        """Simulación básica de política de red."""
        # Esta es una implementación simplificada.
        # En un entorno real, se dependería de iptables o una red de Docker.
        if self.network_policy == 'internal_only':
            return target in ['172.17.0.1', 'localhost']
        elif self.network_policy == 'external_only':
            return not (target.startswith('172.17.') or target.startswith('127.'))
        return True # 'mixed'

class Agent:
    """El núcleo del agente YrYs."""
    def __init__(self, config_path: str):
        self.load_config(config_path)
        self.setup_logging()
        self.ai_api = AIAPI(self.config)
        self.skills = SkillManager(self.config['agent']['skill_directory'])
        self.acl = ACL(self.config['acl'])
        logging.info(f"Agente YrYs '{self.config['agent']['name']}' iniciado. Misión: {self.config['agent']['mission'].strip()}")

    def load_config(self, path: str):
        """Carga la configuración desde un archivo YAML."""
        with open(path, 'r') as f:
            self.config = yaml.safe_load(f)

    def setup_logging(self):
        """Configura el sistema de logging del agente."""
        # Detectar si estamos en Docker o entorno local
        log_file = self.config['logging'].get('file', 'YrYs-Agent/logs/agent.log')
        if '/root/work' in log_file or 'docker' in os.environ.get('PATH', '').lower():
            # Entorno Docker: usar config original
            log_dir = Path(log_file).parent
        else:
            # Entorno local: usar directorio del proyecto o temporal
            log_dir = Path("/Users/mrhardcore/KaliGhost/yrays-agent/logs")
            
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "yrays.log"

        level = {
            'error': logging.ERROR,
            'warn': logging.WARNING,
            'info': logging.INFO,
            'debug': logging.DEBUG
        }.get(self.config['logging']['level'], logging.INFO)

        logging.basicConfig(
            filename=log_file,
            level=level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def think(self, goal: str):
        """Proceso de pensamiento del agente para alcanzar un objetivo."""
        prompt = f"""
Actúa como el agente de IA '{self.config['agent']['name']}'. Tu misión es: {self.config['agent']['mission']}

Objetivo Actual: {goal}

Crea un plan detallado, paso a paso, utilizando HERRAMIENTAS y habilidades (skills) permitidas.
Para cada paso:
1. Describe la acción.
2. Especifica SIEMPRE la herramienta a usar (solo herramientas en la lista permitida: {list(self.acl.allowed_tools.keys())}).
3. Si se necesita crear una nueva habilidad (skill), genera el código Python correspondiente.

No uses herramientas bloqueadas: {', '.join(self.acl.blocked_tools)}.
"""

        plan = self.ai_api.send_task(prompt)
        logging.info(f"Plan generado para el objetivo '{goal}':\n{plan}")
        return plan

    def execute_plan(self, plan: str):
        """Ejecuta un plan paso a paso."""
        # Simplificando el parseo del plan. En una implementación real, se usaría NLP avanzado.
        steps = [line.strip() for line in plan.split('\n') if line.strip().startswith(('1.', '2.', '3.', '4.', '5.'))]
        for step in steps:
            logging.info(f"Ejecutando: {step}")
            # Aquí iría el análisis y ejecución de cada acción, herramienta o creación de skill.
            # Este es un placeholder conceptual.
            if "crear una nueva habilidad" in step.lower() or "genera el código" in step.lower():
                # Simular la creación de una skill
                name = "scan_webserver"
                description = "Ejecuta nikto sobre un host web."
                code = """
def scan_webserver(target: str) -> str:\n    \"\"\"Escanea un servidor web con nikto.\"\"\"\n    import subprocess\n    result = subprocess.run(['nikto', '-h', target], capture_output=True, text=True)\n    return result.stdout\n                """
                self.skills.create_skill(name, description, code)

            elif "usa la herramienta" in step.lower():
                # Simular la ejecución de una herramienta con ACL
                tool_name = "nikto"  # Ejemplo
                args = ["-h", "target.com"]
                if self.acl.can_use_tool(tool_name, args):
                    result = subprocess.run([tool_name, *args], capture_output=True, text=True)
                    logging.info(f"Resultado de {tool_name}: {result.stdout}")
                else:
                    logging.error(f"Acción bloqueada por ACL: {tool_name} {args}")

    def start(self, user_goal: str):
        """Punto de entrada para el agente."""
        plan = self.think(user_goal)
        self.execute_plan(plan)

if __name__ == "__main__":
    # Verificamos que se haya pasado un objetivo
    if len(sys.argv) < 2:
        print("Uso: yrays.py <objetivo_del_usuario>")
        sys.exit(1)

    # Ruta al archivo de configuración (relativa al directorio del script)
    config_path = os.path.join(os.path.dirname(__file__), "config", "config.yaml")

    # Lanzar el agente
    agent = Agent(config_path)
    agent.start(sys.argv[1])
