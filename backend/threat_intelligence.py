#!/usr/bin/env python3
"""
🐉 KaliGhost OSINT & Threat Intelligence Engine
Automated reconnaissance, deep web monitoring, threat analysis
"""

import asyncio
import json
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Any, Set
from datetime import datetime, timedelta
import logging
import hashlib

logger = logging.getLogger(__name__)


class ThreatLevel(Enum):
    """Threat severity levels"""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    INFO = 1


@dataclass
class OSINTFinding:
    """Single OSINT intelligence finding"""
    id: str
    finding_type: str  # "email", "subdomain", "cloud_service", "leaked_cred", "dark_web_mention"
    value: str
    source: str
    threat_level: ThreatLevel
    discovered_at: str
    metadata: Dict[str, Any]
    actionable: bool = True


@dataclass
class ThreatReport:
    """Complete threat intelligence report"""
    id: str
    target: str
    report_type: str  # "target_recon", "third_party_scan", "dark_web_monitor"
    created_at: str
    findings: List[OSINTFinding]
    summary: str
    recommendations: List[str]
    threat_score: float  # 0-100


class OSINTCollector:
    """Automated Open Source Intelligence gathering"""

    def __init__(self):
        self.tools = {
            "emails": ["hunter.io", "email-format", "mailtester"],
            "subdomains": ["subfinder", "assetfinder", "crt.sh"],
            "cloud": ["cloud_enum", "s3scanner", "domain-scanner"],
            "employees": ["linkedin-scraper"],
            "dns": ["dnsdumpster", "dig"],
        }

    async def recon_target(self, target: str) -> List[OSINTFinding]:
        """Comprehensive reconnaissance on target"""
        findings = []
        
        logger.info(f"🔍 Starting OSINT recon on: {target}")

        # Email discovery
        emails = await self._discover_emails(target)
        for email in emails:
            findings.append(OSINTFinding(
                id=hashlib.md5(f"email_{email}".encode()).hexdigest(),
                finding_type="email",
                value=email,
                source="hunter.io",
                threat_level=ThreatLevel.INFO,
                discovered_at=datetime.now().isoformat(),
                metadata={"domain": target}
            ))
            logger.info(f"  📧 Email found: {email}")

        # Subdomain enumeration
        subdomains = await self._enumerate_subdomains(target)
        for subdomain in subdomains:
            findings.append(OSINTFinding(
                id=hashlib.md5(f"subdomain_{subdomain}".encode()).hexdigest(),
                finding_type="subdomain",
                value=subdomain,
                source="subfinder",
                threat_level=ThreatLevel.LOW,
                discovered_at=datetime.now().isoformat(),
                metadata={"parent_domain": target}
            ))
            logger.info(f"  🌐 Subdomain: {subdomain}")

        # Cloud services
        cloud_services = await self._scan_cloud_services(target)
        for service in cloud_services:
            findings.append(OSINTFinding(
                id=hashlib.md5(f"cloud_{service['name']}".encode()).hexdigest(),
                finding_type="cloud_service",
                value=service['name'],
                source="cloud_enum",
                threat_level=ThreatLevel.MEDIUM if not service['public'] else ThreatLevel.HIGH,
                discovered_at=datetime.now().isoformat(),
                metadata=service
            ))
            logger.info(f"  ☁️  Cloud: {service['name']} ({'public' if service['public'] else 'private'})")

        logger.info(f"✅ OSINT recon complete: {len(findings)} findings")
        return findings

    async def _discover_emails(self, domain: str) -> List[str]:
        """Discover email addresses associated with domain"""
        # Simulated - in production: call hunter.io, email-format APIs
        return [
            f"info@{domain}",
            f"admin@{domain}",
            f"contact@{domain}",
            f"support@{domain}",
        ]

    async def _enumerate_subdomains(self, domain: str) -> List[str]:
        """Enumerate subdomains"""
        # Simulated - in production: call subfinder, crt.sh API
        return [
            f"www.{domain}",
            f"api.{domain}",
            f"admin.{domain}",
            f"mail.{domain}",
            f"cdn.{domain}",
        ]

    async def _scan_cloud_services(self, domain: str) -> List[Dict[str, Any]]:
        """Scan for cloud services (S3, Azure, etc)"""
        # Simulated - in production: cloud_enum, s3scanner
        return [
            {"name": f"{domain}-backup", "provider": "S3", "public": True, "risk": "HIGH"},
            {"name": f"{domain}-prod", "provider": "S3", "public": False, "risk": "MEDIUM"},
            {"name": f"{domain}.blob.core.windows.net", "provider": "Azure", "public": False, "risk": "LOW"},
        ]

    async def scan_third_party(self, company_name: str) -> List[Dict[str, Any]]:
        """Scan vendors/suppliers for vulnerabilities"""
        logger.info(f"🔗 Scanning third-party risks for: {company_name}")
        
        vulns = []
        
        # In production: Check breach databases, CVE databases for vendors
        # Simulate finding vulnerable vendor
        vulns.append({
            "vendor": "popular-npm-package",
            "relationship": "dependency",
            "vulnerability": "RCE in v1.2.3",
            "severity": "CRITICAL",
            "your_risk": "HIGH",
            "remediation": "Update to v1.2.4"
        })
        
        logger.info(f"  ⚠️  Found {len(vulns)} third-party vulnerabilities")
        return vulns


class DarkWebMonitor:
    """Continuous dark web monitoring for credentials, code, products"""

    def __init__(self):
        self.monitoring_active = False
        self.last_scan = None
        self.alerts = []

    async def start_monitoring(self, watch_terms: List[str]) -> bool:
        """Start monitoring dark web for watch terms"""
        logger.info(f"🕷️  Starting dark web monitoring for {len(watch_terms)} terms")
        
        self.monitoring_active = True
        self.watch_terms = watch_terms
        
        # In production: Connect to Tor, monitor marketplaces, forums
        # For now: Simulate periodic checks
        await self._simulate_monitoring()
        
        return True

    async def _simulate_monitoring(self):
        """Simulate dark web monitoring"""
        while self.monitoring_active:
            logger.info("  🔍 Checking dark web forums and marketplaces...")
            
            # Simulated finding: credentials leaked
            alert = {
                "timestamp": datetime.now().isoformat(),
                "type": "credentials_found",
                "location": "AlphaBay clone forum",
                "content": "Database dump: company_name_2025_full.sql",
                "severity": "CRITICAL",
                "action": "Immediate password reset recommended"
            }
            
            self.alerts.append(alert)
            logger.warning(f"  🚨 ALERT: {alert['type']} on {alert['location']}")
            
            # Check every hour
            await asyncio.sleep(3600)

    async def stop_monitoring(self):
        """Stop dark web monitoring"""
        self.monitoring_active = False
        logger.info("🕷️  Dark web monitoring stopped")

    def get_alerts(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get recent alerts"""
        cutoff = datetime.now() - timedelta(hours=hours)
        
        return [
            a for a in self.alerts
            if datetime.fromisoformat(a['timestamp']) > cutoff
        ]


class ThreatIntelligenceEngine:
    """Orchestrates OSINT, threat analysis, monitoring"""

    def __init__(self):
        self.osint = OSINTCollector()
        self.darkweb = DarkWebMonitor()
        self.reports = {}

    async def full_threat_assessment(
        self,
        target: str,
        check_third_party: bool = True,
        watch_dark_web: bool = True
    ) -> ThreatReport:
        """Complete threat assessment"""
        from pathlib import Path
        
        logger.info(f"🛡️  FULL THREAT ASSESSMENT: {target}")

        report_id = hashlib.md5(f"{target}_{datetime.now()}".encode()).hexdigest()
        findings = []

        # Phase 1: OSINT
        osint_findings = await self.osint.recon_target(target)
        findings.extend(osint_findings)

        # Phase 2: Third-party scan
        third_party_vulns = []
        if check_third_party:
            third_party_vulns = await self.osint.scan_third_party(target)
            for vuln in third_party_vulns:
                findings.append(OSINTFinding(
                    id=hashlib.md5(f"third_party_{vuln['vendor']}".encode()).hexdigest(),
                    finding_type="third_party_vulnerability",
                    value=f"{vuln['vendor']}: {vuln['vulnerability']}",
                    source="CVE database",
                    threat_level=ThreatLevel.CRITICAL if vuln['severity'] == 'CRITICAL' else ThreatLevel.HIGH,
                    discovered_at=datetime.now().isoformat(),
                    metadata=vuln
                ))

        # Phase 3: Start dark web monitoring
        if watch_dark_web:
            watch_terms = [target, target.replace('.', ''), target.split('.')[0]]
            await self.darkweb.start_monitoring(watch_terms)

        # Calculate threat score
        critical_count = sum(1 for f in findings if f.threat_level == ThreatLevel.CRITICAL)
        high_count = sum(1 for f in findings if f.threat_level == ThreatLevel.HIGH)
        threat_score = min(100, (critical_count * 25 + high_count * 10))

        # Generate recommendations
        recommendations = []
        if critical_count > 0:
            recommendations.append("🚨 IMMEDIATE: Address critical findings")
        if len([f for f in findings if f.finding_type == "subdomain"]) > 10:
            recommendations.append("⚠️  Consider consolidating or hardening subdomain infrastructure")
        if any(f.finding_type == "cloud_service" and f.threat_level == ThreatLevel.HIGH for f in findings):
            recommendations.append("☁️  Audit and restrict cloud storage permissions")

        report = ThreatReport(
            id=report_id,
            target=target,
            report_type="target_recon",
            created_at=datetime.now().isoformat(),
            findings=findings,
            summary=f"Found {len(findings)} intelligence points ({critical_count} critical, {high_count} high)",
            recommendations=recommendations,
            threat_score=threat_score
        )

        self.reports[report_id] = report
        logger.info(f"✅ Threat assessment complete. Score: {threat_score}/100")

        return report


# Singleton
_threat_intel_engine: Optional[ThreatIntelligenceEngine] = None


def get_threat_intelligence_engine() -> ThreatIntelligenceEngine:
    """Get or create singleton threat intelligence engine"""
    global _threat_intel_engine
    if _threat_intel_engine is None:
        _threat_intel_engine = ThreatIntelligenceEngine()
    return _threat_intel_engine
