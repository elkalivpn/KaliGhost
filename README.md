# 🐉 KaliGhost 4.0 ULTIMATE
### La Primera Plataforma de IA de Ciberseguridad que Aprende de Ti Sin Que Tus Datos Salgan de Tu Entorno.

[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-4.0.0--ULTIMATE-gold.svg)](https://github.com/elkalivpn/KaliGhost/releases)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-green.svg)](https://github.com/elkalivpn/KaliGhost)
[![ModelForge](https://img.shields.io/badge/AI-ModelForge%20Integrated-blue.svg)](docs/MODELFORGE.md)

> **Advertencia:** Esta herramienta está diseñada exclusivamente para profesionales de ciberseguridad, equipos Red/Blue Team autorizados y fines educativos. El uso malintencionado es responsabilidad exclusiva del usuario. Lea nuestros [Términos de Uso](LEGAL/TERMS_OF_SERVICE.md).

---

## 🚀 Instalación Automática en 1 Comando

KaliGhost 4.0 incluye un instalador inteligente que configura todo el entorno (Docker, dependencias, iconos de escritorio) automáticamente.

```bash
git clone https://github.com/elkalivpn/KaliGhost.git
cd KaliGhost
chmod +x install.sh && ./install.sh
```

**¿Qué hace el instalador?**
1.  ✅ Verifica e instala Docker, Python y Node.js si faltan.
2.  ✅ Despliega los 5 servicios contenerizados (API, Worker, DB, Redis, Frontend).
3.  ✅ Genera el **icono de acceso directo** en tu escritorio.
4.  ✅ Inicia la interfaz web local en `http://localhost:8001`.
5.  ✅ Te guía para crear tu cuenta y elegir plan.

---

## ⚡ Características Elite

### 🧠 ModelForge™ (Novedad Exclusiva)
Entrena tus propios modelos de IA de ciberseguridad **localmente**.
- 🔒 **Privacidad Total:** Tus datos de entrenamiento (exploits, logs, malware samples) **nunca salen de tu máquina**.
- 🎯 **Fine-Tuning:** Adapta modelos base a tu infraestructura específica.
- 🔄 **Aprendizaje Continuo:** La IA mejora con cada operación que realizas.

### 🛡️ Módulos Operativos
| Módulo | Funcionalidad Clave | Estado |
| :--- | :--- | :--- |
| **Red Team** | Reconocimiento auto, exploits, evasión AV/EDR | ✅ Activo |
| **Blue Team** | Detección de amenazas, respuesta a incidentes | ✅ Activo |
| **Purple Team** | Simulación ATT&CK, validación de defensas | ✅ Activo |
| **Grey Team** | Ingeniería social, phishing simulado | ✅ Activo |
| **Sandbox** | Análisis de malware en contenedores efímeros | ✅ Activo |
| **Forensics** | Análisis de memoria y disco post-incidente | ✅ Activo |
| **Steganography** | Ocultación de datos y volúmenes negables | ✅ Activo |
| **RAM Exec** | Ejecución de código en memoria sin rastros | ✅ Activo |

---

## 💻 Interfaz y Uso

Tras la instalación, accede a:
- **🌐 Dashboard Web:** `http://localhost:8001` (Interfaz principal)
- **📚 API Docs:** `http://localhost:8000/docs` (Swagger UI)
- **📊 Monitorización:** `http://localhost:3001` (Grafana)

**Flujo de Usuario:**
1.  Abre la aplicación desde el icono de tu escritorio o el navegador.
2.  Registra tu cuenta localmente (o conecta tu cuenta Enterprise).
3.  Selecciona tu plan (**Free**, **Pro**, **Enterprise**).
4.  Comienza a operar: Elige un módulo, configura el objetivo y deja que la IA ejecute.

---

## 🏗️ Arquitectura Técnica

Construido para la escala y la seguridad:
- **Backend:** Python FastAPI (Alto rendimiento)
- **Frontend:** React + Three.js (Visualización 3D de redes)
- **IA:** PyTorch + Transformers (Modelos locales vía ModelForge)
- **Datos:** PostgreSQL (Persistencia) + Redis (Caché) + SQLite (Memoria Agente)
- **Infraestructura:** Docker Compose (Orquestación local)

---

## 📄 Licencia y Legal

Este software es **Propietario**.
- **Términos de Servicio:** [Ver Documento](LEGAL/TERMS_OF_SERVICE.md)
- **Política de Privacidad:** [Ver Documento](LEGAL/PRIVACY_POLICY.md)
- **EULA:** [Ver Documento](LEGAL/EULA.md)
- **Descargo de Responsabilidad:** [Ver Documento](LEGAL/DISCLAIMER.md)

*KaliGhost no se hace responsable del uso indebido de esta herramienta. Úsala solo en entornos que poseas o tengas permiso explícito para auditar.*

---

## 🤝 Contribuir y Soporte

- **Reportar Bugs:** Usa la sección de [Issues](https://github.com/elkalivpn/KaliGhost/issues).
- **Documentación Completa:** Visita la carpeta [`docs/`](docs/).
- **Comunidad:** Únete a nuestro Discord (próximamente).

**© 2024 KaliGhost Security. Todos los derechos reservados.**
