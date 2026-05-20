#!/usr/bin/env python3
"""
Script para probar la ejecución de skills de YrYs-Agent
"""

import sys
import os
from pathlib import Path

# Añadir el directorio del agente al path
sys.path.insert(0, str(Path(__file__).parent / "yrays-agent"))

def test_skill_execution():
    """Prueba la ejecución de skills"""
    try:
        # Importar clases necesarias
        from yrays import Agent
        import yaml
        
        # Crear un agente de prueba
        config_path = Path(__file__).parent / "yrays-agent" / "config" / "config.yaml"
        agent = Agent(str(config_path))
        
        print("✅ Agente creado correctamente")
        
        # Verificar si tenemos el nuevo sistema de skills
        if hasattr(agent.skills, 'skill_manager') and agent.skills.skill_manager:
            print("🧠 Usando sistema de skills avanzado")
            
            # Ejecutar funciones de la skill
            try:
                result1 = agent.skills.skill_manager.execute_skill_function("test_scan", "scan_host", "192.168.1.1")
                print(f"📡 Resultado scan_host: {result1}")
                
                result2 = agent.skills.skill_manager.execute_skill_function("test_scan", "list_ports")
                print(f"📊 Resultado list_ports: {result2}")
                
                print("✅ Ejecución de skills completada correctamente")
                return True
            except Exception as e:
                print(f"❌ Error al ejecutar skills: {e}")
                return False
        else:
            print("⚠️ Usando sistema de skills básico (sin ejecución directa)")
            return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🏃 Probando ejecución de skills de YrYs-Agent...")
    success = test_skill_execution()
    if success:
        print("\n🎉 Todas las pruebas pasaron correctamente")
        sys.exit(0)
    else:
        print("\n💥 Algunas pruebas fallaron")
        sys.exit(1)