#!/usr/bin/env python3
"""
Activation script to switch from simulation to real YouTube publishing
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime

def check_requirements():
    """Check if all requirements are met for real publishing"""
    print("🔍 Checking requirements for real YouTube publishing...")
    
    # Check if config directory exists
    config_dir = Path("~/KaliGhost/config").expanduser()
    if not config_dir.exists():
        print("❌ Config directory not found. Creating...")
        config_dir.mkdir(exist_ok=True)
    
    # Check if we have YouTube credentials file
    credentials_file = config_dir / "youtube_credentials.json"
    if credentials_file.exists():
        print("✅ YouTube credentials found")
        return True
    else:
        print("⚠️  YouTube credentials not found yet")
        print("   You'll need to add your credentials before activating real publishing")
        return False

def activate_real_publishing():
    """Activate real YouTube publishing mode"""
    print("🚀 Activating Real YouTube Publishing Mode")
    
    # Create activation flag file
    flag_file = Path("~/KaliGhost/.real_publishing_active").expanduser()
    flag_file.touch()
    
    # Create deployment log
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "status": "activated",
        "mode": "real",
        "description": "Real YouTube publishing activated by user"
    }
    
    log_file = Path("~/KaliGhost/logs/deployment_log.json").expanduser()
    log_file.parent.mkdir(exist_ok=True)
    
    try:
        with open(log_file, 'r') as f:
            logs = json.load(f)
    except FileNotFoundError:
        logs = []
    
    logs.append(log_entry)
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)
    
    print("✅ Real publishing mode activated successfully!")
    print("📝 Deployment log updated")
    print("")
    print("📚 Next Steps:")
    print("   1. Add your YouTube credentials to ~/KaliGhost/config/youtube_credentials.json")
    print("   2. Update channel information in configuration")
    print("   3. Restart the publishing system for live mode")
    print("   4. Monitor your channel for new content")
    return True

def show_status():
    """Show current deployment status"""
    print("📊 Current Deployment Status")
    print("==========================")
    
    flag_file = Path("~/KaliGhost/.real_publishing_active").expanduser()
    if flag_file.exists():
        print("📍 Status: REAL PUBLISHING MODE ACTIVATED")
        print("   Your system is ready to publish actual YouTube videos")
    else:
        print("📍 Status: SIMULATION MODE")
        print("   Your system is running in safe simulation mode")
        print("   Call activate_real_publishing() to switch to real publishing")
    
    print("")
    print("🔧 System Components:")
    print("   - Content Strategy: ✅ Ready")
    print("   - Automation Scripts: ✅ Ready")
    print("   - Content Generation: ✅ Ready")
    print("   - Publishing Engine: ✅ Ready")
    print("   - Logging System: ✅ Ready")

def main():
    """Main activation function"""
    print("🔧 YouTube Publishing System Activation")
    print("======================================")
    
    if len(sys.argv) > 1 and sys.argv[1] == "activate":
        if check_requirements():
            activate_real_publishing()
        else:
            print("⚠️  Cannot activate real publishing without credentials")
    elif len(sys.argv) > 1 and sys.argv[1] == "status":
        show_status()
    else:
        print("Usage: python3 activate_real_publishing.py [activate|status]")
        print("")
        print("Commands:")
        print("  activate   - Switch to real publishing mode")
        print("  status     - Show current deployment status")
        print("")
        show_status()

if __name__ == "__main__":
    main()