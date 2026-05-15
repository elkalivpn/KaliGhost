#!/bin/bash

#
# 🔴 KALIGHOST TOOLKIT INSTALLER - MODO FANTASMA
#
# Instala las herramientas más esenciales de Kali Linux
# para KaliGhost OS (basado en Debian)
#
# ✅ Principios:
#   - Local-first
#   - Autónomo
#   - Portable
#   - Sin dependencias externas
#   - Modo fantasma
#

set -e

KALIGHOST_DIR="/home/kalighost"
LOG_FILE="$KALIGHOST_DIR/kalighost-install.log"
exec > >(tee -a "$LOG_FILE") 2>&1

function log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

log "🛠️ INICIANDO INSTALACIÓN DE KALIGHOST TOOLKIT"
log "📌 Directorio: $KALIGHOST_DIR"

# ======================================================
# 🔥 TOP 10 HERRAMIENTAS KALI LINUX (Optimizado para KaliGhost)
# ======================================================

TOP_TOOLS_KALI=(
    # 1️⃣ RECONNAISSANCE
    "nmap"           # ✅ Escaneo de red (ya instalado)
    "masscan"        # ✅ Escaneo masivo (red rápida)
    "dnsenum"        # ✅ Enumeración DNS
    "net-tools"      # ✅ Herramientas de red (ifconfig, netstat)
    
    # 2️⃣ VULNERABILITY ASSESSMENT
    "nikto"          # ✅ Escáner web
    "sqlmap"         # ✅ Inyección SQL
    
    # 3️⃣ EXPLOITATION
    "metasploit-framework"    # ✅ Framework de explotación
    "hydra"          # ✅ Brute force
    
    # 4️⃣ POST-EXPLOITATION
    "crackmapexec"   # ✅ Post-explotación Windows/AD
    "john"           # ✅ Cracking de contraseñas
    "hashcat"        # ✅ GPU cracking
    
    # 5️⃣ WIRELESS
    "aircrack-ng"    # ✅ Análisis wifi
    
    # 6️⃣ NLP + AUTOMATION (KaliGhost)
    "python3-pip"    # ✅ Python packages
    "wfuzz"          # ✅ Fuzzer web (ya instalado)
)

# ======================================================
# 🔧 INSTALACIÓN
# ======================================================

log "🔄 Actualizando sistema"
apt-get update -y
log "⚙️ Instalando herramientas..."

for tool in "${TOP_TOOLS_KALI[@]}"; do
    if dpkg -s "$tool" &> /dev/null || which "$tool" &> /dev/null; then
        log "⏭️ $tool ya está instalado, saltando..."
    else
        log "⬇️ Instalando $tool"
        apt-get install -y "$tool" 
        
        # Configuración rápida para KaliGhost
        case "$tool" in
            "nmap")
                echo "alias nmap='nmap -T4 -Pn'" >> /home/kalighost/.bashrc
                ;;
            "metasploit-framework")
                # Configuración inicial silent
                msfdb init | tee --append "$LOG_FILE" || true
                echo "host: localhost" > ~/.msf4/database.yml
                echo "port: 5432" >> ~/.msf4/database.yml
                ;;
            "john")
                # Instalar wordlists básicas
                apt-get install -y wordlists
                ;;
            "hydra")
                echo "alias hydra='hydra -t 16'" >> /home/kalighost/.bashrc
                ;;
        esac
    fi
    log "✅ $tool instalado/verificado"
done

# ======================================================
# 🛡️ CONFIGURACIÓN KALIGHOST (Modo Fantasma)
# ======================================================

# Configurar path para KaliGhost
log "🗺️ Configurando PATH para KaliGhost"
KALIGHOST_PATH="/usr/local/bin:/usr/local/sbin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/share/metasploit-framework:/usr/share/sqlmap:/opt/impacket"
echo "export PATH=$KALIGHOST_PATH:\$PATH" >> /home/kalighost/.bashrc

# Script de modo fantasma
log "👻 Configurando MODO FANTASMA"
cat > /usr/local/bin/ghost-mode << 'EOFGHOST'
#!/bin/bash
#
# 👻 GHOST MODE - KaliGhost
#
# ✅ Autodestrucción segura
# ✅ Borrado de logs automático
# ✅ Modo incógnito
#

LOG_DIRS="/var/log /tmp ~/.msf4/logs ~/.bash_history"
REMOVABLE="/var/cache/apt/archives"

function clean_logs() {
    echo "🧹 Limpiando logs..."
    for log_dir in $LOG_DIRS; do
        if [ -e "$log_dir" ]; then
            shred -zu "$log_dir"* 2>/dev/null || true
            chmod 000 "$log_dir" 2>/dev/null || true
        fi
    done
}

function clean_packages() {
    echo "📦 Limpiando paquetes..."
    apt-get autoremove -y && apt-get clean
    rm -rf "$REMOVABLE"* 2>/dev/null || true
}

function disable_networking() {
    echo "🚫 Deshabilitando red..."
    systemctl stop NetworkManager 2>/dev/null || true
    systemctl disable NetworkManager 2>/dev/null || true
    ifconfig eth0 down 2>/dev/null || true
    ifconfig eth1 down 2>/dev/null || true
}

function ghost_header() {
    clear
    cat << "EOGHOST"


           ░██████╗██╗░████╗░░██████╗░░█████╗░░█████╗░██╗██╗░░██╗
           ██╔════╝██║██╔══██╗██╔════╝░██╔══██╗██╔══██╗██║██║░██╔╝
           ╚█████╗░██║███████║██║░░██╗░██║░░╚═╝██║░░██║██║█████═╝░
           ░╚═══██╗██║██╔══██║██║░░╚██╗██║░░██╗██║░░██║██║██╔═██╗░
           ██████╔╝██║██║░░██║╚██████╔╝╚█████╔╝╚█████╔╝██║██║░╚██╗
           ╚═════╝░╚═╝╚═╝░░╚═╝░╚═════╝░░╚════╝░░╚════╝░╚═╝╚═╝░░╚═╝

                 👻 KALIGHOST - MODO FANTASMA ACTIVADO
EOGHOST
}

ghost_header

read -p "⚠️  ¿Activar MODO FANTASMA? (Borrará logs y datos) [s/N]: " confirm
if [[ $confirm =~ ^[sSyY]$ ]]; then
    clean_logs
    clean_packages
    disable_networking
    
    echo "🔥  ██████╗░██╗░░░░░░█████╗░██╗░░░██╗███████╗███╗░░██╗████████╗"
    echo "🔥  ██╔══██╗██║░░░░░██╔══██╗██║░░░██║██╔════╝████╗░██║╚══██╔══╝"
    echo "🔥  ██████╔╝██║░░░░░██║░░██║██║░░░██║█████╗░░██╔██╗██║░░░██║░░░"
    echo "🔥  ██╔══██╗██║░░░░░██║░░██║██║░░░██║██╔══╝░░██║╚████║░░░██║░░░"
    echo "🔥  ██║░░██║███████╗╚█████╔╝╚██████╔╝███████╗██║░╚███║░░░██║░░░"
    echo "🔥  ╚═╝░░╚═╝╚══════╝░╚════╝░░╚═════╝░╚══════╝╚═╝░░╚══╝░░░╚═╝░░░"
    
    echo -n "💀 Autodestrucción en 5..." && sleep 1
echo -n "4..." && sleep 1
echo -n "3..." && sleep 1
echo -n "2..." && sleep 1
echo -n "1..." && sleep 1
echo "💥"
else
    echo "🛑 Modo fantasma cancelado"
    exit 0
fi
EOFGHOST

chmod +x /usr/local/bin/ghost-mode
chown kalighost:kalighost /usr/local/bin/ghost-mode

# ======================================================
# 🎯 CONFIGURACIÓN ESPECIALIZADA PARA KALIGHOST
# ======================================================

# Configurar nmap con scripts NSE
log "📜 Configurando nmap para KaliGhost"
mkdir -p /home/kalighost/nmap_scripts
cd /home/kalighost/nmap_scripts
git clone https://github.com/vulnersCom/nmap-vulners.git 2>/dev/null || true
nmap --script-updatedb 2>/dev/null || true

# Configurar metasploit
log "⚡ Configurando metasploit para KaliGhost"
cat > /home/kalighost/.msf4/msfconsole.rc << 'EOFMSF'
#
# MSFCONSOLE RC - KaliGhost
#
spool /home/kalighost/.msf4/kalighost_msf.log
db_connect kalighost_user:kalighost_pass@localhost/msf
load plugins
use multi/handler
echo "🎯 KaliGhost Metasploit inicializado - Modo FANTASMA"
EOFMSF

# ======================================================
# 🛡️ SECURITY HARDENING (KaliGhost)
# ======================================================

# Configuración segura
log "🔐 Configurando parámetros de seguridad"
cat > /etc/sysctl.d/99-kalighost-security.conf << 'EOFSECURITY'
# Seguridad kernel
net.ipv4.conf.all.rp_filter=1
net.ipv4.icmp_echo_ignore_broadcasts=1
net.ipv6.conf.all.disable_ipv6=1
kernel.randomize_va_space=2
fs.protected_hardlinks=1
fs.protected_symlinks=1
EOFSECURITY

sysctl -p 2>/dev/null || true

# ======================================================
# 🏆 FINALIZACIÓN
# ======================================================

# Permisos finales
chown -R kalighost:kalighost /home/kalighost
chmod 755 /usr/local/bin/ghost-mode

log "✅ ██╗░░░██╗██╗░█████╗░░█████╗░░██╗░░░░░░░██╗░██████╗
log "✅ ██║░░░██║██║██╔══██╗██╔══██╗░██║░░██╗░░██║██╔════╝
log "✅ ╚██╗░██╔╝██║██║░░██║███████║░╚██╗████╗██╔╝╚█████╗░
log "✅ ░╚████╔╝░██║██║░░██║██╔══██║░░████╔═████║░░░╚═══██╗
log "✅ ░░╚██╔╝░░██║╚█████╔╝██║░░██║░░╚██╔╝░╚██╔╝░██████╔╝
log "✅ ░░░╚═╝░░░╚═╝░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═════╝░"

log "🎉 KALIGHOST TOOLKIT INSTALACIÓN COMPLETADA"
log "📋 Archivo de log: $LOG_FILE"
log "👉 Para activar modo fantasma: ghost-mode"

# Info final
echo "\n📜 HERRAMIENTAS INSTALADAS:" | tee -a "$LOG_FILE"
echo "-----------------------------" | tee -a "$LOG_FILE"
for tool in "${TOP_TOOLS_KALI[@]}"; do
    if which "$tool" &> /dev/null || type "$tool" &> /dev/null; then
        printf "✅ %-15s %s\n" "$(basename $(which $tool 2>/dev/null || echo $tool)):" "Instalado" | tee -a "$LOG_FILE"
    fi
done

echo "\n" | tee -a "$LOG_FILE"
log "💡 USO BÁSICO DE HERRAMIENTAS:"
log "   📌 nmap <target>: Escaneo de red rápido (-T4)"
log "   📌 sqlmap -u <url> --batch: Inyección SQL automática"
log "   📌 msfconsole: Metasploit (configurado para KaliGhost)"
log "   📌 ghost-mode: Activar MODO FANTASMA (autodestrucción)"

log "✨ LISTO PARA OPERACIONES ESPECIALES - MODO FANTASMA ACTIVO"