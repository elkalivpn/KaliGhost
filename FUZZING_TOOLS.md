# Herramientas de Fuzzing en KaliGhost

Ultima actualización: 2025-05-15

## HERRAMIENTAS DE FUZZING INSTALADAS ✅

### 1. Wfuzz - Web Application Fuzzer
**Versión**: 3.1.0
**Instalado en**: `/usr/local/bin/wfuzz`
**Descripción**: Herramienta de fuzzing para aplicaciones web

Uso básico:
```bash
# Fuzzing de directorios y archivos
wfuzz -w /path/to/wordlist http://target.com/FUZZ

# Fuzzing de parámetros
wfuzz -w users.txt -w passwords.txt -z file,users.txt -z file,pass.txt http://target.com/login.php?user=FUZZ&pass=FUZ2Z

# Ocultar respuestas 200 OK
wfuzz --hc 200 -w wordlist.txt http://target.com/FUZZ

# Fuzzing con extensions
wfuzz -w wordlist.txt -X POST -d "username=FUZZ" http://target.com/login
```

Características principales:
- ✅ Múltiples payloads simultáneos
- ✅ Filtros HTTP (códigos, tiempo, tamaño)
- ✅ Soporte POST/GET/PUT/DELETE
- ✅ Headers personalizados
- ✅ Proxy support

### 2. Dirsearch - Web Path Scanner  
**Versión**: 0.4.3.post1
**Instalado en**: `/usr/local/bin/dirsearch`
**Descripción**: Escáner de caminos web y directorios

Uso básico:
```bash
# Escaneo básico de directorios
dirsearch -u http://target.com

# Especificar wordlist
dirsearch -u http://target.com -w /path/to/wordlist.txt

# Escaneo con extensions específicas
dirsearch -u http://target.com -e php,html,js,txt

# Escaneo recursivo
dirsearch -u http://target.com -r 3

# Escaneo con proxies
dirsearch -u http://target.com --proxy http://127.0.0.1:8080
```

Características principales:
- ✅ Múltiples threads concurrentes
- ✅ Soporte CURL-like (redirección, cookies)
- ✅ Filtros de respuesta
- ✅ Detección de WAF
- ✅ Exportación en múltiples formatos

## EJEMPLOS DE USO REALES

### Escaneo Completo de Aplicación Web
```bash
# Fase 1: Discovery Directorios
dirsearch -u http://target.com -e php,html,js,txt,zip,rar -x 400,403,404 --random-agent

# Fase 2: Fuzzing de Parámetros
wfuzz -w /usr/share/wordlists/dirb/common.txt -w params.txt --hc 404,403 http://target.com/search?FUZZ=FUZ2Z

# Fase 3: Enumeración de Usuarios
wfuzz -w usernames.txt --sc 200 --hw 15 http://target.com/profile?user=FUZZ
```

### Escaneo de API
```bash
# Fuzzing de endpoints API
wfuzz -w api_endpoints.txt --hc 400,404,405 https://api.target.com/v1/FUZZ

# Testing de múltiples parámetros
wfuzz -w params.txt -w values.txt -z file,params.txt -z file,values.txt https://api.target.com/search?FUZZ=FUZ2Z
```

## CONFIGURACIÓN EN EL AGENTE YrYs

Las herramientas ya están integradas en el archivo de configuración:
- **wfuzz**: Listado en `local_tools.enabled`
- **dirsearch**: Listado en `local_tools.enabled`
- **Configuración YAML**: `/home/kalighost/YrYs-Agent/yrays_config.yaml`

Los comandos pueden ser invocados automáticamente por el agente YrYs durante escaneos autónomos.

## WORDLISTS DISPONIBLES

Para complementar las herramientas de fuzzing, se recomienda instalar wordlists adicionales:
- SecLists (completa colección de wordlists)
- wfuzz payloads default
- dirb (basic wordlists)
- rockyou.txt (password cracking)

## LÍMITES CONOCIDOS

1. **Wordlists**: No están instaladas wordlists por defecto
2. **Proxies**: Requiere configuración adicional para tráfico transparente
3. **Rate limiting**: Las herramientas no tienen límites de velocidad configurados

## INSTALACIÓN ADICIONAL SUGERIDA

```bash
# Instalar más herramientas de fuzzing
pip3 install gobuster feroxbuster nuclei

# Instalar wordlists
apt install -y wordlists seclists

# Instalar herramientas adicionales de escaneo  
apt install -y nikto wpscan
```

## INTEGRACIÓN CON EL WORKFLOW AUTÓNOMO

El agente YrYs puede utilizar estas herramientas en su modo autónomo para:
- Descubrir endpoints ocultos durante reconnaissance
- Enumerar parámetros potencialmente vulnerables
- Testing de inyección SQL en parámetros fuzzeados
- Bypass de autenticación mediante fuzzing de rutas

Las herramientas están completamente integradas en el ecosistema de KaliGhost y pueden ser invocadas por otros módulos del sistema.