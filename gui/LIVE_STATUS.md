# 🐉 KaliGhost Pro v3.0 - EJECUCIÓN EN VIVO

## ✅ SERVICIOS ACTIVOS

### Backend WebSocket
- **Status**: 🟢 RUNNING
- **Puerto**: 5001
- **URL**: http://localhost:5001
- **Health**: http://localhost:5001/health
- **PID**: Ver `list_background_jobs`

### Frontend React
- **Status**: 🟢 RUNNING  
- **Puerto**: 5173
- **URL**: http://localhost:5173
- **Build**: Vite v5.4.21

---

## 🎮 CÓMO USAR

### 1. Abrir GUI en Navegador
```
http://localhost:5173
```

### 2. Interfaz
```
┌─────────────────────────────────────────────────────────┐
│ Header: Logo + Target Input + Phase Selector + Buttons  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Dragon 3D Canvas (Izquierda 60%)                      │
│  - Dragón animado según estado                         │
│  - Aura refleja salud                                  │
│  - Rotación automática                                 │
│                                                         │
│  Execution Monitor (Derecha 40%)                       │
│  - Métricas (CPU, Memory, Disk)                        │
│  - Console con logs                                    │
│  - Threads activos                                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 3. Operación Básica
1. Ingresa target (ej: `192.168.1.0/24`)
2. Selecciona fase (`Reconnaissance`, `Scanning`, etc)
3. Clickea `START`
4. Observa dragón animarse + logs en tiempo real
5. Clickea `PAUSE`, `STOP`, o `👻` (Ghost Mode)

---

## 🔌 Eventos Real-time

### Socket.io Activo
- Métricas: Cada 500ms
- Logs: En tiempo real
- Estado: Sincronizado

### Test de Conectividad
```bash
curl http://localhost:5001/status | jq .
```

---

## 📊 Stack Ejecutándose

```
Frontend: React 18 + Three.js + Socket.io-client
Backend:  FastAPI + Socket.io + Uvicorn + psutil
```

---

## 🐉 Características Disponibles

✅ Dragón 3D vivo (6 estados visuales)
✅ Control total del agente (0-100% scope)
✅ Métricas en tiempo real (CPU, Memory, Disk)
✅ Logs coloreados en consola
✅ Threads tracking automático
✅ Ghost Mode (cleanup + shutdown)
✅ Sin restricciones ni censura

---

## 📁 Logs

```bash
# Backend logs
/Users/mrhardcore/KaliGhost/logs/websocket_backend.log

# Frontend console
Presiona F12 en navegador → Console tab
```

---

## 🛑 Detener Servicios

```bash
# Ctrl+C en cualquier terminal
# O:
kill $(lsof -t -i :5001)  # Backend
kill $(lsof -t -i :5173)  # Frontend
```

---

## 🚀 Estado Final

```
🟢 Backend:  RUNNING en puerto 5001
🟢 Frontend: RUNNING en puerto 5173
🟢 WebSocket: Bidireccional activo
🟢 Dragón 3D: Sincronizado en tiempo real
🟢 Logs: En vivo y coloreados
🟢 Sistema: OPERATIVO Y FUNCIONAL

⚡ LISTA PARA OPERACIONES 🐉
```

---

**Creado**: 2026-05-19  
**Versión**: 3.0.0  
**Estado**: LIVE & OPERATIONAL
