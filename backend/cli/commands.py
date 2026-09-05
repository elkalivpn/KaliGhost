"""
CLI Commands Module
Command handlers for the CLI interface
"""

import sys
import time
from typing import TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    from backend.core import KalighostCore


def start_ide(core: 'KalighostCore', args):
    """Start KaliGhost IDE"""
    print("[*] Starting KaliGhost IDE...")
    
    mode = 'standard'
    kwargs = {}
    
    if args.amnesic:
        mode = 'amnesic'
        print("[!] Amnesic mode enabled - no traces will be left on disk")
    elif args.encrypted:
        mode = 'encrypted'
        if not args.passphrase:
            print("[ERROR] Passphrase required for encrypted mode")
            sys.exit(1)
        kwargs['passphrase'] = args.passphrase
        print("[*] Encrypted persistence enabled")
    
    # Initialize core
    if not core.initialize(mode=mode, **kwargs):
        print("[ERROR] Failed to initialize core")
        sys.exit(1)
    
    # Start services
    if not core.start_services():
        print("[ERROR] Failed to start services")
        core.cleanup()
        sys.exit(1)
    
    print(f"\n[+] KaliGhost IDE started successfully!")
    print(f"[*] Mode: {mode}")
    print(f"[*] Web Interface: http://localhost:{args.port}")
    print(f"[*] API: http://localhost:{args.port}/api/v1")
    print(f"[*] WebSocket: ws://localhost:{args.port}/ws")
    
    if not args.headless:
        print("[*] Opening GUI...")
        # Launch GUI would go here
    
    print("\n[*] Press Ctrl+C to stop\n")
    
    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Shutting down...")
        core.cleanup()
        print("[+] Shutdown complete")


def stop_ide(core: 'KalighostCore', args):
    """Stop KaliGhost IDE"""
    print("[*] Stopping KaliGhost IDE...")
    
    if args.force:
        print("[!] Force stop requested")
    
    # Send SIGTERM to running instance
    pid_file = Path('/tmp/kalighost.pid')
    if pid_file.exists():
        import os
        import signal
        pid = int(pid_file.read_text().strip())
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"[+] Sent TERM signal to process {pid}")
        except ProcessLookupError:
            print("[!] Process not found, may already be stopped")
    else:
        print("[!] No running instance found")
    
    if args.wipe:
        print("[*] Wiping temporary data...")
        # Wipe logic would go here
    
    print("[+] Stop complete")


def manage_agent(core: 'KalighostCore', args):
    """Manage AI Agent"""
    if args.status:
        status = core.agent_status
        print("\n=== Agent Status ===")
        print(f"Loaded: {status['loaded']}")
        print(f"Model: {status['model'] or 'None'}")
        if status['loaded']:
            print(f"GPU: {status.get('gpu', False)}")
        print()
        return
    
    if args.unload:
        print("[*] Unloading agent...")
        core.unload_agent()
        print("[+] Agent unloaded")
        return
    
    # Load agent
    print(f"[*] Loading agent with model: {args.model}")
    if core.load_agent(model=args.model, gpu=args.gpu):
        print(f"[+] Agent loaded successfully")
        print(f"[*] Model: {args.model}")
        print(f"[*] GPU Acceleration: {'Enabled' if args.gpu else 'Disabled'}")
        print(f"[*] Quantization: {args.quantize}")
    else:
        print("[ERROR] Failed to load agent")
        sys.exit(1)


def sandbox_mode(core: 'KalighostCore', args):
    """Run sandbox analysis"""
    from backend.services.sandbox import MalwareSandbox
    
    if not args.malware:
        print("[ERROR] Malware sample required (--malware <file>)")
        sys.exit(1)
    
    malware_path = Path(args.malware)
    if not malware_path.exists():
        print(f"[ERROR] File not found: {malware_path}")
        sys.exit(1)
    
    print(f"[*] Initializing sandbox environment...")
    sandbox = MalwareSandbox(
        isolate=args.isolate,
        network_monitor=args.network,
        timeout=args.timeout
    )
    
    print(f"[*] Analyzing: {malware_path.name}")
    print(f"[*] Timeout: {args.timeout}s")
    print(f"[*] Network isolation: {'Full' if args.isolate else 'Monitored'}")
    
    try:
        results = sandbox.analyze(str(malware_path))
        
        print("\n=== Analysis Results ===")
        print(f"MD5: {results.get('md5', 'N/A')}")
        print(f"SHA256: {results.get('sha256', 'N/A')}")
        print(f"File Type: {results.get('file_type', 'N/A')}")
        print(f"Threat Score: {results.get('threat_score', 0)}/100")
        
        if results.get('behaviors'):
            print("\nBehaviors Detected:")
            for behavior in results['behaviors']:
                print(f"  - {behavior}")
        
        if results.get('network_activity'):
            print("\nNetwork Activity:")
            for activity in results['network_activity']:
                print(f"  - {activity}")
        
        print("\n[+] Analysis complete")
        
    except Exception as e:
        print(f"[ERROR] Analysis failed: {str(e)}")
        sys.exit(1)
    finally:
        sandbox.cleanup()


def purple_team(core: 'KalighostCore', args):
    """Execute purple team operations"""
    from backend.services.purple_team import PurpleTeamOps
    
    print(f"[*] Initializing Purple Team Operations")
    print(f"[*] Target: {args.target}")
    print(f"[*] Mode: {args.mode}")
    print(f"[*] Stealth: {'Enabled' if args.stealth else 'Disabled'}")
    
    ops = PurpleTeamOps(stealth=args.stealth)
    
    try:
        if args.mode == 'recon':
            results = ops.reconnaissance(args.target)
        elif args.mode == 'exploit':
            results = ops.exploitation(args.target)
        elif args.mode == 'post-exploit':
            results = ops.post_exploitation(args.target)
        else:  # full
            results = ops.full_operation(args.target)
        
        print("\n=== Operation Results ===")
        for key, value in results.items():
            print(f"{key}: {value}")
        
        if args.report:
            ops.generate_report(args.report)
            print(f"\n[+] Report saved to: {args.report}")
        
    except Exception as e:
        print(f"[ERROR] Operation failed: {str(e)}")
        if core.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def project_manager(core: 'KalighostCore', args):
    """Manage projects"""
    action = args.action
    
    if action == 'new':
        if not args.name:
            print("[ERROR] Project name required (--name <name>)")
            sys.exit(1)
        
        project = core.create_project(args.name, encrypt=args.encrypt)
        print(f"[+] Project created: {args.name}")
        print(f"[*] Path: {project['path']}")
        print(f"[*] Encrypted: {project['encrypted']}")
    
    elif action == 'open':
        if not args.name and not args.path:
            print("[ERROR] Project name or path required")
            sys.exit(1)
        
        project = core.open_project(args.name or args.path)
        print(f"[+] Project opened: {project['name']}")
    
    elif action == 'list':
        projects = core.workspace_mgr.list_projects()
        print("\n=== Projects ===")
        if not projects:
            print("No projects found")
        else:
            for proj in projects:
                print(f"  - {proj['name']} ({proj['created']})")
                print(f"    Path: {proj['path']}")
                print(f"    Encrypted: {proj['encrypted']}")
        print()
    
    elif action == 'delete':
        if not args.name:
            print("[ERROR] Project name required")
            sys.exit(1)
        
        confirm = input(f"Delete project '{args.name}'? [y/N]: ")
        if confirm.lower() == 'y':
            core.workspace_mgr.delete_project(args.name)
            print(f"[+] Project deleted: {args.name}")
        else:
            print("[!] Deletion cancelled")
    
    elif action == 'export':
        if not args.name:
            print("[ERROR] Project name required")
            sys.exit(1)
        
        output = core.workspace_mgr.export_project(args.name)
        print(f"[+] Project exported to: {output}")


def health_check(core: 'KalighostCore', args):
    """Run system health check"""
    print("[*] Running health check...\n")
    
    checks = {
        'Python Version': sys.version.split()[0],
        'Working Directory': Path.cwd(),
        'Permissions': 'OK' if Path.cwd().exists() else 'FAIL',
    }
    
    # Check dependencies
    try:
        import cryptography
        checks['Cryptography'] = f"v{cryptography.__version__}"
    except ImportError:
        checks['Cryptography'] = 'MISSING'
    
    try:
        import aiohttp
        checks['AIOHTTP'] = f"v{aiohttp.__version__}"
    except ImportError:
        checks['AIOHTTP'] = 'MISSING'
    
    try:
        import docker
        checks['Docker SDK'] = f"v{docker.__version__}"
    except ImportError:
        checks['Docker SDK'] = 'MISSING'
    
    # Check Docker
    try:
        import docker
        client = docker.from_env()
        client.ping()
        checks['Docker Daemon'] = 'Running'
    except:
        checks['Docker Daemon'] = 'Not Running'
    
    # Print results
    print("=== Health Check Results ===")
    for check, result in checks.items():
        status = "✓" if result not in ['MISSING', 'Not Running', 'FAIL'] else "✗"
        print(f"{status} {check}: {result}")
    
    if args.full:
        print("\n=== Detailed Diagnostics ===")
        # Additional checks for full diagnostic
        import psutil
        print(f"CPU Usage: {psutil.cpu_percent()}%")
        print(f"Memory Usage: {psutil.virtual_memory().percent}%")
        print(f"Disk Usage: {psutil.disk_usage('/').percent}%")
    
    # Check for issues
    issues = [k for k, v in checks.items() if v in ['MISSING', 'Not Running', 'FAIL']]
    
    if issues:
        print(f"\n[!] Issues detected: {', '.join(issues)}")
        if args.fix:
            print("[*] Auto-fix not yet implemented")
        sys.exit(1)
    else:
        print("\n[+] All checks passed!")
        sys.exit(0)
