#!/usr/bin/env python3
"""
Launcher de herramientas para KaliGhost
Este script permite ejecutar herramientas específicas desde el contexto MCP
"""

import sys
import subprocess
import argparse
import os

def run_tool(tool_name, args):
    """
    Ejecuta una herramienta específica
    """
    try:
        # Verificar si el comando existe
        cmd = [tool_name] + args
        
        # Ejecutar el comando y capturar la salida
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=60
        )
        
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
        
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'stdout': '',
            'stderr': 'Timeout al ejecutar la herramienta',
            'returncode': -1
        }
    except Exception as e:
        return {
            'success': False,
            'stdout': '',
            'stderr': str(e),
            'returncode': -1
        }

def main():
    parser = argparse.ArgumentParser(description='Launcher de herramientas para KaliGhost')
    parser.add_argument('--tool', required=True, help='Nombre de la herramienta a ejecutar')
    parser.add_argument('--args', nargs='*', help='Argumentos para la herramienta')
    
    args = parser.parse_args()
    
    # Si no se proporcionan argumentos, usamos una lista vacía
    if args.args is None:
        args.args = []
    
    # Ejecutar la herramienta
    result = run_tool(args.tool, args.args)
    
    # Imprimir resultados en formato JSON
    import json
    print(json.dumps(result))

if __name__ == '__main__':
    main()