#!/usr/bin/env python3
"""
Script para verificar la compatibilidad multiplataforma y portabilidad del agente
"""

import os
import sys
from pathlib import Path

def check_portability():
    """Verifica que el agente sea portable y no tenga rutas codificadas"""
    project_root = Path(__file__).parent
    print(f"📁 Raíz del proyecto: {project_root}")
    
    # Verificar estructura de directorios
    required_dirs = [
        "yrays-agent",
        "yrays-agent/config",
        "yrays-agent/skills",
        "yrays-agent/logs",
        "src",
        "src/agent",
        "src/gui"
    ]
    
    print("\n🔍 Verificando estructura de directorios...")
    for dir_path in required_dirs:
        full_path = project_root / dir_path
        if full_path.exists():
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path} (falta)")
    
    # Verificar archivos de configuración
    config_files = [
        "yrays-agent/config/config.yaml",
        "src/agent/main.py",
        "yrays-agent/yrays.py"
    ]
    
    print("\n🔍 Verificando archivos de configuración...")
    for config_file in config_files:
        full_path = project_root / config_file
        if full_path.exists():
            print(f"✅ {config_file}")
            
            # Verificar que no contenga rutas codificadas
            try:
                content = full_path.read_text(encoding='utf-8')
                if '/Users/' in content and '/Users/mrhardcore/' not in content:
                    print(f"⚠️  {config_file} contiene rutas de usuario codificadas")
                elif '/Users/mrhardcore/' in content:
                    print(f"❌ {config_file} contiene rutas codificadas específicas")
                else:
                    print(f"✅ {config_file} no contiene rutas codificadas")
            except Exception as e:
                print(f"❌ Error leyendo {config_file}: {e}")
        else:
            print(f"❌ {config_file} (no encontrado)")
    
    print("\n✅ Verificación de portabilidad completada")

if __name__ == "__main__":
    check_portability()