#!/usr/bin/env python3
"""
Script de prueba para el sistema de skills de YrYs-Agent
"""

import sys
import os
from pathlib import Path

# Añadir el directorio del agente al path
sys.path.insert(0, str(Path(__file__).parent / "yrays-agent"))

def test_skill_system():
    """Prueba el sistema de skills"""
    try:
        # Importar clases necesarias
        from yrays import Agent
        import yaml
        
        # Crear un agente de prueba
        config_path = Path(__file__).parent / "yrays-agent" / "config" / "config.yaml"
        agent = Agent(str(config_path))
        
        print("✅ Agente creado correctamente")
        print(f"📁 Directorio de skills: {agent.skills.skills_dir}")
        
        # Crear una skill de prueba
        skill_name = "test_scan"
        skill_description = "Skill de prueba para escaneo"
        skill_code = '''
def scan_host(host="localhost"):
    """Escanea un host específico"""
    return f"Escaneando host: {host}"

def list_ports():
    """Lista los puertos comunes"""
    common_ports = [22, 80, 443, 3306, 5432]
    return f"Puertos comunes: {common_ports}"
'''
        
        # Crear la skill
        result = agent.skills.create_skill(skill_name, skill_description, skill_code)
        if result:
            print("✅ Skill creada correctamente")
        else:
            print("❌ Fallo al crear la skill")
            return False
        
        # Listar skills
        if hasattr(agent.skills, 'skill_manager') and agent.skills.skill_manager:
            skills_info = agent.skills.skill_manager.list_skills()
            print(f"📚 Skills disponibles: {len(skills_info)}")
            for skill in skills_info:
                print(f"  • {skill['name']}: {skill['description']} ({skill['status']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Probando sistema de skills de YrYs-Agent...")
    success = test_skill_system()
    if success:
        print("\n🎉 Todas las pruebas pasaron correctamente")
        sys.exit(0)
    else:
        print("\n💥 Algunas pruebas fallaron")
        sys.exit(1)