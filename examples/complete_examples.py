#!/usr/bin/env python3
"""
🐉 KaliGhost 3.0 - Complete Examples
Usage examples for all 10 elite modules
"""

import asyncio
from pathlib import Path

# ============================================================================
# 1. ORCHESTRATOR - Multi-Agent Task Decomposition
# ============================================================================

async def example_orchestrator():
    """Example: Decompose and execute complex task with multiple agents"""
    from backend.orchestrator import get_orchestrator, AgentMode
    
    orchestrator = get_orchestrator()
    
    print("\n" + "="*70)
    print("🐉 EXAMPLE 1: ORCHESTRATOR - Multi-Agent Execution")
    print("="*70)
    
    # Task: Build full-stack SaaS
    task = """
    Create a real-time API monitoring SaaS:
    - Go backend with gRPC
    - React dashboard with WebSocket
    - PostgreSQL time-series
    - Stripe integration ($29/month)
    - Deploy to AWS with auto-scaling
    """
    
    # Decompose into sub-tasks
    print(f"\n📋 Decomposing task: {task[:50]}...")
    plan = await orchestrator.decompose_task(
        task=task,
        thread_id="example_001",
        mode=AgentMode.ULTRA  # Multi-agent mode
    )
    
    print(f"  ✅ Plan created: {plan.id}")
    print(f"  📊 Strategy: {plan.decomposition_strategy}")
    print(f"  🤖 Sub-tasks: {len(plan.sub_tasks)}")
    
    # Execute plan
    print(f"\n🚀 Executing {len(plan.sub_tasks)} sub-agents in parallel...")
    result = await orchestrator.execute_plan(plan)
    
    print(f"  ✅ Status: {result['status']}")
    print(f"  ⏱️  Execution time: {result['execution_time_ms']:.0f}ms")
    print(f"  📝 Sub-tasks completed: {len(result['results'])}")


# ============================================================================
# 2. MEMORY SYSTEM - Persistent Context
# ============================================================================

def example_memory():
    """Example: Store and retrieve developer preferences"""
    from backend.memory_system import get_memory_system
    
    print("\n" + "="*70)
    print("🧠 EXAMPLE 2: MEMORY SYSTEM - Persistent Context")
    print("="*70)
    
    memory = get_memory_system()
    
    # Store preferences
    print("\n📝 Storing developer preferences...")
    mem_id = memory.add_memory(
        category="preference",
        content="Always use TypeScript for frontend, Go for backend microservices",
        metadata={"domain": "tech_stack"}
    )
    print(f"  ✅ Preference stored: {mem_id}")
    
    # Search memories
    print("\n🔍 Searching for relevant memories...")
    results = memory.search_memories("Go backend", limit=5)
    for mem in results:
        print(f"  📌 {mem.category}: {mem.content[:60]}...")
    
    # Get profile
    print("\n👤 Getting user profile...")
    profile = memory.get_user_profile()
    print(f"  💾 Total memories: {profile['memory_count']}")
    print(f"  ⚙️  Preferences: {len(profile['preferences'])}")


# ============================================================================
# 3. ELITE SKILLS - Pre-built Workflows
# ============================================================================

def example_elite_skills():
    """Example: Discover and execute elite skills"""
    from backend.elite_skills import get_skill_library, SkillCategory
    
    print("\n" + "="*70)
    print("⚡ EXAMPLE 3: ELITE SKILLS - Pre-built Workflows")
    print("="*70)
    
    skills = get_skill_library()
    
    # List available skills
    print("\n📚 Available Elite Skills:")
    all_skills = skills.list_skills()
    for skill in all_skills:
        print(f"  🎯 {skill.name}")
        print(f"     └─ Steps: {len(skill.steps)} | Est. time: {skill.estimated_time_minutes}m")
    
    # Find skill for task
    print("\n🔍 Finding best skill for task...")
    task = "Create a microservices platform with Go"
    skill = skills.get_skill_for_task(task)
    if skill:
        print(f"  ✅ Matched skill: {skill.name}")
        print(f"     Required tools: {', '.join(skill.required_tools)}")


# ============================================================================
# 4. SECURITY HARDENER - Code Audit & Patching
# ============================================================================

async def example_security_hardener():
    """Example: Full security audit with auto-remediation"""
    from backend.security_hardener import get_security_hardener
    
    print("\n" + "="*70)
    print("🛡️  EXAMPLE 4: SECURITY HARDENER - Code Audit")
    print("="*70)
    
    hardener = get_security_hardener()
    
    # Example vulnerable code
    vulnerable_code = """
    def get_user(user_id):
        query = f"SELECT * FROM users WHERE id = {user_id}"  # SQL injection!
        password = "admin123"  # Hardcoded!
        return db.execute(query)
    """
    
    print("\n📝 Vulnerable code snippet:")
    print(vulnerable_code)
    
    print("\n🔍 Running security audit...")
    audit = await hardener.full_security_audit(
        source_path=Path("."),
        language="python"
    )
    
    print(f"  ✅ Vulnerabilities found: {len(audit.vulnerabilities)}")
    print(f"  📊 Security score: {audit.score}/100")
    print(f"  🔧 Can auto-fix: {audit.remediable_count} issues")


# ============================================================================
# 5. MONETIZATION ENGINE - Stripe + Licensing
# ============================================================================

def example_monetization():
    """Example: Setup pricing tiers and generate licenses"""
    from backend.monetization_engine import get_monetization_engine, LicenseType
    
    print("\n" + "="*70)
    print("💰 EXAMPLE 5: MONETIZATION ENGINE - Stripe Integration")
    print("="*70)
    
    monetization = get_monetization_engine()
    
    # Create pricing tiers
    print("\n💳 Creating pricing tiers...")
    free = monetization.create_pricing_tier(
        name="Free",
        price_usd=0,
        features=["10 API calls/month", "Community support"]
    )
    pro = monetization.create_pricing_tier(
        name="Professional",
        price_usd=29,
        features=["10K API calls/month", "Priority support"]
    )
    print(f"  ✅ Tiers created: Free, Pro")
    
    # Generate license
    print("\n🔐 Generating license...")
    license = monetization.generate_license(
        customer_id="cust_acme_001",
        tier_id=pro.id,
        license_type=LicenseType.SUBSCRIPTION,
        duration_days=30
    )
    print(f"  ✅ License key: {license.license_key}")
    
    # Track usage
    print("\n📊 Tracking usage...")
    monetization.track_usage(
        customer_id="cust_acme_001",
        event_type="api_call",
        quantity=542
    )
    usage = monetization.get_usage_summary("cust_acme_001", days=30)
    print(f"  📈 Total API calls: {usage['total_quantity']}")


# ============================================================================
# 6. THREAT INTELLIGENCE - OSINT + Dark Web
# ============================================================================

async def example_threat_intelligence():
    """Example: OSINT recon and threat assessment"""
    from backend.threat_intelligence import get_threat_intelligence_engine
    
    print("\n" + "="*70)
    print("🕵️  EXAMPLE 6: THREAT INTELLIGENCE - OSINT")
    print("="*70)
    
    threat_intel = get_threat_intelligence_engine()
    
    # Full threat assessment
    print("\n🔍 Running threat assessment on target...")
    report = await threat_intel.full_threat_assessment(
        target="example.com",
        check_third_party=True,
        watch_dark_web=True
    )
    
    print(f"  ✅ Findings: {len(report.findings)}")
    print(f"  📊 Threat score: {report.threat_score}/100")
    print(f"  💡 Recommendations: {len(report.recommendations)}")
    for rec in report.recommendations[:3]:
        print(f"     • {rec}")


# ============================================================================
# 7. INFRASTRUCTURE AUTOMATION - Cloud + Auto-scaling
# ============================================================================

async def example_infrastructure():
    """Example: Provision cloud infrastructure"""
    from backend.infrastructure_automation import (
        get_infrastructure_automation_engine,
        CloudProvider
    )
    
    print("\n" + "="*70)
    print("☁️  EXAMPLE 7: INFRASTRUCTURE - Cloud Auto-scaling")
    print("="*70)
    
    infra = get_infrastructure_automation_engine()
    
    # Setup shadow infrastructure
    print("\n🏗️  Setting up shadow (test) infrastructure...")
    shadow = await infra.setup_shadow_infrastructure(
        app_name="myapp-test",
        provider=CloudProvider.DIGITALOCEAN,
        instance_count=2
    )
    print(f"  ✅ Shadow infra: {len(shadow['instances'])} instances")
    print(f"  💵 Monthly cost: ${shadow['total_cost_usd']:.2f}")
    
    # Create auto-scaling rule
    print("\n📊 Creating auto-scaling rules...")
    infra.autoscaling.create_scaling_rule(
        metric="cpu_percent",
        threshold=75,
        action="scale_up"
    )
    print(f"  ✅ Rule created: CPU > 75% → scale up")
    
    # Manage secrets
    print("\n🔐 Managing secrets...")
    secret = infra.secrets.create_secret(
        name="db_password",
        secret_type="password",
        value="<generated>",
        rotation_days=30
    )
    print(f"  ✅ Secret stored: {secret.name}")


# ============================================================================
# 8. GUI GENERATOR - CLI to Web/Desktop
# ============================================================================

async def example_gui_generator():
    """Example: Convert CLI tool to web UI"""
    from backend.gui_generator import get_gui_automation_engine
    
    print("\n" + "="*70)
    print("🎨 EXAMPLE 8: GUI GENERATOR - CLI → Web UI")
    print("="*70)
    
    gui_engine = get_gui_automation_engine()
    
    print("\n📝 Analyzing CLI tool...")
    analysis = await gui_engine.gui_gen.analyze_cli_tool(
        Path("./my_tool.py")
    )
    print(f"  ✅ Parameters found: {len(analysis['parameters'])}")
    
    print("\n🎨 Generating React UI...")
    react_ui = await gui_engine.gui_gen.generate_react_ui(
        tool_name="MyTool",
        parameters=analysis['parameters']
    )
    print(f"  ✅ React component generated ({len(react_ui)} chars)")
    
    print("\n🖥️  Generating Tauri desktop app...")
    desktop = await gui_engine.gui_gen.generate_tauri_desktop_app(
        tool_name="MyTool",
        parameters=analysis['parameters']
    )
    print(f"  ✅ Desktop app generated")


# ============================================================================
# 9. COMPLIANCE ENGINE - Legal + Ethics
# ============================================================================

async def example_compliance():
    """Example: Full compliance audit"""
    from backend.compliance_engine import (
        get_compliance_and_ethics_engine,
        ComplianceStandard,
        Jurisdiction
    )
    
    print("\n" + "="*70)
    print("⚖️  EXAMPLE 9: COMPLIANCE - Legal + Ethics Audit")
    print("="*70)
    
    compliance = get_compliance_and_ethics_engine()
    
    # Example code
    source_code = "def get_data(): return open('data.csv').read()"
    
    print("\n🏛️  Running full compliance audit...")
    audit = await compliance.full_compliance_audit(
        source_code=source_code,
        company_name="MyStartup Inc",
        jurisdiction=Jurisdiction.US,
        standards=[ComplianceStandard.GDPR, ComplianceStandard.CCPA]
    )
    
    print(f"  ✅ Compliance checks: {len(audit['compliance_checks'])}")
    print(f"  ⚖️  Ethics alerts: {len(audit['ethics_alerts'])}")
    print(f"  📜 Legal docs: {len(audit['legal_documents'])}")
    print(f"  📊 Risk score: {audit['risk_score']}/100")
    print(f"  🚀 Ready for launch: {audit['ready_for_launch']}")


# ============================================================================
# 10. IM CHANNELS - Telegram, Slack, etc
# ============================================================================

async def example_im_channels():
    """Example: Setup IM channel integration"""
    from backend.im_channels import get_im_manager, TelegramChannel
    
    print("\n" + "="*70)
    print("💬 EXAMPLE 10: IM CHANNELS - Telegram/Slack Integration")
    print("="*70)
    
    im_manager = get_im_manager()
    
    print("\n📱 Registering Telegram channel...")
    telegram = TelegramChannel("telegram", {
        "bot_token": "YOUR_TELEGRAM_BOT_TOKEN"
    })
    im_manager.register_channel(telegram)
    print(f"  ✅ Telegram registered")
    
    print("\n⚡ Channels available:")
    for channel_name in im_manager.channels.keys():
        print(f"  • {channel_name}")


# ============================================================================
# MAIN - Run all examples
# ============================================================================

async def main():
    """Run all examples"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*20 + "🐉 KaliGhost 3.0 Examples" + " "*23 + "║")
    print("╚" + "="*68 + "╝")
    
    # Async examples
    await example_orchestrator()
    await example_security_hardener()
    await example_threat_intelligence()
    await example_infrastructure()
    await example_gui_generator()
    await example_compliance()
    await example_im_channels()
    
    # Sync examples
    example_memory()
    example_elite_skills()
    example_monetization()
    
    print("\n" + "="*70)
    print("✅ All examples completed!")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
