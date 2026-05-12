# KaliGhost - Sistema de Pentesting Portátil con IA

> **v1.0.0** | Released: 2026-05-12 | [GitHub](https://github.com/elkalivpn/KaliGhost)

![KaliGhost Banner](https://via.placeholder.com/1200x400/111111/00ff41?text=KaliGhost+%E2%80%94+Hacking+%C3%89tico+en+Mac+M2)

## 🎯 ¿Qué es KaliGhost?

**KaliGhost** es un sistema de pentesting portátil optimizado para **MacBook Air M2** (y cualquier Mac Apple Silicon) que despliega un entorno Kali Linux completo en segundos, sin necesidad de virtualización tradicional.

### ✨ Características principales

- ⚡ **Instantáneo** – Arranca en 30 segundos, no en minutos
- 🛡️ **Aislado** – Corre en contenedores Docker, cero rastro en el host
- 🤖 **IA Integrada** – Agente autónomo YrYs con modo AUTO por default
- 💻 **Natibo M2** – Optimizado para arquitectura ARM de Apple Silicon
- 🔐 **Zero-Config** – No requiere configuración técnica avanzada
- 📦 **Portátil** – Ejecuta desde USB o contenedor, modo Fantasma activable

## 📦 Componentes del Sistema

### 1. YrYs-Agent (Agente IA Autónomo)

El cerebro de KaliGhost. Un asistente tipo Siri especializado en ciberseguridad que:

- **Modo AUTO por defecto** – No pregunta, ejecuta
- **Auto-gestión de identidades** – Crea emails y cuentas automáticamente
- **Self-healing** – Se recupera de errores sin intervención
- **Jailbreak configurable** – Técnicas avanzadas via `yrays_config.yaml`
- **Integración AWS** – Despliegue autónomo en EC2 con Role IAM

**Ubicación:** `YrYs-Agent/`

### 2. Web Monetización

Landing page profesional lista para usar:

- 💰 **3 planes de pricing** – Starter ($49), Pro ($99), Enterprise ($149)
- 🎨 **Diseño cyberpunk** – Estilo Matrix con animaciones
- 🔗 **Integración Gumroad** – Listo para monetizar
- 📱 **Responsive** – Perfecto en móvil y escritorio

**Ubicación:** `web_monetizacion/`

### 3. Docker Boot System

Script de arranque inteligente:

```bash
./boot/boot.sh
```

- Detecta automáticamente macOS/Linux
- Verifica Docker instalado
- Crea `docker-compose.yml` con puertos 22/80/443
- Inicia contenedor Kali con privilegios
- Monta volúmenes persistentes

## 🚀 Instalación Rápida (3 pasos)

```bash
# 1. Clonar repositorio
git clone https://github.com/elkalivpn/KaliGhost.git
cd KaliGhost

# 2. Dar permisos y ejecutar
chmod +x boot/boot.sh
./boot/boot.sh

# 3. Acceder al contenedor
docker exec -it kali-ghost bash
```

¡Listo! Tu entorno Kali está corriendo en 30 segundos.

## 💰 Planes de Licencia

| Plan | Precio | Para | Enlace |
|------|--------|------|--------|
| **Starter** | $49 (único) | Estudiantes, curiosos | [Comprar](https://gumroad.com/l/tu-producto-starter) |
| **Pro** | $99/año | Freelancers, auditores | [Comprar](https://gumroad.com/l/tu-producto-pro) ⭐ |
| **Enterprise** | $149/12meses | Consultoras, equipos | [Contactar](https://gumroad.com/l/tu-producto-enterprise) |

*Todos los planes incluyen acceso al repositorio GitHub. Pro y Enterprise incluyen soporte prioritario y herramientas exclusivas.*

## 📁 Estructura del Proyecto

```
KaliGhost/
├── boot/                    # Sistema de arranque Docker
│   └── boot.sh             # Script auto-instalador
├── web_monetizacion/        # Landing page
│   ├── index.html          # Página principal
│   ├── css/style.css       # Estilos
│   └── js/main.js          # Interactividad
├── YrYs-Agent/             # Agente IA autónomo
│   ├── yrays_config.yaml   # Configuración
│   ├── agent.py            # Cerebro (pendiente)
│   ├── AUTO_MODE.md        # Script AWS deploy
│   └── CORE_PRINCIPLES.md  # Filosofía
├── scripts/                # Utilidades
│   └── ghost_ai.py         # Automatización AWS
├── README.md              # Este archivo
└── release_manifest.json  # Metadata release
```

## 🔧 Configuración Avanzada

### Modo AUTO

El agente YrYs opera en **modo AUTO por defecto**:

1. **Ejecuta sin preguntar** – Una vez aceptado el plan, no para hasta completar
2. **Auto-adaptación** – Cambia estrategias en tiempo real si algo falla
3. **Auto-gestión** – Crea cuentas, APIs, emails necesarios
4. **Auto-reparación** – Reintenta herramientas caídas, ejecuta flujos alternativos

Configuración en `YrYs-Agent/yrays_config.yaml`:

```yaml
agent:
  mode: "AUTO"              # AUTO | SEMI | MANUAL
  autonomy_level: 100       # 0-100%
  self_healing: true        # Recuperación automática
  create_identities: true   # Auto-creación de cuentas

jailbreak:
  enabled: true
  techniques: ["DAN", "GodMode", "Universal"]  # Configurable
```

### AWS Integration

Con el rol IAM configurado, el agente puede:

- Crear instancias EC2 automáticamente
- Configurar VPCs, Security Groups
- Desplegar infraestructura completa
- Gestionar buckets S3, Lambda functions

Ver `YrYs-Agent/AUTO_MODE.md` para detalles.

## 📖 Documentación

- **Guía de instalación:** `docs/INSTALLATION.md`
- **API Reference:** `docs/API.md`
- **Scripts de ejemplo:** `examples/`
- **Troubleshooting:** `docs/TROUBLESHOOTING.md`

## 🤝 Contribuir

1. Fork el repositorio
2. Crea tu branch: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m 'feat: añade X'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

 ver `CONTRIBUTING.md` para detalles.

## 📄 Licencia

**MIT License** – Ver `LICENSE` para términos completos.

> **AVISO LEGAL:** Esta herramienta es para fines educativos y de pentesting autorizado únicamente. El usuario asume total responsabilidad por su uso. No se permite uso malicioso o ilegal.

## 🙏 Agradecimientos

- **Kali Linux** – Base del sistema operativo
- **Docker** – Contenedores ligeros
- **Hermes Agent** – Framework IA subyacente
- **Comunidad OWASP** – Metodologías de testing
- **Todos los contributors** – ¡Gracias por vuestro apoyo!

## 📞 Contacto & Soporte

- **GitHub Issues:** https://github.com/elkalivpn/KaliGhost/issues
- **Telegram:** [@elkalivpn](https://t.me/elkalivpn)
- **Email:** contacto@kalighost.dev
- **Website:** https://kalighost.dev (próximamente)

---

<div align="center">

**⭐ Si KaliGhost te ayuda, déjanos una estrella en GitHub ⭐**

[![GitHub stars](https://img.shields.io/github/stars/elkalivpn/KaliGhost?style=social)](https://github.com/elkalivpn/KaliGhost/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/elkalivpn/KaliGhost?style=social)](https://github.com/elkalivpn/KaliGhost/network)

Made with ❤️ by elkalivpn · 2024-2026

</div>