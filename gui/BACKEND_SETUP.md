# 🐉 KaliGhost Pro - Backend WebSocket Setup Guide

## 📋 Resumen

Este backend realiza la comunicación bidireccional en tiempo real entre:
- **Frontend GUI** (React + Three.js)
- **Agente YrYs** (Ejecución de pentesting)
- **Sistema** (Métricas, logs, estado)

## 🏗️ Arquitectura

```
┌─────────────────┐
│  GUI (React)    │
│   (5173)        │
└────────┬────────┘
         │
    Socket.io (WS)
         │
┌────────┴────────┐
│  Backend        │
│ (FastAPI)       │
│  (5000)         │
└────────┬────────┘
         │
    API + Events
         │
┌────────┴────────┐
│ YrYs-Agent      │
│ (Execution)     │
└─────────────────┘
```

## 📦 Requisitos

- Python 3.9+
- pip o poetry
- Sistema Unix/Linux recomendado (macOS, Kali Linux)

## 🚀 Instalación

### Paso 1: Instalar Dependencias Backend

```bash
# Ir al directorio GUI
cd /Users/mrhardcore/KaliGhost/gui

# Crear virtual environment (recomendado)
python3 -m venv venv_backend
source venv_backend/bin/activate  # En Windows: venv_backend\Scripts\activate

# Instalar dependencias
pip install -r requirements_backend.txt
```

### Paso 2: Instalar Dependencias Frontend

```bash
# En el mismo directorio gui/
npm install

# O con yarn/pnpm
yarn install
# pnpm install
```

## 🎯 Ejecución

### Terminal 1: Iniciar Backend WebSocket

```bash
cd /Users/mrhardcore/KaliGhost/gui

# Activar venv (si no está activado)
source venv_backend/bin/activate

# Ejecutar backend
python websocket_backend.py
```

Verás:
```
================================================================================
KaliGhost Pro - WebSocket Backend
================================================================================
INFO:     Started server process [12345]
INFO:     Uvicorn running on http://0.0.0.0:5000
```

### Terminal 2: Iniciar Frontend Dev Server

```bash
cd /Users/mrhardcore/KaliGhost/gui

# Ejecutar Vite dev server
npm run dev
```

Verás:
```
VITE v5.0.0  ready in 245 ms

➜  Local:   http://localhost:5173/
➜  press h to show help
```

### Terminal 3 (Opcional): Ver logs del backend

```bash
tail -f /Users/mrhardcore/KaliGhost/logs/websocket_backend.log
```

## 🌐 Acceso

Abre en tu navegador:
- **GUI**: http://localhost:5173
- **Backend Health**: http://localhost:5000/health
- **Backend Status**: http://localhost:5000/status

## 🎮 Eventos Socket.io

### Client → Server

#### `start_operation`
```javascript
socket.emit('start_operation', {
  target: '192.168.1.0/24',
  phase: 'reconnaissance'
});
```

#### `pause_operation`
```javascript
socket.emit('pause_operation');
```

#### `resume_operation`
```javascript
socket.emit('resume_operation');
```

#### `terminate_operation`
```javascript
socket.emit('terminate_operation');
```

#### `execute_command`
```javascript
socket.emit('execute_command', {
  command: 'nmap -p- <target>'
});
```

#### `update_config`
```javascript
socket.emit('update_config', {
  execution_scope: 90,
  behavior_mode: 'aggressive',
  max_threads: 10,
  timeout_seconds: 3600
});
```

#### `inject_custom_behavior`
```javascript
socket.emit('inject_custom_behavior', `
def custom_behavior(agent_state):
    if agent_state.target_found:
        agent.escalate_privilege()
    return agent_state
`);
```

#### `ghost_mode`
```javascript
socket.emit('ghost_mode');
```

### Server → Client (Broadcast)

#### `connection_established`
```json
{
  "client_id": "socket_id",
  "agent_state": "idle",
  "timestamp": "2026-05-15T14:30:00"
}
```

#### `metrics_update`
```json
{
  "type": "metrics_update",
  "metrics": {
    "cpu_percent": 45.2,
    "memory_percent": 62.1,
    "memory_used_mb": 5120,
    "memory_total_mb": 8192,
    "disk_percent": 55.3
  },
  "threads": [
    {
      "thread_id": 0,
      "name": "Network Reconnaissance",
      "progress": 45.0,
      "cpu_percent": 32.1,
      "memory_mb": 128
    }
  ],
  "agent_state": "executing"
}
```

#### `log_entry`
```json
{
  "type": "log_entry",
  "log": {
    "timestamp": "14:30:45",
    "level": "info",
    "message": "Operation started - Target: 192.168.1.0/24",
    "source": "agent"
  }
}
```

## 🔌 API REST Endpoints

### GET /health
Healthcheck del servidor

```bash
curl http://localhost:5000/health
```

Response:
```json
{
  "status": "ok",
  "agent_state": "idle",
  "timestamp": "2026-05-15T14:30:00"
}
```

### GET /status
Estado completo del agente

```bash
curl http://localhost:5000/status
```

Response:
```json
{
  "state": "idle",
  "health": 100,
  "operation_progress": 0.0,
  "operation_phase": "idle",
  "current_target": null,
  "active_threads_count": 0,
  "metrics": {...},
  "config": {...}
}
```

### GET /logs?count=50
Obtener últimos N logs

```bash
curl http://localhost:5000/logs?count=50
```

### POST /config
Actualizar configuración

```bash
curl -X POST http://localhost:5000/config \
  -H "Content-Type: application/json" \
  -d '{
    "execution_scope": 90,
    "behavior_mode": "aggressive",
    "max_threads": 10
  }'
```

## 📊 Structure de Datos

### AgentState (Enum)
```
- IDLE: Esperando operación
- INITIALIZING: Inicializando
- ANALYZING: Analizando objetivo
- EXECUTING: Ejecutando
- WARNING: Estado de alerta
- ERROR: Error crítico
- PAUSED: Pausado por usuario
- GHOST: Ghost Mode activo
- SHUTDOWN: Apagando
```

### AgentConfig (Dataclass)
```python
execution_scope: int = 90              # 0-100%
behavior_mode: str = "balanced"        # aggressive, balanced, conservative
max_threads: int = 10
timeout_seconds: int = 3600
max_memory_gb: int = 8
network_bandwidth_unlimited: bool = True
custom_python_code: str = ""
allowed_actions: List[str]
restricted_actions: List[str]
```

## 🧪 Testing

### Test 1: Conectividad

```bash
# Terminal 1: Backend
python websocket_backend.py

# Terminal 2: Simple client test
python3 << 'EOF'
import socketio
import asyncio

sio = socketio.AsyncClient()

@sio.event
async def connect():
    print("Connected!")
    
@sio.event
async def broadcast(data):
    print(f"Broadcast: {data}")

async def main():
    await sio.connect('http://localhost:5000')
    await sio.wait()

asyncio.run(main())
EOF
```

### Test 2: Start Operation

```python
# Test con logs en tiempo real
socket.emit('start_operation', {
    'target': '192.168.1.0/24',
    'phase': 'reconnaissance'
})

# Los logs deberían aparecer en tiempo real en la GUI
```

## 📝 Logs

### Ubicación
```
/Users/mrhardcore/KaliGhost/logs/websocket_backend.log
```

### Niveles
- DEBUG: Información detallada
- INFO: Eventos normales
- SUCCESS: Operación completada
- WARNING: Posible problema
- ERROR: Error ocurrido
- CRITICAL: Error crítico

## 🚨 Troubleshooting

### Error: "Port 5000 already in use"

```bash
# Encontrar proceso usando puerto 5000
lsof -i :5000

# Matar proceso
kill -9 <PID>

# O usar otro puerto
BACKEND_PORT=5001 python websocket_backend.py
```

### Error: "Can't connect to backend from GUI"

1. Verificar que backend está corriendo: `http://localhost:5000/health`
2. Verificar firewall no bloquea puerto 5000
3. Verificar CORS está habilitado (está habilitado por defecto)
4. Check `VITE_BACKEND_URL` environment variable

```bash
# Setear URL diferente si es necesario
export VITE_BACKEND_URL=http://192.168.1.100:5000
npm run dev
```

### Error: "Socket.io connection timeout"

- Aumentar timeout en cliente
- Verificar conexión de red
- Chequear logs backend

### Memory leak en logs

```python
# El código limita a últimos 99 logs automáticamente
# Si necesitas aumentar/reducir:
# En websocket_backend.py línea ~450
setLogs(prev => [...prev.slice(-99), data.log]);  # Cambiar 99 por otro valor
```

## 🔐 Seguridad

### En Producción

1. **CORS**: Restringir a dominio específico
   ```python
   CORS(
       origins=["https://tudominio.com"],
       credentials=True
   )
   ```

2. **Autenticación**: Agregar token JWT
   ```python
   @sio.event
   async def connect(sid, environ, auth):
       token = auth.get('token')
       # Verificar token
   ```

3. **Rate Limiting**: Limitar eventos por cliente
   ```python
   from slowapi import Limiter
   limiter = Limiter()
   ```

4. **HTTPS**: Usar WSS en lugar de WS
   ```python
   sio = AsyncServer(
       async_mode='asgi',
       engineio_logger=True,
       manage_handled_exc_in_middleware=True,
       # Requiere SSL
   )
   ```

## 📈 Performance Tuning

### Métricas Broadcast

Actualmente se envía cada 500ms. Ajustar en:

```python
# websocket_backend.py, línea ~520
await asyncio.sleep(0.5)  # Cambiar a 1.0 para menos frecuencia
```

### Limpieza de Logs

```python
# Guardar solo últimos N logs
setLogs(prev => [...prev.slice(-50), data.log]);  # Reducir de 99 a 50
```

### Conexiones Persistentes

```python
# Socket.io reconnection settings
socketRef.current = io(BACKEND_URL, {
  reconnectionDelay: 1000,
  reconnectionDelayMax: 5000,
  reconnectionAttempts: 5  # Cambiar si necesario
});
```

## 🎯 Próximos Pasos

1. Integración con Agente YrYs real (API hooks)
2. Persistencia de operaciones (MongoDB/PostgreSQL)
3. Autenticación y autorización
4. Dashboard de múltiples usuarios
5. Historial de operaciones
6. Exportación de reportes

## 📞 Support

Para problemas, revisar:
- Logs: `/Users/mrhardcore/KaliGhost/logs/websocket_backend.log`
- Console del navegador: F12 → Console
- Terminal backend: output directo

---

**Última actualización**: 2026-05-15  
**Versión**: 1.0.0
