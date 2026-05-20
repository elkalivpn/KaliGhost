#!/usr/bin/env python3
"""
Sistema de Gestión de Skills para YrYs-Agent
Permite crear, cargar, ejecutar y gestionar habilidades dinámicas de forma segura
"""

import os
import sys
import importlib.util
import logging
import traceback
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
import ast
import inspect

class SkillSecurityChecker:
    """Verifica la seguridad del código de las skills"""
    
    # Patrones peligrosos que no deben estar en el código
    DANGEROUS_PATTERNS = [
        r'os\.system',
        r'subprocess\.(call|Popen|run)',
        r'eval\(',
        r'exec\(',
        r'compile\(',
        r'input\(',
        r'open\([^)]*[,\'\"](?:w|a)',  # Escritura de archivos
        r'open\([^)]*\)[^)]*\.write',
        r'socket\.',
        r'requests\.(post|put|delete)',
        r'urllib\.(request|parse)',
        r'delete',
        r'remove',
        r'rmdir',
        r'mkdir',
        r'chmod',
        r'chown',
        r'import (os|subprocess|sys)',
    ]
    
    # Módulos peligrosos
    DANGEROUS_MODULES = [
        'os', 'subprocess', 'sys', 'socket', 'requests', 
        'urllib', 'shutil', 'pickle', 'marshal'
    ]
    
    @classmethod
    def check_code_security(cls, code: str) -> tuple[bool, List[str]]:
        """
        Verifica la seguridad del código de una skill
        Retorna (es_seguro, lista_de_advertencias)
        """
        warnings = []
        
        # Verificar patrones peligrosos
        import re
        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, code):
                warnings.append(f"Patrón peligroso detectado: {pattern}")
        
        # Verificar imports peligrosos
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name in cls.DANGEROUS_MODULES:
                            warnings.append(f"Módulo peligroso importado: {alias.name}")
                elif isinstance(node, ast.ImportFrom):
                    if node.module in cls.DANGEROUS_MODULES:
                        warnings.append(f"Módulo peligroso importado: {node.module}")
        except SyntaxError:
            warnings.append("Código con errores de sintaxis")
        
        # Verificar longitud del código
        if len(code) > 10000:  # 10KB límite
            warnings.append("Código demasiado largo")
        
        return len(warnings) == 0, warnings

class Skill:
    """Representa una habilidad ejecutable"""
    
    def __init__(self, name: str, description: str, module_path: Path):
        self.name = name
        self.description = description
        self.module_path = module_path
        self.loaded_module = None
        self.functions = {}
        self.created_at = None
        self.last_used = None
    
    def load(self) -> bool:
        """Carga el módulo de la skill"""
        try:
            spec = importlib.util.spec_from_file_location(self.name, self.module_path)
            if spec is None:
                logging.error(f"No se pudo crear la especificación para {self.name}")
                return False
                
            self.loaded_module = importlib.util.module_from_spec(spec)
            
            # Inyectar funciones auxiliares seguras
            self.loaded_module.safe_print = self._safe_print
            self.loaded_module.safe_log = self._safe_log
            
            spec.loader.exec_module(self.loaded_module)
            
            # Encontrar funciones ejecutables
            self.functions = {}
            for name, obj in inspect.getmembers(self.loaded_module):
                if inspect.isfunction(obj) and not name.startswith('_'):
                    self.functions[name] = obj
            
            logging.info(f"Skill '{self.name}' cargada con {len(self.functions)} funciones")
            return True
        except Exception as e:
            logging.error(f"Error al cargar skill '{self.name}': {e}")
            logging.error(traceback.format_exc())
            return False
    
    def execute_function(self, function_name: str, *args, **kwargs) -> Any:
        """Ejecuta una función específica de la skill"""
        if not self.loaded_module:
            if not self.load():
                raise Exception(f"No se pudo cargar la skill '{self.name}'")
        
        if function_name not in self.functions:
            raise Exception(f"Función '{function_name}' no encontrada en skill '{self.name}'")
        
        try:
            self.last_used = None  # Podríamos usar datetime.now()
            result = self.functions[function_name](*args, **kwargs)
            return result
        except Exception as e:
            logging.error(f"Error al ejecutar función '{function_name}' en skill '{self.name}': {e}")
            logging.error(traceback.format_exc())
            raise
    
    def _safe_print(self, *args, **kwargs):
        """Función segura para imprimir"""
        print("[SKILL]", *args, **kwargs)
    
    def _safe_log(self, level: str, message: str):
        """Función segura para loggear"""
        getattr(logging, level.lower(), logging.info)(f"[SKILL-{self.name}] {message}")
    
    def unload(self):
        """Descarga la skill de memoria"""
        if self.loaded_module:
            # Limpiar referencias
            self.loaded_module = None
            self.functions = {}

class SkillManager:
    """Gestiona la creación, carga y ejecución de Skills"""
    
    def __init__(self, skills_dir: str):
        self.skills_dir = Path(skills_dir)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        self.loaded_skills: Dict[str, Skill] = {}
        self.security_checker = SkillSecurityChecker()
        logging.info(f"Gestor de Skills inicializado en {self.skills_dir}")
    
    def create_skill(self, name: str, description: str, code: str) -> bool:
        """
        Crea una nueva habilidad de forma segura
        Retorna True si se creó correctamente, False en caso de error
        """
        try:
            # Validar nombre de skill
            valid_name = ''.join(c for c in name if c.isalnum() or c in '._-').rstrip()
            if not valid_name:
                logging.error("Nombre de skill inválido")
                return False
            
            # Verificar seguridad del código
            is_secure, warnings = self.security_checker.check_code_security(code)
            if not is_secure:
                logging.error(f"Skill '{name}' rechazada por fallos de seguridad: {warnings}")
                return False
            
            # Crear archivo de skill
            skill_path = self.skills_dir / f"{valid_name}.py"
            
            # Verificar si ya existe
            if skill_path.exists():
                logging.warning(f"La habilidad '{name}' ya existe. Sobrescribiendo.")
            
            # Escribir código de la skill
            with open(skill_path, 'w', encoding='utf-8') as f:
                f.write(f'# Skill: {name}\n')
                f.write(f'# Descripción: {description}\n')
                f.write('# Generado automáticamente por YrYs-Agent\n\n')
                f.write(code)
            
            # Establecer permisos seguros
            os.chmod(skill_path, 0o600)  # Solo lectura/escritura para el propietario
            
            # Crear/actualizar objeto Skill
            skill = Skill(valid_name, description, skill_path)
            self.loaded_skills[valid_name] = skill
            
            logging.info(f"Habilidad '{name}' creada y registrada")
            return True
            
        except Exception as e:
            logging.error(f"Error al crear skill '{name}': {e}")
            logging.error(traceback.format_exc())
            return False
    
    def load_skill(self, name: str) -> bool:
        """Carga una skill específica"""
        skill_path = self.skills_dir / f"{name}.py"
        
        if not skill_path.exists():
            logging.error(f"Skill '{name}' no encontrada en {skill_path}")
            return False
        
        if name in self.loaded_skills:
            # Recrear objeto Skill para recargar desde disco
            del self.loaded_skills[name]
        
        skill = Skill(name, "Cargada desde disco", skill_path)
        if skill.load():
            self.loaded_skills[name] = skill
            return True
        else:
            return False
    
    def get_skill(self, name: str) -> Optional[Skill]:
        """Obtiene una skill cargada"""
        return self.loaded_skills.get(name)
    
    def execute_skill_function(self, skill_name: str, function_name: str, *args, **kwargs) -> Any:
        """Ejecuta una función específica de una skill"""
        skill = self.get_skill(skill_name)
        if not skill:
            # Intentar cargar la skill
            if not self.load_skill(skill_name):
                raise Exception(f"Skill '{skill_name}' no disponible")
            skill = self.get_skill(skill_name)
        
        return skill.execute_function(function_name, *args, **kwargs)
    
    def list_skills(self) -> List[Dict[str, str]]:
        """Lista todas las skills disponibles"""
        skills_info = []
        
        # Skills cargadas en memoria
        for name, skill in self.loaded_skills.items():
            skills_info.append({
                'name': name,
                'description': skill.description,
                'status': 'loaded',
                'functions': list(skill.functions.keys())
            })
        
        # Skills en disco no cargadas aún
        for skill_file in self.skills_dir.glob("*.py"):
            name = skill_file.stem
            if name not in self.loaded_skills:
                skills_info.append({
                    'name': name,
                    'description': 'Disponible en disco',
                    'status': 'available',
                    'functions': []
                })
        
        return skills_info
    
    def unload_skill(self, name: str):
        """Descarga una skill de memoria"""
        if name in self.loaded_skills:
            self.loaded_skills[name].unload()
            del self.loaded_skills[name]
            logging.info(f"Skill '{name}' descargada")
    
    def delete_skill(self, name: str) -> bool:
        """Elimina una skill permanentemente"""
        try:
            # Descargar primero si está cargada
            self.unload_skill(name)
            
            # Eliminar archivo
            skill_path = self.skills_dir / f"{name}.py"
            if skill_path.exists():
                skill_path.unlink()
                logging.info(f"Skill '{name}' eliminada")
                return True
            else:
                logging.warning(f"Skill '{name}' no encontrada para eliminar")
                return False
        except Exception as e:
            logging.error(f"Error al eliminar skill '{name}': {e}")
            return False

# Función de ejemplo para crear una skill básica
def create_example_skill(skill_manager: SkillManager) -> bool:
    """Crea una skill de ejemplo para demostración"""
    example_code = '''
def saludar(nombre="mundo"):
    """Saluda a alguien"""
    return f"¡Hola, {nombre}! Soy una skill de ejemplo."

def calcular_suma(a, b):
    """Calcula la suma de dos números"""
    return a + b

def escanear_puertos_basicos(host):
    """Simula un escaneo de puertos básico"""
    puertos_comunes = [22, 80, 443, 3306, 5432]
    return f"Puertos a escanear en {host}: {puertos_comunes}"
'''
    
    return skill_manager.create_skill(
        "ejemplo_basico", 
        "Skill de ejemplo con funciones básicas", 
        example_code
    )

# Ejemplo de uso
if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Crear gestor de skills
    manager = SkillManager("./skills_test")
    
    # Crear skill de ejemplo
    if create_example_skill(manager):
        print("✅ Skill de ejemplo creada")
        
        # Listar skills
        skills = manager.list_skills()
        print(f"📚 Skills disponibles: {len(skills)}")
        for skill in skills:
            print(f"  • {skill['name']}: {skill['description']} ({skill['status']})")
        
        # Ejecutar funciones de ejemplo
        try:
            resultado1 = manager.execute_skill_function("ejemplo_basico", "saludar", "Agente")
            print(f"🗣️  Resultado: {resultado1}")
            
            resultado2 = manager.execute_skill_function("ejemplo_basico", "calcular_suma", 5, 3)
            print(f"🔢 Resultado: {resultado2}")
            
            resultado3 = manager.execute_skill_function("ejemplo_basico", "escanear_puertos_basicos", "localhost")
            print(f"📡 Resultado: {resultado3}")
        except Exception as e:
            print(f"❌ Error al ejecutar skill: {e}")
    else:
        print("❌ Fallo al crear skill de ejemplo")