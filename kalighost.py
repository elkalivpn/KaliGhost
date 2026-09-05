#!/usr/bin/env python3
"""
KaliGhost IDE - Main Entry Point
Advanced Security Development Environment for Elite Researchers

This is the main CLI entry point for KaliGhost IDE, providing access to:
- IDE launcher with security features
- AI agent management
- Sandbox environments
- Purple team operations
- Project management
"""

import argparse
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from backend.core import KalighostCore
from backend.cli.commands import (
    start_ide,
    stop_ide,
    manage_agent,
    sandbox_mode,
    purple_team,
    project_manager,
    health_check
)


def print_banner():
    """Display KaliGhost ASCII art banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗            ║
    ║   ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝            ║
    ║   ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗            ║
    ║   ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║            ║
    ║   ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║            ║
    ║   ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝            ║
    ║                                                           ║
    ║          Ghost Edition - Uncensored AI Agent              ║
    ║     For Elite Security Researchers & Developers           ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def create_parser():
    """Create argument parser with all subcommands"""
    parser = argparse.ArgumentParser(
        prog='kalighost',
        description='KaliGhost IDE - Advanced Security Development Environment',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  kalighost start --amnesic                    # Start in amnesic mode
  kalighost start --encrypted                  # Start with encrypted persistence
  kalighost agent --model uncensored-v1        # Launch AI agent
  kalighost sandbox --malware sample.exe       # Analyze malware in sandbox
  kalighost purple-team --target 192.168.1.0/24
  kalighost health-check                       # System health verification
        """
    )
    
    parser.add_argument('--version', '-v', action='version', version='KaliGhost IDE v1.0.0')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Start command
    start_parser = subparsers.add_parser('start', help='Start KaliGhost IDE')
    start_parser.add_argument('--amnesic', action='store_true', 
                              help='Run in amnesic mode (no disk traces)')
    start_parser.add_argument('--encrypted', action='store_true',
                              help='Enable encrypted persistence')
    start_parser.add_argument('--passphrase', type=str,
                              help='Passphrase for encrypted volume')
    start_parser.add_argument('--port', type=int, default=8080,
                              help='Web interface port')
    start_parser.add_argument('--headless', action='store_true',
                              help='Run without GUI (API only)')
    
    # Stop command
    stop_parser = subparsers.add_parser('stop', help='Stop KaliGhost IDE')
    stop_parser.add_argument('--force', action='store_true',
                             help='Force stop all processes')
    stop_parser.add_argument('--wipe', action='store_true',
                             help='Wipe temporary data on stop')
    
    # Agent command
    agent_parser = subparsers.add_parser('agent', help='Manage AI Agent')
    agent_parser.add_argument('--model', type=str, default='uncensored-v1',
                              choices=['uncensored-v1', 'security-expert', 'malware-analyst'],
                              help='AI model to load')
    agent_parser.add_argument('--gpu', action='store_true',
                              help='Use GPU acceleration')
    agent_parser.add_argument('--quantize', type=str, default='q4_k_m',
                              help='Quantization level for model')
    agent_parser.add_argument('--status', action='store_true',
                              help='Show agent status')
    agent_parser.add_argument('--unload', action='store_true',
                              help='Unload current model')
    
    # Sandbox command
    sandbox_parser = subparsers.add_parser('sandbox', help='Sandbox environment')
    sandbox_parser.add_argument('--malware', type=str,
                                help='Analyze malware sample')
    sandbox_parser.add_argument('--network', action='store_true',
                                help='Enable network monitoring')
    sandbox_parser.add_argument('--isolate', action='store_true',
                                help='Full network isolation')
    sandbox_parser.add_argument('--timeout', type=int, default=300,
                                help='Analysis timeout in seconds')
    
    # Purple team command
    purple_parser = subparsers.add_parser('purple-team', help='Purple team operations')
    purple_parser.add_argument('--target', type=str, required=True,
                               help='Target IP/CIDR')
    purple_parser.add_argument('--mode', type=str, default='full',
                               choices=['recon', 'exploit', 'post-exploit', 'full'],
                               help='Operation mode')
    purple_parser.add_argument('--stealth', action='store_true',
                               help='Low and slow stealth mode')
    purple_parser.add_argument('--report', type=str,
                               help='Output report file')
    
    # Project command
    project_parser = subparsers.add_parser('project', help='Project management')
    project_parser.add_argument('action', type=str,
                                choices=['new', 'open', 'list', 'delete', 'export'],
                                help='Project action')
    project_parser.add_argument('--name', type=str, help='Project name')
    project_parser.add_argument('--path', type=str, help='Project path')
    project_parser.add_argument('--encrypt', action='store_true',
                                help='Encrypt project workspace')
    
    # Health check command
    health_parser = subparsers.add_parser('health-check', 
                                          help='System health verification')
    health_parser.add_argument('--full', action='store_true',
                               help='Run full diagnostic suite')
    health_parser.add_argument('--fix', action='store_true',
                               help='Auto-fix detected issues')
    
    return parser


def main():
    """Main entry point"""
    print_banner()
    
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # Initialize core
    core = KalighostCore(verbose=args.verbose, debug=args.debug)
    
    try:
        if args.command == 'start':
            start_ide(core, args)
        elif args.command == 'stop':
            stop_ide(core, args)
        elif args.command == 'agent':
            manage_agent(core, args)
        elif args.command == 'sandbox':
            sandbox_mode(core, args)
        elif args.command == 'purple-team':
            purple_team(core, args)
        elif args.command == 'project':
            project_manager(core, args)
        elif args.command == 'health-check':
            health_check(core, args)
        else:
            parser.print_help()
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user. Cleaning up...")
        core.cleanup()
        sys.exit(130)
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
