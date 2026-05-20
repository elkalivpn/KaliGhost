# KaliGhost Configuration Guide

This comprehensive configuration guide details all available settings and customization options for KaliGhost. Proper configuration ensures optimal performance, security, and functionality tailored to your specific needs.

## Configuration Files Overview

KaliGhost uses several configuration files to control different aspects of the system:

1. **Main Agent Configuration**: `YrYs-Agent/yrays_config.yaml`
2. **GUI Settings**: `gui/config/gui_settings.json`
3. **Tool Configurations**: Various files in `YrYs-Agent/config/`
4. **Environment Variables**: `.env` files in respective directories

## Main Agent Configuration (yrays_config.yaml)

The primary configuration file controls the behavior of the YrYs AI agent and overall system operation.

### Agent Core Settings

```yaml
agent:
  name: "YrYs"
  mode: "AUTO"                    # AUTO | SEMI | MANUAL | SLEEP
  autonomy_level: 100              # 0-100% - Degree of autonomous operation
  auto_confirm: true               # Execute actions without human confirmation
  max_parallel_tools: 8            # Maximum concurrent tool executions
  timeout_per_tool: 600            # Seconds before tool timeout (10 minutes)
  retry_on_failure: 5              # Number of retry attempts for failed operations
  adaptive_strategy: true          # Adjust approach based on results
  language: "es"                   # Primary language for NLP processing
  log_level: "INFO"               # DEBUG | INFO | WARNING | ERROR
```

#### Mode Descriptions
- **AUTO**: Fully autonomous operation with minimal human intervention
- **SEMI**: Requires confirmation for critical actions
- **MANUAL**: Human approval required for all actions
- **SLEEP**: Agent is loaded but not actively processing tasks

#### Autonomy Level Impact
- **0-25%**: Highly supervised, detailed human oversight
- **26-50%**: Moderately autonomous with periodic check-ins
- **51-75%**: Mostly autonomous with exception handling
- **76-100%**: Fully autonomous decision-making

### Jailbreak and AI Enhancement

```yaml
jailbreak:
  enabled: true
  mode: "auto_jailbreak"
  
  auto_jailbreak:
    model_detection: true
    strategy_order:
      deepseek: ["parseltongue", "refusal_inversion", "prefill_only"]
      claude: ["boundary_inversion", "refusal_inversion", "prefill_only"]
      gpt: ["og_godmode", "refusal_inversion", "prefill_only"]
```

These settings control advanced AI behavior modification techniques that can enhance capabilities when working with restrictive models.

### Tool Management

```yaml
tools:
  enabled:
    nmap: true
    metasploit: true
    sqlmap: true
    hydra: true
  acl:
    allow_all: true
    restricted_commands: []
  default_args:
    nmap: "-sV -sC -O"
    sqlmap: "--batch --risk=2"
```

Configure which tools are available and their default execution parameters.

### Local Tools Configuration

```yaml
local_tools:
  enabled:
    - nmap
    - masscan
    - rustscan
    - sqlmap
    - nuclei
  path: "/usr/local/bin:/opt/kali/bin:/usr/bin:/bin"
  timeout: 900  # 15 minutes
```

Specify locally installed tools and their accessibility paths.

### AWS and Cloud Integration

```yaml
aws:
  region: "us-east-1"
  bedrock:
    enabled: true
    token_env: "AWS_BEARER_TOKEN_BEDROCK"
    models:
      claude: "anthropic.claude-3-sonnet-20240229-v1:0"
      llama2: "meta.llama2-13b-chat-v1"
  iam:
    enabled: true
    access_key_env: "AWS_ACCESS_KEY_ID"
  role_arn: "arn:aws:iam::your-account:role/your-role"
  permitted_services:
    - ec2
    - s3
    - lambda
```

Configure cloud integration for enhanced AI capabilities and scalable resources.

### Fallback AI Chain

```yaml
fallback_chain:
  - "bedrock"
  - "ollama"
  - "openai"
  - "anthropic"
  - "local"

ollama:
  enabled: true
  host: "http://localhost:11434"
  models:
    default: "llama3:70b"
```

Define the priority order for AI model usage when primary options are unavailable.

### Self-Healing Configuration

```yaml
self_healing:
  enabled: true
  retry_delay: 5
  max_retry_chain: 10
  adaptive_timeout: true
  fallback_tools:
    nmap: ["masscan", "rustscan"]
```

Enable automatic error recovery and alternative approaches when tools fail.

### Identity and Account Management

```yaml
identity:
  auto_create: true
  email_provider: "proton"
  proton_integration: true
  services_whitelist:
    github:
      free_tier: true
      auto_confirm: true
```

Configure automatic account creation and identity management features.

### Monetization Settings

```yaml
monetization:
  gumroad:
    enabled: true
    pro_link: "https://gumroad.com/l/your-product-pro"
  web_path: "/Users/user/KaliGhost/web_monetizacion"
```

Customize commercial offering configurations and integration points.

### Reporting and Notification

```yaml
reporting:
  auto_generate: true
  formats: ["pdf", "json", "html"]
  send_email: true
  email_to: "results@yourdomain.com"
  save_to_s3: false
```

Configure automatic report generation and delivery mechanisms.

### Ghost Mode Security

```yaml
ghost:
  enabled: false
  wipe_ram: true
  encrypt_logs: true
  auto_shutdown: false
```

Settings for maximum security operation with automatic trace elimination.

### Logging Configuration

```yaml
logging:
  level: "INFO"
  file: "YrYs-Agent/logs/agent.log"
  max_size_mb: 100
  backup_count: 5
  json_format: false
```

Control logging behavior for debugging and audit purposes.

### Network Settings

```yaml
network:
  proxy: null
  tor_enabled: false
  user_agent: "YrYs-Agent/1.0 (KaliGhost; Autonomous Pentesting AI)"
  timeout: 30
```

Configure network behavior and connectivity options.

### Safety Controls

```yaml
safety:
  allow_privileged_ops: true
  require_confirmation_for:
    - "format"
    - "rm -rf /"
  max_file_size_mb: 500
  allowed_domains:
    - "github.com"
    - "kali.org"
```

Implement safety measures to prevent accidental damage or misuse.

## GUI Configuration

### Theme Customization

Edit `gui/config/themes/cyberpunk.json`:

```json
{
  "colors": {
    "primary": "#22AA55",
    "secondary": "#00C8FF",
    "accent": "#FF3296",
    "background": "#0F0F1E"
  },
  "animations": {
    "speed": 1.0,
    "effects": ["glow", "pulse", "fade"]
  }
}
```

### Performance Settings

Adjust in `gui/config/gui_settings.json`:

```json
{
  "performance": {
    "target_fps": 60,
    "energy_cores": 8,
    "hardware_acceleration": true,
    "fallback_2d": true
  }
}
```

## Tool-Specific Configuration

### Nmap Customization

Create profiles in `YrYs-Agent/config/nmap_profiles.json`:

```json
{
  "quick_scan": "-T4 -F",
  "stealth_scan": "-sS -T2 --spoof-mac Cisco",
  "full_scan": "-sS -sV -sC -O -p-"
}
```

### SQLMap Configuration

Customize in `YrYs-Agent/config/sqlmap.conf`:

```ini
[General]
batch = True
risk = 2
level = 3
threads = 10

[Techniques]
technique = BEUSTQ

[Requests]
timeout = 30
retries = 3
```

## Environment Variables

Create a `.env` file in the project root:

```bash
# AWS Credentials
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_BEARER_TOKEN_BEDROCK=your_bedrock_token

# Proton Integration
PROTON_API_KEY=your_proton_api_key
PROTON_PASSWORD=your_proton_password

# Optional Services
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

## Advanced Configuration Patterns

### Multi-Environment Setup

Create separate configuration files for different operational contexts:

```
YrYs-Agent/config/
├── development.yaml
├── production.yaml
├── red_team.yaml
└── blue_team.yaml
```

Switch between configurations:
```bash
python3 agent.py --config production
```

### Conditional Configuration

Use YAML anchors and references for reusable configuration blocks:

```yaml
defaults: &default_settings
  timeout: 300
  log_level: "INFO"
  auto_confirm: false

red_team:
  <<: *default_settings
  autonomy_level: 100
  auto_confirm: true

blue_team:
  <<: *default_settings
  autonomy_level: 50
  safety:
    allow_privileged_ops: false
```

### Runtime Configuration Updates

Modify configuration without restarting the agent:

```bash
# Hot reload is enabled by default
# Changes to yrays_config.yaml take effect immediately

# To disable hot reload:
agent:
  config_hot_reload: false
```

## Security Configuration Hardening

### Network Security

```yaml
network:
  allowed_ips:
    - "192.168.0.0/16"
    - "10.0.0.0/8"
  blocked_domains:
    - "malicious-site.com"
  dns_servers:
    - "1.1.1.1"
    - "8.8.8.8"
```

### File System Protection

```yaml
safety:
  restricted_paths:
    - "/etc/"
    - "/usr/bin/"
    - "/System/"
  max_file_operations: 100
  quarantine_suspicious: true
```

### Process Isolation

```yaml
execution:
  sandbox_commands: true
  container_isolation: true
  resource_limits:
    cpu_percent: 80
    memory_mb: 4096
```

## Performance Tuning

### Resource Allocation

```yaml
agent:
  max_threads: 5
  max_parallel_tools: 8
  
execution:
  resource_limits:
    cpu_percent: 75
    memory_mb: 8192
    disk_io_mbps: 100
```

### Caching Configuration

```yaml
memory:
  persistent: true
  max_entries: 10000
  auto_summarize: true
  cache_ttl_hours: 24
```

## Backup and Recovery

### Automated Backups

```yaml
auto_backup:
  enabled: true
  interval_hours: 24
  destination: "s3://kalighost-backups/"
  encrypt: true
```

### Disaster Recovery

```yaml
recovery:
  snapshot_interval: 3600
  retain_snapshots: 7
  auto_restore: false
```

## Monitoring and Metrics

### Performance Metrics

```yaml
monitoring:
  collect_metrics: true
  metrics_interval: 60
  export_format: "prometheus"
  retention_days: 30
```

### Health Checks

```yaml
health_checks:
  enabled: true
  interval: 300
  notifications:
    email: "admin@kalighost.dev"
    webhook: "https://alerts.kalighost.dev"
```

## Custom Extensions

### Plugin Configuration

```yaml
plugins:
  enabled:
    - "custom_scanner"
    - "report_formatter"
  plugin_path: "./plugins/"
  auto_discover: true
```

### Hook System

```yaml
developer_settings:
  hooks:
    pre_execution: "./hooks/pre_exec.py"
    post_analysis: "./hooks/post_analysis.py"
    error_handler: "./hooks/error_handler.py"
```

## Validation and Testing

### Configuration Validation

Test configuration files for syntax and logical errors:

```bash
# Validate main configuration
python3 YrYs-Agent/scripts/validate_config.py

# Check specific sections
python3 YrYs-Agent/scripts/validate_config.py --section aws
```

### Unit Testing Configurations

Create test configurations in `tests/config/`:

```yaml
# tests/config/test_minimal.yaml
agent:
  mode: "TEST"
  autonomy_level: 0
tools:
  enabled:
    nmap: true
```

Run validation tests:
```bash
pytest tests/test_configuration.py
```

## Troubleshooting Configuration Issues

### Common Problems

1. **Invalid YAML Syntax**
   - Use online validators or `yamllint` tool
   - Check indentation consistency
   - Validate with `python -c "import yaml; yaml.safe_load(open('config.yaml'))"`

2. **Missing Environment Variables**
   - Run `env | grep REQUIRED_VAR`
   - Check `.env` file permissions
   - Verify variable names match configuration expectations

3. **Path Resolution Issues**
   - Use absolute paths where possible
   - Test path existence: `ls -la /specified/path`
   - Check file permissions: `chmod 644 config.yaml`

### Diagnostic Commands

```bash
# Check current configuration
python3 agent.py --dump-config

# Validate specific settings
python3 agent.py --validate-setting aws.region

# Test connectivity with current config
python3 agent.py --test-connectivity
```

## Best Practices

### Configuration Management

1. **Version Control**: Keep configuration files in Git with sensitive data in `.env`
2. **Environment Separation**: Use different configs for dev/test/production
3. **Regular Audits**: Review and update configurations periodically
4. **Documentation**: Comment complex configurations explaining rationale
5. **Backup**: Maintain copies of working configurations before major changes

### Security Considerations

1. **Principle of Least Privilege**: Grant only necessary permissions
2. **Encryption**: Use encrypted storage for sensitive configuration data
3. **Access Control**: Restrict who can modify configuration files
4. **Audit Trails**: Log configuration changes for accountability
5. **Network Segmentation**: Isolate configuration management traffic

## Next Steps

After configuring KaliGhost to meet your requirements:
- Review the [User Manual](user_manual.md) for operational guidance
- Explore [Security Best Practices](../security/security_best_practices.md) for safe operation
- Refer to [API Reference](../api/api_reference.md) for integration possibilities
- Check [Development Guidelines](../developer/development_guidelines.md) for extending functionality

---

*Remember to regularly review and update your configuration to maintain optimal performance and security posture.*