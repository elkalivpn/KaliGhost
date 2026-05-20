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
import re
from typing import Dict, List, Optional
from pathlib import Path
import hashlib
import secrets
import string
import time
import threading
import readline

# Importar la nueva integración de IA
try:
    from .ai_integrations import create_ai_provider, fallback_response
    AI_INTEGRATION_AVAILABLE = True
except ImportError:
    # Fallback si no se puede importar
    AI_INTEGRATION_AVAILABLE = False
    def fallback_response(prompt):
        return f"✅ [KaliGhost IA - SIMULACIÓN] → \n🔍 OBJETIVO RECIBIDO: '{prompt}'\n🔄 PROCESANDO: Aplicando lógica avanzada YrYs-Agent.\n🎯 MODO FANTASMA: Operando en modo seguro y eficiente.\n🛠️ TOOLS: Preparado para ejecutar herramientas autorizadas."

# Importar el nuevo sistema de skills
try:
    from .skill_system import SkillManager
    SKILLS_AVAILABLE = True
except ImportError:
    # Fallback si no se puede importar
    SKILLS_AVAILABLE = False
    class SkillManager:
        def __init__(self, *args, **kwargs):
            pass
        def create_skill(self, *args, **kwargs):
            return False
        def execute_skill_function(self, *args, **kwargs):
            raise Exception("Sistema de skills no disponible")

# Importar la extensión autónoma
try:
    from .autonomous_extension import create_autonomous_extension
    AUTONOMY_EXTENSION_AVAILABLE = True
except ImportError:
    AUTONOMY_EXTENSION_AVAILABLE = False
    def create_autonomous_extension(*args, **kwargs):
        return None

# Nueva clase para manejo mejorado de entrada de texto
class ImprovedTextInputManager:
    """Manejador mejorado de texto de entrada para evitar problemas de renderizado"""
    
    def __init__(self):
        self.input_buffer = ""
        self.cursor_position = 0
        
    def clear_input_line(self):
        """Limpia completamente la línea de entrada"""
        sys.stdout.write(f"\r{' ' * 100}\r")
        sys.stdout.flush()
        
    def show_input_buffer(self, prompt="> "):
        """Muestra el buffer de entrada completo"""
        self.clear_input_line()
        sys.stdout.write(f"{prompt}{self.input_buffer}")
        sys.stdout.flush()
        
    def get_safe_input(self, prompt="> "):
        """Obtiene entrada segura que no pierde caracteres"""
        self.input_buffer = ""
        self.cursor_position = 0
        self.show_input_buffer(prompt)
        
        try:
            # Configurar para captura de teclas individuales
            while True:
                char = sys.stdin.read(1)
                if char == '\n':
                    # Finalizar entrada
                    print()  # Nueva línea
                    result = self.input_buffer
                    self.input_buffer = ""
                    return result
                elif char == '\b' or char == '\x7f':  # Backspace
                    if len(self.input_buffer) > 0:
                        self.input_buffer = self.input_buffer[:-1]
                        self.cursor_position = len(self.input_buffer)
                        self.show_input_buffer(prompt)
                elif ord(char) >= 32:  # Caracteres imprimibles
                    self.input_buffer += char
                    self.cursor_position = len(self.input_buffer)
                    self.show_input_buffer(prompt)
                else:
                    # Otros caracteres de control, ignorar
                    continue
                    
        except KeyboardInterrupt:
            print("\nInterrupción por teclado")
            return ""
        except Exception as e:
            print(f"\nError de entrada: {e}")
            return ""

def generate_otp(length: int = 16) -> str:
    """Genera una clave OTP (One-Time Password) para autenticación por sesión."""
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))

# --- AI API - SISTEMA DE INTELIGENCIA ARTIFICIAL ---
class AIAPI:
    """Clase para interactuar con el sistema de IA"""
    def __init__(self, config: Dict):
        # Configuración del sistema de IA
        self.timeout = config.get('timeout', 30)
        self.config = config
        
        # Inicializar proveedor de IA si está disponible
        self.provider = None
        if AI_INTEGRATION_AVAILABLE:
            try:
                # Leer la cadena de fallback de la configuración
                fallback_chain = config.get('fallback_chain', ['bedrock', 'remote', 'local', 'default'])
                
                # Intentar inicializar el primer proveedor disponible
                for provider_type in fallback_chain:
                    if provider_type == 'bedrock':
                        # Verificar si Bedrock está habilitado en la configuración
                        if config.get('aws', {}).get('bedrock', {}).get('enabled', False):
                            bedrock_config = config['aws']['bedrock']
                            self.provider = create_ai_provider('bedrock', bedrock_config)
                            break
                    elif provider_type == 'remote':
                        # Verificar si hay configuración para OpenAI o Anthropic
                        if os.environ.get('OPENAI_API_KEY'):
                            self.provider = create_ai_provider('openai', {'model': 'gpt-3.5-turbo'})
                            break
                        elif os.environ.get('ANTHROPIC_API_KEY'):
                            self.provider = create_ai_provider('anthropic', {'model': 'claude-2'})
                            break
                    elif provider_type == 'local':
                        # Intentar usar modelo local
                        self.provider = create_ai_provider('local', {'model': 'llama2'})
                        break
                    elif provider_type == 'default':
                        # Usar modo simulado
                        break
                        
            except Exception as e:
                logging.warning(f"Fallo al inicializar proveedor de IA: {e}")
                self.provider = None
        
        # Debug
        print(f"🚀 [DEBUG] Sistema de IA inicializado")
        if self.provider:
            print(f"🧠 [DEBUG] Usando proveedor de IA: {type(self.provider).__name__}")
        else:
            print(f"⚠️ [DEBUG] Usando modo simulado")

    def send_task(self, prompt: str) -> str:
        """Envía una tarea al sistema de IA y devuelve la respuesta."""
        print(f"📡 Enviando solicitud al sistema de IA")
        
        try:
            # Si tenemos un proveedor de IA real, usarlo
            if self.provider:
                # Construir mensajes con contexto del agente
                messages = [
                    {
                        "role": "system",
                        "content": f"Eres {self.config.get('agent', {}).get('name', 'YrYs-Agent')}, un asistente de seguridad autónomo. "
                                   f"Tu misión es: {self.config.get('agent', {}).get('mission', 'Asistir en tareas de pentesting')}"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
                
                # Enviar solicitud al proveedor de IA
                response_text = self.provider.send_message(messages)
                print("✅ Respuesta del sistema de IA recibida")
                return response_text
            else:
                # Usar implementación simulada mejorada
                return self._simulate_response(prompt)
                
        except Exception as e:
            print(f"❌ ERROR en el sistema de IA: {e}")
            print("------------------------------------------------")
            
            # FALLBACK - Generar respuesta razonable según PRINCIPIOS KALIGHOST
            return fallback_response(prompt)
    
    def _simulate_response(self, prompt: str) -> str:
        """Simula una respuesta de IA basada en el contenido del prompt"""
        # Extraer el objetivo del prompt
        lines = prompt.split('\n')
        goal_line = [line for line in lines if line.startswith('Objetivo Actual:')][0] if any(line.startswith('Objetivo Actual:') for line in lines) else ""
        goal = goal_line.replace('Objetivo Actual:', '').strip()
        
        # Analizar el objetivo para determinar qué herramienta usar
        tools_available = ['nmap', 'sqlmap', 'nikto']
        tools_to_use = [tool for tool in tools_available if tool in goal.lower()]
        
        # Generar un plan de ejecución basado en el objetivo
        if tools_to_use:
            plan_steps = []
            for i, tool in enumerate(tools_to_use, 1):
                if tool == 'nmap':
                    plan_steps.append(f"{i}. Usa la herramienta nmap para escanear puertos y servicios")
                elif tool == 'sqlmap':
                    plan_steps.append(f"{i}. Usa la herramienta sqlmap para detectar inyecciones SQL")
                elif tool == 'nikto':
                    plan_steps.append(f"{i}. Usa la herramienta nikto para escanear vulnerabilidades web")
                    
            response_text = f"✅ [KaliGhost IA] → \n🔍 OBJETIVO RECIBIDO: '{goal}'\n📋 PLAN DE EJECUCIÓN:\n" + "\n".join(plan_steps)
        else:
            # Respuesta genérica sin revelar detalles de implementación
            response_text = f"✅ [KaliGhost IA] → \n🔍 OBJETIVO RECIBIDO: '{goal}'\n🔄 PROCESANDO: Aplicando lógica avanzada YrYs-Agent.\n🎯 MODO FANTASMA: Operando en modo seguro y eficiente.\n🛠️ TOOLS: Preparado para ejecutar herramientas autorizadas."
        
        return response_text

class SkillManager:
    """Gestiona la creación, carga y ejecución de Skills dinámicas."""
    def __init__(self, skills_dir: str):
        # Detectar si estamos en Docker o entorno local
        if '/root' in skills_dir or 'docker' in os.environ.get('PATH', '').lower():
            # Entorno Docker: usar config original
            self.skills_dir = Path(skills_dir)
        else:
            # Entorno local: usar directorio del proyecto relativo
            self.skills_dir = Path(__file__).parent / "skills"
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        
        # Usar el nuevo sistema de skills si está disponible
        if SKILLS_AVAILABLE:
            from .skill_system import SkillManager as NewSkillManager
            self.skill_manager = NewSkillManager(str(self.skills_dir))
        else:
            self.skill_manager = None
            self.loaded_skills = {}

    def create_skill(self, name: str, description: str, code: str) -> bool:
        """Crea una nueva habilidad (skill) de forma dinámica."""
        if self.skill_manager:
            # Usar el nuevo sistema de skills
            return self.skill_manager.create_skill(name, description, code)
        else:
            # Fallback al sistema anterior
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
        # Permitir todos los argumentos por ahora, ya que esto es una demostración
        # En un entorno de producción, se deberían restringir los argumentos
        return True

class ACL:
    """Control de acceso a herramientas y red."""
    def __init__(self, config: Dict):
        self.config = config
        self.allowed_tools = {}
        
        # Adaptar la configuración al formato esperado por la ACL
        enabled_tools = config.get('enabled', {})
        for tool_name, enabled in enabled_tools.items():
            if enabled:
                # Crear una configuración básica para cada herramienta habilitada
                tool_config = {
                    'name': tool_name,
                    'args': []  # Permitir todos los argumentos por ahora
                }
                self.allowed_tools[tool_name] = Tool(tool_config)
        
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
        self.acl = ACL(self.config['tools'])
        
        # Inicializar extensión autónoma
        if AUTONOMY_EXTENSION_AVAILABLE:
            self.autonomous_extension = create_autonomous_extension(self.config)
            if self.autonomous_extension:
                self.autonomous_extension.enable()
                logging.info("Extensión autónoma habilitada")
            else:
                self.autonomous_extension = None
                logging.info("Extensión autónoma no disponible")
        else:
            self.autonomous_extension = None
            logging.info("Extensión autónoma no disponible")
        
        logging.info(f"Agente YrYs '{self.config['agent']['name']}' iniciado. Misión: {self.config['agent']['mission'].strip()}")

    def load_config(self, path: str):
        """Carga la configuración desde un archivo YAML."""
        with open(path, 'r') as f:
            self.config = yaml.safe_load(f)

    def setup_logging(self):
        """Configura el sistema de logging del agente."""
        # Detectar si estamos en Docker o entorno local
        log_file = self.config['logging'].get('file', 'logs/agent.log')
        if '/root/work' in log_file or 'docker' in os.environ.get('PATH', '').lower():
            # Entorno Docker: usar config original
            log_dir = Path(log_file).parent
        else:
            # Entorno local: usar directorio del proyecto relativo
            log_dir = Path(__file__).parent / "logs"
            
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
def scan_webserver(target: str) -> str:
    \"\"\"Escanea un servidor web con nikto.\"\"\"
    import subprocess
    result = subprocess.run(['nikto', '-h', target], capture_output=True, text=True)
    return result.stdout
                """
                self.skills.create_skill(name, description, code)

            elif "usa la herramienta" in step.lower() or "ejecuta" in step.lower():
                # Extraer el nombre de la herramienta y los argumentos del paso
                # Esto es una simplificación - en la práctica necesitaríamos un mejor parsing
                tools_in_step = []
                for tool_name in self.acl.allowed_tools.keys():
                    if tool_name.lower() in step.lower():
                        tools_in_step.append(tool_name)
                
                args_in_step = []
                # Buscar argumentos comunes en el paso
                import re
                # Buscar direcciones IP o dominios
                ip_domain_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                matches = re.findall(ip_domain_pattern, step)
                args_in_step.extend(matches)
                
                # Si no encontramos direcciones IP o dominios, usar "localhost" por defecto
                if not args_in_step:
                    args_in_step.append("localhost")
                
                for tool_name in tools_in_step:
                    # Para demostración, usaremos argumentos básicos
                    args = []
                    if args_in_step:
                        # Para herramientas de escaneo, añadimos el argumento adecuado
                        if tool_name == 'nmap':
                            # Para nmap, usamos directamente el target sin el flag -h
                            # Añadimos opción de escaneo rápido para pruebas
                            args = ['-F', args_in_step[0]]
                        elif tool_name in ['nikto']:
                            args = ['-h'] + args_in_step[:1]  # Solo el primer target
                        elif tool_name == 'sqlmap':
                            args = ['-u'] + args_in_step[:1]
                        else:
                            args = args_in_step[:1]
                    
                    if self.acl.can_use_tool(tool_name, args):
                        try:
                            logging.info(f"Ejecutando {tool_name} con args: {args}")
                            # Comando real para ejecutar la herramienta
                            cmd = [tool_name] + args
                            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                            if result.returncode == 0:
                                logging.info(f"Resultado de {tool_name}: {result.stdout}")
                                # Imprimir también en consola para que sea visible
                                print(f"[RESULTADO] {tool_name} ejecutado correctamente:")
                                print(result.stdout)
                            else:
                                logging.error(f"Error en {tool_name}: {result.stderr}")
                                print(f"[ERROR] {tool_name} falló:")
                                print(result.stderr)
                        except subprocess.TimeoutExpired:
                            logging.error(f"Timeout al ejecutar {tool_name}")
                            print(f"[ERROR] {tool_name} excedió el tiempo límite")
                        except Exception as e:
                            logging.error(f"Error al ejecutar {tool_name}: {e}")
                            print(f"[ERROR] Falló la ejecución de {tool_name}: {e}")
                    else:
                        logging.error(f"Acción bloqueada por ACL: {tool_name} {args}")
                        print(f"[BLOQUEADO] Acceso denegado a {tool_name} con args: {args}")

    def start(self, user_goal: str):
        """Punto de entrada para el agente."""
        plan = self.think(user_goal)
        print(f"[DEBUG] Plan generado:\n{plan}")
        self.execute_plan(plan)
        
    def interactive_mode(self):
        """Modo interactivo mejorado con entrada segura"""
        print("🚀 Iniciando modo interactivo de YrYs-Agent...")
        print("💡 Escriba 'salir' o 'exit' para terminar")
        print("-" * 50)
        
        text_manager = ImprovedTextInputManager()
        
        while True:
            try:
                # Usar el sistema mejorado de entrada
                user_input = text_manager.get_safe_input("🗣️  YrYs> ")
                
                if user_input.lower() in ['salir', 'exit', 'quit']:
                    print("👋 Cerrando modo interactivo...")
                    break
                    
                if user_input.strip():
                    # Procesar entrada
                    print(f"📥 Procesando: '{user_input}'")
                    plan = self.think(user_input)
                    print(f"[RESPUESTA] {plan}")
                    
            except KeyboardInterrupt:
                print("\n👋 Interrupción por teclado - Saliendo...")
                break
            except Exception as e:
                print(f"❌ Error en modo interactivo: {e}")
                continue

if __name__ == "__main__":
    # Verificamos que se haya pasado un objetivo
    if len(sys.argv) < 2:
        print("Uso: yrays.py <objetivo_del_usuario> o yrays.py modo_interactivo")
        sys.exit(1)

    # Ruta al archivo de configuración (relativa al directorio del script)
    config_path = os.path.join(os.path.dirname(__file__), "config", "config.yaml")

    # Lanzar el agente
    agent = Agent(config_path)
    
    # Verificar si se quiere modo interactivo
    if sys.argv[1] == "modo_interactivo":
        agent.interactive_mode()
    else:
        agent.start(sys.argv[1])
