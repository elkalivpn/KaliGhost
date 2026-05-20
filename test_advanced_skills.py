#!/usr/bin/env python3
"""
Script para probar la ejecución de skills con el nuevo sistema de YrYs-Agent
"""

import sys
import os
from pathlib import Path

# Añadir el directorio del agente al path
sys.path.insert(0, str(Path(__file__).parent / "yrays-agent"))

def test_advanced_skill_system():
    """Prueba el sistema de skills avanzado"""
    try:
        # Importar el sistema de skills directamente
        sys.path.insert(0, str(Path(__file__).parent / "yrays-agent"))
        from skill_system import SkillManager
        import tempfile
        import shutil
        
        # Crear un directorio temporal para las skills
        with tempfile.TemporaryDirectory() as temp_dir:
            skills_dir = Path(temp_dir) / "skills"
            skills_dir.mkdir()
            
            # Crear un gestor de skills
            manager = SkillManager(str(skills_dir))
            print("✅ Gestor de skills creado correctamente")
            print(f"📁 Directorio de skills: {skills_dir}")
            
            # Crear una skill de prueba
            skill_name = "network_utils"
            skill_description = "Utilidades de red para escaneo y análisis"
            skill_code = '''
def scan_port(host, port):
    """Simula el escaneo de un puerto específico"""
    return f" Puerto {port} en {host}: {'ABIERTO' if port in [22, 80, 443] else 'CERRADO'}"

def list_common_ports():
    """Lista los puertos comunes"""
    return [22, 80, 443, 3306, 5432, 8080]

def format_results(results):
    """Formatea los resultados de escaneo"""
    formatted = "\\n".join(results)
    return f"Resultados del escaneo:\\n{formatted}"
'''
            
            # Crear la skill
            result = manager.create_skill(skill_name, skill_description, skill_code)
            if result:
                print("✅ Skill creada correctamente")
            else:
                print("❌ Fallo al crear la skill")
                return False
            
            # Listar skills
            skills_info = manager.list_skills()
            print(f"📚 Skills disponibles: {len(skills_info)}")
            for skill in skills_info:
                print(f"  • {skill['name']}: {skill['description']} ({skill['status']})")
                if skill['functions']:
                    print(f"    Funciones: {', '.join(skill['functions'])}")
            
            # Ejecutar funciones de la skill
            try:
                # Ejecutar list_common_ports
                ports = manager.execute_skill_function("network_utils", "list_common_ports")
                print(f"📊 Puertos comunes: {ports}")
                
                # Ejecutar scan_port para algunos puertos
                results = []
                for port in ports[:3]:  # Solo los primeros 3 para la prueba
                    result = manager.execute_skill_function("network_utils", "scan_port", "localhost", port)
                    results.append(result)
                    print(f"📡 {result}")
                
                # Ejecutar format_results
                formatted = manager.execute_skill_function("network_utils", "format_results", results)
                print(f"📄 Resultados formateados:")
                print(formatted)
                
                print("✅ Ejecución de skills completada correctamente")
                return True
            except Exception as e:
                print(f"❌ Error al ejecutar skills: {e}")
                import traceback
                traceback.print_exc()
                return False
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_security_features():
    """Prueba las características de seguridad del sistema de skills"""
    try:
        # Importar el sistema de skills directamente
        sys.path.insert(0, str(Path(__file__).parent / "yrays-agent"))
        from skill_system import SkillManager, SkillSecurityChecker
        import tempfile
        
        # Crear un directorio temporal para las skills
        with tempfile.TemporaryDirectory() as temp_dir:
            skills_dir = Path(temp_dir) / "skills"
            skills_dir.mkdir()
            
            # Crear un gestor de skills
            manager = SkillManager(str(skills_dir))
            
            # Probar código peligroso
            dangerous_code = '''
import os
import subprocess

def delete_system():
    os.system("rm -rf /")
    
def execute_arbitrary_command(cmd):
    subprocess.call(cmd, shell=True)
'''
            
            print("🛡️ Probando sistema de seguridad...")
            is_safe, warnings = SkillSecurityChecker.check_code_security(dangerous_code)
            if not is_safe:
                print("✅ Sistema de seguridad detectó código peligroso:")
                for warning in warnings:
                    print(f"  ⚠️ {warning}")
            else:
                print("❌ Sistema de seguridad falló en detectar código peligroso")
                return False
            
            # Intentar crear una skill peligrosa
            result = manager.create_skill("dangerous", "Skill peligrosa", dangerous_code)
            if not result:
                print("✅ Sistema de skills rechazó correctamente la skill peligrosa")
            else:
                print("❌ Sistema de skills permitió crear una skill peligrosa")
                return False
            
            # Probar código seguro
            safe_code = '''
def calculate_sum(a, b):
    """Calcula la suma de dos números"""
    return a + b

def greet_user(name):
    """Saluda a un usuario"""
    return f"Hola, {name}!"
'''
            
            result = manager.create_skill("safe_utils", "Utilidades seguras", safe_code)
            if result:
                print("✅ Sistema de skills aceptó correctamente la skill segura")
                
                # Ejecutar funciones seguras
                sum_result = manager.execute_skill_function("safe_utils", "calculate_sum", 5, 3)
                greet_result = manager.execute_skill_function("safe_utils", "greet_user", "Agente")
                
                print(f"🔢 Suma: {sum_result}")
                print(f"🙋 Saludo: {greet_result}")
            else:
                print("❌ Sistema de skills rechazó incorrectamente la skill segura")
                return False
            
            return True
            
    except Exception as e:
        print(f"❌ Error en la prueba de seguridad: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔬 Probando sistema de skills avanzado de YrYs-Agent...")
    
    print("\n=== Prueba de funcionalidad básica ===")
    success1 = test_advanced_skill_system()
    
    print("\n=== Prueba de seguridad ===")
    success2 = test_security_features()
    
    if success1 and success2:
        print("\n🎉 Todas las pruebas pasaron correctamente")
        sys.exit(0)
    else:
        print("\n💥 Algunas pruebas fallaron")
        sys.exit(1)