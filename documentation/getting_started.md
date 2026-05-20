# Getting Started with KaliGhost

Welcome to KaliGhost, the cutting-edge penetration testing platform that combines portability, power, and autonomous AI capabilities. This guide provides essential information to help you quickly begin using or contributing to KaliGhost.

## What is KaliGhost?

KaliGhost is an innovative penetration testing operating system built specifically for modern Apple Silicon Macs (M1/M2/M3). Unlike traditional penetration testing distributions that require heavy virtualization, KaliGhost leverages Docker containers and native ARM optimizations to deliver exceptional performance.

### Key Features

#### For Security Professionals
- **Native Performance**: Optimized for Apple Silicon architecture with near-bare-metal speeds
- **Autonomous AI Agent (YrYs)**: Intelligent assistant that can plan and execute security assessments
- **Professional GUI**: Cyberpunk-themed 3D interface with system monitoring capabilities
- **Portable Operation**: Run complete pentesting environment from USB without installation
- **Ghost Mode**: Automatic secure deletion of all traces upon shutdown

#### For Developers
- **Extensible Architecture**: Modular design for easy customization and tool addition
- **Modern Frameworks**: Built with contemporary technologies (Python, PySide6, Docker)
- **API Integration**: Support for cloud AI services like AWS Bedrock
- **Open Source Foundation**: Community-driven development with commercial opportunities

## System Requirements

### Minimum Requirements
- **Operating System**: macOS 11+ (Big Sur) or Linux (Ubuntu 20.04+, Debian, Kali)
- **Processor**: Apple Silicon (M1/M2/M3) or Intel x64
- **Memory**: 4GB RAM (8GB recommended)
- **Storage**: 20GB available space
- **Network**: Internet connection for Docker images and AI models

### Recommended Specifications
- **Memory**: 16GB+ RAM
- **Storage**: 50GB+ SSD
- **GPU**: Any Apple Silicon GPU (for GUI acceleration)

## Quick Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/elkalivpn/KaliGhost.git
   cd KaliGhost
   ```

2. **Verify Docker Installation**
   ```bash
   docker --version
   docker ps
   ```

3. **Launch KaliGhost**
   ```bash
   chmod +x boot/boot.sh
   ./boot.sh
   ```

4. **Access the Environment**
   ```bash
   docker exec -it kali-ghost bash
   ```

## First Steps

### For Users
1. Launch the Professional GUI:
   ```bash
   cd gui
   ./start_professional_gui.sh
   ```
   
2. Start the YrYs AI agent:
   ```bash
   cd YrYs-Agent
   python3 agent.py --auto
   ```

3. Execute your first automated scan:
   ```bash
   python3 agent.py --task "Scan 192.168.1.0/24 for open ports"
   ```

### For Developers
1. Review the architecture documentation in `documentation/developer/`
2. Examine the configuration files in `src/agent/yrays_config.yaml`
3. Explore the GUI source code in `gui/professional_kalighost_gui.py`
4. Check existing tools in `YrYs-Agent/tools/`

## Support Channels

### Community Support
- **GitHub Issues**: Bug reports and feature requests
- **Telegram Group**: Real-time community discussion
- **Documentation**: Comprehensive guides and tutorials

### Commercial Support
- **Premium Support Plans**: SLA-backed assistance for enterprise users
- **Training Programs**: Hands-on workshops and certification courses
- **Custom Development**: Bespoke solutions for specific requirements

## Next Steps

Depending on your role, proceed to the appropriate documentation:

- **Security Professionals**: Visit the [User Manual](user/user_manual.md)
- **Developers**: Review the [Development Guidelines](developer/development_guidelines.md)
- **Administrators**: Examine the [Configuration Guide](user/configuration_guide.md)
- **All Users**: Check the [FAQ](faq.md) for common questions

---

*Note: KaliGhost is intended for authorized security testing only. Always ensure you have proper written authorization before conducting any penetration testing activities.*