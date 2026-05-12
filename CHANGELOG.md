# Changelog - KaliGhost

All notable changes to KaliGhost will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.0.0] - 2026-05-12

### 🎉 Added (Primera release pública)

#### YrYs-Agent (Agente IA Autónomo)
- **Modo AUTO por default** – Ejecución sin preguntar, 100% autónomo
- **Auto-gestión de identidades** – Crea emails/cuentas automáticamente
- **Self-healing system** – Recuperación automática de errores
- **Jailbreak configurable** – Técnicas DAN, GodMode, Universal vía YAML
- **AWS Integration** – Despliegue autónomo en EC2 con Role IAM
- **yrays_config.yaml** – Configuración completa y extensible

#### Web Monetización
- Landing page completa `web_monetizacion/index.html`
- 3 planes de pricing: Starter ($49), Pro ($99), Enterprise ($149)
- Integración Gumroad lista (links placeholders)
- Diseño cyberpunk profesional con Tailwind CSS
- Sección features, pricing, CTA, footer
- Responsive mobile-first

#### Docker Boot System
- `boot/boot.sh` – Script auto-instalador inteligente
- Detección automática macOS/Linux/WSL2
- Generación dinámica de `docker-compose.yml`
- Puertos 22/80/443 expuestos
- Volúmenes persistentes configurados
- Contenedor Kali Linux privilegiado

#### Documentación
- `README.md` completo con Badges GitHub
- `docs/INSTALLATION.md` – Guía instalación paso a paso
- `release_manifest.json` – Metadata estructurada del release
- `CHANGELOG.md` – Este archivo

### 🔧 Changed

- Estructura de proyecto reorganizada para modularidad
- Configuración centralizada en YAML
- HTML optimizado para SEO y conversions

### 🐛 Fixed

- Corrección de etiquetas HTML mal cerradas en navbar
- Paths inconsistentes en referencias cruzadas
- Permisos de ejecución en scripts

### 🗑️ Removed

- Código legacy de pruebas anteriores
- Scripts de debug no productivos

---

## [Unreleased]

### 🔜 Próximas features (v1.1.0)

#### YrYs-Agent v1.1
- Interface gráfica PySide6 (GUI cyberpunk)
- Voice commands integración (Siri-like)
- plugins system dinámico
- Multi-agent orchestration (fase 2)

#### AWS Expansion
- Auto-scaling de agentes en EC2
- S3 report storage automatizado
- Lambda functions para triggers
- CloudWatch monitoring

#### Web Platform
- Dashboard cliente para seguimiento de pentests
- Portal de pago Stripe integrado
- Sistema de tickets/soporte
- Analytics con Plausible/Piwik

#### Mobile
- App React Native para control remoto
- Push notifications de reportes
- QR code para compartir auditorías

---

## [v0.9.0-beta] - 2026-05-01 (Internal)

### Added (Beta interna)
- Primer prototipo agente YrYs
- Script boot.sh experimental
- HTML básico de monetización

### Known Issues
- Modo AUTO no completamente estable
- AWS integration requiere manual intervention
- Web no responsive en móviles pequeños

---

## [v0.1.0-alpha] - 2026-04-15 (Alpha)

### Added (Alpha)
- Concepto inicial KaliGhost
- Dockerfile base Kali Linux
- Repositorio Git inicial
- Primer README básico

---

## 📊 Estadísticas de Contribución

| Versión | Commits | Archivos agregados | Líneas de código |
|---------|---------|-------------------|------------------|
| v0.1.0-alpha | 12 | 8 | 450 |
| v0.9.0-beta | 47 | 23 | 2,100 |
| v1.0.0 | 89 | 35 | 8,500+ |

---

## 🔄 Upgrade Guide

### De v0.9.0-beta a v1.0.0

```bash
cd ~/KaliGhost
git pull origin main
# Backup de tu config old
cp YrYs-Agent/yrays_config.yaml ~/backup_yrays_old.yaml
# Usa la nueva plantilla
cp YrYs-Agent/yrays_config.yaml.template YrYs-Agent/yrays_config.yaml
# Fusiona tu config anterior
# (ver docs/MIGRATION.md para detalles)
```

### De v0.1.0-alpha a v0.9.0-beta

Se requiere reinstalación completa. Ver `docs/MIGRATION.md`.

---

**Nota:** Las versiones anteriores (< v1.0.0) no tienen soporte oficial.