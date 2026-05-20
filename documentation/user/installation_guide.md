# KaliGhost Installation Guide

This guide provides detailed instructions for installing and setting up KaliGhost on your system. KaliGhost offers multiple installation methods to accommodate different use cases and security requirements.

## System Requirements

### Hardware Requirements

#### Minimum Specifications
- **CPU**: Apple Silicon (M1/M2/M3) or Intel x64 processor
- **RAM**: 4GB minimum (8GB recommended for serious pentesting)
- **Storage**: 20GB available disk space
- **Graphics**: Any integrated graphics (dedicated GPU recommended for GUI)

#### Recommended Specifications
- **RAM**: 16GB or more
- **Storage**: 50GB+ SSD
- **Graphics**: Apple Silicon GPU for optimal 3D GUI performance

### Software Requirements

#### Supported Operating Systems
- **macOS**: Version 11 (Big Sur) or later
- **Linux**: Ubuntu 20.04+, Debian 11+, Kali Linux 2022+

#### Required Software
- **Docker**: Latest version (with WSL2 backend on Windows)
- **Git**: For cloning the repository
- **Terminal**: Bash, Zsh, or any POSIX-compliant shell

## Installation Methods

### Option 1: Container Installation (Recommended)

This is the default and recommended installation method that provides isolation and portability.

#### Step-by-Step Instructions

1. **Install Docker**
   ```bash
   # macOS - Using Homebrew
   brew install --cask docker
   
   # Linux
   sudo apt update
   sudo apt install docker.io docker-compose
   ```

2. **Launch Docker Desktop**
   ```bash
   # macOS
   open -a Docker
   
   # Wait for the Docker icon to finish animating in the menu bar
   ```

3. **Verify Docker Installation**
   ```bash
   docker --version
   docker ps
   ```

4. **Clone KaliGhost Repository**
   ```bash
   git clone https://github.com/elkalivpn/KaliGhost.git
   cd KaliGhost
   ```

5. **Make Boot Script Executable**
   ```bash
   chmod +x boot/boot.sh
   ```

6. **Initialize KaliGhost**
   ```bash
   mkdir -p work/scripts work/logs
   ./boot/boot.sh
   ```

7. **Verify Container Operation**
   ```bash
   docker ps | grep kali-ghost
   ```

8. **Access KaliLinux Environment**
   ```bash
   docker exec -it kali-ghost bash
   ```

#### Expected Output

Successful initialization should produce output similar to:
```
🚀 Iniciando KaliGhost...
✅ Detectado macOS (MacBook Air M2).
✅ KaliGhost iniciado. Puedes acceder al contenedor con:
   docker exec -it kali-ghost bash
```

### Option 2: Portable USB Installation (Ghost Mode)

For maximum portability and security, KaliGhost can be installed on an encrypted USB drive.

#### Prerequisites
- USB drive with at least 32GB storage
- LUKS encryption capability (Linux) or built-in macOS encryption

#### Installation Steps

1. **Prepare Encrypted USB**
   ```bash
   # Linux with LUKS encryption
   sudo cryptsetup luksFormat /dev/sdX
   sudo cryptsetup open /dev/sdX kalighost_usb
   sudo mkfs.ext4 /dev/mapper/kalighost_usb
   sudo mount /dev/mapper/kalighost_usb /mnt
   ```

2. **Copy KaliGhost to USB**
   ```bash
   cp -r ~/KaliGhost /Volumes/KaliGhostUSB/
   ```

3. **Configure Ghost Mode**
   Edit `YrYs-Agent/yrays_config.yaml`:
   ```yaml
   ghost:
     enabled: true
     wipe_ram: true
     encrypt_logs: true
     auto_shutdown: true
     ephemeral_fs: true
   ```

4. **Run from USB**
   ```bash
   cd /Volumes/KaliGhostUSB/KaliGhost
   ./boot.sh
   ```

### Option 3: Native Installation (Linux Only)

For users who prefer running KaliGhost natively on Linux systems:

#### Warning
This method is not recommended for macOS due to compatibility issues.

#### Installation Steps

1. **Update Package Lists**
   ```bash
   sudo apt update
   ```

2. **Install Kali Linux Tools**
   ```bash
   sudo apt install -y kali-linux-default
   ```

3. **Clone KaliGhost Repository**
   ```bash
   git clone https://github.com/elkalivpn/KaliGhost.git
   ```

4. **Install Python Dependencies**
   ```bash
   cd KaliGhost/YrYs-Agent
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Run Installation Script**
   ```bash
   python3 agent.py --install-deps
   ```

## Post-Installation Configuration

### Configure YrYs Agent

1. **Edit Configuration File**
   ```bash
   nano YrYs-Agent/yrays_config.yaml
   ```

2. **Essential Parameters to Review**
   ```yaml
   agent:
     mode: "AUTO"  # AUTO | SEMI | MANUAL
     autonomy_level: 100  # 0-100%
   
   aws:
     role_arn: "arn:aws:iam::your-account:role/your-role"
     region: "us-east-1"
   
   monetization:
     # Update with your actual Gumroad links
     gumroad_pro: "https://gumroad.com/l/your-product"
   ```

### Test Agent Functionality

1. **Run Diagnostic Test**
   ```bash
   cd YrYs-Agent
   python3 agent.py --test-auto
   ```

2. **Expected Output**
   ```
   [YrYs-Agent] Modo AUTO activado
   [YrYs-Agent] Objetivo: test_connectivity
   [YrYs-Agent] ✓ Herramientas verificadas
   [YrYs-Agent] ✓ AWS conectado
   [YrYs-Agent] ✓ Listo para ejecutar
   ```

### Customize Monetization Web Page

1. **Edit Web Files**
   ```bash
   nano web_monetizacion/index.html
   ```

2. **Key Modifications**
   - Replace placeholder Gumroad links with your actual product URLs
   - Modify pricing according to your business model
   - Update company name and contact information
   - Customize color scheme in `css/style.css`

## Troubleshooting Common Issues

### Docker Not Starting

**Solution:**
```bash
# macOS
open -a Docker
# Wait for icon animation to complete
docker ps
./boot.sh
```

### Permissions Denied on boot.sh

**Solution:**
```bash
chmod +x boot/boot.sh
sudo chown $USER boot/boot.sh
```

### Container Startup Failure

**Diagnosis:**
```bash
# Check which processes use conflicting ports
lsof -i :22
lsof -i :80
lsof -i :443

# Kill conflicting processes
kill -9 <PID>

# Or modify docker-compose.yml to use alternative ports
# ports: - "2222:22" - "8080:80" - "8443:443"
```

### YrYs Agent Failures

**Debug Steps:**
```bash
cd YrYs-Agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 agent.py --debug
```

Check `YrYs-Agent/LOG.md` for detailed error information.

## Verification Checklist

Before beginning serious pentesting work, verify these components:

- [ ] Docker container is running properly
- [ ] All required tools are accessible
- [ ] YrYs AI agent initializes correctly
- [ ] GUI launches without errors
- [ ] AWS credentials are configured (if needed)
- [ ] Gumroad links are updated (for commercial use)
- [ ] Network connectivity is functional
- [ ] Storage has sufficient free space

## Next Steps

After successful installation, proceed to:
1. [User Manual](user_manual.md) for operational guidance
2. [Configuration Guide](configuration_guide.md) for advanced customization
3. [Security Best Practices](../security/security_best_practices.md) for safe operation

---

*Remember: KaliGhost is a powerful tool designed for authorized security testing. Ensure you have explicit written permission before testing any systems.*