#!/bin/bash
# Script de instalación de dependencias para YrYs-Agent

echo "🚀 Instalando dependencias para YrYs-Agent..."

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias básicas
pip install pyyaml boto3 requests

# Instalar dependencias opcionales para IA
echo "🧠 Instalando dependencias de IA (opcional)..."
pip install openai anthropic || echo "⚠️ Advertencia: No se pudieron instalar todas las dependencias de IA"

# Instalar dependencias para modelos locales
echo "💻 Instalando dependencias para modelos locales (opcional)..."
pip install ollama || echo "⚠️ Advertencia: No se pudieron instalar dependencias para modelos locales"

echo "✅ Instalación completada. Las dependencias opcionales pueden instalarse manualmente si se necesitan."

# Crear directorios necesarios
mkdir -p ./skills
mkdir -p ./logs
mkdir -p ./memory

echo "📁 Directorios creados: skills, logs, memory"