# Guía de Instalación - KaliGhost v1.0.0

## 📋 Requisitos del Sistema

### Mínimos
- **OS:** macOS 11+ (Big Sur) o Linux (Ubuntu 20.04+, Debian, Kali)
- **CPU:** Apple Silicon (M1/M2/M3) o Intel x64
- **RAM:** 4GB (8GB recomendado para pentesting serio)
- **Almacenamiento:** 20GB libres
- **Red:** Internet para descargar imágenes Docker y módulos IA

### Recomendados para Producción
- **RAM:** 16GB+
- **Almacenamiento:** 50GB+ SSD
- **Docker Desktop:** Última versión (con WSL2 backend en Windows)

---

## 🚀 Instalación Rápida (3 minutos)

### Paso 1: Clonar repositorio

```bash
git clone https://github.com/elkalivpn/KaliGhost.git
cd KaliGhost
```

### Paso 2: Verificar Docker

```bash
# Verificar que Docker está instalado y corriendo
docker --version
docker ps
```

**Si Docker no está instalado:**

- **macOS:** `brew install --cask docker` → Abre Docker Desktop
- **Linux:** `sudo apt-get install docker.io docker-compose`
- **Windows:** Descarga Docker Desktop for Windows

### Paso 3: Ejecutar boot.sh

```bash
chmod +x boot/boot.sh
./boot.sh
```

**Output esperado:**
```
🚀 Iniciando KaliGhost...
✅ Detectado macOS (MacBook Air M2).
✅ KaliGhost iniciado. Puedes acceder al contenedor con:
   docker exec -it kali-ghost bash
```

### Paso 4: Acceder al entorno

```bash
docker exec -it kali-ghost bash
```

¡Ya estás dentro de Kali Linux con todas las herramientas listas!

---

## 🔧 Instalación Detallada

### Opción A: Contenedor Docker (Recomendada)

```bash
# 1. Clonar
git clone https://github.com/elkalivpn/KaliGhost.git
cd KaliGhost

# 2. Configurar variables de entorno (opcional)
export KALIGHOST_WORKDIR=~/KaliGhost/work

# 3. Inicializar
mkdir -p work/scripts work/logs
./boot/boot.sh

# 4. Verificar contenedor
docker ps | grep kali-ghost

# 5. Acceder
docker exec -it kali-ghost bash
```

### Opción B: Modo USB Portable (Modo Fantasma)

```bash
# 1. Copiar repo a USB cifrado con LUKS
# (Asume USB montado en /Volumes/KaliGhostUSB)
cp -r ~/KaliGhost /Volumes/KaliGhostUSB/

# 2. Ejecutar desde USB
cd /Volumes/KaliGhostUSB/KaliGhost
./boot.sh

# 3. Al apagar, el USB se borra automágicamente
# (Configurar en YrYs-Agent/yrays_config.yaml: ghost_mode: true)
```

### Opción C: Instalación Nativa (Linux bare metal)

```bash
# Solo si quieres Kali nativo (no recomendado para Mac)
sudo apt update
sudo apt install -y kali-linux-default
git clone https://github.com/elkalivpn/KaliGhost.git
cd KaliGhost/YrYs-Agent
python3 agent.py --install-deps
```

---

## ⚙️ Configuración Post-Instalación

### 1. Configurar Agente YrYs

```bash
# Editar configuración
nano YrYs-Agent/yrays_config.yaml
```

Parámetros clave:

```yaml
agent:
  mode: "AUTO"  # AUTO | SEMI | MANUAL
  autonomy_level: 100  # 0-100%
  max_retries: 3

aws:
  role_arn: "arn:aws:iam::233896339713:role/service-role/DevOpsAgentRole-WebappAdmin-vt2y0ajh"
  region: "us-east-1"

monetization:
  gumroad_starter: "https://gumroad.com/l/tu-producto-starter"
  gumroad_pro: "https://gumroad.com/l/tu-producto-pro"
  gumroad_enterprise: "https://gumroad.com/l/tu-producto-enterprise"
```

### 2. Probar agente autónomo

```bash
cd YrYs-Agent
python3 agent.py --test-auto
```

Deberías ver:
```
[YrYs-Agent] Modo AUTO activado
[YrYs-Agent] Objetivo: test_connectivity
[YrYs-Agent] ✓ Herramientas verificadas
[YrYs-Agent] ✓ AWS conectado
[YrYs-Agent] ✓ Listo para ejecutar
```

### 3. Personalizar web de monetización

Edita `web_monetizacion/index.html`:

- Cambia enlaces Gumroad por los tuyos reales
- Modifica precios según tu modelo
- Añade tu logo en la navbar
- Personaliza colores en `css/style.css`

---

## 🐛 Solución de Problemas

### Docker no inicia

```bash
# En macOS
open -a Docker
# Espera a que el icono deje de animarse, luego:
docker ps
./boot.sh
```

### Permisos denegados en boot.sh

```bash
chmod +x boot/boot.sh
# Si persiste:
sudo chown $USER boot/boot.sh
```

### Contenedor no puede iniciar (puertos ocupados)

```bash
# Ver qué usa los puertos 22/80/443
lsof -i :22
lsof -i :80
lsof -i :443

# Mata procesos conflictivos
kill -9 <PID>

# O modifica docker-compose.yml para usar otros puertos
# ports: - "2222:22" - "8080:80" - "8443:443"
```

### Agente YrYs falla al iniciar

```bash
cd YrYs-Agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 agent.py --debug
```

Ver `YrYs-Agent/LOG.md` para logs detallados.

---

## 🎯 Uso Diario

### Inicio rápido

```bash
# 1. Iniciar contenedor (si no está corriendo)
cd ~/KaliGhost
./boot.sh

# 2. Entrar a Kali
docker exec -it kali-ghost bash

# 3. Lanzar agente en modo AUTO
cd /root/KaliGhost/YrYs-Agent
python3 agent.py --auto
```

### Ejemplo: Pentest automatizado

```bash
# El agente interpreta lenguaje natural
python3 agent.py --task "Escanea la red 192.168.1.0/24 y encuentra vulnerabilidades web"

# Output automático:
[+] Escaneo Nmap iniciado...
[+] Detectado puerto 8080 abierto
[+] Ejecutando Nikto...
[+] Vulnerabilidad encontrada: CVE-2024-XXXX
[+] Generando reporte PDF...
[✓] Pentest completado: report.pdf
```

---

## 🔐 Modo Fantasma (Ghost Mode)

Para máxima privacidad (como Tails OS):

```bash
cd YrYs-Agent
nano yrays_config.yaml
```

Configura:

```yaml
ghost_mode:
  enabled: true
  wipe_on_shutdown: true  # Borra TODO al apagar
  no_logging: true        # Sin logs en disco
  ram_only: true          # Todo en memoria RAM
  auto_encrypt: true      # Cifrado LUKS automático
```

**ADVERTENCIA:** En ghost mode, TODOS los datos se pierdan al apagar. Asegúrate de guardar reportes externamente antes de shutdown.

---

## 📊 Monitoreo y Mantenimiento

### Ver logs del contenedor

```bash
docker logs -f kali-ghost
```

### Ver logs del agente

```bash
docker exec -it kali-ghost tail -f /root/KaliGhost/YrYs-Agent/logs/agent.log
```

### Backup de datos importantes

```bash
# Dentro del contenedor
tar -czf /root/backup_$(date +%Y%m%d).tar.gz /root/work/reports

# Copiar a host
docker cp kali-ghost:/root/backup.tar.gz ~/Backups/
```

### Actualizar KaliGhost

```bash
cd ~/KaliGhost
git pull origin main
./boot.sh  # Reinicia contenedor con nueva imagen
```

---

## 🆘 Soporte Técnico

- **GitHub Issues:** https://github.com/elkalivpn/KaliGhost/issues
- **Telegram:** @elkalivpn
- **Email:** contacto@kalighost.dev
- **Discord:** (próximamente)

👉 **Incluye en tu reporte:**
1. Versión de KaliGhost (`git rev-parse HEAD`)
2. OS y arquitectura (`uname -a`)
3. Versión Docker (`docker --version`)
4. Logs relevantes (con `docker logs kali-ghost`)

---

## 📖 Recursos Adicionales

- [Documentación Oficial](https://kalighost.dev/docs) (próximamente)
- [Ejemplos de Tareas AUTO](examples/auto-tasks/)
- [Configuración AWS](docs/aws-setup.md)
- [Integración Gumroad](docs/gumroad-setup.md)
- [License](LICENSE)

---

**¿Problemas?** Revisa `docs/TROUBLESHOOTING.md` o abre un Issue en GitHub.

✨ **KaliGhost — Pentesting portátil, rápido, autónomo.**