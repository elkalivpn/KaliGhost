#!/usr/bin/env python3
"""
🐉 KaliGhost Compliance & Ethics Engine
Legal automation, policy generation, regulatory compliance checking
"""

import json
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class Jurisdiction(Enum):
    """Legal jurisdictions"""
    US = "us"
    EU = "eu"
    UK = "uk"
    CANADA = "ca"
    AUSTRALIA = "au"
    SINGAPORE = "sg"
    JAPAN = "jp"


class ComplianceStandard(Enum):
    """Compliance standards"""
    GDPR = "gdpr"  # EU data protection
    HIPAA = "hipaa"  # Healthcare
    PCI_DSS = "pci_dss"  # Payment cards
    SOC_2 = "soc_2"  # Security controls
    ISO_27001 = "iso_27001"  # Information security
    CCPA = "ccpa"  # California privacy
    OWASP = "owasp"  # Web application security


class RiskLevel(Enum):
    """Legal/ethical risk levels"""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    NONE = 1


@dataclass
class ComplianceCheck:
    """Single compliance requirement"""
    id: str
    standard: ComplianceStandard
    requirement: str
    description: str
    code_implications: List[str]
    passing: bool
    remediation: Optional[str] = None


@dataclass
class EthicsAlert:
    """Ethical/legal concern"""
    id: str
    alert_type: str  # "unauthorized_access", "data_exfiltration", "encryption_bypass", etc
    risk_level: RiskLevel
    description: str
    affected_code: str
    legal_implication: str
    recommendation: str


@dataclass
class LegalDocument:
    """Generated legal document"""
    id: str
    doc_type: str  # "tos", "privacy_policy", "data_processing", "acceptable_use"
    jurisdiction: Jurisdiction
    content: str
    generated_at: str
    review_required: bool = True


class ComplianceEngine:
    """Regulatory compliance checking"""

    def __init__(self):
        self.standards_map = {
            ComplianceStandard.GDPR: self._check_gdpr,
            ComplianceStandard.HIPAA: self._check_hipaa,
            ComplianceStandard.PCI_DSS: self._check_pci_dss,
        }

    async def audit_compliance(
        self,
        source_code: str,
        data_types: List[str],
        standards: List[ComplianceStandard]
    ) -> List[ComplianceCheck]:
        """Audit code against compliance standards"""
        checks = []

        logger.info(f"🔍 Auditing compliance for {len(standards)} standards")

        for standard in standards:
            checker = self.standards_map.get(standard)
            if checker:
                result = checker(source_code, data_types)
                checks.append(result)
                logger.info(f"  {'✅' if result.passing else '❌'} {standard.value}: {result.requirement}")

        return checks

    def _check_gdpr(self, code: str, data_types: List[str]) -> ComplianceCheck:
        """Check GDPR compliance (EU data protection)"""
        # Check for encryption, consent mechanisms, data minimization
        has_encryption = "encrypt" in code.lower() or "ssl" in code.lower()
        has_consent = "consent" in code.lower() or "agree" in code.lower()
        has_deletion = "delete" in code.lower() or "purge" in code.lower()

        passing = has_encryption and has_consent and has_deletion

        return ComplianceCheck(
            id="gdpr_check",
            standard=ComplianceStandard.GDPR,
            requirement="Data Protection Regulation",
            description="Ensure data encryption, consent collection, and right to deletion",
            code_implications=["add_encryption", "implement_consent_flow", "add_data_deletion"],
            passing=passing,
            remediation="Implement AES-256 encryption, explicit consent forms, GDPR deletion endpoint" if not passing else None
        )

    def _check_hipaa(self, code: str, data_types: List[str]) -> ComplianceCheck:
        """Check HIPAA compliance (healthcare)"""
        has_encryption = "encrypt" in code.lower()
        has_audit_log = "log" in code.lower() or "audit" in code.lower()
        has_access_control = "permission" in code.lower() or "role" in code.lower()

        passing = has_encryption and has_audit_log and has_access_control

        return ComplianceCheck(
            id="hipaa_check",
            standard=ComplianceStandard.HIPAA,
            requirement="Healthcare Data Privacy",
            description="Ensure encryption, audit logging, and access controls for PHI",
            code_implications=["add_audit_logging", "enforce_access_controls"],
            passing=passing,
            remediation="Add comprehensive audit logging and role-based access control" if not passing else None
        )

    def _check_pci_dss(self, code: str, data_types: List[str]) -> ComplianceCheck:
        """Check PCI-DSS compliance (payment cards)"""
        # Check for hardcoded card numbers, unencrypted transmission
        has_no_card_storage = "card" not in code.lower() or "tokenize" in code.lower()
        has_encryption = "encrypt" in code.lower()
        has_tls = "tls" in code.lower() or "https" in code.lower()

        passing = has_no_card_storage and has_encryption and has_tls

        return ComplianceCheck(
            id="pci_dss_check",
            standard=ComplianceStandard.PCI_DSS,
            requirement="Payment Card Data Security",
            description="Never store raw card data, use tokenization and encryption",
            code_implications=["remove_card_storage", "use_tokenization", "enforce_tls"],
            passing=passing,
            remediation="Use payment gateway tokenization (Stripe/PayPal), TLS 1.2+, no card storage" if not passing else None
        )


class EthicsEngine:
    """Detect unethical/illegal code patterns"""

    RED_LINE_PATTERNS = {
        "unauthorized_access": [
            r"\.\.\/",  # Path traversal
            r"os\.system",  # Dangerous command execution
            r"eval\(",  # Code injection
            r"exec\(",  # Code execution
        ],
        "data_exfiltration": [
            r"requests\.post.*password",
            r"urllib.*credentials",
            r"send.*database",
        ],
        "encryption_bypass": [
            r"disable.*ssl",
            r"verify.*False",
            r"insecure.*certificate",
        ],
        "credential_hardcoding": [
            r"password\s*=\s*['\"]",
            r"api_key\s*=\s*['\"]",
            r"secret\s*=\s*['\"]",
        ]
    }

    async def check_ethics(self, source_code: str) -> List[EthicsAlert]:
        """Check code for ethical/legal violations"""
        alerts = []

        logger.info("⚖️  Running ethics and legality check")

        import re

        for alert_type, patterns in self.RED_LINE_PATTERNS.items():
            for pattern in patterns:
                matches = re.finditer(pattern, source_code, re.IGNORECASE)
                for match in matches:
                    line_num = source_code[:match.start()].count('\n') + 1

                    alert = EthicsAlert(
                        id=f"ethical_{alert_type}_{line_num}",
                        alert_type=alert_type,
                        risk_level=RiskLevel.CRITICAL if alert_type in ["unauthorized_access", "data_exfiltration"] else RiskLevel.HIGH,
                        description=f"Detected {alert_type} pattern at line {line_num}",
                        affected_code=source_code.split('\n')[line_num - 1][:100],
                        legal_implication=self._legal_implication(alert_type),
                        recommendation=self._recommendation(alert_type)
                    )
                    alerts.append(alert)
                    logger.warning(f"  🚨 {alert_type} detected at line {line_num}")

        if not alerts:
            logger.info("  ✅ No ethical violations detected")

        return alerts

    def _legal_implication(self, alert_type: str) -> str:
        """Get legal implication of violation"""
        implications = {
            "unauthorized_access": "Violates CFAA (Computer Fraud and Abuse Act) and similar laws",
            "data_exfiltration": "Violates GDPR, HIPAA, PCI-DSS, potential prosecution for data theft",
            "encryption_bypass": "May violate encryption standards and expose users to harm",
            "credential_hardcoding": "Violates security best practices, potential data breach liability",
        }
        return implications.get(alert_type, "Potential legal violation")

    def _recommendation(self, alert_type: str) -> str:
        """Get remediation recommendation"""
        recommendations = {
            "unauthorized_access": "Implement proper authorization checks, validate user permissions before accessing resources",
            "data_exfiltration": "Remove code that sends data without explicit user consent, implement audit logging",
            "encryption_bypass": "Enable TLS verification, use secure connection defaults",
            "credential_hardcoding": "Store secrets in environment variables or secure vaults (AWS Secrets Manager, HashiCorp Vault)",
        }
        return recommendations.get(alert_type, "Review and remediate per legal requirements")


class LegalDocumentGenerator:
    """Generate legal documents for products"""

    TEMPLATES = {
        "tos": "Terms of Service",
        "privacy_policy": "Privacy Policy",
        "data_processing": "Data Processing Agreement",
        "acceptable_use": "Acceptable Use Policy",
    }

    async def generate_tos(
        self,
        company_name: str,
        jurisdiction: Jurisdiction,
        services_description: str
    ) -> LegalDocument:
        """Generate Terms of Service"""
        logger.info(f"📜 Generating ToS for {company_name} ({jurisdiction.value})")

        content = f"""
TERMS OF SERVICE

Effective Date: {datetime.now().strftime('%B %d, %Y')}

1. AGREEMENT TO TERMS
By accessing and using {company_name} (the "Service"), you accept and agree to be bound by 
and comply with the terms and provision of this agreement.

2. SERVICES DESCRIPTION
{services_description}

3. JURISDICTION
These Terms are governed by the laws of {jurisdiction.value.upper()}.

4. LIMITATION OF LIABILITY
{company_name} SHALL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, 
CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING BUT NOT LIMITED TO DAMAGES 
FOR LOSS OF PROFITS, GOODWILL, USE, DATA, OR OTHER INTANGIBLE LOSSES.

5. ACCEPTABLE USE POLICY
Users agree NOT to:
  - Attempt unauthorized access
  - Disrupt service availability
  - Transmit malware or harmful code
  - Violate intellectual property rights
  - Harass or threaten other users

6. MODIFICATIONS
{company_name} reserves the right to modify these terms at any time with notice.

7. TERMINATION
{company_name} may terminate accounts that violate these terms.
"""

        doc = LegalDocument(
            id=f"tos_{company_name.lower()}",
            doc_type="tos",
            jurisdiction=jurisdiction,
            content=content,
            generated_at=datetime.now().isoformat(),
            review_required=True
        )

        logger.info(f"✅ ToS generated ({len(content)} chars)")
        return doc

    async def generate_privacy_policy(
        self,
        company_name: str,
        jurisdiction: Jurisdiction,
        data_types: List[str]
    ) -> LegalDocument:
        """Generate Privacy Policy"""
        logger.info(f"📜 Generating Privacy Policy for {company_name}")

        data_list = "\n  - ".join(data_types)

        content = f"""
PRIVACY POLICY

Effective Date: {datetime.now().strftime('%B %d, %Y')}

1. INFORMATION WE COLLECT
{company_name} collects the following types of information:
  - {data_list}

2. HOW WE USE YOUR DATA
We use collected data to:
  - Provide and improve our services
  - Communicate with users
  - Comply with legal obligations
  - Prevent fraud and abuse

3. DATA PROTECTION
We implement industry-standard security measures including:
  - AES-256 encryption
  - TLS for data transmission
  - Regular security audits
  - Access controls

4. YOUR RIGHTS
You have the right to:
  - Access your personal data
  - Request data correction
  - Request data deletion (subject to legal obligations)
  - Opt-out of marketing communications

5. THIRD-PARTY DISCLOSURE
We do NOT sell your data to third parties. We may share data with:
  - Service providers (under confidentiality agreements)
  - Legal authorities (when required by law)

6. CONTACT US
For privacy inquiries, contact: privacy@{company_name.lower()}.com
"""

        doc = LegalDocument(
            id=f"privacy_{company_name.lower()}",
            doc_type="privacy_policy",
            jurisdiction=jurisdiction,
            content=content,
            generated_at=datetime.now().isoformat(),
            review_required=True
        )

        logger.info(f"✅ Privacy Policy generated")
        return doc


class ComplianceAndEthicsEngine:
    """Orchestrates compliance, ethics, and legal operations"""

    def __init__(self):
        self.compliance = ComplianceEngine()
        self.ethics = EthicsEngine()
        self.legal_gen = LegalDocumentGenerator()

    async def full_compliance_audit(
        self,
        source_code: str,
        company_name: str,
        jurisdiction: Jurisdiction,
        standards: List[ComplianceStandard]
    ) -> Dict[str, Any]:
        """Complete compliance, ethics, and legal audit"""
        logger.info(f"🏛️  FULL COMPLIANCE AUDIT for {company_name}")

        # Compliance checks
        compliance_checks = await self.compliance.audit_compliance(
            source_code,
            data_types=["user_data", "payment_info"],
            standards=standards
        )

        # Ethics check
        ethics_alerts = await self.ethics.check_ethics(source_code)

        # Generate legal documents
        tos = await self.legal_gen.generate_tos(
            company_name,
            jurisdiction,
            "Software as a Service"
        )

        privacy_policy = await self.legal_gen.generate_privacy_policy(
            company_name,
            jurisdiction,
            ["email", "usage_data", "payment_method"]
        )

        # Calculate risk score
        compliance_passed = sum(1 for c in compliance_checks if c.passing)
        ethics_issues = len(ethics_alerts)
        risk_score = max(0, 100 - (ethics_issues * 20) - ((len(compliance_checks) - compliance_passed) * 10))

        logger.info(f"✅ Audit complete:")
        logger.info(f"  • Compliance: {compliance_passed}/{len(compliance_checks)} passed")
        logger.info(f"  • Ethics alerts: {ethics_issues}")
        logger.info(f"  • Risk score: {risk_score}/100")

        return {
            "compliance_checks": compliance_checks,
            "ethics_alerts": ethics_alerts,
            "legal_documents": [tos, privacy_policy],
            "risk_score": risk_score,
            "ready_for_launch": risk_score >= 75 and ethics_issues == 0
        }


# Singleton
_compliance_engine: Optional[ComplianceAndEthicsEngine] = None


def get_compliance_and_ethics_engine() -> ComplianceAndEthicsEngine:
    """Get or create singleton compliance engine"""
    global _compliance_engine
    if _compliance_engine is None:
        _compliance_engine = ComplianceAndEthicsEngine()
    return _compliance_engine
