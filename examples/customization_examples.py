"""
customization_examples.py - Complete KaliGhost 3.0 Customization Examples

Shows developers how to customize every aspect of KaliGhost without limitations.
"""

from backend.config_manager import (
    get_config_manager,
    configure_agent,
    update_system_prompt,
    set_config_value,
    get_config_value,
)


def example_1_basic_configuration():
    """Example 1: Basic Configuration"""
    print("\n" + "="*70)
    print("📝 Example 1: Basic Configuration")
    print("="*70)
    
    manager = get_config_manager()
    
    # Get current values
    app_mode = get_config_value("core.mode")
    debug_enabled = get_config_value("core.debug")
    
    print(f"Current mode: {app_mode}")
    print(f"Debug enabled: {debug_enabled}")
    
    # Change mode
    set_config_value("core.mode", "development")
    set_config_value("core.debug", True)
    set_config_value("core.logging.level", "DEBUG")
    
    print("✅ Configuration updated to development mode with debug enabled")


def example_2_customize_agent_behavior():
    """Example 2: Customize Individual Agent Behavior"""
    print("\n" + "="*70)
    print("🤖 Example 2: Customize Agent Behavior")
    print("="*70)
    
    # Make orchestrator more aggressive in decomposition
    configure_agent(
        "orchestrator",
        temperature=0.3,  # More deterministic
        max_tokens=8192,  # Allow longer responses
        timeout_seconds=600,  # Longer timeout
        max_retries=5  # More retries
    )
    
    # Make security agent stricter
    configure_agent(
        "security_agent",
        temperature=0.1,  # Very deterministic
        timeout_seconds=900,
        max_retries=10
    )
    
    # Make monetization agent more creative
    configure_agent(
        "monetization_agent",
        temperature=0.9,  # Very creative
        top_p=1.0
    )
    
    print("✅ Agent behaviors customized!")
    print("   - Orchestrator: More deterministic")
    print("   - Security: Stricter")
    print("   - Monetization: More creative")


def example_3_modify_system_prompts():
    """Example 3: Modify System Prompts"""
    print("\n" + "="*70)
    print("💬 Example 3: Modify System Prompts")
    print("="*70)
    
    manager = get_config_manager()
    
    # Custom orchestrator prompt
    custom_orchestrator_prompt = """
    You are KaliGhost's Orchestrator Agent.
    
    Your role: Decompose complex tasks into manageable subtasks.
    Your style: Professional, strategic, forward-thinking.
    
    Requirements:
    - Always prioritize security
    - Think about scalability from the start
    - Consider cost implications
    - Plan for edge cases
    
    Be thorough but concise in your decomposition.
    """
    
    update_system_prompt("orchestrator", custom_orchestrator_prompt)
    
    # Custom security agent prompt
    custom_security_prompt = """
    You are KaliGhost's Security Hardening Agent.
    
    Your role: Identify and fix vulnerabilities.
    Your approach: Aggressive security-first methodology.
    
    Always check for:
    - OWASP Top 10 vulnerabilities
    - Supply chain risks
    - Cryptographic weaknesses
    - Authentication/Authorization flaws
    - Data exposure risks
    
    Generate production-ready fixes.
    """
    
    update_system_prompt("security_agent", custom_security_prompt)
    
    print("✅ System prompts customized for your organization!")


def example_4_add_custom_agents():
    """Example 4: Add Custom Agents"""
    print("\n" + "="*70)
    print("➕ Example 4: Add Custom Agents")
    print("="*70)
    
    manager = get_config_manager()
    
    # Add ML/AI specialist agent
    manager.add_custom_agent("ml_specialist", {
        "enabled": True,
        "model": "gpt-4",
        "temperature": 0.6,
        "max_tokens": 8192,
        "timeout_seconds": 600,
        "system_prompt": """
        You are KaliGhost's ML/AI Specialist Agent.
        
        Expertise:
        - Machine learning architecture design
        - Model selection and training
        - Performance optimization
        - Production deployment
        
        Provide state-of-the-art ML solutions.
        """,
        "tools": ["tensorflow", "pytorch", "scikit-learn"],
        "specializations": ["nlp", "computer_vision", "timeseries"]
    })
    
    # Add DevOps specialist agent
    manager.add_custom_agent("devops_specialist", {
        "enabled": True,
        "model": "gpt-3.5-turbo",
        "temperature": 0.4,
        "system_prompt": """
        You are KaliGhost's DevOps Specialist Agent.
        
        Expertise:
        - Infrastructure as Code
        - CI/CD pipeline design
        - Kubernetes orchestration
        - Observability and monitoring
        
        Design robust, scalable infrastructure.
        """,
        "tools": ["terraform", "kubernetes", "github-actions"],
        "cloud_providers": ["aws", "gcp", "azure"]
    })
    
    print("✅ Custom agents added!")
    print("   - ML Specialist: For AI/ML tasks")
    print("   - DevOps Specialist: For infrastructure")


def example_5_create_custom_workflows():
    """Example 5: Create Custom Workflows"""
    print("\n" + "="*70)
    print("🔄 Example 5: Create Custom Workflows")
    print("="*70)
    
    manager = get_config_manager()
    
    # Custom "AI-Powered Application" workflow
    ai_app_workflow = {
        "name": "AI-Powered Application",
        "description": "Build complete AI application with ML ops",
        "steps": [
            {
                "id": "analyze",
                "agent": "orchestrator",
                "task": "Analyze AI application requirements",
                "timeout": 300
            },
            {
                "id": "ml_design",
                "agent": "ml_specialist",
                "task": "Design ML architecture",
                "timeout": 600,
                "depends_on": ["analyze"]
            },
            {
                "id": "backend_setup",
                "agent": "infrastructure_agent",
                "task": "Setup backend infrastructure",
                "timeout": 450,
                "depends_on": ["analyze"]
            },
            {
                "id": "security_check",
                "agent": "security_agent",
                "task": "Secure AI model and APIs",
                "timeout": 600,
                "depends_on": ["ml_design", "backend_setup"]
            },
            {
                "id": "devops_setup",
                "agent": "devops_specialist",
                "task": "Setup CI/CD and monitoring",
                "timeout": 450,
                "depends_on": ["security_check"]
            },
            {
                "id": "deploy",
                "agent": "infrastructure_agent",
                "task": "Deploy to production",
                "timeout": 300,
                "depends_on": ["devops_setup"]
            }
        ]
    }
    
    manager.add_custom_workflow("ai_powered_app", ai_app_workflow)
    
    # Custom "Enterprise Application" workflow
    enterprise_workflow = {
        "name": "Enterprise Application",
        "description": "Build scalable enterprise app with compliance",
        "steps": [
            {
                "id": "requirements",
                "agent": "orchestrator",
                "task": "Gather enterprise requirements"
            },
            {
                "id": "design",
                "agent": "orchestrator",
                "task": "Design enterprise architecture",
                "depends_on": ["requirements"]
            },
            {
                "id": "compliance_check",
                "agent": "compliance_agent",
                "task": "Check compliance requirements",
                "depends_on": ["requirements"]
            },
            {
                "id": "security_plan",
                "agent": "security_agent",
                "task": "Plan security strategy",
                "depends_on": ["design", "compliance_check"]
            },
            {
                "id": "implementation",
                "agent": "infrastructure_agent",
                "task": "Implement infrastructure",
                "depends_on": ["security_plan"]
            },
            {
                "id": "monetization",
                "agent": "monetization_agent",
                "task": "Setup billing and licensing",
                "depends_on": ["implementation"]
            }
        ]
    }
    
    manager.add_custom_workflow("enterprise_app", enterprise_workflow)
    
    print("✅ Custom workflows created!")
    print("   - AI-Powered Application: ML + Production")
    print("   - Enterprise Application: Compliance + Security")


def example_6_enable_disable_features():
    """Example 6: Enable/Disable Features"""
    print("\n" + "="*70)
    print("🎚️ Example 6: Enable/Disable Features")
    print("="*70)
    
    manager = get_config_manager()
    
    # Enable all features
    manager.enable_feature("features.agents.orchestrator_enabled")
    manager.enable_feature("features.agents.security_hardening")
    manager.enable_feature("features.advanced.multi_agent_collaboration")
    
    # Disable experimental features
    manager.disable_feature("features.experimental.web3_integration")
    manager.disable_feature("features.experimental.autonomous_coding")
    
    # Enable threat monitoring
    manager.enable_feature("integrations.channels.telegram")
    manager.disable_feature("integrations.channels.wechat")
    
    print("✅ Features configured!")
    print("   - Core agents: Enabled")
    print("   - Multi-agent collaboration: Enabled")
    print("   - Web3 integration: Disabled")
    print("   - Telegram: Enabled")


def example_7_model_switching():
    """Example 7: Switch Between Models"""
    print("\n" + "="*70)
    print("🧠 Example 7: Switch Between Models")
    print("="*70)
    
    manager = get_config_manager()
    
    # Use GPT-4 for critical agents
    set_config_value("agents.orchestrator.model", "gpt-4")
    set_config_value("agents.security_agent.model", "gpt-4")
    
    # Use GPT-3.5-turbo for faster agents
    set_config_value("agents.infrastructure_agent.model", "gpt-3.5-turbo")
    set_config_value("agents.monetization_agent.model", "gpt-3.5-turbo")
    
    # Use local models (if configured)
    set_config_value("agents.threat_agent.model", "mistral-7b")
    
    # Set fallback models
    manager.set("models.fallback", [
        {"provider": "openai", "model_name": "gpt-3.5-turbo"},
        {"provider": "anthropic", "model_name": "claude-opus"}
    ])
    
    print("✅ Models configured!")
    print("   - Critical agents: GPT-4")
    print("   - Standard agents: GPT-3.5-turbo")
    print("   - Threat agent: Local Mistral-7B")


def example_8_security_customization():
    """Example 8: Customize Security Settings"""
    print("\n" + "="*70)
    print("🔒 Example 8: Customize Security Settings")
    print("="*70)
    
    manager = get_config_manager()
    
    # Tighten security
    set_config_value("security.auth.jwt_algorithm", "RS256")
    set_config_value("security.auth.token_expiry_hours", 1)  # 1 hour
    set_config_value("security.api.rate_limit", 100)  # 100 req/hour
    set_config_value("security.api.require_https", True)
    
    # Sandbox configuration
    set_config_value("security.sandbox.timeout_seconds", 60)
    set_config_value("security.sandbox.memory_limit_mb", 512)
    set_config_value("security.sandbox.network_access", False)
    
    print("✅ Security tightened!")
    print("   - JWT: RS256 algorithm")
    print("   - Token expiry: 1 hour")
    print("   - Rate limit: 100 requests/hour")
    print("   - Sandbox: Memory 512MB, no network")


def example_9_performance_tuning():
    """Example 9: Performance Tuning"""
    print("\n" + "="*70)
    print("⚡ Example 9: Performance Tuning")
    print("="*70)
    
    manager = get_config_manager()
    
    # Enable caching
    set_config_value("performance.cache.enabled", True)
    set_config_value("performance.cache.ttl_seconds", 7200)  # 2 hours
    set_config_value("performance.cache.max_size_mb", 2048)
    
    # Connection pool
    set_config_value("performance.connection_pool.min_size", 10)
    set_config_value("performance.connection_pool.max_size", 50)
    
    # Worker threads
    set_config_value("performance.async.worker_threads", 20)
    
    # Batch processing
    set_config_value("performance.batching.enabled", True)
    set_config_value("performance.batching.batch_size", 50)
    
    print("✅ Performance optimized!")
    print("   - Cache: 2 hour TTL, 2GB max")
    print("   - Connection pool: 10-50 connections")
    print("   - Workers: 20 threads")
    print("   - Batching: 50 items per batch")


def example_10_runtime_modifications():
    """Example 10: Runtime Modifications"""
    print("\n" + "="*70)
    print("🔧 Example 10: Runtime Modifications")
    print("="*70)
    
    manager = get_config_manager()
    
    print("Getting current configuration...")
    current_mode = get_config_value("core.mode")
    print(f"Current mode: {current_mode}")
    
    print("\nModifying at runtime...")
    set_config_value("core.mode", "emergency")
    set_config_value("security.sandbox.timeout_seconds", 30)
    set_config_value("agents.orchestrator.temperature", 0.1)
    
    print("\nModifying agent behavior on the fly...")
    configure_agent(
        "security_agent",
        temperature=0.0,  # Completely deterministic
        max_retries=10,
        timeout_seconds=1800  # 30 minutes
    )
    
    print("\n✅ Runtime modifications complete!")
    print("   - Mode switched to: emergency")
    print("   - Security agent: Ultra-strict mode")


def example_11_export_import_configs():
    """Example 11: Export and Import Configurations"""
    print("\n" + "="*70)
    print("📤📥 Example 11: Export/Import Configurations")
    print("="*70)
    
    manager = get_config_manager()
    
    # Export current configuration
    manager.export_config("config/my_custom_config.yaml")
    print("✅ Current configuration exported to: config/my_custom_config.yaml")
    
    # Make modifications
    set_config_value("core.mode", "production")
    set_config_value("core.debug", False)
    
    # Export modified configuration
    manager.export_config("config/production_config.yaml")
    print("✅ Production configuration exported")
    
    # Later, import configuration
    # manager.import_config("config/production_config.yaml")
    print("✅ Ready to import configurations later")


def run_all_examples():
    """Run all customization examples"""
    print("\n" + "="*80)
    print("🐉 KALIGHOST 3.0 - COMPLETE CUSTOMIZATION EXAMPLES")
    print("="*80)
    
    example_1_basic_configuration()
    example_2_customize_agent_behavior()
    example_3_modify_system_prompts()
    example_4_add_custom_agents()
    example_5_create_custom_workflows()
    example_6_enable_disable_features()
    example_7_model_switching()
    example_8_security_customization()
    example_9_performance_tuning()
    example_10_runtime_modifications()
    example_11_export_import_configs()
    
    print("\n" + "="*80)
    print("✅ ALL CUSTOMIZATION EXAMPLES COMPLETED!")
    print("="*80)
    print("""
Your KaliGhost 3.0 is now fully customized:
✓ Agent behaviors modified
✓ System prompts personalized
✓ Custom agents added
✓ Workflows created
✓ Features toggled
✓ Models switched
✓ Security hardened
✓ Performance tuned
✓ Runtime modifications applied

KaliGhost adapts to YOUR needs, not the other way around!
    """)


if __name__ == "__main__":
    run_all_examples()
