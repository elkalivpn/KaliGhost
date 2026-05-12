#!/bin/bash

# KaliGhost - Script de Inicio (boot.sh)

echo "🚀 Iniciando KaliGhost..."

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Instalándolo..."
    brew install docker
fi

# Verificar si WSL2 está activo
if [ "$WSL_DISTRO_NAME" ]; then
    echo "⚠️  Estás en WSL2. Asegúrate de tener Docker Desktop para Windows instalado."
    exit 1
fi

# Verificar si estamos en macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "✅ Detectado macOS (MacBook Air M2)."
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "✅ Detectado Linux. Continuando..."
else
    echo "❌ Sistema no soportado."
    exit 1
fi

# Crear directorio de trabajo
mkdir -p ~/KaliGhost/work

# Crear el archivo de configuración de Docker
cat > ~/KaliGhost/work/docker-compose.yml << 'DOCKEREOF'
version: '3.8'

services:
  kali:
    image: kalilinux/kali-rolling:latest
    container_name: kali-ghost
    privileged: true
    ports:
      - "22:22"
      - "80:80"
      - "443:443"
    networks:
      - ghost-network
    volumes:
      - ./work/scripts:/root/work
      - ./work/logs:/root/logs

networks:
  ghost-network:
    driver: bridge

DOCKEREOF

# Iniciar los contenedores
echo "🚀 Iniciando contenedores..."
docker-compose up -d

echo "✅ KaliGhost iniciado. Puedes acceder al contenedor con:"
echo "   docker exec -it kali-ghost bash"
