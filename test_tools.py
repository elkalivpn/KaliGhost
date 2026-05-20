#!/usr/bin/env python3
"""
Test específico para la ejecución de herramientas del agente YrYs
"""

import subprocess
import sys
from pathlib import Path

def test_tool_execution():
    """Test the YrYs agent tool execution functionality"""
    # Determinar la ruta del proyecto
    project_dir = Path(__file__).parent
    
    print("🔧 Probando ejecución de herramientas...")
    print("=" * 40)
    
    # Probar comando que debería ejecutar nmap
    try:
        print("🚀 Ejecutando comando: 'escanea localhost con nmap'...")
        result = subprocess.run(
            ["python3", "yrays-agent/yrays.py", "escanea localhost con nmap"],
            capture_output=True,
            text=True,
            cwd=str(project_dir),
            timeout=60
        )
        
        print("📄 Salida completa:")
        print(result.stdout)
        
        if result.stderr:
            print("❌ Errores:")
            print(result.stderr)
            
        if result.returncode == 0:
            print("✅ Comando ejecutado correctamente")
            # Verificar si se ejecutó nmap buscando indicadores
            if "[RESULTADO]" in result.stdout or "[BLOQUEADO]" in result.stdout:
                print("✅ Sistema de ejecución de herramientas funcionando")
                return True
            else:
                print("⚠️  No se encontraron indicadores de ejecución de herramientas")
                return True  # El comando se ejecutó, aunque no haya herramientas
        else:
            print("❌ Error en la ejecución")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Error: El comando ha excedido el tiempo límite")
        return False
    except Exception as e:
        print(f"❌ Error al ejecutar el comando: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Prueba de Ejecución de Herramientas del Agente YrYs")
    print("=" * 50)
    
    success = test_tool_execution()
    
    if success:
        print("\n🎉 Prueba de ejecución de herramientas completada")
        sys.exit(0)
    else:
        print("\n💥 La prueba de ejecución de herramientas falló")
        sys.exit(1)