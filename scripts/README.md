# 🎯 Scripts y Demos de KaliGhost

## 📋 ÍNDICE

- [Introducción](#introducción)
- [Scripts Disponibles](#scripts-disponibles)
- [Demos Interactivas](#demos-interactivas)
- [Configuraciones](#configuraciones)
- [Uso con YrYs-Agent](#uso-con-yr ys-agent)
- [Contribuir](#contribuir)

## 🎯 INTRODUCCIÓN

Esta sección contiene scripts automatizados y demos interactivas diseñadas para demostrar las capacidades de KaliGhost y facilitar tareas comunes de pentesting. Todos los scripts están optimizados para funcionar con el agente YrYs y siguen las mejores prácticas de seguridad.

## 🛠️ SCRIPTS DISPONIBLES

### 🔧 Scripts de Automatización

#### `demo_pentest_workflow.sh`
**Descripción**: Demostración completa del flujo de trabajo automatizado de pentesting
**Características**:
- Integración de múltiples herramientas
- Manejo seguro de errores
- Registro detallado de actividades
- Modo demostración seguro
**Uso**:
```bash
# Ejecutar demo contra objetivo seguro
./demo_pentest_workflow.sh scanme.nmap.org
```

#### `setup_kalighost_partitions.sh`
**Descripción**: Script de particionamiento para discos externos KaliGhost
**Características**:
- Creación de particiones exFAT
- Optimización para macOS/Linux
- Modo interactivo y no interactivo
**Uso**:
```bash
# Particionar disco /dev/sdb
./setup_kalighost_partitions.sh /dev/sdb
```

### 📊 Scripts de Análisis

#### `analyze_scan_results.py`
**Descripción**: Análisis automatizado de resultados de escaneo
**Características**:
- Procesamiento de múltiples formatos (XML, JSON, TXT)
- Correlación inteligente de hallazgos
- Generación de reportes ejecutivos
**Uso**:
```bash
# Analizar resultados de Nmap
python3 analyze_scan_results.py nmap_output.xml
```

#### `vulnerability_correlator.sh`
**Descripción**: Correlación de vulnerabilidades encontradas
**Características**:
- Consolidación de múltiples fuentes
- Priorización por severidad
- Recomendaciones de mitigación
**Uso**:
```bash
# Correlacionar hallazgos de múltiples herramientas
./vulnerability_correlator.sh /path/to/results/
```

## 🎮 DEMOS INTERACTIVAS

### 🌟 Demo de Workflow Completo
El script `demo_pentest_workflow.sh` proporciona una experiencia completa que demuestra:
1. **Reconocimiento de red** (Nmap, Masscan, RustScan)
2. **Enumeración de servicios** (Detección avanzada)
3. **Análisis web** (Dirsearch, Gobuster, Wfuzz, FFuF)
4. **Testing de vulnerabilidades** (SQLMap, Nikto)
5. **Análisis forense** (Tshark, Tcpdump)
6. **Integración con Metasploit** (Modo demo)

### 🎯 Modos de Ejecución
```bash
# Modo rápido (bajo impacto)
./demo_pentest_workflow.sh --quick target.com

# Modo normal (balance estándar)
./demo_pentest_workflow.sh target.com

# Modo completo (análisis exhaustivo)
./demo_pentest_workflow.sh --thorough target.com

# Modo simulado (sin escaneos reales)
./demo_pentest_workflow.sh --simulate target.com
```

### 📈 Características de Seguridad
- ✅ Verificación automática de autorización
- ✅ Límites de tasa configurables
- ✅ Exclusiones de rangos sensibles
- ✅ Modo demo para entornos seguros
- ✅ Registro completo de actividades

## ⚙️ CONFIGURACIONES

### `demo_workflow_config.yaml`
Archivo de configuración principal para la demo:
```yaml
# Perfiles de escaneo
scan_profiles:
  quick:    # Rápido y discreto
  normal:   # Balance estándar  
  thorough: # Completo y exhaustivo

# Herramientas habilitadas
tools:
  nmap: true
  masscan: true
  # ...

# Wordlists predeterminadas
wordlists:
  web_directories: "/usr/share/dirb/wordlists/common.txt"
```

### `agent_integration.conf`
Configuración para integración con YrYs-Agent:
```ini
[General]
enable_agent_control = true
auto_submit_findings = false
notification_level = high

[Security]
require_authorization = true
exclude_private_networks = true
rate_limit = 1000

[Output]
format = json
compress_results = true
```

## 🤖 USO CON YrYs-AGENT

### Skills de Automatización
Los scripts pueden ser utilizados como skills personalizadas:

```python
# skill_auto_pentest.py
def execute(self, target):
    """Ejecutar pentest automatizado"""
    cmd = f"/opt/kalighost/scripts/demo_pentest_workflow.sh {target}"
    return self.run_command(cmd)
```

### Workflows Programados
```yaml
# workflow_weekly_scan.yaml
name: "Weekly Network Scan"
schedule: "0 2 * * 1"  # Lunes 2 AM
steps:
  - name: "Network Discovery"
    script: "demo_pentest_workflow.sh"
    args: ["--quick", "{{NETWORK_RANGE}}"]
    
  - name: "Detailed Analysis" 
    script: "analyze_scan_results.py"
    args: ["{{RESULTS_FILE}}"]
    
  - name: "Report Generation"
    skill: "generate_security_report"
    params: 
      findings: "{{ANALYSIS_RESULTS}}"
```

### Comandos de Voz del Agente
```bash
YrYs, ejecuta un escaneo rápido en 192.168.1.0/24
YrYs, analiza los resultados del último escaneo
YrYs, genera un informe ejecutivo de vulnerabilidades
```

## 📊 MONITOREO Y MÉTRICAS

### Dashboards Integrados
- **Panel de Estado**: Progreso en tiempo real
- **Métricas de Rendimiento**: Velocidad y eficiencia
- **Hallazgos Críticos**: Alertas prioritarias
- **Historial de Actividades**: Logging completo

### Exportación de Datos
```bash
# Exportar resultados en múltiples formatos
./demo_pentest_workflow.sh --export-format json target.com
./demo_pentest_workflow.sh --export-format pdf target.com
./demo_pentest_workflow.sh --export-format html target.com
```

## 🤝 CONTRIBUIR

### Cómo Contribuir
1. **Fork** el repositorio
2. **Crea** una nueva rama para tu feature
3. **Desarrolla** tu script siguiendo nuestras guías
4. **Documenta** su uso y funcionalidades
5. **Envía** un Pull Request

### Estándares de Codificación
- Scripts en Bash/Python (shebang apropiado)
- Comentarios claros y descriptivos
- Manejo adecuado de errores
- Compatibilidad con KaliGhost
- Seguridad por diseño

### Requisitos de Seguridad
- ✅ Verificación de entradas
- ✅ Limitaciones de recursos
- ✅ Control de autorización
- ✅ Logging apropiado
- ✅ Manejo seguro de credenciales

---

## 🚀 COMENZANDO

### Ejecución Rápida
```bash
# Dar permisos de ejecución
chmod +x *.sh

# Ejecutar demo segura
./demo_pentest_workflow.sh scanme.nmap.org

# Ver resultados
ls /tmp/kalighost_demo_*/
```

### Personalización
```bash
# Editar configuración
nano config/demo_workflow_config.yaml

# Ejecutar con perfil específico
./demo_pentest_workflow.sh --profile thorough target.com
```

### Integración con IDE
Los scripts están diseñados para integrarse con:
- **Visual Studio Code**: Extensiones de debugging
- **PyCharm**: Perfiles de ejecución
- **Vim/Neovim**: Compatibilidad con snippets

---

📅 **Última actualización**: 2026-05-15  
📍 **Ubicación**: `/Users/mrhardcore/KaliGhost/scripts/`  
👥 **Mantenido por**: Equipo de Desarrollo de KaliGhost  
🔐 **Clasificación**: Código de Automatización - Uso Restringido

⚠️ **Importante**: Todos los scripts deben usarse solamente en entornos autorizados para actividades de pentesting y educación en seguridad informática.

---
[Volver al Índice Principal](../README.md) | [Documentación de Herramientas](../docs/tools/) | [Configuración del Sistema](../config/)