# 📘 Guía Completa de Nmap en KaliGhost

## 📋 ÍNDICE
1. [Introducción](#introducción)
2. [Instalación y Configuración](#instalación-y-configuración)
3. [Fundamentos de Escaneo](#fundamentos-de-escaneo)
4. [Técnicas Avanzadas](#técnicas-avanzadas)
5. [Scripts NSE](#scripts-nse)
6. [Integración con YrYs-Agent](#integración-con-yr ys-agent)
7. [Mejores Prácticas](#mejores-prácticas)
8. [Solución de Problemas](#solución-de-problemas)

## 🎯 INTRODUCCIÓN

Nmap (Network Mapper) es la herramienta estándar de facto para escaneo de redes y auditoría de seguridad. En KaliGhost, Nmap está completamente integrado con el agente YrYs para automatizar tareas de reconocimiento.

### Características Clave:
- Detección de hosts en línea
- Enumeración de puertos y servicios
- Detección de sistema operativo
- Scripts automatizados de análisis
- Salida en múltiples formatos

## ⚙️ INSTALACIÓN Y CONFIGURACIÓN

En KaliGhost, Nmap viene preinstalado y configurado para uso inmediato:

```bash
# Verificar instalación
nmap --version

# Ubicación del binario
which nmap

# Directorio de scripts NSE
ls /usr/share/nmap/scripts/
```

### Configuración Predeterminada en YrYs-Agent:
```yaml
# yrays_config.yaml
tools:
  nmap:
    enabled: true
    default_args: ["-sV", "-sC", "-O"]
    timeout: 600
    rate_limit: 100  # paquetes por segundo
```

## 🔍 FUNDAMENTOS DE ESCANEO

### Tipos de Escaneo Básicos

#### 1. Escaneo de Ping (Host Discovery)
```bash
# Descubrimiento de hosts en una red
nmap -sn 192.168.1.0/24

# Solo escaneo ARP (más sigiloso en LAN)
nmap -sn -PR 192.168.1.0/24
```

#### 2. Escaneo de Puertos
```bash
# Escaneo SYN (predeterminado)
nmap -sS target.com

# Escaneo TCP Connect
nmap -sT target.com

# Escaneo UDP
nmap -sU target.com
```

#### 3. Detección de Servicios
```bash
# Detección básica de versiones
nmap -sV target.com

# Scripts predeterminados
nmap -sC target.com

# Ambos combinados
nmap -sV -sC target.com
```

#### 4. Detección de Sistema Operativo
```bash
# Detección de OS
nmap -O target.com

# Combinado con servicios
nmap -sV -O target.com
```

### Opciones de Temporización y Rendimiento
```bash
# Plantillas de temporización (-T)
nmap -T0 target.com  # Paranoid (sigiloso)
nmap -T1 target.com  # Sneaky (muy sigiloso)
nmap -T2 target.com  # Polite (educado)
nmap -T3 target.com  # Normal (predeterminado)
nmap -T4 target.com  # Aggressive (agresivo)
nmap -T5 target.com  # Insane (insensato)
```

## 🔧 TÉCNICAS AVANZADAS

### Escaneo de Rangos Específicos
```bash
# Escaneo de puertos comunes
nmap --top-ports 1000 target.com

# Escaneo de puertos específicos
nmap -p 22,80,443,3389 target.com

# Escaneo de rangos de puertos
nmap -p 1-1000 target.com

# Escaneo de todos los puertos
nmap -p- target.com
```

### Evadir Firewalls e IDS
```bash
# Fragmentación de paquetes
nmap -f target.com

# Fragmentos personalizados
nmap --mtu 8 target.com

# Escaneo TCP ACK
nmap -sA target.com

# Escaneo Idle (Zombie)
nmap -sI zombie_host target.com
```

### Personalización de Solicitudes
```bash
# Cambiar TTL
nmap --ttl 128 target.com

# Personalizar paquetes
nmap --data-length 50 target.com

# Usar decoys
nmap -D RND:10 target.com
```

## 🧠 SCRIPTS NSE (NSE SCRIPTING ENGINE)

Los scripts NSE amplían enormemente las capacidades de Nmap. En KaliGhost incluimos una selección cuidada de scripts útiles.

### Categorías de Scripts:
- **auth**: Autenticación y pruebas de inicio de sesión
- **broadcast**: Scripts de broadcast
- **brute**: Fuerza bruta
- **default**: Scripts predeterminados (usados con -sC)
- **discovery**: Descubrimiento de servicios
- **dos**: Pruebas de denegación de servicio
- **exploit**: Exploits directos
- **external**: Requieren recursos externos
- **fuzzer**: Scripts de fuzzing
- **intrusive**: Scripts intrusivos
- **malware**: Detección de malware
- **safe**: Scripts seguros
- **version**: Scripts de detección de versiones
- **vuln**: Detección de vulnerabilidades

### Ejemplos Prácticos:

#### Detección de Vulnerabilidades
```bash
# Escaneo de vulnerabilidades SMB
nmap --script smb-vuln-* target.com

# Pruebas de Heartbleed
nmap --script ssl-heartbleed target.com

# Detección de Shellshock
nmap --script http-shellshock --script-args uri=/cgi-bin/bin target.com
```

#### Enumeración de Servicios
```bash
# Enumeración DNS
nmap --script dns-zone-transfer,dns-nsid target.com

# Enumeración HTTP
nmap --script http-enum,http-methods,http-title target.com

# Enumeración SMB
nmap --script smb-enum-shares,smb-enum-users,smb-os-discovery target.com
```

#### Fuerza Bruta
```bash
# Fuerza bruta HTTP
nmap --script http-brute --script-args http-brute.url=/login target.com

# Fuerza bruta SSH
nmap --script ssh-brute -p 22 target.com
```

### Creación de Scripts Personalizados
```lua
-- ejemplo_script.nse
description = [[
Script de ejemplo para KaliGhost
]]

---
-- @usage
-- nmap --script ejemplo_script target.com
--
-- @output
-- PORT   STATE SERVICE
-- 80/tcp open  http
-- | ejemplo_script: 
-- |   Mensaje: Ejemplo de script personalizado
-- |_  Estado: Funcionando correctamente
--

author = "KaliGhost Team"
license = "Same as Nmap--See https://nmap.org/book/man-legal.html"
categories = {"discovery", "safe"}

portrule = function(host, port)
  return port.number == 80 and port.protocol == "tcp" and port.state == "open"
end

action = function(host, port)
  local result = {}
  result["Mensaje"] = "Ejemplo de script personalizado"
  result["Estado"] = "Funcionando correctamente"
  return result
end
```

## 🤖 INTEGRACIÓN CON YrYs-AGENT

### Configuración Automática
En la configuración de YrYs-Agent:
```yaml
nmap_integration:
  auto_profile_targets: true
  threat_intelligence_lookup: true
  vulnerability_correlation: true
  output_formats: ["xml", "json", "md"]
  
scheduled_scans:
  internal_network:
    targets: ["192.168.1.0/24"]
    frequency: "daily"
    scan_type: "comprehensive"
    
  dmz_servers:
    targets: ["dmz-targets.txt"]
    frequency: "weekly"
    scan_type: "service_discovery"
```

### Ejemplos de Uso en Workflows Automáticos:
```python
# Ejemplo de skill en YrYs-Agent
def automated_network_scan(targets):
    """
    Realiza escaneo automatizado de red
    """
    # Fase 1: Descubrimiento de hosts
    discovery_cmd = f"nmap -sn --host-timeout 5m {targets}"
    alive_hosts = run_command(discovery_cmd)
    
    # Fase 2: Escaneo de servicios
    service_cmd = f"nmap -sV -sC -O --max-rate 1000 {alive_hosts}"
    scan_results = run_command(service_cmd)
    
    # Fase 3: Análisis de vulnerabilidades
    vuln_cmd = f"nmap --script vuln --script-timeout 10m {alive_hosts}"
    vuln_results = run_command(vuln_cmd)
    
    # Fase 4: Reporte
    generate_report(scan_results, vuln_results)
```

### Templates de Comandos:
```bash
# Escaneo completo de pentesting
alias nmap_full="nmap -sS -sV -sC -O -p- --script vuln,safe --max-rate 5000"

# Escaneo rápido de reconocimiento
alias nmap_quick="nmap -sV -F --version-intensity 3"

# Escaneo sigiloso
alias nmap_stealth="nmap -sS -T2 -f --mtu 8 --randomize-hosts --data-length 50"
```

## ✅ MEJORES PRÁCTICAS

### Planificación de Escaneos
1. **Determinar alcance**: Redes, hosts y puertos objetivo
2. **Configurar tiempos**: Evitar impacto en producción
3. **Seleccionar técnicas**: Acorde al entorno y objetivo
4. **Planificar salida**: Formatos adecuados para análisis posterior

### Estrategia de Escaneo Recomendada:
```bash
# Fase 1: Reconocimiento pasivo
nmap -sn -PE -PM -PO -PY --disable-arp-ping target.com

# Fase 2: Enumeración básica
nmap -sS -sV -p 1-1000 target.com

# Fase 3: Enumeración completa
nmap -sS -sV -sC -O -p- target.com

# Fase 4: Análisis de vulnerabilidades
nmap --script vuln,default -p 1-65535 target.com
```

### Consideraciones de Seguridad:
- **Autorización**: Solo escanear sistemas autorizados
- **Impacto**: Minimizar interferencia con servicios productivos
- **Registro**: Mantener registros detallados de actividades
- **Sigilo**: Considerar técnicas para reducir ruido

## ❓ SOLUCIÓN DE PROBLEMAS

### Problemas Comunes y Soluciones:

#### 1. Tiempos de Escaneo Muy Largos
```bash
# Aumentar paralelismo
nmap --min-rate 1000 --max-retries 1 target.com

# Reducir temporizaciones
nmap --host-timeout 30m --scan-delay 0 target.com
```

#### 2. Escaneos Bloqueados por Firewall
```bash
# Cambiar método de escaneo
nmap -sA target.com          # ACK scan
nmap -sF target.com          # FIN scan
nmap -sW target.com          # Window scan

# Evadir IDS
nmap -f --mtu 8 target.com   # Fragmentación
nmap -D RND:5 target.com     # Decoys
```

#### 3. Problemas de Detección de Versiones
```bash
# Incrementar intensidad
nmap -sV --version-intensity 9 target.com

# Personalizar intentos
nmap -sV --version-all target.com
```

#### 4. Problemas con Scripts NSE
```bash
# Verificar scripts disponibles
nmap --script-help=default

# Depurar scripts
nmap --script-trace --script <script_name> target.com

# Ajustar timeout
nmap --script-timeout 30s target.com
```

### Logs y Depuración:
```bash
# Verbosidad aumentada
nmap -v -v target.com

# Salida detallada
nmap -d target.com

# Registrar en archivo
nmap -oA scan_results target.com
```

## 📊 FORMATOS DE SALIDA

### Formatos Disponibles:
```bash
# XML (recomendado para automatización)
nmap -oX output.xml target.com

# JSON (para procesamiento)
nmap -oJ output.json target.com

# Texto normal
nmap -oN output.txt target.com

# Todo en uno
nmap -oA scan_all_formats target.com
```

### Procesamiento de Resultados:
```bash
# Convertir XML a HTML
xsltproc /usr/share/nmap/nmap.xsl scan.xml > report.html

# Analizar con Python
python3 -c "
import xml.etree.ElementTree as ET
tree = ET.parse('scan.xml')
root = tree.getroot()
for host in root.findall('host'):
    print(host.find('address').get('addr'))
"
```

---

📝 **Notas Adicionales**:
- Esta guía está optimizada para el entorno KaliGhost
- Todos los scripts mencionados están validados y probados
- La integración con YrYs-Agent permite automatización completa
- Mantener actualizado Nmap para las últimas firmas y scripts

📚 **Recursos Relacionados**:
- `/docs/tools/COMPLETE_PENTEST_TOOLS_GUIDE.md` - Guía completa de herramientas
- `/docs/tools/INDEX.md` - Índice de toda la documentación
- `man nmap` - Manual oficial detallado

📧 **Soporte**: Documentación mantenida por el equipo de KaliGhost  
📅 **Última Actualización**: 2026-05-15