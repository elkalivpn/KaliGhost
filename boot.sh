#!/bin/bash

# === KaliGhost para MacBook Air M2 (ARM64) ===
# Detección automática de entorno y arranque

echo "🚀 Iniciando KaliGhost en tu M2..."

# 1. Verificar arquitectura
ARCH=$(uname -m)
if [ "$ARCH" != "arm64" ]; then
    echo "❌ Error: Este script está diseñado para Apple Silicon (M1/M2/M3). Tu arquitectura: $ARCH"
    exit 1
fi

# 2. Verificar si estamos en un contenedor (Docker/LXC) o nativo
if [ -f /.dockerenv ]; then
    echo "🐳 Entorno detectado: Docker/Contenedor. Arrancando servicios internos..."
    # Comandos específicos para Docker (si los hubiera)
    exec bash
else
    echo "💻 Entorno detectado: Mac Nativo (M2)."
    
    # 3. Verificar si Docker está instalado
    if ! command -v docker &> /dev/null; then
        echo "⚠️ Docker no está instalado. Se requiere para el entorno aislado."
        echo "👉 Instala Docker Desktop para Mac (ARM64) desde: https://docs.docker.com/desktop/install/mac-install/"
        exit 1
    fi

    echo "✅ Docker listeo. Inicializando contenedor Kali Linux..."
    
    # 4. Ejecutar el contenedor Kali Linux optimizado para ARM
    # Usamos la imagen oficial de Kali (que tiene soporte ARM64)
    docker run -it --rm \
        --name kali-m2 \
        -v $PWD:/root/work \
        -e DEBIAN_FRONTEND=noninteractive \
        kalilinux/kali-rolling \
        /bin/bash
fi

echo "🛑 Sesión finalizada."