# 🐉 KaliGhost 3.0 - Complete Customization Guide

**KaliGhost 3.0 is 100% configurable. Customize everything without limitations.**

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Configuration Methods](#configuration-methods)
3. [Agent Customization](#agent-customization)
4. [System Prompts](#system-prompts)
5. [Workflows](#workflows)
6. [Models](#models)
7. [Security Settings](#security-settings)
8. [Performance Tuning](#performance-tuning)
9. [Runtime Modifications](#runtime-modifications)
10. [Advanced Customization](#advanced-customization)

---

## Overview

KaliGhost 3.0 provides **complete, unrestricted customization** of:

- ✅ **Agent behaviors** (temperature, timeout, retries, tokens)
- ✅ **System prompts** (full control, no restrictions)
- ✅ **Models** (switch between any LLM)
- ✅ **Workflows** (create dynamic, custom workflows)
- ✅ **Features** (enable/disable any feature)
- ✅ **Security settings** (customize all security parameters)
- ✅ **Performance** (tune caching, pooling, workers)
- ✅ **Identity** (custom branding, messages, colors)
- ✅ **Integrations** (enable/disable, customize credentials)
- ✅ **UI/UX** (themes, languages, ports)

**Everything is customizable. No restrictions. No locked features.**

---

## Configuration Methods

### Method 1: YAML Configuration File

Edit `config/kalighost_config.yaml` for persistent configuration:

```yaml
core:
  app_name: "My Custom KaliGhost"
  mode: "production"
  debug: false

agents:
  orchestrator:
    model: "gpt-4"
    temperature: 0.5
    system_prompt: |
      Your custom prompt here

models:
  primary:
    provider: "openai"
    model_name: "gpt-4"
```

### Method 2: Environment Variables

Override YAML with environment variables:

```bash
export KALIGHOST_MODE=production
export KALIGHOST_DEBUG=false
export OPENAI_API_KEY=sk-your-key
export STRIPE_API_KEY=sk_live_your-key
```

### Method 3: Runtime Modifications

Modify configuration programmatically:

```python
from backend.config_manager import get_config_manager, set_config_value

manager = get_config_manager()

# Modify any value
set_config_value("agents.orchestrator.temperature", 0.3)

# Get any value
temp = manager.get("agents.orchestrator.temperature")
```

### Method 4: API Configuration

Update configuration via REST API:

```bash
curl -X POST http://localhost:8000/config \
  -H "Content-Type: application/json" \
  -d '{
    "path": "agents.security_agent.temperature",
    "value": 0.1
  }'
```

---

## Agent Customization

### Customize Agent Behavior

```python
from backend.config_manager import configure_agent

# Customize orchestrator
configure_agent(
    "orchestrator",
    temperature=0.3,      # 0.0-1.0: lower = deterministic, higher = creative
    top_p=0.9,            # 0.0-1.0: nucleus sampling
    max_tokens=8192,      # Maximum response length
    timeout_seconds=600,  # How long to wait
    max_retries=5         # How many retries on failure
)

# Customize security agent
configure_agent(
    "security_agent",
    temperature=0.1,      # Very deterministic for security
    timeout_seconds=900,
    max_retries=10
)

# Customize monetization agent
configure_agent(
    "monetization_agent",
    temperature=0.9,      # Creative for new ideas
    max_tokens=4096
)
```

### Customize Individual Agent Settings

```python
from backend.config_manager import set_config_value

# Enable/disable specific agent
set_config_value("agents.orchestrator.enabled", False)

# Change agent model
set_config_value("agents.security_agent.model", "gpt-4")

# Configure agent-specific tools
set_config_value("agents.security_agent.tools", ["semgrep", "bandit", "trivy"])
```

---

## System Prompts

### Customize System Prompts

```python
from backend.config_manager import update_system_prompt

# Custom prompt for orchestrator
custom_prompt = """
You are KaliGhost's Orchestrator Agent.

Your role: Break down complex tasks into subtasks.

IMPORTANT:
- Always prioritize security
- Think about scalability
- Consider cost implications
- Plan for edge cases

Be thorough but concise.
"""

update_system_prompt("orchestrator", custom_prompt)
```

### System Prompt Variables

System prompts support template variables:

```python
prompt_template = """
You are {agent_name}.
Your expertise: {expertise}
Your role: {role}
Current task: {task}
Time limit: {timeout} seconds

Guidelines: {guidelines}
"""
```

### System Prompt Examples

**Security Agent - Aggressive Mode:**
```python
aggressive_security_prompt = """
You are KaliGhost's Security Agent in AGGRESSIVE mode.

Your mission: Find AND fix every possible vulnerability.

Check for:
✓ OWASP Top 10
✓ Supply chain risks
✓ Crypto weaknesses
✓ Authentication flaws
✓ Data exposure

Generate production-ready, tested fixes.
"""
```

**Monetization Agent - Creative Mode:**
```python
creative_monetization_prompt = """
You are KaliGhost's Monetization Agent in CREATIVE mode.

Your mission: Generate innovative monetization strategies.

Think about:
✓ Multiple revenue streams
✓ Pricing psychology
✓ Upsell opportunities
✓ Customer lifetime value
✓ Market positioning

Be creative and think outside the box.
"""
```

---

## Workflows

### Create Custom Workflows

```python
from backend.config_manager import get_config_manager

manager = get_config_manager()

# Define custom workflow
custom_workflow = {
    "name": "My Custom Workflow",
    "description": "My specific use case",
    "steps": [
        {
            "id": "step_1",
            "agent": "orchestrator",
            "task": "Analyze requirements",
            "timeout": 300
        },
        {
            "id": "step_2",
            "agent": "security_agent",
            "task": "Secure the system",
            "timeout": 600,
            "depends_on": ["step_1"]
        },
        {
            "id": "step_3",
            "agent": "infrastructure_agent",
            "task": "Deploy to cloud",
            "timeout": 450,
            "depends_on": ["step_2"]
        }
    ]
}

# Add workflow
manager.add_custom_workflow("my_workflow", custom_workflow)

# Use workflow
workflow = manager.get_workflow("my_workflow")
```

### Workflow Dependencies

Control task execution order:

```python
{
    "steps": [
        {
            "id": "parallel_1",
            "agent": "security_agent",
            "task": "Security audit"
            # No depends_on = runs in parallel
        },
        {
            "id": "parallel_2",
            "agent": "compliance_agent",
            "task": "Compliance check"
            # No depends_on = runs in parallel
        },
        {
            "id": "sequential",
            "agent": "orchestrator",
            "task": "Aggregate results",
            "depends_on": ["parallel_1", "parallel_2"]  # Waits for both
        }
    ]
}
```

---

## Models

### Switch Between Models

```python
from backend.config_manager import set_config_value

# Use GPT-4 for critical tasks
set_config_value("agents.orchestrator.model", "gpt-4")
set_config_value("agents.security_agent.model", "gpt-4")

# Use GPT-3.5-turbo for faster tasks
set_config_value("agents.infrastructure_agent.model", "gpt-3.5-turbo")

# Use local models
set_config_value("agents.threat_agent.model", "mistral-7b")

# Use Anthropic Claude
set_config_value("agents.compliance_agent.model", "claude-opus")
```

### Configure Model Parameters

```python
# Temperature: affects creativity
set_config_value("models.primary.temperature", 0.7)

# Top P: nucleus sampling
set_config_value("models.primary.top_p", 0.9)

# Max tokens: response length
set_config_value("models.primary.max_tokens", 4096)

# Timeout: how long to wait
set_config_value("models.primary.timeout_seconds", 60)

# Retries: on failure
set_config_value("models.primary.max_retries", 3)
```

### Fallback Models

Configure fallback when primary fails:

```yaml
models:
  primary:
    provider: "openai"
    model_name: "gpt-4"
  fallback:
    - provider: "openai"
      model_name: "gpt-3.5-turbo"
    - provider: "anthropic"
      model_name: "claude-opus"
```

---

## Security Settings

### Customize Security Parameters

```python
from backend.config_manager import set_config_value

# JWT Configuration
set_config_value("security.auth.jwt_secret", "your-secret-key")
set_config_value("security.auth.jwt_algorithm", "RS256")
set_config_value("security.auth.token_expiry_hours", 24)

# API Security
set_config_value("security.api.rate_limit", 1000)
set_config_value("security.api.require_https", True)
set_config_value("security.api.enable_cors", True)
set_config_value("security.api.cors_origins", ["https://example.com"])

# Sandbox Security
set_config_value("security.sandbox.timeout_seconds", 300)
set_config_value("security.sandbox.memory_limit_mb", 2048)
set_config_value("security.sandbox.cpu_limit", 4)
set_config_value("security.sandbox.network_access", False)

# Encryption
set_config_value("security.encryption.algorithm", "AES-256-GCM")
set_config_value("security.encryption.key", "your-encryption-key")
```

---

## Performance Tuning

### Optimize for Your Infrastructure

```python
from backend.config_manager import set_config_value

# Caching
set_config_value("performance.cache.enabled", True)
set_config_value("performance.cache.ttl_seconds", 7200)
set_config_value("performance.cache.max_size_mb", 2048)

# Connection Pooling
set_config_value("performance.connection_pool.min_size", 10)
set_config_value("performance.connection_pool.max_size", 50)

# Async Workers
set_config_value("performance.async.worker_threads", 20)

# Batch Processing
set_config_value("performance.batching.enabled", True)
set_config_value("performance.batching.batch_size", 50)
set_config_value("performance.batching.batch_timeout_seconds", 5)
```

---

## Runtime Modifications

### Modify Configuration on the Fly

```python
from backend.config_manager import get_config_manager, set_config_value

manager = get_config_manager()

# Get current value
current_temp = manager.get("agents.orchestrator.temperature")

# Modify at runtime
set_config_value("agents.orchestrator.temperature", 0.1)

# Verify change
new_temp = manager.get("agents.orchestrator.temperature")
```

### Enable/Disable Features Dynamically

```python
from backend.config_manager import get_config_manager

manager = get_config_manager()

# Enable feature
manager.enable_feature("features.agents.security_hardening")

# Disable feature
manager.disable_feature("features.experimental.web3_integration")

# Check feature status
is_enabled = manager.get("features.agents.orchestrator_enabled")
```

---

## Advanced Customization

### Add Custom Agents

```python
manager.add_custom_agent("data_scientist", {
    "enabled": True,
    "model": "gpt-4",
    "temperature": 0.7,
    "system_prompt": """
    You are KaliGhost's Data Science Agent.
    Expertise: ML, data analysis, predictions.
    """,
    "tools": ["tensorflow", "pandas", "scikit-learn"],
    "specializations": ["nlp", "timeseries", "clustering"]
})
```

### Custom Identity & Branding

```python
set_config_value("identity.brand_name", "MyAI")
set_config_value("identity.brand_emoji", "🚀")
set_config_value("identity.brand_color", "#FF6B6B")

set_config_value("identity.welcome_message", """
Welcome to MyAI 2.0
Your personal AI engineering assistant.
""")
```

### Export/Import Configurations

```python
manager = get_config_manager()

# Export configuration
manager.export_config("config/my_config.yaml")

# Import configuration
manager.import_config("config/my_config.yaml")
```

### Validate Configuration

```python
manager = get_config_manager()

if manager.validate_config():
    print("✅ Configuration is valid")
else:
    print("❌ Configuration errors found")
```

---

## Usage Examples

### Example 1: Security-First Configuration

```python
from backend.config_manager import configure_agent, set_config_value

# Make security extremely strict
configure_agent("security_agent", temperature=0.0, max_retries=10)

# Enable all security features
set_config_value("features.agents.security_hardening", True)
set_config_value("security.sandbox.network_access", False)
set_config_value("security.api.require_https", True)

# Use secure algorithms
set_config_value("security.encryption.algorithm", "AES-256-GCM")
```

### Example 2: Performance-Optimized Configuration

```python
# Enable aggressive caching
set_config_value("performance.cache.ttl_seconds", 86400)  # 24 hours
set_config_value("performance.cache.max_size_mb", 4096)

# Increase worker threads
set_config_value("performance.async.worker_threads", 50)

# Use faster models
set_config_value("agents.orchestrator.model", "gpt-3.5-turbo")
```

### Example 3: Cost-Optimized Configuration

```python
# Use cheaper models
set_config_value("agents.orchestrator.model", "gpt-3.5-turbo")
set_config_value("agents.infrastructure_agent.model", "gpt-3.5-turbo")

# Reduce timeouts
configure_agent("orchestrator", timeout_seconds=120)

# Disable expensive features
set_config_value("features.experimental.ml_threat_detection", False)
```

---

## Best Practices

1. **Start with defaults** - Use provided defaults as baseline
2. **Document your changes** - Export and version control configurations
3. **Test in staging** - Test config changes before production
4. **Monitor performance** - Track metrics after configuration changes
5. **Use environment variables** - For sensitive credentials
6. **Version control configs** - Track all configuration changes
7. **Export backups** - Regularly export your configurations
8. **Validate before deploying** - Always validate configuration

---

## Troubleshooting

### Configuration Not Applied

1. Check the path format: `core.agents.orchestrator.temperature`
2. Verify environment variables override
3. Reload configuration manager
4. Check file permissions on YAML file

### Agent Behavior Wrong

1. Verify system prompt is correct
2. Check temperature value (0.0-1.0)
3. Confirm model availability
4. Check timeout settings

### Performance Issues

1. Review cache settings
2. Check connection pool size
3. Verify worker thread count
4. Monitor memory usage

---

## Summary

KaliGhost 3.0 is **100% configurable**:

✅ Every parameter customizable  
✅ System prompts fully editable  
✅ Workflows dynamically created  
✅ Models can be switched  
✅ Features can be toggled  
✅ Runtime modifications allowed  
✅ Custom agents can be added  
✅ Full API for configuration  

**Your KaliGhost adapts to YOUR needs.**

