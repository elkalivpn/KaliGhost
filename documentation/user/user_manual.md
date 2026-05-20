# KaliGhost User Manual

This comprehensive user manual provides detailed guidance on operating KaliGhost for penetration testing and security assessment activities. It covers all aspects of daily usage, from launching the interface to performing complex security evaluations.

## Table of Contents

1. [Launching KaliGhost](#launching-kalighost)
2. [Interface Overview](#interface-overview)
3. [Using the YrYs AI Agent](#using-the-yr ys-ai-agent)
4. [Performing Security Assessments](#performing-security-assessments)
5. [Working with Tools](#working-with-tools)
6. [Generating Reports](#generating-reports)
7. [Ghost Mode Operations](#ghost-mode-operations)
8. [Advanced Features](#advanced-features)

## Launching KaliGhost

### Starting the Environment

To begin using KaliGhost, you first need to launch the Docker container environment:

```bash
# Navigate to KaliGhost directory
cd ~/KaliGhost

# Start the container
./boot.sh

# Access the KaliLinux environment
docker exec -it kali-ghost bash
```

### Launching the Professional GUI

The KaliGhost Professional GUI provides a cyberpunk-themed interface with advanced visualization capabilities:

```bash
# From within the KaliGhost environment
cd gui
./start_professional_gui.sh
```

The GUI will launch with:
- 3D animated cyber dragon visualization
- Real-time system monitoring
- Tool access panels
- Operation console

## Interface Overview

### Professional GUI Components

#### Main 3D Viewport
- **Interactive Dragon**: Real-time 3D rendering with OpenGL acceleration
- **Energy Core Particles**: Orbiting visual effects indicating system status
- **HUD Overlay**: System status information and performance metrics
- **Camera Controls**: Rotate, zoom, and pan viewing perspectives

#### Dashboard Panels
1. **System Status Panel** (Left Side)
   - Agent status indicators
   - Resource usage meters (CPU, Memory)
   - Mission control buttons (Start/Stop operations)
   - Security mode toggle (Ghost Mode)

2. **Tools Panel** (Right Side)
   - Reconnaissance tools (Scanners, Enumerators)
   - Exploitation frameworks (Metasploit, SQLMap)
   - Fuzzing utilities (WFuzz, Dirsearch)
   - Post-exploitation tools (Mimikatz variants)

3. **Console Panel** (Bottom)
   - Real-time system logs
   - Operation status updates
   - Error reporting
   - Debug information

### Command-Line Interface

For users preferring CLI interaction:

```bash
# Direct agent access
cd YrYs-Agent
python3 agent.py [options]

# Available options:
# --auto: Autonomous operation mode
# --task "<description>": Specific task execution
# --debug: Enable detailed logging
# --help: Show all available options
```

## Using the YrYs AI Agent

### Autonomous Operation Mode

The YrYs agent can operate in fully autonomous mode, planning and executing security assessments with minimal human intervention:

```bash
# Launch in autonomous mode
python3 agent.py --auto

# Agent will automatically:
# 1. Identify network targets
# 2. Plan appropriate scanning strategy
# 3. Execute selected tools
# 4. Analyze results
# 5. Generate reports
```

### Task-Based Interaction

Submit specific tasks to the AI agent using natural language:

```bash
# Example tasks
python3 agent.py --task "Scan the network 192.168.1.0/24 and identify web servers"

python3 agent.py --task "Perform a comprehensive vulnerability assessment on target server"

python3 agent.py --task "Test for SQL injection vulnerabilities on the login form"
```

### Semi-Autonomous Mode

For controlled operation where human approval is required for critical actions:

```bash
# Configure in yrays_config.yaml
agent:
  mode: "SEMI"  # Requires human confirmation for dangerous operations
  auto_confirm: false
```

## Performing Security Assessments

### Network Discovery

Begin any assessment with reconnaissance:

```bash
# Using the AI agent
python3 agent.py --task "Discover all devices on network 192.168.1.0/24"

# Using classic tools
nmap -sn 192.168.1.0/24
arp-scan --local
```

### Port Scanning

Detailed port analysis:

```bash
# Standard service detection
nmap -sV -sC 192.168.1.100

# Fast scanning with Masscan
masscan -p1-65535 192.168.1.100

# Modern approach with Rustscan
rustscan -a 192.168.1.100 --ulimit 5000
```

### Web Application Testing

Web-focused assessments:

```bash
# Directory brute-forcing
ffuf -u http://target.com/FUZZ -w /path/to/wordlist.txt

# Vulnerability scanning
nikto -h http://target.com

# SQL injection testing
sqlmap -u "http://target.com/vuln.php?id=1" --batch --risk=3
```

### Wireless Security Testing

Wi-Fi security evaluations:

```bash
# Monitor mode setup (requires compatible adapter)
airmon-ng start wlan0

# Network discovery
airodump-ng wlan0mon

# Capture handshake
airodump-ng -c <channel> --bssid <target_mac> -w capture wlan0mon
```

## Working with Tools

### Tool Categories

#### Reconnaissance
- Nmap: Network discovery and port scanning
- Masscan: Ultra-fast port scanner
- Rustscan: Modern Rust-based scanner
- DNS enumeration tools

#### Vulnerability Assessment
- Nuclei: Template-based vulnerability scanner
- Nikto: Web server scanner
- OpenVAS: Comprehensive vulnerability assessment

#### Exploitation
- Metasploit Framework: Exploitation and post-exploitation
- SQLMap: Automated SQL injection
- Hydra: Password brute-forcing
- John the Ripper: Password cracking

#### Post-Exploitation
- Mimikatz: Windows credential extraction
- PowerShell Empire: Post-exploitation framework
- BloodHound: Active Directory analysis

### Managing Tools

#### Updating Tools
```bash
# Update all tools
./scripts/update_tools.sh

# Update specific tool
apt update && apt upgrade metasploit-framework
```

#### Adding Custom Tools
```bash
# Install from package manager
apt install custom-tool-name

# Install from source
git clone https://github.com/user/custom-tool.git
cd custom-tool
make && sudo make install
```

## Generating Reports

### Automated Reporting

Reports are automatically generated after assessments:

```bash
# Reports are saved in:
# /root/KaliGhost/reports/

# Available formats:
# - PDF: Professional presentation-ready documents
# - HTML: Interactive web-based reports
# - JSON: Structured data for processing
# - Markdown: Simple text-based format
```

### Customizing Reports

Modify report templates in `YrYs-Agent/templates/`:

- `report_template.html`: Web-based template
- `report_template.tex`: LaTeX template for PDF generation
- `executive_summary.md`: Executive summary format

### Sending Reports

Configure automatic report delivery:

```yaml
# In yrays_config.yaml
reporting:
  auto_generate: true
  formats: ["pdf", "json", "html"]
  send_email: true
  email_to: "analyst@company.com"
  save_to_s3: true
  s3_bucket: "security-reports-bucket"
```

## Ghost Mode Operations

### Activating Ghost Mode

Ghost Mode enables maximum security by automatically wiping all traces upon shutdown:

```bash
# Enable in configuration
nano YrYs-Agent/yrays_config.yaml

ghost:
  enabled: true
  wipe_ram: true
  encrypt_logs: true
  auto_shutdown: true
  ephemeral_fs: true
```

### Ghost Mode Features

When Ghost Mode is active:
- All volatile memory is cleared on shutdown
- Logs are encrypted and optionally deleted
- Network configurations are reset
- Temporary files are securely erased
- System states are not preserved between sessions

### Using Ghost Mode Safely

Important considerations when using Ghost Mode:
1. Always save important data externally before shutdown
2. Configure automatic report export to external storage
3. Ensure internet connectivity for cloud backups if needed
4. Test shutdown procedures to verify proper cleanup

## Advanced Features

### Cloud Integration

Enhance capabilities with AWS Bedrock integration:

```yaml
# AWS configuration
aws:
  region: "us-east-1"
  bedrock:
    enabled: true
    models:
      claude: "anthropic.claude-3-sonnet-20240229-v1:0"
      llama2: "meta.llama2-13b-chat-v1"
```

Benefits of cloud integration:
- Access to more powerful AI models
- Scalable computing resources
- Persistent knowledge storage
- Collaborative analysis capabilities

### Multi-Agent Collaboration

Coordinate multiple YrYs agents for complex assessments:

```bash
# Launch coordinator agent
python3 coordinator.py --targets "target1,target2,target3"

# Coordinator will distribute tasks among worker agents
# and aggregate results for comprehensive reporting
```

### Automated Identity Management

KaliGhost can automatically create and manage service accounts:

```yaml
# Identity configuration
identity:
  auto_create: true
  email_provider: "proton"
  proton_integration: true
  services_whitelist:
    github:
      auto_confirm: true
    hackerone:
      auto_confirm: true
```

Capabilities include:
- Proton email account creation
- GitHub account provisioning
- Bug bounty platform registration
- API key management through Proton Vault

## Daily Operations Workflow

### Morning Startup

1. Launch KaliGhost container
2. Start Professional GUI
3. Initialize YrYs agent
4. Verify tool availability
5. Check pending tasks

### During Operations

1. Monitor system resources
2. Review AI agent recommendations
3. Validate critical actions in semi-autonomous mode
4. Document findings in real-time
5. Adjust scanning parameters as needed

### End of Day Procedures

1. Generate and export reports
2. Backup important findings externally
3. Clean up temporary files
4. Deactivate Ghost Mode (if used)
5. Shut down environment securely

## Best Practices

### Operational Security

1. Always use VPN or Tor for sensitive operations
2. Regularly update tools and signatures
3. Maintain separate environments for different clients
4. Encrypt all stored data and reports
5. Use strong authentication for all services

### Performance Optimization

1. Monitor resource utilization during scans
2. Adjust parallel processing settings based on system capacity
3. Use appropriate scan intensity for target environment
4. Schedule resource-intensive operations during off-peak hours
5. Regularly clean temporary files and logs

### Legal Compliance

1. Obtain written authorization before testing any system
2. Document all activities thoroughly
3. Follow responsible disclosure practices
4. Respect privacy and data protection regulations
5. Maintain professional liability insurance

## Troubleshooting

### Common Issues

#### Slow Performance
- Reduce animation complexity in GUI
- Lower energy_cores count in 3D renderer
- Reduce frame rate target
- Close unnecessary background processes

#### Connection Problems
- Verify Docker network configuration
- Check firewall rules
- Test internet connectivity
- Validate proxy settings if applicable

#### AI Agent Errors
- Check AWS credentials and permissions
- Verify Bedrock model access
- Review configuration file syntax
- Examine detailed logs for specific errors

## Next Steps

Further enhance your KaliGhost experience by exploring:
- [Configuration Guide](configuration_guide.md) for advanced customization
- [API Reference](../api/api_reference.md) for integration possibilities
- [Security Best Practices](../security/security_best_practices.md) for safe operation
- [Development Guidelines](../developer/development_guidelines.md) for extending functionality

---

*Remember: KaliGhost provides powerful capabilities that must be used responsibly and ethically. Always ensure you have explicit written authorization before conducting any security assessments.*