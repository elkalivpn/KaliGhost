#!/usr/bin/env python3
"""
🐉 KaliGhost CLI - Elite Developer Command Line Interface
Main entry point for KaliGhost 3.0
"""

import click
import asyncio
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

# ============================================================================
# CLI GROUP
# ============================================================================

@click.group()
@click.version_option(version="3.0.0", prog_name="KaliGhost")
def cli():
    """🐉 KaliGhost 3.0 - Elite Developer Agentic Environment"""
    pass


# ============================================================================
# ORCHESTRATION COMMANDS
# ============================================================================

@cli.group()
def orchestrate():
    """Multi-agent task orchestration"""
    pass


@orchestrate.command()
@click.argument('task', nargs=-1, required=True)
@click.option('--mode', type=click.Choice(['flash', 'standard', 'pro', 'ultra']), default='standard', help='Execution mode')
@click.option('--thread-id', default='cli_default', help='Thread ID for context')
def execute(task, mode, thread_id):
    """Execute a task (single or multi-agent)"""
    task_str = ' '.join(task)
    
    console.print(Panel(f"[bold cyan]🚀 Executing Task[/bold cyan]\n{task_str}", title="KaliGhost Orchestrator"))
    
    async def run():
        from backend.orchestrator import get_orchestrator, AgentMode
        
        orchestrator = get_orchestrator()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            progress.add_task("[cyan]Decomposing task...", total=None)
            
            plan = await orchestrator.decompose_task(
                task=task_str,
                thread_id=thread_id,
                mode=AgentMode(mode)
            )
            
            progress.add_task("[cyan]Executing sub-agents...", total=None)
            result = await orchestrator.execute_plan(plan)
        
        # Display results
        table = Table(title="Execution Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        table.add_row("Status", result['status'])
        table.add_row("Sub-tasks", str(result['sub_task_count']))
        table.add_row("Execution Time", f"{result['execution_time_ms']:.0f}ms")
        console.print(table)
    
    asyncio.run(run())


# ============================================================================
# MEMORY COMMANDS
# ============================================================================

@cli.group()
def memory():
    """Persistent memory management"""
    pass


@memory.command()
@click.argument('category')
@click.argument('content')
@click.option('--meta', help='Metadata JSON')
def add(category, content, meta):
    """Add memory entry"""
    from backend.memory_system import get_memory_system
    
    memory_sys = get_memory_system()
    mem_id = memory_sys.add_memory(category, content)
    
    console.print(f"✅ Memory added: [cyan]{mem_id}[/cyan]")


@memory.command()
@click.argument('query')
@click.option('--category', help='Filter by category')
@click.option('--limit', default=10, help='Max results')
def search(query, category, limit):
    """Search memories"""
    from backend.memory_system import get_memory_system
    
    memory_sys = get_memory_system()
    results = memory_sys.search_memories(query, category=category, limit=limit)
    
    table = Table(title=f"Memory Search: '{query}'")
    table.add_column("Category", style="cyan")
    table.add_column("Content", style="white")
    table.add_column("Score", style="green")
    
    for mem in results:
        table.add_row(mem.category, mem.content[:50], f"{mem.relevance_score:.2f}")
    
    console.print(table)


@memory.command()
def profile():
    """Get user profile from memories"""
    from backend.memory_system import get_memory_system
    
    memory_sys = get_memory_system()
    profile = memory_sys.get_user_profile()
    
    console.print(Panel(f"""
[bold]User Profile[/bold]
Total Memories: {profile['memory_count']}
Preferences: {len(profile['preferences'])}
Facts: {len(profile['facts'])}
Learned Skills: {len(profile['learned_skills'])}
    """, title="Profile"))


# ============================================================================
# SECURITY COMMANDS
# ============================================================================

@cli.group()
def security():
    """Security auditing and hardening"""
    pass


@security.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--language', default='python', help='Programming language')
def audit(path, language):
    """Run security audit on code"""
    
    console.print(f"🛡️  Auditing [cyan]{path}[/cyan] ({language})...")
    
    async def run():
        from backend.security_hardener import get_security_hardener
        
        hardener = get_security_hardener()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            progress.add_task("[cyan]Running SAST...", total=None)
            
            audit_result = await hardener.full_security_audit(
                Path(path), language
            )
        
        # Display results
        table = Table(title="Security Audit Results")
        table.add_column("Finding", style="cyan")
        table.add_column("Severity", style="red")
        
        for vuln in audit_result.vulnerabilities[:10]:
            severity_color = "red" if vuln.severity.name == "CRITICAL" else "yellow"
            table.add_row(vuln.type.value, f"[{severity_color}]{vuln.severity.name}[/{severity_color}]")
        
        console.print(table)
        console.print(f"\n📊 Security Score: [bold green]{audit_result.score}/100[/bold green]")
    
    asyncio.run(run())


# ============================================================================
# MONETIZATION COMMANDS
# ============================================================================

@cli.group()
def monetize():
    """Monetization management"""
    pass


@monetize.command()
@click.argument('name')
@click.argument('price', type=float)
@click.option('--features', multiple=True, help='Feature list')
@click.option('--interval', default='month', help='Billing interval')
def tier(name, price, features, interval):
    """Create pricing tier"""
    from backend.monetization_engine import get_monetization_engine
    
    monetization = get_monetization_engine()
    tier_obj = monetization.create_pricing_tier(
        name=name,
        price_usd=price,
        features=list(features) if features else [],
        billing_interval=interval
    )
    
    console.print(f"✅ Tier created: [cyan]{tier_obj.id}[/cyan] - ${price}/{interval}")


@monetize.command()
@click.argument('customer_id')
@click.argument('tier_id')
@click.option('--days', default=30, help='License duration')
def license(customer_id, tier_id, days):
    """Generate license"""
    from backend.monetization_engine import get_monetization_engine, LicenseType
    
    monetization = get_monetization_engine()
    lic = monetization.generate_license(
        customer_id=customer_id,
        tier_id=tier_id,
        license_type=LicenseType.SUBSCRIPTION,
        duration_days=days
    )
    
    console.print(f"🔐 License: [cyan]{lic.license_key}[/cyan]")


@monetize.command()
@click.option('--days', default=30, help='Period')
def revenue(days):
    """Get revenue summary"""
    from backend.monetization_engine import get_monetization_engine
    
    monetization = get_monetization_engine()
    summary = monetization.get_revenue_summary(days=days)
    
    table = Table(title=f"Revenue Summary ({days} days)")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Total Revenue", f"${summary['total_revenue_usd']:.2f}")
    table.add_row("Customers", str(summary['customer_count']))
    table.add_row("Avg Invoice", f"${summary['avg_invoice_usd']:.2f}")
    
    console.print(table)


# ============================================================================
# INFRASTRUCTURE COMMANDS
# ============================================================================

@cli.group()
def infra():
    """Infrastructure management"""
    pass


@infra.command()
@click.argument('app_name')
@click.option('--provider', default='digitalocean', help='Cloud provider')
@click.option('--count', default=2, help='Instance count')
def provision(app_name, provider, count):
    """Provision cloud infrastructure"""
    
    console.print(f"☁️  Provisioning {count} instances on {provider}...")
    
    async def run():
        from backend.infrastructure_automation import get_infrastructure_automation_engine, CloudProvider
        
        infra_engine = get_infrastructure_automation_engine()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            progress.add_task("[cyan]Creating instances...", total=None)
            
            shadow = await infra_engine.setup_shadow_infrastructure(
                app_name=app_name,
                provider=CloudProvider[provider.upper()],
                instance_count=count
            )
        
        console.print(f"\n✅ Infrastructure created!")
        console.print(f"   Monthly cost: ${shadow['total_cost_usd']:.2f}")
    
    asyncio.run(run())


@infra.command()
def cost():
    """Get monthly infrastructure costs"""
    from backend.infrastructure_automation import get_infrastructure_automation_engine
    
    infra_engine = get_infrastructure_automation_engine()
    total_cost = infra_engine.cloud.get_monthly_cost()
    
    console.print(f"💵 Total monthly cost: [bold green]${total_cost:.2f}[/bold green]")


# ============================================================================
# COMPLIANCE COMMANDS
# ============================================================================

@cli.group()
def compliance():
    """Compliance and legal"""
    pass


@compliance.command()
@click.argument('company_name')
@click.option('--jurisdiction', default='us', help='Jurisdiction')
@click.option('--standards', multiple=True, help='Compliance standards')
def audit_compliance(company_name, jurisdiction, standards):
    """Run compliance audit"""
    
    console.print(f"⚖️  Auditing {company_name} for compliance...")
    
    async def run():
        from backend.compliance_engine import (
            get_compliance_and_ethics_engine,
            Jurisdiction,
            ComplianceStandard
        )
        
        compliance_eng = get_compliance_and_ethics_engine()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            progress.add_task("[cyan]Auditing code...", total=None)
            
            standards_list = [ComplianceStandard[s.upper()] for s in standards] if standards else []
            
            audit = await compliance_eng.full_compliance_audit(
                source_code="",  # Would read from file in practice
                company_name=company_name,
                jurisdiction=Jurisdiction[jurisdiction.upper()],
                standards=standards_list
            )
        
        console.print(f"\n📊 Risk Score: {audit['risk_score']}/100")
        console.print(f"🚀 Ready for launch: {'✅ Yes' if audit['ready_for_launch'] else '❌ No'}")
    
    asyncio.run(run())


# ============================================================================
# THREAT INTELLIGENCE COMMANDS
# ============================================================================

@cli.group()
def threats():
    """Threat intelligence and OSINT"""
    pass


@threats.command()
@click.argument('target')
def recon(target):
    """Run OSINT reconnaissance"""
    
    console.print(f"🕵️  Scanning {target}...")
    
    async def run():
        from backend.threat_intelligence import get_threat_intelligence_engine
        
        threat_engine = get_threat_intelligence_engine()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            progress.add_task("[cyan]Gathering intelligence...", total=None)
            
            report = await threat_engine.full_threat_assessment(target)
        
        console.print(f"\n📊 Threat Score: {report.threat_score}/100")
        console.print(f"📝 Findings: {len(report.findings)}")
    
    asyncio.run(run())


# ============================================================================
# SKILLS COMMANDS
# ============================================================================

@cli.group()
def skills():
    """Elite skills management"""
    pass


@skills.command()
def list():
    """List available skills"""
    from backend.elite_skills import get_skill_library
    
    skill_lib = get_skill_library()
    all_skills = skill_lib.list_skills()
    
    table = Table(title="Available Elite Skills")
    table.add_column("Skill", style="cyan")
    table.add_column("Category", style="magenta")
    table.add_column("Steps", style="green")
    
    for skill in all_skills:
        table.add_row(skill.name, skill.category.value, str(len(skill.steps)))
    
    console.print(table)


# ============================================================================
# SERVER COMMANDS
# ============================================================================

@cli.group()
def server():
    """Server management"""
    pass


@server.command()
@click.option('--port', default=8000, help='API port')
@click.option('--host', default='0.0.0.0', help='Host')
@click.option('--workers', default=4, help='Worker processes')
def start(port, host, workers):
    """Start KaliGhost gateway server"""
    import uvicorn
    
    console.print(Panel(f"[bold green]🐉 KaliGhost Gateway[/bold green]\nHost: {host}:{port}", title="Starting Server"))
    
    uvicorn.run(
        "backend.kalighost_gateway:app",
        host=host,
        port=port,
        workers=workers,
        reload=False
    )


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Entry point"""
    try:
        cli()
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
