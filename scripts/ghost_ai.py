#!/usr/bin/env python3
"""
Ghost AI - Asistente de Automatización para KaliGhost
Analiza escaneos Nmap y genera exploits/informes automáticamente.
"""

import sys
import subprocess
import json
import os

# CONFIGURACIÓN: Pon aquí tu API KEY (Ej: OpenAI, Groq, o una local)
# Si no tienes una, el script simulará la IA con reglas básicas para que funcione ya.
API_KEY = os.getenv("GHOST_AI_KEY", "") 
MODEL = "gpt-4o-mini"  # Cambia por tu modelo preferido

def analizar_nmap(xml_file):
    """Ejecuta Nmap y devuelve el resultado en formato XML"""
    print(f"🔍 Escaneando {xml_file}...")
    try:
        result = subprocess.run(['nmap', '-sV', '-oX', '-', xml_file], capture_output=True, text=True, check=True)
        return result.stdout
    except FileNotFoundError:
        print("❌ Error: 'nmap' no está instalado. Ejecuta 'apt update && apt install nmap' primero.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en el escaneo: {e}")
        return None

def generar_informe_ia(nmap_output):
    """Envía los datos a la IA y devuelve el análisis"""
    
    # SIMULACIÓN DE IA (Si no hay API KEY, usa lógica básica para demostración)
    if not API_KEY:
        print("\n⚠️  Modo SIMULACIÓN: No se detectó API Key. Generando informe básico...")
        if "80/tcp" in nmap_output or "443/tcp" in nmap_output:
            return """
            🚨 VULNERABILIDADES DETECTADAS (Simuladas):
            1. Puerto 80/443 abierto: Posible servidor web expuesto.
            2. Recomendación: Ejecutar 'nikto -h <IP>' para escaneo web detallado.
            3. Script sugerido:
               nikto -h <IP_TARGET> -o report_nikto.html
            """
        else:
            return """
            ✅ Estado: Sin puertos web comunes detectados.
            1. Recomendación: Verificar servicios en puertos altos.
            2. Script sugerido:
               nmap -sC -sV <IP_TARGET>
            """
    
    # Si tienes una API KEY, aquí iría la llamada real a la API (ej. OpenAI)
    # Este es un ejemplo de cómo se estructuraría:
    """
    import openai
    client = openai.OpenAI(api_key=API_KEY)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Eres un experto en ciberseguridad. Analiza el siguiente escaneo Nmap y sugiere 3 exploits y un script de automatización."},
            {"role": "user", "content": nmap_output}
        ]
    )
    return response.choices.message.content
    """
    return "Error: API Key no configurada o servicio no disponible."


def main():
    if len(sys.argv) < 2:
        print("👻 KaliGhost AI - Asistente de Automatización")
        print("Uso: python3 ghost_ai.py <IP_O_DOMINIO>")
        print("Ejemplo: python3 ghost_ai.py 192.168.1.1")
        sys.exit(1)

    target = sys.argv[1]
    
    # Paso 1: Escanear
    nmap_xml = analizar_nmap(target)
    if not nmap_xml:
        return

    # Paso 2: Analizar con IA
    informe = generar_informe_ia(nmap_xml)

    # Paso 3: Mostrar resultado
    print("\n" + "="*50)
    print("📊 INFORME DE INTELIGENCIA ARTIFICIAL")
    print("="*50)
    print(informe)
    print("="*50)
    print("💡 Tip: Copia los scripts sugeridos y guárdalos en /root/work/")

if __name__ == "__main__":
    main()