#!/usr/bin/env python3
"""
Professional Security Scanner for KaliGhost Pro
Advanced vulnerability assessment and security analysis tool
"""

import argparse
import sys
import os
import json
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import subprocess
import threading
from datetime import datetime

class ProfessionalSecurityScanner:
    """Professional security scanner with advanced analysis capabilities"""
    
    def __init__(self):
        self.findings = []
        self.scan_targets = []
        self.scan_options = {}
        self.report_format = "json"
        self.verbose = False
        self.output_file = None
        
    def scan_project_security(self, project_path: str) -> Dict:
        """Perform comprehensive security scan of project"""
        if self.verbose:
            print("🔍 [PROFESSIONAL SECURITY SCAN] Starting comprehensive analysis...")
            
        findings = {
            "scan_timestamp": datetime.now().isoformat(),
            "project_path": project_path,
            "findings": [],
            "summary": {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
                "info": 0
            }
        }
        
        # Check file permissions
        permission_findings = self._check_file_permissions(project_path)
        findings["findings"].extend(permission_findings)
        
        # Check for sensitive files
        sensitive_findings = self._check_sensitive_files(project_path)
        findings["findings"].extend(sensitive_findings)
        
        # Check dependencies
        dependency_findings = self._check_dependencies(project_path)
        findings["findings"].extend(dependency_findings)
        
        # Check configuration files
        config_findings = self._check_config_files(project_path)
        findings["findings"].extend(config_findings)
        
        # Calculate summary
        for finding in findings["findings"]:
            severity = finding["severity"].lower()
            if severity in findings["summary"]:
                findings["summary"][severity] += 1
                
        return findings
    
    def _check_file_permissions(self, project_path: str) -> List[Dict]:
        """Check for insecure file permissions"""
        findings = []
        insecure_files = []
        
        # Common files that should have restricted permissions
        sensitive_patterns = [
            "*.key", "*.pem", "*.cert", "*.crt", 
            "config/*.ini", "config/*.json", "config/*.yaml",
            ".env", "*.secret", "secrets/*"
        ]
        
        for pattern in sensitive_patterns:
            files = list(Path(project_path).glob(pattern))
            insecure_files.extend(files)
            
        for file_path in insecure_files:
            try:
                stat_info = file_path.stat()
                # Check if file has group/others read permissions
                if stat_info.st_mode & 0o077:
                    findings.append({
                        "id": f"PERM-{hashlib.md5(str(file_path).encode()).hexdigest()[:8]}",
                        "type": "Insecure File Permissions",
                        "severity": "HIGH",
                        "file": str(file_path),
                        "description": f"File has insecure permissions: {oct(stat_info.st_mode)[-3:]}",
                        "recommendation": "Restrict file permissions to 600 or 400",
                        "details": {
                            "current_permissions": oct(stat_info.st_mode)[-3:],
                            "expected_permissions": "600 or 400"
                        }
                    })
            except Exception as e:
                if self.verbose:
                    print(f"⚠️  Warning checking permissions for {file_path}: {e}")
                    
        return findings
    
    def _check_sensitive_files(self, project_path: str) -> List[Dict]:
        """Check for accidentally committed sensitive files"""
        findings = []
        sensitive_patterns = [
            "*password*", "*secret*", "*token*", "*apikey*",
            "*.pem", "*.key", "id_rsa*", "*.env*"
        ]
        
        exclude_dirs = {".git", "venv", "__pycache__", "node_modules"}
        
        for root, dirs, files in os.walk(project_path):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                file_path = Path(root) / file
                file_str = str(file_path).lower()
                
                # Check against sensitive patterns
                for pattern in sensitive_patterns:
                    if pattern.replace("*", "") in file_str:
                        # Read file to check for actual sensitive content
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read(1000)  # Read first 1000 chars
                                
                            # Check for common sensitive content patterns
                            sensitive_indicators = [
                                "password", "secret", "token", "api_key", "aws_access",
                                "-----BEGIN PRIVATE KEY-----", "-----BEGIN RSA PRIVATE KEY-----"
                            ]
                            
                            for indicator in sensitive_indicators:
                                if indicator.lower() in content.lower():
                                    findings.append({
                                        "id": f"SENS-{hashlib.md5(str(file_path).encode()).hexdigest()[:8]}",
                                        "type": "Sensitive Information Exposure",
                                        "severity": "CRITICAL",
                                        "file": str(file_path),
                                        "description": f"Potentially sensitive file containing '{indicator}'",
                                        "recommendation": "Remove sensitive information and use secure storage",
                                        "details": {
                                            "indicator_found": indicator,
                                            "file_preview": content[:200] + "..." if len(content) > 200 else content
                                        }
                                    })
                                    break  # Found one, no need to check others
                        except Exception as e:
                            if self.verbose:
                                print(f"⚠️  Warning reading {file_path}: {e}")
                            
        return findings
    
    def _check_dependencies(self, project_path: str) -> List[Dict]:
        """Check for vulnerable dependencies"""
        findings = []
        
        # Check Python requirements
        requirements_files = ["requirements.txt", "requirements-dev.txt"]
        for req_file in requirements_files:
            req_path = Path(project_path) / req_file
            if req_path.exists():
                try:
                    result = subprocess.run([
                        sys.executable, "-m", "pip", "list", "--outdated", "--format", "json"
                    ], capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0:
                        outdated_packages = json.loads(result.stdout)
                        for package in outdated_packages:
                            findings.append({
                                "id": f"DEP-{package['name'][:8]}",
                                "type": "Outdated Dependency",
                                "severity": "MEDIUM",
                                "file": str(req_path),
                                "description": f"Package {package['name']} can be updated from {package['version']} to {package['latest_version']}",
                                "recommendation": f"Update {package['name']} to latest version",
                                "details": {
                                    "current_version": package['version'],
                                    "latest_version": package['latest_version'],
                                    "package_name": package['name']
                                }
                            })
                except Exception as e:
                    if self.verbose:
                        print(f"⚠️  Warning checking dependencies: {e}")
                        
        return findings
    
    def _check_config_files(self, project_path: str) -> List[Dict]:
        """Check configuration files for security issues"""
        findings = []
        config_files = list(Path(project_path).glob("**/*.ini"))
        config_files.extend(Path(project_path).glob("**/*.yaml"))
        config_files.extend(Path(project_path).glob("**/*.yml"))
        config_files.extend(Path(project_path).glob("**/*.json"))
        
        for config_file in config_files:
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Check for common security misconfigurations
                insecure_patterns = [
                    ("debug = true", "DEBUG-ENABLED", "MEDIUM"),
                    ("password =", "HARDCODED-PASSWORD", "CRITICAL"),
                    ("secret =", "HARDCODED-SECRET", "CRITICAL"),
                    ("key =", "HARDCODED-KEY", "HIGH"),
                    ("admin = true", "PRIVILEGE-ESCALATION", "HIGH")
                ]
                
                for pattern, finding_id, severity in insecure_patterns:
                    if pattern.lower() in content.lower():
                        findings.append({
                            "id": f"CONF-{finding_id}",
                            "type": "Insecure Configuration",
                            "severity": severity,
                            "file": str(config_file),
                            "description": f"Insecure configuration pattern found: '{pattern}'",
                            "recommendation": "Review and secure configuration settings",
                            "details": {
                                "pattern_matched": pattern,
                                "file_line_count": len(content.split('\n'))
                            }
                        })
            except Exception as e:
                if self.verbose:
                    print(f"⚠️  Warning checking config file {config_file}: {e}")
                    
        return findings
    
    def generate_report(self, findings: Dict, format: str = "json") -> str:
        """Generate professional security report"""
        if format.lower() == "json":
            return json.dumps(findings, indent=2)
        elif format.lower() == "html":
            return self._generate_html_report(findings)
        else:
            return self._generate_text_report(findings)
    
    def _generate_text_report(self, findings: Dict) -> str:
        """Generate text format security report"""
        report = []
        report.append("=" * 80)
        report.append("PROFESSIONAL SECURITY SCAN REPORT")
        report.append("=" * 80)
        report.append(f"Scan Timestamp: {findings['scan_timestamp']}")
        report.append(f"Project Path: {findings['project_path']}")
        report.append("")
        
        # Summary
        report.append("SUMMARY")
        report.append("-" * 20)
        summary = findings['summary']
        report.append(f"Critical Issues: {summary['critical']}")
        report.append(f"High Issues: {summary['high']}")
        report.append(f"Medium Issues: {summary['medium']}")
        report.append(f"Low Issues: {summary['low']}")
        report.append(f"Info Issues: {summary['info']}")
        report.append("")
        
        # Detailed findings
        if findings['findings']:
            report.append("DETAILED FINDINGS")
            report.append("-" * 20)
            for i, finding in enumerate(findings['findings'], 1):
                report.append(f"{i}. [{finding['severity']}] {finding['type']}")
                report.append(f"   File: {finding['file']}")
                report.append(f"   Description: {finding['description']}")
                report.append(f"   Recommendation: {finding['recommendation']}")
                if 'details' in finding:
                    report.append(f"   Details: {finding['details']}")
                report.append("")
        else:
            report.append("No security issues found.")
            
        report.append("=" * 80)
        report.append("END OF REPORT")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def _generate_html_report(self, findings: Dict) -> str:
        """Generate HTML format security report"""
        html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Professional Security Scan Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background-color: #22AA55; color: white; padding: 20px; border-radius: 5px; }
        .summary { background-color: #f5f5f5; padding: 15px; margin: 20px 0; border-radius: 5px; }
        .finding { border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }
        .critical { border-left: 5px solid #ff5555; }
        .high { border-left: 5px solid #ffaa00; }
        .medium { border-left: 5px solid #ffff00; }
        .low { border-left: 5px solid #22aa55; }
        .info { border-left: 5px solid #969696; }
        .severity-critical { color: #ff5555; font-weight: bold; }
        .severity-high { color: #ffaa00; font-weight: bold; }
        .severity-medium { color: #ffff00; font-weight: bold; }
        .severity-low { color: #22aa55; font-weight: bold; }
        .severity-info { color: #969696; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Professional Security Scan Report</h1>
        <p>Scan Timestamp: {timestamp}</p>
        <p>Project Path: {project_path}</p>
    </div>
    
    <div class="summary">
        <h2>Summary</h2>
        <p>Critical Issues: <span class="severity-critical">{critical}</span></p>
        <p>High Issues: <span class="severity-high">{high}</span></p>
        <p>Medium Issues: <span class="severity-medium">{medium}</span></p>
        <p>Low Issues: <span class="severity-low">{low}</span></p>
        <p>Info Issues: <span class="severity-info">{info}</span></p>
    </div>
    
    <div class="findings">
        <h2>Detailed Findings</h2>
        {findings_html}
    </div>
</body>
</html>
        """
        
        findings_html = ""
        if findings['findings']:
            for finding in findings['findings']:
                severity_class = finding['severity'].lower()
                findings_html += f"""
        <div class="finding {severity_class}">
            <h3>[<span class="severity-{severity_class}">{finding['severity']}</span>] {finding['type']}</h3>
            <p><strong>File:</strong> {finding['file']}</p>
            <p><strong>Description:</strong> {finding['description']}</p>
            <p><strong>Recommendation:</strong> {finding['recommendation']}</p>
            {f"<p><strong>Details:</strong> {finding['details']}</p>" if 'details' in finding else ""}
        </div>
                """
        else:
            findings_html = "<p>No security issues found.</p>"
            
        return html_template.format(
            timestamp=findings['scan_timestamp'],
            project_path=findings['project_path'],
            critical=findings['summary']['critical'],
            high=findings['summary']['high'],
            medium=findings['summary']['medium'],
            low=findings['summary']['low'],
            info=findings['summary']['info'],
            findings_html=findings_html
        )

def main():
    """Main function for professional security scanner"""
    parser = argparse.ArgumentParser(description="Professional Security Scanner for KaliGhost Pro")
    parser.add_argument("project_path", nargs="?", default=".", help="Path to project directory")
    parser.add_argument("--format", choices=["json", "text", "html"], default="text", help="Report format")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--check-permissions", action="store_true", help="Check file permissions")
    parser.add_argument("--check-sensitive", action="store_true", help="Check for sensitive files")
    parser.add_argument("--check-dependencies", action="store_true", help="Check dependencies")
    parser.add_argument("--check-config", action="store_true", help="Check configuration files")
    
    args = parser.parse_args()
    
    # Create scanner instance
    scanner = ProfessionalSecurityScanner()
    scanner.verbose = args.verbose
    scanner.output_file = args.output
    
    # Determine what to check
    if not any([args.check_permissions, args.check_sensitive, args.check_dependencies, args.check_config]):
        # Check everything by default
        check_all = True
    else:
        check_all = False
    
    # Perform security scan
    try:
        findings = scanner.scan_project_security(args.project_path)
        
        # Generate report
        report = scanner.generate_report(findings, args.format)
        
        # Output report
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"✅ Professional security report saved to {args.output}")
        else:
            print(report)
            
    except Exception as e:
        print(f"❌ Error during security scan: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()