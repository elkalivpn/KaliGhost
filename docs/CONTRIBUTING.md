# Contribuyendo a KaliGhost

¡Gracias por tu interés en contribuir! KaliGhost es un proyecto de código abierto y valoramos toda ayuda.

## 🎯 Cómo Contribuir

### 1. Reportar Bugs

Antes de crear un issue:

1. **Busca issues existentes** – Quizás ya fue reportado
2. **Revisa Troubleshooting** – `docs/TROUBLESHOOTING.md`
3. **Proporciona detalles**:

```markdown
**Descripción**
Descripción clara y concisa del bug.

**Pasos para reproducir**
1. Ir a '...'
2. Hacer clic en '...'
3. Ver error

**Comportamiento esperado**
Qué esperabas que sucediera.

**Capturas de pantalla**
Si aplica, añade screenshots.

**Entorno:**
- OS: [e.g. macOS 14.2, Ubuntu 22.04]
- Docker version: [e.g. Docker Desktop 4.21]
- Versión KaliGhost: [e.g. v1.0.0]
```

### 2. Sugerir Features

Las nuevas features se discuten en **GitHub Discussions** primero.

```markdown
**Propuesta: [Nombre conciso]**

**Problema**
Qué problema resuelve esta feature.

**Solución propuesta**
Descripción técnica de la implementación.

**Alternativas consideradas**
Otras approaches que descartaste.

**Impacto**
- Complexity: [bajo/medio/alto]
- Breaking changes: [sí/no]
- Monetización: [afecta pricing?]
```

### 3. Enviar Pull Requests

#### Flujo de trabajo estándar

```bash
# 1. Fork el repo
# 2. Clona tu fork
git clone https://github.com/TU_USUARIO/KaliGhost.git
cd KaliGhost

# 3. Crea branch para tu feature
git checkout -b feature/nombre-feature

# 4. Haz tus cambios
# ...

# 5. Commit con mensaje convencional
git add .
git commit -m "feat: añade integración con Shodan API"

# 6. Push a tu fork
git push origin feature/nombre-feature

# 7. Abre PR en GitHub
```

#### Convenciones de commit

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```
<tipo>[ámbito opcional]: <descripción>

[ cuerpo opcional ]

[pie de página opcional]
```

**Tipos:**
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Formato (sin cambio de código)
- `refactor`: Refactorización de código
- `perf`: Mejora de performance
- `test`: Añadir tests
- `chore`: Cambios en build/scripts

**Ejemplos:**
```
feat(agent): añade modo SLEEP para ahorro de recursos
fix(web): corrige enlace Gumroad en plan Enterprise
docs(readme): actualiza instrucciones de instalación
```

### 4. Code Review Process

1. **Un maintainer asignará reviewer** dentro de 48h
2. **Revisiones constructivas** – Espera feedback
3. **CI debe pasar** – GitHub Actions ejecuta tests automáticos
4. **Al menos 1 approve** antes de merge
5. **Squash & Merge** – Commits limpios en main

**Review guidelines:**
- ¿Es seguro? (no vulnerabilities)
- ¿Funciona en M2 y x64?
- ¿Mantiene AUTO mode sin breakage?
- ¿Documentación actualizada?
- ¿Tests incluidos?

---

## 📁 Estructura del Código

```
KaliGhost/
├── YrYs-Agent/           # Lógica del agente IA
│   ├── agent.py          # Clase principal Agent
│   ├── skills/           # Skills/plugins del agente
│   ├── config/           # Config loaders
│   └── utils/            # Helper functions
├── boot/                 # Docker initialization
├── web_monetizacion/     # Frontend landing page
│   ├── pages/            # HTML pages
│   ├── css/              # Styles
│   └── js/               # Client logic
├── scripts/              # Utilidades CLI
├── docs/                 # Documentación técnica
├── tests/                # Test suite (pendiente)
└── examples/             # Ejemplos de uso
```

**Regla de oro:** Cada módulo debe ser testable independientemente.

---

## 🔧 Setup de Desarrollo Local

### Prerrequisitos

```bash
# Python 3.11+
python3 --version  # >= 3.11

# Docker & Docker Compose
docker --version
docker compose version

# Git
git --version

# (Opcional) Poetry para gestión de dependencias
pip install poetry
```

### Instalar dependencias

```bash
cd ~/KaliGhost

# Backend (Agente YrYs)
cd YrYs-Agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend (Web)
cd ../web_monetizacion
# Solo HTML/CSS/JS puro – no build necesario

# Tests
cd tests
pip install pytest pytest-cov
```

### Ejecutar en modo desarrollo

```bash
# Terminal 1: Docker contenedor
./boot/boot.sh

# Terminal 2: Agente en vivo (hot-reload)
cd YrYs-Agent
python3 agent.py --dev --reload

# Terminal 3: Servidor web local (opcional)
cd web_monetizacion
python3 -m http.server 8080
# http://localhost:8080
```

### Ejecutar tests

```bash
cd ~/KaliGhost

# Tests unitarios
pytest tests/unit/

# Tests integración (requiere Docker)
pytest tests/integration/

# Con coverage
pytest --cov=YrYs-Agent --cov-report=html
```

---

## 🎨 Estilos de Código

### Python (YrYs-Agent)

- **Formatter:** Black (line length 100)
- **Linter:** Flake8 + mypy
- **Docstrings:** Google style

```bash
# Auto-formatear
cd YrYs-Agent
black .
flake8 --max-line-length=100
mypy .
```

### HTML/CSS/JS (Web)

- **HTML:** Validar en https://validator.w3.org/
- **CSS:** Tailwind CSS v3+ (no CSS custom pesado)
- **JS:** ES6 modules, sin jQuery

---

## 🔐 Política de Seguridad

**NO** subas:
- Claves API reales (usa `.env.example` como plantilla)
- PEM keys (`*.pem`) – ya están en `.gitignore`
- Datos de usuarios
- Logs con información sensible

Si encuentras vulnerability:

1. **NO abras issue público**
2. Email security@kalighost.dev
3. Espera 90 días antes de disclosure público

---

## 📜 Código de Conducta

KaliGhost sigue el [Contributor Covenant](https://www.contributor-covenant.org/).

- **Respeto** – Sin acoso, discriminación o ataques personales
- **Colaboración** – Constructivo, no destructivo
- **Ética** – Solo uso autorizado/legítimo

Reporta violaciones a conduct@kalighost.dev.

---

## 🏷️ Tags & Releases

- **v1.x.x** – Stable releases (producción)
- **v1.x.x-rc.x** – Release candidates
- **v1.x.x-beta.x** – Beta pública
- **main** – Código estable (último release)
- **dev** – Desarrollo activo (puede ser inestable)

**Crear un release:**
Solo maintainers pueden crear releases oficiales. PRs fusionados a `main` automáticamente触发 GitHub Actions que:
1. Incrementa versión (semver)
2. Construye artefactos (Docker image, binary)
3. Genera changelog
4. Crea tag y release en GitHub

---

## 📚 Recursos

- [Documentación YrYs-Agent](docs/AGENT.md)
- [API Reference](docs/API.md)
- [Arquitectura](docs/ARCHITECTURE.md)
- [Ejemplos](examples/)
- [Roadmap](ROADMAP.md)

---

## 🙏 Agradecimientos

Los contribuidores son la razón por la que KaliGhost existe. Todos aparecen en:
- `CREDITS.md`
- Badges en README
- Mención en releases

**First-time contributor?** ¡Bienvenido! Marca tu PR con `[first-timer]` y te guiaremos.

---

**¿Listo?** Fork now y empieza a codear.

*Questions?* Email dev@kalighost.dev o Telegram @elkalivpn.