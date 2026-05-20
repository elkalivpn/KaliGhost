#!/bin/bash
# Dashboard visual para monitorear agentes autónomos de KaliGhost

SESSION="kalighost-dashboard"
PROJECT_DIR="${HOME}/KaliGhost"
LOG_DIR="${PROJECT_DIR}/yrays-agent/logs"

start_dashboard() {
    # Crear directorio de logs si no existe
    mkdir -p "$LOG_DIR"
    
    # Matar sesión anterior si existe
    tmux kill-session -t "$SESSION" 2>/dev/null || true
    
    # Crear nueva sesión con 4 paneles
    tmux new-session -d -s "$SESSION" -x 240 -y 50
    
    # Panel 0.0: Agente principal de KaliGhost
    tmux send-keys -t "$SESSION:0.0" "cd $PROJECT_DIR && echo '=== KALIGHOST AGENTE PRINCIPAL ===' && date" Enter
    tmux send-keys -t "$SESSION:0.0" "echo 'Directorio de trabajo: $PROJECT_DIR'" Enter
    tmux send-keys -t "$SESSION:0.0" "ls -la" Enter
    
    # Panel 0.1: Logs de actividad de agentes
    tmux split-window -t "$SESSION:0.0" -h
    tmux send-keys -t "$SESSION:0.1" "cd $LOG_DIR && echo '=== LOGS DE ACTIVIDAD DE AGENTES ===' && date" Enter
    tmux send-keys -t "$SESSION:0.1" "touch proactive_monitor.log orchestrator.log yrays.log" Enter
    tmux send-keys -t "$SESSION:0.1" "tail -f proactive_monitor.log orchestrator.log yrays.log 2>/dev/null | head -n 100 || echo 'Esperando logs...'" Enter
    
    # Panel 0.2: Recursos del sistema y estado de agentes
    tmux split-window -t "$SESSION:0.1" -v
    tmux send-keys -t "$SESSION:0.2" "cd $PROJECT_DIR && echo '=== RECURSOS DEL SISTEMA Y ESTADO DE AGENTES ===' && date" Enter
    tmux send-keys -t "$SESSION:0.2" "watch -n ${DASHBOARD_REFRESH_INTERVAL:-2} 'echo \"Estado de procesos:\"; ps aux | grep -E \"(python.*proactive|python.*orchestrator|python.*yrays)\" | grep -v grep || echo \"Sin procesos agente activos\"; echo \"---\"; echo \"Recursos del sistema:\"; vm_stat | head -3 2>/dev/null || sysctl hw.memsize hw.ncpu | awk \"{print \\$2}\"; uptime'" Enter
    
    # Panel 0.3: Progreso de workflows y tareas
    tmux split-window -t "$SESSION:0.0" -v
    tmux send-keys -t "$SESSION:0.3" "cd $PROJECT_DIR/orchestrator/workflows && echo '=== PROGRESO DE WORKFLOWS Y TAREAS ===' && date" Enter
    tmux send-keys -t "$SESSION:0.3" "mkdir -p workflows 2>/dev/null || true" Enter
    tmux send-keys -t "$SESSION:0.3" "watch -n ${RESOURCE_UPDATE_INTERVAL:-3} 'echo \"Workflows actuales:\"; ls -la *.json 2>/dev/null || echo \"Sin workflows definidos\"; echo \"---\"; echo \"Estado de directorios:\"; du -sh ../logs/* 2>/dev/null || echo \"Sin datos de logs\"'" Enter
    
    # Layout parejo
    tmux select-layout -t "$SESSION" tiled
    
    echo "Dashboard iniciado: tmux attach -t $SESSION"
    echo "Directorio de proyecto: $PROJECT_DIR"
    echo "Directorio de logs: $LOG_DIR"
}

show_status() {
    echo "=== Estado del Dashboard de KaliGhost ==="
    tmux list-sessions 2>/dev/null | grep -E "$SESSION" || echo "Dashboard no está corriendo"
    echo ""
    
    echo "Procesos de agentes:"
    ps aux | grep -E "(python.*proactive|python.*orchestrator|python.*yrays)" | grep -v grep || echo "Sin procesos agente detectados"
    echo ""
    
    echo "Logs recientes:"
    if [ -f "$LOG_DIR/proactive_monitor.log" ]; then
        echo "--- Logs de monitoreo proactivo ---"
        tail -3 "$LOG_DIR/proactive_monitor.log" 2>/dev/null || echo "Sin logs de monitoreo"
    fi
    
    if [ -f "$LOG_DIR/orchestrator.log" ]; then
        echo "--- Logs del orquestador ---"
        tail -3 "$LOG_DIR/orchestrator.log" 2>/dev/null || echo "Sin logs del orquestador"
    fi
}

stop_dashboard() {
    tmux kill-session -t "$SESSION" 2>/dev/null && echo "Dashboard detenido" || echo "Dashboard no estaba corriendo"
}

attach_dashboard() {
    if tmux has-session -t "$SESSION" 2>/dev/null; then
        tmux attach -t "$SESSION"
    else
        echo "Dashboard no está corriendo. Inicia con: $0 start"
        return 1
    fi
}

case "$1" in
    start) start_dashboard ;;
    status) show_status ;;
    stop) stop_dashboard ;;
    attach) attach_dashboard ;;
    *) echo "Usage: $0 {start|stop|status|attach}" ;;
esac