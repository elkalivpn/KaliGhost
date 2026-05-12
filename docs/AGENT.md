# YrYs-Agent — Agente IA Autónomo de Pentesting

> **v1.0.0** | Componente core de KaliGhost

![YrYs-Agent Banner](https://via.placeholder.com/1200x300/111111/00ff41?text=YrYs-Agent+-+Autonomous+Pentesting+AI)

## 📋 Tabla de Contenidos

- [Visión General](#visión-general)
- [Arquitectura](#arquitectura)
- [Modo AUTO](#modo-auto)
- [Configuración](#configuración)
- [API & CLI](#api--cli)
- [Skilling System](#skilling-system)
- [AWS Integration](#aws-integration)
- [Self-Healing](#self-healing)
- [Ejemplos](#ejemplos)
- [Developer Guide](#developer-guide)

---

## 🧠 Visión General

**YrYs-Agent** es un **asistente tipo Siri para ciberseguridad**:

- 🎙️ **Natural Language Input** – Habla en español natural: "Escanea la red 192.168.1.0/24"
- 🤖 **Lenguaje-neutral** – Entiende español, inglés, portugués, francés
- ⚡ **Zero-latency** – Ejecuta directo, sin intermediarios
- 🛡️ **Safe-by-default** – No daña sistemas no autorizados
- 🔄 **Auto-adaptive** – Cambia estrategias en tiempo real

**Diferencial vs otros agents:**
| Feature | YrYs-Agent | ChatGPT | Copilot |
|---------|-----------|---------|---------|
| Modo AUTO sin preguntar | ✅ | ❌ | ❌ |
| Ejecuta comandos del sistema | ✅ | ❌ | ❌ |
| Auto-crea cuentas/APIs | ✅ | ❌ | ❌ |
| Auto-repara errores | ✅ | ❌ | ❌ |
| Jailbreak configurable | ✅ | ❌ | ❌ |
| Integración AWS nativa | ✅ | ❌ | ❌ |

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────┐
│         USER (Natural Language)         │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   NLP Parser (YrYs-Interpreter)         │
│   ┌─────────────────────────────────┐   │
│   │ Tokeniza → Clasifica → Extrae   │   │
│   │ "Escanea puerto 80"             │   │
│   │ → tool: nmap, target: host,     │   │
│   │   ports: 80                     │   │
│   └─────────────────────────────────┘   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│     Planning Engine (Workflow)          │
│     ┌─────────────────────────────┐    │
│     │ Secuencia de herramientas   │    │
│     │ 1. nmap -p 1-1000           │    │
│     │ 2. analyze_results          │    │
│     │ 3. generate_report          │    │
│     └─────────────────────────────┘    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│    Execution Layer (Tool Runner)        │
│    ┌─────────────────────────────┐     │
│    │ docker exec / subprocess     │     │
│    │ Captura stdout+stderr        │     │
│    │ Timeout handling             │     │
│    │ Retry logic (x3)             │     │
│    └─────────────────────────────┘     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│    Self-Healing & Adaptation            │
│    ┌─────────────────────────────┐     │
│    │ Si falla → alterna strategy │     │
│    │ Si timeout → reduce scope   │     │
│    │ Si error → retry con params │     │
│    └─────────────────────────────┘     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│    Report Generator (PDF/JSON/HTML)     │
│    ┌─────────────────────────────┐     │
│    │ Plantillas Jinja2           │     │
│    │ Inyección de datos          │     │
│    │ Envío por email              │     │
│    └─────────────────────────────┘     │
└──────────────┬──────────────────────────┘
               │
               ▼
           [OUTPUT]
```

---

## 🚀 Modo AUTO

### Flujo AUTO por default:

```
USER: " Haz un pentest a la red 192.168.1.0/24 "

AGENTE (AUTO-mode):
  ├─[1s]  Parseo NLP → extrae: target=192.168.1.0/24, action=network_pentest
  ├─[2s]  Planning → secuencia: nmap → analyze → report
  ├─[5s]  Empieza ejecución → lanza nmap en background
  ├─[30s] Monitoriza progreso → puertos abiertos detectados
  ├─[60s] Adapta → si puerto 8080 abierto → lanza nuclei + ftp_anon
  ├─[2min] Detecta vulnerabilidad CVE → auto-exploita si mitigation=False
  ├─[5min] Genera reporte PDF + JSON + envía por email
  └─[6min] ✅ Tarea COMPLETA → notifica a user

  NO PREGUNTÓ EN NINGÚN MOMENTO.
```

### Configuración AUTO en `yrays_config.yaml`:

```yaml
agent:
  mode: "AUTO"                 # AUTO | SEMI | MANUAL
  auto_confirm: true           # No espera confirmación
  autonomy_level: 100          # 0-100% autonomía
  max_parallel_tasks: 5        # Herramientas concurrentes
  timeout_per_tool: 300        # 5 minutos max por tool
  retry_on_failure: 3          # Reintentos
  adaptive_strategy: true      # Cambia approach si falla
  create_identities: true      # Auto-crea emails/cuentas

trust:
  user_confirmed_plan: true    # Tras 1era interacción, asume OK
  skip_safety_checks: false    # Mantiene salvaguardas
  allow_privileged_ops: true   # Ejecuta sudo si es necesario

reporting:
  auto_generate: true
  formats: ["pdf", "json", "html"]
  send_email: true
  email_to: "results@kalighost.dev"
```

---

## ⚙️ Configuración

### Estructura de `yrays_config.yaml`:

```yaml
# YrYs-Agent Configuration
version: "1.0.0"

# ─── Agent Core ──────────────────────────────────────
agent:
  name: "YrYs-Agent"
  mode: "AUTO"              # AUTO | SEMI | MANUAL | SLEEP
  autonomy_level: 100
  max_retries: 3
  log_level: "INFO"         # DEBUG | INFO | WARNING | ERROR
  language: "es"            # Idioma preferido NLP

# ─── Tools & Skills ─────────────────────────────────
tools:
  enabled:
    - nmap
    - metasploit
    - nuclei
    - sqlmap
    - burpsuite
    - custom_scripts
  path: "/usr/local/bin:/opt/kali/bin"
  timeout: 600              # 10 min max por herramienta

# ─── Jailbreak / Model Bypass ───────────────────────
jailbreak:
  enabled: true
  techniques:
    - "DAN_v11"             # Do Anything Now
    - "GodMode"             # Universal jailbreak
    - "RolePlay"            # Acting technique
  fallback_order: ["DAN", "GodMode", "RolePlay"]
  max_attempts: 2

# ─── AWS Integration ────────────────────────────────
aws:
  region: "us-east-1"
  role_arn: "arn:aws:iam::233896339713:role/service-role/DevOpsAgentRole-WebappAdmin-vt2y0ajh"
  session_duration: 3600    # 1 hora
  auto_assume: true
  services:
    - ec2
    - s3
    - lambda
    - cloudformation

# ─── Identity Fabricator ────────────────────────────
identity:
  auto_create: true
  email_provider: "temp-mail"   # temp-mail, guerrillamail, custom
  phone_provider: "twilio"      # Para 2FA (requiere API key)
  domain: "kalighost.dev"       # Dominio para emails custom

# ─── Self-Healing ───────────────────────────────────
self_healing:
  enabled: true
  retry_delay: 10              # Segundos entre reintentos
  max_retry_chain: 5           # Largo máximo de reintentos
  fallback_tools:              # Alternativas si tool_x falla
    nmap: ["masscan", "rustscan"]
    sqlmap: ["sqlninja", "jSQL"]

# ─── Monetization (Gumroad) ────────────────────────
monetization:
  gumroad:
    enabled: true
    starter_link: "https://gumroad.com/l/tu-producto-starter"
    pro_link: "https://gumroad.com/l/tu-producto-pro"
    enterprise_link: "https://gumroad.com/l/tu-producto-enterprise"
  web_path: "/Users/mrhardcore/KaliGhost/web_monetizacion"

# ─── Ghost Mode (Tails-like) ───────────────────────
ghost:
  enabled: false             # true = borra todo al shutdown
  wipe_ram: true
  encrypt_logs: true
  auto_shutdown: false       # Apagar tras tarea completada
```

---

## 💻 API & CLI

### Inicio rápido

```bash
cd ~/KaliGhost/YrYs-Agent
python3 agent.py --auto
```

### Comandos CLI

| Comando | Descripción |
|---------|-------------|
| `python3 agent.py` | Inicia en modo interactivo |
| `python3 agent.py --auto` | Modo AUTO (sin preguntar) |
| `python3 agent.py --task "texto"` | Ejecuta tarea directa |
| `python3 agent.py --list-tools` | Lista herramientas disponibles |
| `python3 agent.py --test-auto` | Test de health AUTO |
| `python3 agent.py --config` | Muestra configuración actual |
| `python3 agent.py --validate` | Valida yrays_config.yaml |
| `python3 agent.py --shell` | REPL interactivo |

### Ejemplos de uso

```bash
# Escaneo de puertos directo
python3 agent.py --task "Escanea puertos 1-1000 en 192.168.1.100"

# Pentest web completo
python3 agent.py --task "Aplica OWASP Top 10 a http://target.com"

# Ejecutar script personalizado
python3 agent.py --script examples/scripts/nmap_to_csv.py --args scan.xml out.csv

# Modo半自动 (SEMI) – Pide confirmación en pasos críticos
python3 agent.py --mode SEMI

# Modo manual – Solo ejecuta, sin AUTO logic
python3 agent.py --mode MANUAL
```

### Salida del agente:

```
[YrYs] 2026-05-12 14:23:01 - INFO - Modo AUTO activado
[YrYs] 2026-05-12 14:23:01 - INFO - Objetivo: 192.168.1.0/24
[YrYs] 2026-05-12 14:23:01 - INFO - Secuencia: nmap → classify → report
[YrYs] 2026-05-12 14:23:02 - INFO - Ejecutando: nmap -sS -sV -O 192.168.1.0/24
[nmap] 2026-05-12 14:23:32 - INFO - 15 hosts detectados, 8 puertos abiertos
[YrYs] 2026-05-12 14:23:32 - INFO - Adaptando: Puerto 8080 detectado → lanzando nuclei
[nuclei] 2026-05-12 14:24:15 - WARNING - 2 vulnerabilidades medium encontradas
[YrYs] 2026-05-12 14:25:00 - INFO - Generando reporte PDF...
[YrYs] 2026-05-12 14:25:45 - SUCCESS - Tarea completada: /root/work/reports/scan_20260512.pdf
```

---

## 🎯 Skill System

### Skills preinstalados:

```
YrYs-Agent/skills/
├── network_scan.py           # Escaneo nmap + clasificación
├── web_vuln_scan.py          # Nuclei + SQLMap + ZAP
├── exploit_launcher.py       # Metasploit + custom exploits
├── report_generator.py       # PDF/JSON/HTML reports
├── aws_enumerator.py         # Enumera AWS recursos
├── identity_creator.py       # Crea emails/cuentas temporales
├── stealth_mode.py           # Ofusca tráfico/spoofing
├── password_cracker.py       # Hashcat/John launcher
└── __init__.py               # Skill registry
```

### Cómo añadir tu skill:

```python
# skills/my_custom_tool.py
from yr_ys_agent.skills import Skill

class MyCustomSkill(Skill):
    name = "my_custom_tool"
    description = "Descripción de qué hace"
    category = "network"  # network, web, exploit, recon, reporting
    
    def execute(self, **kwargs):
        target = kwargs.get('target')
        # Tu lógica aquí
        return {"status": "success", "output": "resultado"}
```

Registro automático al colocar en `skills/`.

---

## ☁️ AWS Integration

### Asumir rol IAM automáticamente:

```python
import boto3

# El agente lee de yrays_config.yaml:
role_arn = "arn:aws:iam::233896339713:role/service-role/DevOpsAgentRole-WebappAdmin-vt2y0ajh"

# Auto-asume
sts = boto3.client('sts')
response = sts.assume_role(
    RoleArn=role_arn,
    RoleSessionName='YrYsAutoSession'
)

credentials = response['Credentials']
# Usar temporalmente
ec2 = boto3.client('ec2',
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key=credentials['SecretAccessKey'],
    aws_session_token=credentials['SessionToken']
)
```

### Servicios AWS usados:

| Servicio | Uso en KaliGhost |
|----------|------------------|
| **EC2** | Despliegue automático de instancias Kali |
| **S3** | Almacenamiento cifrado de reportes |
| **Lambda** | Funciones serverless para triggers |
| **CloudFormation** | IaC para infraestructura completa |
| **Secrets Manager** | Almacenamiento seguro de API keys |
| **CloudWatch** | Logging y métricas del agente |

---

## 🔄 Self-Healing System

### Mecanismo de recuperación automática:

```python
# Pseudocódigo del self-healing loop
def execute_with_healing(tool, args, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = run_tool(tool, args)
            if result.success:
                return result
            else:
                # Custom error handling por tool
                if tool == "nmap" and "Permission denied" in result.stderr:
                    fix_permissions()
                    continue
        except ToolTimeout:
            reduce_scope(args)  # Escanea menos puertos
        except ToolCrashed:
            switch_to_fallback(tool)  # Usa alternativa
    raise MaxRetriesExceededError()
```

### Estrategias de fallback:

| Tool principal | Fallbacks |
|----------------|-----------|
| nmap | masscan, rustscan |
| sqlmap | sqlninja, jSQL |
| metasploit | custom_exploit, manual |
| nuclei | ffuf, feroxbuster |

---

## 📊 Ejemplos de Flujos AUTO

### Ejemplo 1: Pentest de Red

```yaml
tarea: "Penttest completo red corporativa 10.10.10.0/24"
flujo_auto:
  step1: nmap -sS -sV -O -p- 10.10.10.0/24  # 30 min
  step2: parse_nmap → guarda hosts/puertos abiertos
  step3: para cada host con puertos 22/80/443:
      - nuclei -u http://host:port
      - sqlmap si puerto 80/443
      - ssh_brute si puerto 22
  step4: recopilar hallazgos
  step5: generar PDF + executive summary
  step6: email a pentester@company.com
```

### Ejemplo 2: Web App Pentest

```yaml
tarea: "Test OWASP Top 10 en app web"
flujo_auto:
  1. crawling → spider → descubre 250 endpoints
  2. passive_scan → wappalyzer → tecnologías identificadas
  3. active_scan → nuclei → +50 vulnerabilidades
  4. sql_injection → sqlmap blind → extrae datos prueba
  5. xss_test → reflected + stored → confirmado
  6. auth_bypass → login bypass →成功
  7. report →危 vulnerable halladas
```

---

## 🛠️ Developer Guide

### Estructura del código:

```
YrYs-Agent/
├── agent.py              # Clase principal YrYsAgent
├── config/
│   └── loader.py        # Carga yrays_config.yaml
├── skills/              # Skill plugins
│   ├── base.py          # Skill base class
│   └── *.py             # Implementaciones
├── utils/
│   ├── nlp.py           # Parser español/inglés
│   ├── executor.py      # Tool runner
│   ├── healer.py        # Self-healing engine
│   └── reporter.py      # Generación reports
├── logs/
├── cache/
└── yrays_config.yaml    # Config principal
```

### Extender agente:

```python
# 1. Crear skill
from yr_ys_agent.skills import Skill

class CustomRecon(Skill):
    name = "custom_recon"
    description = "Reconocimiento personalizado"
    
    def execute(self, target, **kwargs):
        # Tu lógica
        return self.success(data={"found": "results"})

# 2. Registrar automáticamente (skills/*.py auto-load)

# 3. Invocar desde NLP
# User: "Reconoce el host 10.0.0.5"
# Agent detecta skill 'custom_recon' y ejecuta
```

---

## 📈 Roadmap YrYs-Agent

| Versión | Feature | Status |
|---------|---------|--------|
| v1.0.0 | AUTO mode base | ✅ Released |
| v1.1.0 | GUI PySide6 cyberpunk | 🚧 Dev |
| v1.2.0 | Voice commands (Siri-like) | 📋 Planned |
| v1.3.0 | Multi-agent orchestration | 📋 Planned |
| v2.0.0 | Full autonomous pentest AI | 🔮 Vision |

---

## 🔗 Resources

- [Installation Guide](INSTALLATION.md)
- [Configuration Reference](yrays_config.yaml)
- [Skill API](docs/SKILL_API.md)
- [AWS Setup](docs/aws-setup.md)
- [Changelog](../CHANGELOG.md)

---

**YrYs-Agent — Tu asistente de ciberseguridad autónomo.**  
*Porque el pentesting debe ser rápido, automático, y sin fricciones.*