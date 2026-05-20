# KaliGhost Troubleshooting Guide

This comprehensive troubleshooting guide helps you resolve common issues encountered while using KaliGhost. Solutions are organized by category to help you quickly find and fix problems.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Docker-Related Problems](#docker-related-problems)
3. [GUI and Display Issues](#gui-and-display-issues)
4. [YrYs AI Agent Problems](#yr ys-ai-agent-problems)
5. [Tool and Functionality Issues](#tool-and-functionality-issues)
6. [Network and Connectivity](#network-and-connectivity)
7. [Performance Problems](#performance-problems)
8. [Security and Ghost Mode](#security-and-ghost-mode)
9. [Cloud Integration Issues](#cloud-integration-issues)
10. [General Tips and Best Practices](#general-tips-and-best-practices)

## Installation Issues

### Problem: Repository Cloning Fails

**Symptoms**: 
- `git clone` command times out
- Authentication errors
- Permission denied messages

**Solutions**:
```bash
# Check internet connectivity
ping github.com

# Try HTTPS instead of SSH
git clone https://github.com/elkalivpn/KaliGhost.git

# Configure Git proxy if needed
git config --global http.proxy http://proxy.company.com:8080

# Increase Git buffer size for large repositories
git config --global http.postBuffer 524288000
```

### Problem: Missing Dependencies

**Symptoms**:
- Commands not found
- Import errors in Python
- GUI fails to launch

**Solutions**:
```bash
# Install core dependencies
sudo apt update
sudo apt install git docker.io docker-compose python3-pip

# macOS with Homebrew
brew install git docker docker-compose

# Verify Docker installation
docker --version
docker-compose --version
```

### Problem: Insufficient Disk Space

**Symptoms**:
- Installation fails midway
- "No space left on device" errors
- Docker build failures

**Solutions**:
```bash
# Check available disk space
df -h

# Clean up Docker images and containers
docker system prune -a

# Remove unused volumes
docker volume prune

# Free up space by removing old Docker images
docker image ls
docker image rm [IMAGE_ID]
```

## Docker-Related Problems

### Problem: Docker Daemon Not Running

**Symptoms**:
- `Cannot connect to the Docker daemon` error
- `docker ps` returns connection errors
- KaliGhost boot script fails

**Solutions**:
```bash
# macOS - Start Docker Desktop
open -a Docker
# Wait for the whale icon to stop animating

# Linux - Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group (Linux)
sudo usermod -aG docker $USER
# Log out and back in for changes to take effect

# Verify Docker is running
docker info
```

### Problem: Container Fails to Start

**Symptoms**:
- `docker: Error response from daemon` messages
- Port binding conflicts
- Container exits immediately

**Solutions**:
```bash
# Check running containers
docker ps -a

# View container logs
docker logs kali-ghost

# Check for port conflicts
lsof -i :22
lsof -i :80
lsof -i :443

# Stop conflicting processes
kill -9 [PROCESS_ID]

# Use alternative ports in docker-compose.yml
# ports:
#   - "2222:22"
#   - "8080:80"
#   - "8443:443"
```

### Problem: Permission Denied Accessing Container

**Symptoms**:
- `Permission denied` when running `docker exec`
- Unable to access container filesystem
- Commands fail with access errors

**Solutions**:
```bash
# Check container status
docker ps | grep kali-ghost

# Restart container if stopped
docker start kali-ghost

# Use root user explicitly
docker exec -u root -it kali-ghost bash

# Check user permissions inside container
docker exec -it kali-ghost id

# Add user to appropriate groups
docker exec -u root kali-ghost usermod -aG sudo [username]
```

## GUI and Display Issues

### Problem: GUI Fails to Launch

**Symptoms**:
- Black or blank screen
- OpenGL errors
- Missing PySide6 libraries

**Solutions**:
```bash
# Check OpenGL support
glxinfo | grep "OpenGL version"

# Install missing GUI dependencies (Linux)
sudo apt install python3-pyside6 python3-opengl libgl1-mesa-dev

# macOS specific fix
export QT_MAC_WANTS_LAYER=1

# Try 2D fallback mode
# Edit gui/professional_kalighost_gui.py
# Set OPENGL_AVAILABLE = False temporarily
```

### Problem: Slow GUI Performance

**Symptoms**:
- Laggy animations
- Low frame rates
- Unresponsive interface

**Solutions**:
```bash
# Reduce animation complexity
# Edit gui/config/gui_settings.json
{
  "performance": {
    "target_fps": 30,
    "energy_cores": 4,
    "effects": ["glow"]  # Reduce effects
  }
}

# Close other resource-intensive applications
# Ensure adequate RAM (8GB+ recommended)

# Check GPU acceleration
glxinfo | grep -i "direct rendering"
```

### Problem: 3D Rendering Errors

**Symptoms**:
- Visual artifacts
- Segmentation faults
- Missing textures or models

**Solutions**:
```bash
# Update graphics drivers
# Linux:
sudo ubuntu-drivers autoinstall

# Check OpenGL version requirement
# Minimum OpenGL 2.0 required, 4.0+ recommended

# Run with software rendering as fallback
export LIBGL_ALWAYS_SOFTWARE=1
./gui/start_professional_gui.sh
```

## YrYs AI Agent Problems

### Problem: Agent Fails to Initialize

**Symptoms**:
- Import errors
- Configuration file issues
- Missing dependencies

**Solutions**:
```bash
# Check Python environment
python3 --version
pip3 list | grep -E "(openai|anthropic| boto)"

# Install missing dependencies
cd YrYs-Agent
pip3 install -r requirements.txt

# Validate configuration file
python3 scripts/validate_config.py

# Check YAML syntax
python3 -c "import yaml; yaml.safe_load(open('yrays_config.yaml'))"
```

### Problem: AI Model Connection Failures

**Symptoms**:
- Timeout errors connecting to AI services
- Invalid API key messages
- Model not found errors

**Solutions**:
```bash
# Verify API keys in environment
echo $OPENAI_API_KEY
echo $AWS_BEARER_TOKEN_BEDROCK

# Test connectivity
curl -v https://api.openai.com/v1/models
curl -v -H "Authorization: Bearer $AWS_BEARER_TOKEN_BEDROCK" \
  https://bedrock-runtime.us-east-1.amazonaws.com/model/...

# Check firewall/proxy settings
# Ensure outbound connections to AI service endpoints

# Verify model availability in region
# Some models are only available in specific regions
```

### Problem: Agent Produces Unexpected Results

**Symptoms**:
- Incorrect tool selection
- Misunderstood commands
- Irrelevant responses

**Solutions**:
```bash
# Check agent mode in configuration
# AUTO mode may be too aggressive for complex tasks

# Try SEMI mode for better control
agent:
  mode: "SEMI"
  auto_confirm: false

# Provide more specific instructions
# Instead of "scan the network"
# Use "perform a SYN scan of 192.168.1.0/24 using nmap"

# Review jailbreak settings if using restrictive models
jailbreak:
  enabled: false  # Try disabling for more predictable behavior
```

## Tool and Functionality Issues

### Problem: Tools Not Found or Not Working

**Symptoms**:
- "Command not found" errors
- Tools exit with errors
- Unexpected output format

**Solutions**:
```bash
# Verify tool installation
which nmap
which sqlmap
which metasploit-framework

# Update tools to latest versions
apt update && apt upgrade

# Reinstall problematic tools
apt remove [tool-name]
apt install [tool-name]

# Check tool dependencies
ldd $(which nmap)  # Check shared library dependencies
```

### Problem: Metasploit Framework Issues

**Symptoms**:
- Database connection failures
- Module loading errors
- Payload generation problems

**Solutions**:
```bash
# Initialize MSF database
msfdb init

# Check database status
msfdb status

# Rebuild database if corrupted
msfdb reinit

# Update Metasploit
msfupdate

# Check PostgreSQL service (dependency)
sudo systemctl status postgresql
sudo systemctl start postgresql
```

### Problem: Nmap Scan Issues

**Symptoms**:
- Slow scans
- Permission denied errors
- Incomplete results

**Solutions**:
```bash
# Run with appropriate privileges
sudo nmap -sS target  # SYN scan requires root

# Adjust timing parameters
nmap -T3 target  # Slower but more reliable than -T4/-T5

# Use alternative scan techniques
nmap -sT target  # TCP connect scan (no root required)
nmap -sn target  # Host discovery only

# Check for firewall interference
# Try different source ports
nmap --source-port 53 target  # DNS port often allowed
```

## Network and Connectivity

### Problem: Internet Access Issues

**Symptoms**:
- Failed software updates
- Cloud service connection failures
- Download timeouts

**Solutions**:
```bash
# Test basic connectivity
ping 8.8.8.8
ping google.com

# Check DNS resolution
nslookup google.com
dig google.com

# Verify proxy settings if applicable
echo $http_proxy
echo $https_proxy

# Test specific service connectivity
curl -v https://github.com
curl -v https://api.openai.com
```

### Problem: Docker Network Issues

**Symptoms**:
- Containers cannot reach internet
- Host cannot reach containers
- Port mapping problems

**Solutions**:
```bash
# Check Docker network configuration
docker network ls
docker network inspect bridge

# Test container networking
docker run --rm alpine ping -c 4 google.com

# Restart Docker networking
sudo systemctl restart docker

# Flush iptables rules if customized
sudo iptables -F
```

### Problem: Proxy Configuration

**Symptoms**:
- All external requests fail
- Specific error messages about proxy
- Corporate network restrictions

**Solutions**:
```bash
# Set proxy environment variables
export http_proxy=http://proxy.company.com:8080
export https_proxy=http://proxy.company.com:8080
export no_proxy="localhost,127.0.0.1,localaddress,.localdomain.com"

# Configure Docker daemon for proxy
# Create/edit /etc/docker/daemon.json:
{
  "proxies": {
    "default": {
      "httpProxy": "http://proxy.company.com:8080",
      "httpsProxy": "http://proxy.company.com:8080",
      "noProxy": "localhost,127.0.0.1"
    }
  }
}

# Restart Docker after changes
sudo systemctl restart docker
```

## Performance Problems

### Problem: High CPU Usage

**Symptoms**:
- System becomes unresponsive
- Fans running at high speed
- Operations taking unusually long

**Solutions**:
```bash
# Monitor resource usage
top
htop
docker stats

# Limit concurrent operations
# In yrays_config.yaml:
agent:
  max_parallel_tools: 2  # Reduce from default of 8

# Adjust tool-specific settings
nmap --host-timeout 30m  # Limit individual scan time
sqlmap --threads 5       # Reduce concurrent threads

# Check for infinite loops or stuck processes
ps aux | grep -E "(nmap|sqlmap|metasploit)"
kill -9 [STUCK_PROCESS_PID]
```

### Problem: Memory Exhaustion

**Symptoms**:
- Out of memory errors
- System swapping heavily
- Applications crashing unexpectedly

**Solutions**:
```bash
# Monitor memory usage
free -h
docker stats

# Limit memory allocation
# In docker-compose.yml:
services:
  kali-ghost:
    mem_limit: 8g  # Limit to 8GB

# Optimize tool usage
# Reduce wordlist sizes for fuzzing tools
ffuf -w smaller-wordlist.txt

# Limit scope of operations
# Scan smaller IP ranges or fewer ports
nmap -p 1-1000 target  # Instead of -p-
```

### Problem: Slow Tool Execution

**Symptoms**:
- Scans taking hours to complete
- Tools hanging or freezing
- Poor throughput on network operations

**Solutions**:
```bash
# Optimize scan parameters
nmap -T3 target  # Conservative timing
masscan --rate 1000 target  # Limit packets per second

# Check network bandwidth
iperf3 -c speedtest.server.com

# Use local tools instead of cloud when possible
# Local processing is often faster than cloud round-trips

# Parallelize appropriately
# Balance between concurrency and resource contention
```

## Security and Ghost Mode

### Problem: Ghost Mode Not Cleaning Up

**Symptoms**:
- Files remaining after shutdown
- Memory not cleared properly
- Network traces persisting

**Solutions**:
```bash
# Verify ghost mode configuration
# In yrays_config.yaml:
ghost:
  enabled: true
  wipe_ram: true
  auto_shutdown: true

# Manually trigger cleanup
./scripts/manual_cleanup.sh

# Check for locked files preventing deletion
lsof /path/to/kalighost

# Ensure proper shutdown procedure
# Don't kill -9 the container, use docker stop instead
```

### Problem: Encryption Failures

**Symptoms**:
- Failed to encrypt logs
- Password prompts not working
- LUKS mounting issues

**Solutions**:
```bash
# Check encryption configuration
# Ensure proper password handling
# Verify LUKS setup if using portable installation

# Test encryption functionality
echo "test" | openssl enc -aes-256-cbc -pass pass:testpassword

# Check available encryption tools
which cryptsetup
which openssl
```

### Problem: Permission and Access Control Issues

**Symptoms**:
- Unauthorized access attempts
- Permission denied on sensitive operations
- Security alerts triggering

**Solutions**:
```bash
# Review safety configuration
# In yrays_config.yaml:
safety:
  allow_privileged_ops: false  # Restrict if needed
  require_confirmation_for:
    - "rm -rf /"
    - "format"

# Check file permissions
ls -la sensitive_files
chmod 600 sensitive_files

# Audit access logs
tail -f /var/log/auth.log
```

## Cloud Integration Issues

### Problem: AWS Bedrock Connection Failures

**Symptoms**:
- Authentication errors
- Service unavailable messages
- Region-specific problems

**Solutions**:
```bash
# Verify AWS credentials
echo $AWS_ACCESS_KEY_ID
echo $AWS_BEARER_TOKEN_BEDROCK

# Check region configuration
# Bedrock availability varies by region
# us-east-1, us-west-2, eu-central-1 commonly available

# Test with AWS CLI
aws bedrock list-models --region us-east-1

# Verify IAM permissions
# Bedrock requires specific policy attachments
```

### Problem: Proton Integration Issues

**Symptoms**:
- Failed account creation
- Credential storage problems
- Email verification delays

**Solutions**:
```bash
# Verify Proton API key
echo $PROTON_API_KEY

# Check Proton service status
# Visit protonstatus.com or community forums

# Test API connectivity
curl -H "X-API-Key: $PROTON_API_KEY" \
  https://api.proton.me/core/v4/status

# Review identity configuration
# In yrays_config.yaml:
identity:
  proton_integration: true
  proton_email: "agent@kalighost.dev"
```

### Problem: Ollama Local Model Issues

**Symptoms**:
- Models failing to load
- Insufficient system resources
- Download failures

**Solutions**:
```bash
# Check Ollama service status
ollama list

# Pull required models manually
ollama pull llama3:70b
ollama pull mistral:7b

# Check system resources
# Large models require significant RAM
# llama3:70b needs ~80GB RAM for full context

# Use quantized versions for limited hardware
ollama pull llama3:8b-instruct-q8_0  # Smaller, 8-bit quantized
```

## General Tips and Best Practices

### Preventive Maintenance

```bash
# Regular cleanup schedule
# Add to crontab:
0 2 * * 0 docker system prune -f  # Weekly Docker cleanup
0 3 * * * find /tmp -type f -mtime +7 -delete  # Clean old temp files

# Update tools regularly
./scripts/update_tools.sh

# Backup configurations
cp YrYs-Agent/yrays_config.yaml YrYs-Agent/yrays_config.backup.$(date +%Y%m%d)
```

### Diagnostic Commands

```bash
# System information
uname -a
df -h
free -h
docker info

# KaliGhost specific diagnostics
./scripts/diagnose.sh

# Check for known issues
./scripts/check_issues.sh
```

### Log Analysis

```bash
# Agent logs
tail -f YrYs-Agent/logs/agent.log

# Docker logs
docker logs -f kali-ghost

# System logs
tail -f /var/log/syslog

# Filter specific errors
grep -i "error" YrYs-Agent/logs/*.log
```

### Performance Monitoring

```bash
# Real-time monitoring
htop
iotop
docker stats

# Long-term monitoring
# Install and configure Prometheus + Grafana
# For detailed performance dashboards
```

## When to Seek Additional Help

If you've tried the above solutions and are still experiencing problems:

1. **Check GitHub Issues**: Search existing reports at https://github.com/elkalivpn/KaliGhost/issues
2. **Community Support**: Join the Telegram group @elkalivpn for real-time assistance
3. **Documentation Review**: Ensure you're following the latest instructions
4. **Provide Detailed Information**: When seeking help, include:
   - KaliGhost version (`git rev-parse HEAD`)
   - Operating system details (`uname -a`)
   - Exact error messages
   - Steps to reproduce the issue
   - Relevant log excerpts

## Creating Useful Bug Reports

When submitting issues, include this information:

```bash
# Essential debugging information
echo "KaliGhost Version: $(git rev-parse HEAD)"
echo "OS: $(uname -a)"
echo "Docker Version: $(docker --version)"
echo "Python Version: $(python3 --version)"

# Relevant environment variables (without values)
env | grep -E "(AWS|OPENAI|PROTON)" | cut -d= -f1

# Recent log entries
tail -20 YrYs-Agent/logs/agent.log
```

---

*Remember: KaliGhost is a powerful security tool that must be used responsibly. Ensure you have proper authorization before troubleshooting on any networks or systems.*