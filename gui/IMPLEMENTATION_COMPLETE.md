# 🐉 KaliGhost Pro v3.0 - Backend WebSocket Implementation

## ✅ Archivos Creados

### 1. **websocket_backend.py** (21KB)
**Propósito**: Servidor FastAPI + Socket.io principal

**Componentes**:
- `AgentStateManager`: Gestiona estado del agente, logs, threads
- `KaliGhostSocketServer`: Servidor Socket.io con manejo bidireccional
- Eventos: `start_operation`, `pause_operation`, `execute_command`, `ghost_mode`
- REST API: `/health`, `/status`, `/logs`, `/config`
- Loops de broadcast: Métricas cada 500ms, logs en tiempo real
- Integración con psutil para monitoreo del sistema

**Responsabilidades**:
✓ Comunicación real-time GUI ↔ Agente
✓ Sincronización de estado
✓ Broadcasting de métricas
✓ Gestión de configuración del agente
✓ Logging centralizado

---

### 2. **KaliGhostGUI.jsx** (15KB - REESCRITO)
**Propósito**: Componente React principal de GUI

**Cambios respecto a versión anterior**:
- ✅ WebSocket real-time integrado
- ✅ Header mejorado con input de target y selector de fase
- ✅ Button states (START/PAUSE/STOP)
- ✅ Conexión status indicator
- ✅ Dragón con 5+ estados visuales sincronizados
- ✅ Metrics bar en tiempo real (CPU, Memory, Disk)
- ✅ Thread tracking automático
- ✅ Auto-scroll de logs

**Eventos Socket.io manejados**:
- `connection_established`: Inicial
- `metrics_update`: Cada 500ms
- `log_entry`: En tiempo real
- `operation_started/paused/resumed/terminated`: Estado
- `broadcast`: Cualquier evento

---

### 3. **KaliGhostGUI.css** (15KB - EXTENDIDO)
**Adiciones**:
- `.header-center`: Inputs de target y fase
- `.target-input`, `.phase-select`: Estilos profesionales
- `.connection-status`: Indicador de conexión
- `.metrics-bar`: Grid de 3 columnas para CPU/Memory/Disk
- `.metric-item`, `.metric-fill`: Barras de progreso dinámicas
- `.btn-danger`: Botón Ghost Mode rojo peligroso
- `.empty-state`: Mensaje cuando no hay threads activos

---

### 4. **requirements_backend.txt** (230 bytes)
**Dependencias**:
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-socketio==5.10.0
aiofiles==23.2.1
psutil==5.9.8
pydantic==2.5.3
python-dotenv==1.0.0
```

---

### 5. **package.json** (1.2KB)
**Dependencias Frontend**:
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "@react-three/fiber": "^8.15.0",
    "@react-three/drei": "^9.88.0",
    "three": "^r156",
    "socket.io-client": "^4.7.0",
    "zustand": "^4.4.0"
  }
}
```

---

### 6. **vite.config.js** (540 bytes)
**Configuración Vite**:
- Puerto 5173
- CORS habilitado
- Code splitting optimizado
- Source maps deshabilitados en build

---

### 7. **index.html** (1KB)
**Entry point HTML**:
- Fonts Google (Inter, Courier Prime, JetBrains Mono)
- Favicon como emoji dragón
- Div root para React

---

### 8. **src/main.jsx** (270 bytes)
**Entry point React**:
- Monta KaliGhostGUI en #root
- Importa CSS global

---

### 9. **BACKEND_SETUP.md** (9.6KB)
**Documentación completa**:
- Arquitectura del sistema
- Instalación paso a paso
- Ejecución en 2 terminales
- Referencia de eventos Socket.io
- REST API endpoints
- Testing y troubleshooting
- Security en producción
- Performance tuning

---

### 10. **start.sh** (3.2KB)
**Script de inicio rápido**:
- Crea venv automáticamente
- Instala dependencias Python y Node
- Lanza Backend y Frontend en paralelo
- Cleanup automático al Ctrl+C
- Mensajes coloreados informativos

---

## 🏗️ Arquitectura Implementada

```
┌─────────────────────────────────────────────────────────┐
│               NAVEGADOR (http://localhost:5173)         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │      REACT + THREE.JS (KaliGhostGUI.jsx)        │   │
│  │                                                  │   │
│  │  ┌──────────────────────────────────────────┐   │   │
│  │  │  Header Bar                              │   │   │
│  │  │  - Target Input                          │   │   │
│  │  │  - Phase Selector                        │   │   │
│  │  │  - Operation Controls                    │   │   │
│  │  │  - Ghost Mode Button                     │   │   │
│  │  └──────────────────────────────────────────┘   │   │
│  │                                                  │   │
│  │  ┌──────────────────────────────────────────┐   │   │
│  │  │  Dragon Canvas (3D Rendering)            │   │   │
│  │  │  - Real-time state sync                  │   │   │
│  │  │  - Aura reflects agent health            │   │   │
│  │  │  - Animation based on operation state    │   │   │
│  │  └──────────────────────────────────────────┘   │   │
│  │                                                  │   │
│  │  ┌──────────────────────────────────────────┐   │   │
│  │  │  Execution Monitor                       │   │   │
│  │  │  - Metrics Bar (CPU/Memory/Disk)         │   │   │
│  │  │  - Live Console Logs                     │   │   │
│  │  │  - Active Threads List                   │   │   │
│  │  └──────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────┘   │
│                                                         │
└──────────────────────┬──────────────────────────────────┘
                       │
                 Socket.io (WS)
                       │
┌──────────────────────┴──────────────────────────────────┐
│     FASTAPI SERVER (http://localhost:5000)             │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │  WebSocket Handler (Socket.io)                   │  │
│  │  - Bidirectional communication                   │  │
│  │  - Event routing                                 │  │
│  │  - Broadcast to all clients                      │  │
│  └───────────────────────────────────────────────────┘  │
│                                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │  AgentStateManager                               │  │
│  │  - State machine (IDLE → EXECUTING → etc)        │  │
│  │  - Log queue                                     │  │
│  │  - Thread tracking                               │  │
│  │  - Metrics collection                            │  │
│  │  - Configuration storage                         │  │
│  └───────────────────────────────────────────────────┘  │
│                                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │  REST API Endpoints                              │  │
│  │  - GET /health                                   │  │
│  │  - GET /status                                   │  │
│  │  - GET /logs                                     │  │
│  │  - POST /config                                  │  │
│  └───────────────────────────────────────────────────┘  │
│                                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Broadcast Loops                                 │  │
│  │  - Metrics: every 500ms                          │  │
│  │  - Logs: on new entry                            │  │
│  └───────────────────────────────────────────────────┘  │
│                                                          │
└──────────────────────┬──────────────────────────────────┘
                       │
                    API / Hooks
                       │
        ┌──────────────┴──────────────┐
        │                             │
   ┌────────────────┐         ┌──────────────┐
   │  YrYs-Agent    │         │  System      │
   │  (Execution)   │         │  (psutil)    │
   └────────────────┘         └──────────────┘
```

---

## 🎯 Flujo de Operación

### Iniciando la GUI:

1. **Usuario ejecuta `./start.sh`**
   - Crea venv si no existe
   - Instala dependencias
   - Lanza Backend en Puerto 5000
   - Lanza Frontend en Puerto 5173

2. **Frontend conecta a Backend**
   - Socket.io establece conexión WS
   - Evento `connection_established` enviado
   - GUI recibe `client_id` y estado actual

3. **Backend inicia loops de broadcast**
   - Cada 500ms: Envía métricas (CPU, Memory, Disk)
   - En tiempo real: Envía nuevos logs
   - Estado actualizado automáticamente

### Ejecutando Operación:

1. **Usuario ingresa target y fase**
   ```
   Target: 192.168.1.0/24
   Phase: Reconnaissance
   ```

2. **Usuario clickea START**
   - GUI emite `start_operation` evento
   - Backend cambia state → INITIALIZING
   - Dragón comienza a animarse
   - Threads se crean automáticamente

3. **Backend simula operación**
   - Crea N threads con datos realistas
   - Envía logs de progreso
   - Actualiza métricas del sistema
   - Dragón refleja estado en tiempo real

4. **GUI recibe actualizaciones**
   - Logs aparecen en consola automáticamente
   - Threads activos muestran progreso
   - Métricas se actualizan
   - Dragón anima según estado

### Finalizando:

1. **Usuario clickea STOP**
   - Emite `terminate_operation`
   - Backend limpia threads
   - Estado vuelve a IDLE
   - Dragón regresa a reposo

2. **Ghost Mode (Opcional)**
   - Usuario clickea botón 👻
   - Confirma acción
   - Backend inicia secuencia cleanup
   - Sistema se apaga limpiamente

---

## 📊 Estados del Dragón

| Estado | Animación | Aura | Ojos | Caso de Uso |
|--------|-----------|------|------|------------|
| `idle` | Respiración | Verde pulsante | Parpadeando | Esperando |
| `analyzing` | Cabeza alzada | Verde brillante | Abiertos intensamente | Reconocimiento |
| `executing` | Alas expandidas | Cyan pulsante | Brillando | En ejecución |
| `warning` | Temblor | Amarillo errático | Dilatadas | Problema detectado |
| `error` | Caída | Rojo pulsante | Cerrados | Error crítico |
| `paused` | Congelado | Verde oscuro | Cerrados | Pausado |
| `ghost` | Desvanecimiento | Rojo oscuro fade | Desaparecen | Ghost Mode |

---

## 🔌 Flujo de Datos en Tiempo Real

```
┌─────────────────────────────────────────────────────────┐
│  BACKEND METRICS LOOP (every 500ms)                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. Update system metrics via psutil                   │
│     - CPU usage                                        │
│     - Memory usage                                     │
│     - Disk usage                                       │
│     - Network I/O                                      │
│                                                         │
│  2. Update thread data                                 │
│     - Progress                                         │
│     - CPU allocation                                   │
│     - Memory allocation                                │
│                                                         │
│  3. Compile metrics_update event                       │
│     {                                                  │
│       "type": "metrics_update",                        │
│       "metrics": {...},                                │
│       "threads": [...],                                │
│       "agent_state": "executing",                      │
│       "timestamp": "2026-05-15T14:30:00"              │
│     }                                                  │
│                                                         │
│  4. Broadcast to all connected clients                 │
│     await self.broadcast_to_all(metrics_update)       │
│                                                         │
└─────────────────────────────────────────────────────────┘
         │
         ├─────────────────────────────────────┐
         ▼                                       ▼
    ┌─────────────────┐              ┌─────────────────┐
    │ FRONTEND STATE  │              │  UI UPDATES     │
    │                 │              │                 │
    │ setMetrics(...) │─────────────▶│ Redraw          │
    │ setThreadData...│              │ Animation       │
    │ setAgentState...│              │ Transitions     │
    │                 │              │                 │
    └─────────────────┘              └─────────────────┘
         │
         ▼
    ┌─────────────────────────────────────┐
    │  THREE.JS DRAGON UPDATE             │
    │                                     │
    │  1. Check new agent state           │
    │  2. Switch animation if needed      │
    │  3. Update aura color based health  │
    │  4. Render 60 FPS                   │
    │                                     │
    └─────────────────────────────────────┘
```

---

## 🚀 Próximas Fases

### Fase 3: Pulir el Dragón 3D
- Geometría procedural mejorada
- Shaders personalizados avanzados
- Simulación de física (alas)
- Partículas de energía

### Fase 4: Integración Real del Agente YrYs
- Conectar con API del agente existente
- Ejecutar skills reales
- Capturar outputs verdaderos
- Reportes generados automáticamente

### Fase 5: Dashboard & Reportería
- Historial de operaciones
- Gráficos de resultados
- Export multi-formato (PDF, JSON, CSV)
- Temas alternativos

---

## 📦 Todos los Archivos Están Listos para Usar

```bash
# Inicio rápido:
./start.sh

# O manual:
# Terminal 1:
python websocket_backend.py

# Terminal 2:
npm run dev

# Luego abrir:
http://localhost:5173
```

¡Todo está conectado, sincronizado y listo para operar!

---

**Creado**: 2026-05-15  
**Versión**: 3.0.0  
**Stack**: React 18 + Three.js + FastAPI + Socket.io  
**Estado**: ✅ Completamente Funcional
