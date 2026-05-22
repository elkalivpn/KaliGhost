import { useEffect, useRef, useCallback } from 'react';
import { io, Socket } from 'socket.io-client';
import { useAppStore } from '@/stores/app-store';

export function useWebSocketConnection() {
  const socketRef = useRef<Socket | null>(null);
  const {
    setAgents,
    updateAgent,
    setRunningProcesses,
    setMemoryUsage,
    setNetworkIO,
  } = useAppStore();

  useEffect(() => {
    // Conectar al servidor WebSocket
    const wsUrl = process.env.NEXT_PUBLIC_WEBSOCKET_URL || 'ws://localhost:5001/socket.io';
    
    const socket = io(wsUrl, {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: 5,
      query: {
        clientType: 'gui',
      },
    });

    // Conexión establecida
    socket.on('connection_established', (data) => {
      console.log('✓ Connected to KaliGhost Backend', data);
    });

    // Broadcast - eventos generales del sistema
    socket.on('broadcast', (data) => {
      console.log('Broadcast:', data);
      
      if (data.type === 'operation_started') {
        console.log('Operation started:', data);
      } else if (data.type === 'operation_paused') {
        console.log('Operation paused');
      } else if (data.type === 'operation_resumed') {
        console.log('Operation resumed');
      } else if (data.type === 'operation_terminated') {
        console.log('Operation terminated');
      }
    });

    // Actualización de métricas del sistema
    socket.on('broadcast', (data) => {
      if (data.type === 'metrics_update') {
        const metrics = data.metrics;
        setMemoryUsage(Math.round(metrics.memory_percent));
        setNetworkIO(
          `${(metrics.network_sent_mb + metrics.network_recv_mb).toFixed(2)} MB`
        );
      }
    });

    // Sincronización con agente real
    socket.on('broadcast', (data) => {
      if (data.type === 'agent_status_sync') {
        const status = data.status;
        if (status.active_threads_count) {
          setRunningProcesses(status.active_threads_count);
        }
      }
    });

    // Logs en tiempo real
    socket.on('broadcast', (data) => {
      if (data.type === 'log_entry') {
        console.log(`[${data.log.level}] ${data.log.message}`);
      }
    });

    // Manejo de errores
    socket.on('error', (error) => {
      console.error('Socket error:', error);
    });

    socket.on('disconnect', () => {
      console.log('Disconnected from KaliGhost Backend');
    });

    socketRef.current = socket;

    return () => {
      socket.disconnect();
    };
  }, [setAgents, updateAgent, setRunningProcesses, setMemoryUsage, setNetworkIO]);

  // Función para emitir eventos al backend
  const emit = useCallback(
    (event: string, data?: any) => {
      if (socketRef.current?.connected) {
        socketRef.current.emit(event, data);
      } else {
        console.warn('Socket not connected');
      }
    },
    []
  );

  // Acciones disponibles
  const actions = {
    startOperation: (target: string, phase: string) =>
      emit('start_operation', { target, phase }),
    pauseOperation: () => emit('pause_operation'),
    resumeOperation: () => emit('resume_operation'),
    terminateOperation: () => emit('terminate_operation'),
    executeCommand: (command: string) => emit('execute_command', { command }),
    updateConfig: (config: any) => emit('update_config', config),
    requestStatus: () => emit('request_status'),
  };

  return { socket: socketRef.current, actions, isConnected: socketRef.current?.connected ?? false };
}
