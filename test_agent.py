#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad del agente YrYs
"""

import subprocess
import sys
from pathlib import Path

def test_agent():
    """Test the YrYs agent functionality"""
    # Determinar la ruta del proyecto
    project_dir = Path(__file__).parent
    agent_path = project_dir / "yrays-agent" / "yrays.py"
    
    print(f"🔍 Verificando agente en: {agent_path}")
    
    if not agent_path.exists():
        print("❌ Error: No se encuentra el agente YrYs")
        return False
    
    # Probar comando básico
    try:
        print("🚀 Probando comando básico...")
        result = subprocess.run(
            ["python3", str(agent_path), "prueba de diagnóstico del sistema"],
            capture_output=True,
            text=True,
            cwd=str(project_dir),
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ Agente ejecutado correctamente")
            print("📄 Salida:")
            print(result.stdout)
            return True
        else:
            print("❌ Error en la ejecución del agente")
            print("📄 Error:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Error: El comando ha excedido el tiempo límite")
        return False
    except Exception as e:
        print(f"❌ Error al ejecutar el agente: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Prueba de Agente YrYs")
    print("=" * 30)
    
    success = test_agent()
    
    if success:
        print("\n🎉 Todas las pruebas pasaron correctamente")
        sys.exit(0)
    else:
        print("\n💥 Algunas pruebas fallaron")
        sys.exit(1)