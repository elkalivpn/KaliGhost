# KaliGhost Pro - Docker Architecture

Arquitectura Docker completa, production-ready y multi-arquitectura (ARM64/AMD64).

## 🏗️ Estructura Creada

```
gui/
├── backend/
│   ├── Dockerfile (dev + production stages)
│   ├── .dockerignore
│   ├── websocket_backend.py
│   └── requirements_backend.txt
├── frontend/
│   ├── Dockerfile (dev + production stages)
│   ├── .dockerignore
│   ├── nginx.conf (reverse proxy)
│   ├── package.json
│   ├── vite.config.js
│   └── src/
├── docker-compose.yml (desarrollo)
├── docker-compose.prod.yml (override para producción)
├── .env.example (variables de entorno)
├── build-multiarch.sh (Buildx multi-arch)
├── dev-setup.sh (setup inicial)
└── README_DOCKER.md
```

## 🚀 Inicio Rápido (Desarrollo)

### 1. Setup Inicial
```bash
cd /Users/mrhardcore/KaliGhost/gui
cp .env.example .env
./dev-setup.sh
```

Esto:
- Crea `.env` desde `.env.example`
- Construye imágenes Docker
- Inicia todos los servicios
- Espera healthchecks

### 2. Acceder a la Aplicación
```
Frontend:  http://localhost:5173
Backend:   http://localhost:8000
API Docs:  http://localhost:8000/docs
Database:  localhost:5432 (kaliuser/kalighost_dev_pass)
Redis:     localhost:6379
```

### 3. Ver Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f frontend
docker-compose logs -f backend
docker-compose logs -f db
```

### 4. Detener
```bash
docker-compose down
# Incluir volúmenes (purgar DB):
docker-compose down -v
```

## 🔧 Stages en Dockerfiles

### Backend (FastAPI)
- **development**: Uvicorn con `--reload` para hot-reload
- **production**: Usuario no-root, healthcheck, sin reload

### Frontend (React)
- **development**: Vite dev server con hot-reload en puerto 5173
- **builder**: Construye el bundle estático
- **production**: Nginx sirviendo static files + proxy a backend

## 📦 Multi-Arquitectura (Buildx)

### Build Local (Solo tu M2, ARM64)
```bash
docker build -t kali-backend:dev ./backend
docker build -t kali-frontend:dev ./frontend
```

### Build Multi-Arch (ARM64 + AMD64)
```bash
# Setup (una sola vez)
chmod +x build-multiarch.sh
./build-multiarch.sh

# Con push a Docker Hub
PUSH=true ./build-multiarch.sh
```

**Nota:** Para push, primero configura:
```bash
export REGISTRY=docker.io
export NAMESPACE=tu_usuario
docker login
```

## 🛡️ Seguridad

- ✅ Backend non-root user (production)
- ✅ Health checks en todos los servicios
- ✅ Volúmenes read-only donde sea posible
- ✅ Base images slim/alpine
- ✅ Secrets separados en producción
- ✅ .dockerignore para reducir contexto

## 📊 Variables de Entorno

Ver `.env.example`. Copiar a `.env` y personalizar:

```bash
# Database
DB_USER=kaliuser
DB_PASSWORD=kalighost_dev_pass
DB_NAME=kalidb

# Redis
REDIS_URL=redis://redis:6379/0

# Backend
ENVIRONMENT=development
LOG_LEVEL=DEBUG

# Frontend
VITE_BACKEND_URL=http://localhost:8000
```

## 🌐 Producción

### Deploy en VPS/Cloud
```bash
# En el servidor:
git clone <repo>
cd gui
cp .env.example .env
# Editar .env con valores reales
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Con SSL (Let's Encrypt)
```bash
# Crear certificados
certbot certonly --standalone -d tu-dominio.com

# Actualizar nginx.conf para SSL (ver ejemplo comentado)
# Remontar en compose
```

### Reverse Proxy Nginx (Producción)
```yaml
# docker-compose.prod.yml
proxy:
  image: nginx:alpine
  ports:
    - "80:80"
    - "443:443"
  volumes:
    - ./frontend/nginx.conf:/etc/nginx/conf.d/default.conf:ro
    - /etc/letsencrypt:/etc/letsencrypt:ro
```

## 📈 Escalamiento

Para múltiples instancias del backend:
```bash
docker-compose up -d --scale backend=3
```

Para load balancing, agregar HAProxy o usar Docker Swarm.

## 🔍 Debugging

### Logs
```bash
docker-compose logs -f backend
docker-compose logs backend --tail 100
```

### Inspeccionar Container
```bash
docker-compose exec backend bash
docker-compose exec frontend sh
docker-compose exec db psql -U kaliuser -d kalidb
```

### Red/Networking
```bash
docker network ls
docker network inspect kali-network
docker-compose exec backend ping redis
```

## 🗑️ Limpieza

```bash
# Detener y eliminar contenedores
docker-compose down

# Eliminar volúmenes
docker-compose down -v

# Limpiar imágenes no usadas
docker image prune -a

# Limpiar todo (⚠️)
docker system prune -a --volumes
```

## 📝 Notas

- Frontend dev server corre en `5173` con hot-reload automático
- Backend dev server corre en `8000` con `--reload` automático
- Cambios en archivos Python/JSX se reflejan sin reiniciar
- Base images: `python:3.11-slim`, `node:20-alpine`, `nginx:alpine`
- DB persist en volumen `pgdata` (entre restarts)
- Logs enviados a archivos JSON (rotación automática 10MB)
