# KaliGhost Pro - FastAPI Web Edition

Versión moderna de KaliGhost usando el patrón **FastAPI + Web UI** igual a LEO AI.

## 📁 Nuevos Archivos

- **`kalighost_api.py`** — Backend FastAPI con motor de pentesting
- **`kalighost_ui.html`** — UI Web cyberpunk (dark theme, terminal real-time)
- **`run_kalighost_web.sh`** — Launcher automático
- **`requirements_web.txt`** — Dependencias Python

## 🚀 Inicio Rápido

```bash
cd /Users/mrhardcore/KaliGhost

# Opción 1: Launcher automático
bash run_kalighost_web.sh

# Opción 2: Manual
python3 -m venv venv_kalighost
source venv_kalighost/bin/activate
pip install -r requirements_web.txt
python3 kalighost_api.py
```

Luego abre: **http://localhost:8000/kalighost_ui.html**

## 🎯 Características

✅ FastAPI backend (igual a LEO AI)
✅ Web UI con tema cyberpunk oscuro
✅ Terminal real-time con slash-commands (/scan, /tools, /status)
✅ REST API en http://localhost:8000
✅ Documentación automática en http://localhost:8000/docs
✅ Panel izquierdo: categorías de herramientas
✅ Panel central: terminal interactivo
✅ Panel derecho: dashboard de stats y estado del dragón
✅ 67 herramientas de pentesting integradas

## 📡 API Endpoints

- `GET /health` — Health check
- `GET /status` — Status completo
- `GET /logs` — Últimos logs
- `POST /scan?target=X&scan_type=basic|deep` — Ejecutar scan
- `GET /tools` — Listar herramientas
- `POST /execute-tool` — Ejecutar tool específica
- `POST /dragon-mode` — Cambiar modo dragón
- `GET /docs` — Swagger UI

## 💻 Comandos en Terminal

- `/scan example.com basic` — Quick scan
- `/scan example.com deep` — Deep reconnaissance
- `/tools` — Ver herramientas disponibles
- `/status` — Status sistema
- `/help` — Ayuda

## 🐉 Dragon Modes

- IDLE — En espera
- ACTIVE — Scan en progreso
- BUSY — Múltiples operaciones
- ALERT — Alerta de seguridad
- ERROR — Error en operación
- SUCCESS — Operación exitosa
- GHOST — Ghost mode (cleanup)

## 📊 Dashboard (Panel Derecho)

- Estado del dragón en tiempo real
- CPU, Memory, Disk usage
- Contador de operaciones
- Herramientas disponibles
- Última operación ejecutada

## 🔧 Mejoras sobre GUI PySide6

✅ No requiere OpenGL/PySide6 (más ligero)
✅ Accesible desde cualquier navegador
✅ Mejor rendimiento
✅ Mismo estilo TUI que LEO AI
✅ Terminal con logs en tiempo real
✅ Responsive y profesional
✅ Fácil de extender

## 📝 Próximos Pasos

1. Integrar herramientas reales de pentesting
2. Agregar WebSocket para actualizaciones en vivo
3. Agregar autenticación y roles
4. Integrar Ollama LLM para análisis
5. Exportar reportes PDF
6. Historial de operaciones persistente

---

**Nota**: Para compatibilidad con código existente de KaliGhost, ambas versiones (PySide6 y FastAPI) pueden coexistir. Esta es la nueva versión moderna recomendada.
