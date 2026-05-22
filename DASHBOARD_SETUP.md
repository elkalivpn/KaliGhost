# 🐉 KaliGhost - Dashboard Principal

El dashboard Next.js es ahora la aplicación principal de KaliGhost, sirviendo desde la raíz del proyecto.

## 📁 Estructura

```
kalighost/
├── src/                        # Next.js + React source (Principal)
│   ├── app/                   # Pages & layouts
│   ├── components/            # React components
│   ├── hooks/
│   │   ├── use-toast.ts
│   │   ├── use-mobile.ts
│   │   └── useWebSocketConnection.ts  # WebSocket real-time
│   ├── stores/                # Zustand (sin mocks)
│   ├── types/
│   └── lib/
├── public/                     # Static assets
├── prisma/                     # Database schema
├── gui/                        # Backend WebSocket Python
│   └── websocket_backend.py   # FastAPI + Socket.IO
├── core/                       # Agente KaliGhost
├── orchestrator/               # Orchestración
├── logs/                       # Logs de ambos servicios
├── Dockerfile                  # Multi-stage Next.js
├── Dockerfile.backend          # Python FastAPI
├── docker-compose.yml          # Orquestación
├── package.json               # Dependencias Next.js + Node
├── requirements.txt           # Dependencias Python
├── tsconfig.json
├── tailwind.config.ts
├── next.config.ts
└── setup-integration.sh        # Script de setup
```

## 🚀 Inicio Rápido

### Con Docker Compose (Recomendado)

```bash
cd /Users/mrhardcore/kalighost

# Build y ejecutar
docker-compose up -d

# Ver status
docker-compose ps

# Logs en vivo
docker-compose logs -f
```

**Acceso:**
- 🌐 **Dashboard Principal**: http://localhost:3000
- 🔌 **Backend WebSocket**: http://localhost:5001
- ✅ **Health Check**: http://localhost:5001/health

### Local (Desarrollo)

```bash
# Terminal 1: Backend
cd /Users/mrhardcore/kalighost
python -m gui.websocket_backend

# Terminal 2: Frontend (desde raíz)
cd /Users/mrhardcore/kalighost
bun install
bun run dev
```

### Script Automático

```bash
bash /Users/mrhardcore/kalighost/setup-integration.sh
docker-compose up -d
```

## ✨ Cambios Realizados

### ✅ Dashboard como Raíz
- Archivos de configuración Next.js en la raíz
- `src/` es la principal carpeta de código
- `package.json` es el principal (incluye `socket.io-client`)
- Build output en raíz

### ✅ Backend Mejorado
- Mocks completamente removidos
- Ejecución real de comandos del sistema
- Sincronización real-time con agente
- Integración real del estado

### ✅ Comunicación Real-time
- Hook `useWebSocketConnection` bidireccional
- Eventos de Socket.IO entre frontend/backend
- Sincronización automática de métricas
- Reconnection automática

### ✅ Docker Compose
- Frontend corre en puerto 3000 (principal)
- Backend corre en puerto 5001
- Ambos en misma red Docker
- Health checks configurados

## 🔧 Configuración

### Variables de Entorno (Frontend)

```bash
NEXT_PUBLIC_API_URL=http://localhost:5001
NEXT_PUBLIC_WEBSOCKET_URL=ws://localhost:5001/socket.io
NODE_ENV=production
```

### Variables de Entorno (Backend)

```bash
WEBSOCKET_HOST=0.0.0.0
WEBSOCKET_PORT=5001
PYTHONUNBUFFERED=1
LOG_LEVEL=INFO
```

## 📊 Eventos WebSocket

### Frontend → Backend
```
- start_operation: Iniciar operación
- pause_operation: Pausar
- resume_operation: Reanudar
- terminate_operation: Terminar
- execute_command: Ejecutar comando real
- update_config: Cambiar configuración
- request_status: Solicitar estado
```

### Backend → Frontend
```
- metrics_update: Métricas del sistema en vivo
- log_entry: Nuevas entradas de log
- agent_status_sync: Sync con agente real
- command_executed: Comando completado
- operation_*: Estado de operaciones
```

## 🛠️ Troubleshooting

### Error: Port 3000 en uso
```bash
lsof -ti:3000 | xargs kill -9
docker-compose up -d
```

### Error: Port 5001 en uso
```bash
lsof -ti:5001 | xargs kill -9
docker-compose restart backend
```

### Frontend no conecta con Backend
```bash
# Verificar red Docker
docker network ls
docker network inspect kalighost-network

# Verificar logs
docker-compose logs backend
docker-compose logs frontend
```

### WebSocket no conecta
```bash
# Verificar health del backend
curl http://localhost:5001/health

# Ver logs de conexión
docker-compose logs frontend | grep -i socket
```

## 📦 Dependencias Principales

### Frontend (package.json)
- `next@^16.1.1`
- `react@^19.0.0`
- `socket.io-client@^4.8.1`
- `zustand@^5.0.6`
- `@radix-ui/*` (componentes UI)
- `recharts@^2.15.4` (gráficos)
- `tailwindcss@^4`

### Backend (requirements.txt)
- `fastapi>=0.104.0`
- `uvicorn>=0.24.0`
- `python-socketio>=5.10.0`
- `psutil>=5.9.0`
- `python-engineio>=4.8.0`

## 🔐 Notas de Seguridad

- CORS configurado para todos los orígenes (cambiar en producción)
- WebSocket sin autenticación (agregar JWT)
- Sin HTTPS (agregar SSL en producción)
- Todos los comandos se ejecutan con permisos del usuario (considerar sandbox)

## 📈 Próximos Pasos

1. Agregar autenticación JWT
2. Implementar base de datos para persistencia
3. Mejorar seguridad de ejecución de comandos
4. Agregar trazabilidad completa
5. Integración con más herramientas de pentesting

## 🎯 Características

- ✅ Dashboard completo sin mocks
- ✅ Real-time WebSocket communication
- ✅ Sincronización con agente real
- ✅ Docker multi-contenedor
- ✅ Health checks automáticos
- ✅ Logs centralizados
- ✅ Interfaz moderna con Tailwind + Shadcn
- ✅ Gráficos en tiempo real

## 📝 Verificación Final

```bash
# 1. Verificar estructura
ls -la /Users/mrhardcore/kalighost/src/
ls -la /Users/mrhardcore/kalighost/public/

# 2. Verificar configuración
cat /Users/mrhardcore/kalighost/package.json | grep socket.io-client
cat /Users/mrhardcore/kalighost/requirements.txt | grep -E "fastapi|socketio"

# 3. Iniciar
cd /Users/mrhardcore/kalighost
docker-compose up -d

# 4. Verificar
curl http://localhost:3000
curl http://localhost:5001/health
```

---

**Dashboard Principal** - Ahora KaliGhost se abre en http://localhost:3000 como aplicación frontend completa.
