#!/bin/bash

set -e

action=${1:-build}

if [ "$action" = "build" ]; then
    echo "🔧 Construyendo imagen de KaliGhost..."
    docker compose build
elif [ "$action" = "start" ]; then
    echo "🚀 Iniciando KaliGhost..."
    if [ -f ".env" ]; then
        echo "Cargando variables de entorno"
        set -a; source .env; set +a
    fi
    docker compose up -d
elif [ "$action" = "stop" ]; then
    echo "🛑 Deteniendo KaliGhost..."
    docker compose down
elif [ "$action" = "logs" ]; then
    echo "📊 Mostrando logs..."
    docker compose logs -f
elif [ "$action" = "exec" ]; then
    echo "💻 Accediendo al contenedor..."
    docker compose exec kalighost bash
else
    echo "Uso: $0 {build|start|stop|logs|exec}"
    exit 1
fi