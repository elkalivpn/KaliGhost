import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera } from '@react-three/drei';
import * as THREE from 'three';
import { io } from 'socket.io-client';
import './KaliGhostGUI.css';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5001';

import CyberDragon from './CyberDragon';

// ============================================================================
// DRAGON CANVAS - Wrapper para el dragón 3D
// ============================================================================

const DragonCanvas = ({ agentState }) => {
  return (
    <Canvas
      className="dragon-canvas"
      shadows
      gl={{ antialias: true, alpha: true }}
    >
      <color attach="background" args={['#0A0E27']} />
      <PerspectiveCamera makeDefault position={[0, 0, 4]} />
      <OrbitControls 
        enableRotate={true}
        enablePan={false}
        autoRotate={agentState !== 'executing'}
        autoRotateSpeed={2}
      />
      
      <ambientLight intensity={0.4} />
      <directionalLight 
        position={[5, 10, 7]} 
        intensity={0.8}
        castShadow
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
      />
      <pointLight position={[-5, -5, 5]} intensity={0.3} color={0xFF0080} />
      
      <CyberDragon state={agentState} health={85} />
      
      <gridHelper args={[20, 20]} position={[0, -2, 0]} />
    </Canvas>
  );
};

// ============================================================================
// EXECUTION MONITOR
// ============================================================================

const ExecutionMonitor = ({ logs, threadData, metrics, agentState, logsEndRef }) => {
  return (
    <div className="panel execution-monitor">
      <h2>⚡ Execution Engine</h2>
      
      <div className="metrics-bar">
        <div className="metric-item">
          <label>CPU</label>
          <div className="metric-bar">
            <div 
              className="metric-fill" 
              style={{ 
                width: `${metrics.cpu_percent}%`,
                backgroundColor: metrics.cpu_percent > 80 ? '#FF2D55' : '#00FF88'
              }} 
            />
          </div>
          <span className="metric-value">{metrics.cpu_percent.toFixed(1)}%</span>
        </div>
        <div className="metric-item">
          <label>Memory</label>
          <div className="metric-bar">
            <div 
              className="metric-fill" 
              style={{ 
                width: `${metrics.memory_percent}%`,
                backgroundColor: metrics.memory_percent > 80 ? '#FF2D55' : '#00FF88'
              }} 
            />
          </div>
          <span className="metric-value">{metrics.memory_percent.toFixed(1)}%</span>
        </div>
        <div className="metric-item">
          <label>Disk</label>
          <div className="metric-bar">
            <div className="metric-fill" style={{ width: `${metrics.disk_percent}%` }} />
          </div>
          <span className="metric-value">{metrics.disk_percent.toFixed(1)}%</span>
        </div>
      </div>
      
      <div className="console">
        {logs.map((log, i) => (
          <div key={i} className={`log-line log-${log.level}`}>
            <span className="timestamp">[{log.timestamp}]</span>
            <span className="message">{log.message}</span>
          </div>
        ))}
        <div ref={logsEndRef} />
      </div>
      
      <div className="threads">
        <h3>Active Threads ({threadData.length})</h3>
        {threadData.length === 0 ? (
          <div className="empty-state">No active threads</div>
        ) : (
          threadData.map((thread) => (
            <div key={thread.thread_id} className="thread-item">
              <span className="thread-name">[T{thread.thread_id}] {thread.name}</span>
              <div className="progress-bar">
                <div 
                  className="progress-fill" 
                  style={{ width: `${thread.progress}%` }}
                />
              </div>
              <span className="thread-stats">CPU: {thread.cpu_percent.toFixed(1)}% | MEM: {thread.memory_mb.toFixed(0)}MB</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

// ============================================================================
// MAIN GUI
// ============================================================================

export default function KaliGhostGUI() {
  const [agentState, setAgentState] = useState('idle');
  const [logs, setLogs] = useState([
    { timestamp: '00:00:00', level: 'info', message: '🐉 KaliGhost Pro initialized' },
    { timestamp: '00:00:01', level: 'info', message: 'Dragon awakened - Ready for operations' }
  ]);
  const [threadData, setThreadData] = useState([]);
  const [metrics, setMetrics] = useState({
    cpu_percent: 0,
    memory_percent: 0,
    memory_used_mb: 0,
    memory_total_mb: 0,
    disk_percent: 0
  });
  const [isConnected, setIsConnected] = useState(false);
  const [operationTarget, setOperationTarget] = useState('');
  const [operationPhase, setOperationPhase] = useState('reconnaissance');
  
  const socketRef = useRef(null);
  const logsEndRef = useRef(null);
  
  useEffect(() => {
    socketRef.current = io(BACKEND_URL, {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: 5
    });
    
    socketRef.current.on('connect', () => {
      console.log('✅ Connected to backend');
      setIsConnected(true);
    });
    
    socketRef.current.on('disconnect', () => {
      console.log('❌ Disconnected from backend');
      setIsConnected(false);
    });
    
    socketRef.current.on('connection_established', (data) => {
      setLogs(prev => [...prev, {
        timestamp: new Date().toLocaleTimeString(),
        level: 'success',
        message: `GUI connected to backend (ID: ${data.client_id})`
      }]);
    });
    
    socketRef.current.on('log_entry', (data) => {
      if (data.log) {
        setLogs(prev => [...prev.slice(-99), data.log]);
      }
    });
    
    socketRef.current.on('broadcast', (data) => {
      if (data.type === 'log_entry' && data.log) {
        setLogs(prev => [...prev.slice(-99), data.log]);
      }
    });
    
    socketRef.current.on('metrics_update', (data) => {
      if (data.metrics) setMetrics(data.metrics);
      if (data.threads) setThreadData(data.threads);
      if (data.agent_state) setAgentState(data.agent_state);
    });
    
    socketRef.current.on('operation_started', () => {
      setAgentState('executing');
    });
    
    socketRef.current.on('operation_paused', () => {
      setAgentState('paused');
    });
    
    socketRef.current.on('operation_resumed', () => {
      setAgentState('executing');
    });
    
    socketRef.current.on('operation_terminated', () => {
      setAgentState('idle');
      setThreadData([]);
    });
    
    return () => socketRef.current?.disconnect();
  }, []);
  
  const handleStartOperation = useCallback(() => {
    if (!operationTarget) {
      alert('Please enter a target');
      return;
    }
    socketRef.current?.emit('start_operation', {
      target: operationTarget,
      phase: operationPhase
    });
  }, [operationTarget, operationPhase]);
  
  const handlePauseOperation = useCallback(() => {
    socketRef.current?.emit('pause_operation');
  }, []);
  
  const handleTerminateOperation = useCallback(() => {
    socketRef.current?.emit('terminate_operation');
  }, []);
  
  const handleGhostMode = useCallback(() => {
    if (window.confirm('⚠️ ACTIVATE GHOST MODE? This will cleanup all traces and shutdown.')) {
      socketRef.current?.emit('ghost_mode');
    }
  }, []);
  
  return (
    <div className="kalighost-gui">
      <header className="header-bar">
        <div className="logo">
          <h1>🐉 KaliGhost Pro</h1>
          <span className={`connection-status ${isConnected ? 'connected' : 'disconnected'}`}>
            {isConnected ? '● Connected' : '○ Disconnected'}
          </span>
        </div>
        <div className="header-center">
          <input 
            type="text"
            placeholder="Target (e.g., 192.168.1.0/24)"
            value={operationTarget}
            onChange={(e) => setOperationTarget(e.target.value)}
            className="target-input"
            disabled={agentState === 'executing'}
          />
          <select 
            value={operationPhase}
            onChange={(e) => setOperationPhase(e.target.value)}
            className="phase-select"
            disabled={agentState === 'executing'}
          >
            <option value="reconnaissance">Reconnaissance</option>
            <option value="scanning">Scanning</option>
            <option value="exploitation">Exploitation</option>
            <option value="post-exploitation">Post-Exploitation</option>
          </select>
        </div>
        <div className="header-controls">
          {agentState !== 'executing' ? (
            <button 
              className="btn-start"
              onClick={handleStartOperation}
              disabled={!isConnected || !operationTarget}
            >
              ▶ START
            </button>
          ) : (
            <>
              <button className="btn-secondary" onClick={handlePauseOperation}>
                ⏸ PAUSE
              </button>
              <button className="btn-secondary" onClick={handleTerminateOperation}>
                ⏹ STOP
              </button>
            </>
          )}
          <button className="btn-danger" onClick={handleGhostMode} title="Ghost Mode Cleanup">
            👻
          </button>
          <button className="btn-settings">⚙️</button>
        </div>
      </header>
      
      <div className="main-workspace">
        <div className="canvas-container">
          <DragonCanvas agentState={agentState} />
        </div>
      </div>
      
      <div className="console-area">
        <ExecutionMonitor 
          logs={logs} 
          threadData={threadData}
          metrics={metrics}
          agentState={agentState}
          logsEndRef={logsEndRef}
        />
      </div>
    </div>
  );
}
