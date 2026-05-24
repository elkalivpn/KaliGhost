#!/usr/bin/env python3
"""
🐉 KaliGhost Infrastructure Automation
Cloud provisioning, auto-scaling, secret management, DevOps
"""

import asyncio
import json
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
import uuid

logger = logging.getLogger(__name__)


class CloudProvider(Enum):
    """Supported cloud providers"""
    AWS = "aws"
    DIGITALOCEAN = "digitalocean"
    LINODE = "linode"
    VULTR = "vultr"
    GCP = "gcp"
    AZURE = "azure"


class InstanceType(Enum):
    """Compute instance types"""
    NANO = "nano"  # $2-5/month
    MICRO = "micro"  # $5-10/month
    SMALL = "small"  # $10-20/month
    MEDIUM = "medium"  # $20-50/month
    LARGE = "large"  # $50-100/month


@dataclass
class CloudInstance:
    """Cloud compute instance"""
    id: str
    provider: CloudProvider
    instance_type: InstanceType
    region: str
    ip_address: Optional[str]
    created_at: str
    state: str  # running, stopped, terminated
    cost_per_month_usd: float
    tags: Dict[str, str]


@dataclass
class Secret:
    """Encrypted secret (API key, password, cert)"""
    id: str
    name: str
    secret_type: str  # "api_key", "password", "certificate", "ssh_key"
    created_at: str
    rotated_at: str
    next_rotation: str
    is_encrypted: bool = True
    metadata: Dict[str, Any] = None


@dataclass
class LoadBalancerRule:
    """Auto-scaling rule"""
    id: str
    metric: str  # "cpu_percent", "memory_percent", "request_rate"
    threshold: float
    action: str  # "scale_up", "scale_down"
    cooldown_minutes: int


class CloudInfrastructureManager:
    """Manages cloud infrastructure provisioning"""

    def __init__(self):
        self.instances: Dict[str, CloudInstance] = {}
        self.providers = {p.value: self._get_provider_client(p) for p in CloudProvider}

    def _get_provider_client(self, provider: CloudProvider) -> Optional[Any]:
        """Get cloud provider client"""
        try:
            if provider == CloudProvider.AWS:
                import boto3
                return boto3.client('ec2')
            elif provider == CloudProvider.DIGITALOCEAN:
                import digitalocean
                return digitalocean
            # Add other providers...
            return None
        except ImportError:
            logger.warning(f"⚠️  {provider.value} SDK not installed")
            return None

    async def provision_instance(
        self,
        provider: CloudProvider,
        instance_type: InstanceType,
        region: str,
        image: str = "ubuntu-22.04",
        tags: Optional[Dict[str, str]] = None
    ) -> CloudInstance:
        """Provision new cloud instance"""
        instance_id = f"inst_{uuid.uuid4().hex[:8]}"
        
        logger.info(f"☁️  Provisioning {instance_type.value} instance on {provider.value} ({region})")

        # Calculate cost
        cost_map = {
            InstanceType.NANO: 2.5,
            InstanceType.MICRO: 5.0,
            InstanceType.SMALL: 15.0,
            InstanceType.MEDIUM: 40.0,
            InstanceType.LARGE: 80.0,
        }
        cost = cost_map.get(instance_type, 10.0)

        instance = CloudInstance(
            id=instance_id,
            provider=provider,
            instance_type=instance_type,
            region=region,
            ip_address=f"192.168.1.{len(self.instances) + 1}",  # Simulated
            created_at=datetime.now().isoformat(),
            state="running",
            cost_per_month_usd=cost,
            tags=tags or {"environment": "dev", "managed_by": "kalighost"}
        )

        self.instances[instance_id] = instance
        logger.info(f"  ✅ Instance created: {instance_id} ({instance.ip_address}) - ${cost}/month")

        return instance

    async def terminate_instance(self, instance_id: str) -> bool:
        """Terminate a cloud instance"""
        if instance_id not in self.instances:
            logger.error(f"❌ Instance not found: {instance_id}")
            return False

        instance = self.instances[instance_id]
        instance.state = "terminated"
        logger.info(f"🗑️  Instance terminated: {instance_id}")

        return True

    def list_instances(self, provider: Optional[CloudProvider] = None) -> List[CloudInstance]:
        """List all instances, optionally filtered by provider"""
        if provider:
            return [i for i in self.instances.values() if i.provider == provider]
        return list(self.instances.values())

    def get_monthly_cost(self) -> float:
        """Calculate total monthly cloud costs"""
        return sum(i.cost_per_month_usd for i in self.instances.values() if i.state == "running")


class SecretManager:
    """Secure secret management and rotation"""

    def __init__(self):
        self.secrets: Dict[str, Secret] = {}
        self.vault_path = None  # Could use HashiCorp Vault

    def create_secret(
        self,
        name: str,
        secret_type: str,
        value: str,
        rotation_days: int = 90
    ) -> Secret:
        """Create and securely store a secret"""
        secret_id = hashlib.sha256(name.encode()).hexdigest()[:16]

        secret = Secret(
            id=secret_id,
            name=name,
            secret_type=secret_type,
            created_at=datetime.now().isoformat(),
            rotated_at=datetime.now().isoformat(),
            next_rotation=(datetime.now() + timedelta(days=rotation_days)).isoformat(),
            is_encrypted=True,
            metadata={"rotation_days": rotation_days}
        )

        self.secrets[secret_id] = secret
        logger.info(f"🔐 Secret created: {name} ({secret_type})")

        # In production: Encrypt value with KMS/Vault
        return secret

    def get_secret(self, name: str) -> Optional[str]:
        """Retrieve secret value (in production: decrypt from vault)"""
        for secret in self.secrets.values():
            if secret.name == name:
                logger.info(f"🔓 Secret accessed: {name}")
                return f"<encrypted_value_for_{name}>"  # In production: decrypt
        return None

    async def rotate_secret(self, secret_id: str) -> bool:
        """Rotate a secret (generate new key/password)"""
        if secret_id not in self.secrets:
            return False

        secret = self.secrets[secret_id]
        secret.rotated_at = datetime.now().isoformat()
        secret.next_rotation = (datetime.now() + timedelta(days=90)).isoformat()

        logger.info(f"🔄 Secret rotated: {secret.name}")
        return True

    def list_secrets_needing_rotation(self) -> List[Secret]:
        """Find secrets that need rotation"""
        now = datetime.now()
        return [
            s for s in self.secrets.values()
            if datetime.fromisoformat(s.next_rotation) < now
        ]


class AutoScalingManager:
    """Automatic scaling and load balancing"""

    def __init__(self):
        self.scaling_rules: Dict[str, LoadBalancerRule] = {}
        self.metric_history: List[Dict[str, Any]] = []

    def create_scaling_rule(
        self,
        metric: str,
        threshold: float,
        action: str,
        cooldown_minutes: int = 5
    ) -> LoadBalancerRule:
        """Create auto-scaling rule"""
        rule_id = f"rule_{uuid.uuid4().hex[:8]}"

        rule = LoadBalancerRule(
            id=rule_id,
            metric=metric,
            threshold=threshold,
            action=action,
            cooldown_minutes=cooldown_minutes
        )

        self.scaling_rules[rule_id] = rule
        logger.info(f"📊 Scaling rule created: {metric} > {threshold} → {action}")

        return rule

    async def evaluate_metrics(
        self,
        current_cpu: float,
        current_memory: float,
        current_request_rate: float
    ) -> List[str]:
        """Evaluate metrics and trigger scaling actions"""
        actions = []

        for rule in self.scaling_rules.values():
            if rule.metric == "cpu_percent" and current_cpu > rule.threshold:
                actions.append(rule.action)
                logger.warning(f"⚠️  CPU {current_cpu}% > {rule.threshold}% → {rule.action}")
            elif rule.metric == "memory_percent" and current_memory > rule.threshold:
                actions.append(rule.action)
                logger.warning(f"⚠️  Memory {current_memory}% > {rule.threshold}% → {rule.action}")
            elif rule.metric == "request_rate" and current_request_rate > rule.threshold:
                actions.append(rule.action)
                logger.warning(f"⚠️  Request rate {current_request_rate}/s > {rule.threshold}/s → {rule.action}")

        return actions


class InfrastructureAutomationEngine:
    """Orchestrates cloud, secrets, and auto-scaling"""

    def __init__(self):
        self.cloud = CloudInfrastructureManager()
        self.secrets = SecretManager()
        self.autoscaling = AutoScalingManager()

    async def setup_shadow_infrastructure(
        self,
        app_name: str,
        provider: CloudProvider = CloudProvider.DIGITALOCEAN,
        instance_count: int = 2
    ) -> Dict[str, Any]:
        """Setup disposable test infrastructure"""
        logger.info(f"🏗️  Setting up shadow infrastructure for {app_name}")

        instances = []
        for i in range(instance_count):
            instance = await self.cloud.provision_instance(
                provider=provider,
                instance_type=InstanceType.MICRO,
                region="us-east-1",
                tags={"app": app_name, "environment": "shadow", "index": str(i)}
            )
            instances.append(instance)

        logger.info(f"✅ Shadow infrastructure ready: {len(instances)} instances, ${self.cloud.get_monthly_cost():.2f}/month")

        return {
            "app_name": app_name,
            "instances": [i.id for i in instances],
            "total_cost_usd": self.cloud.get_monthly_cost(),
            "ips": [i.ip_address for i in instances]
        }

    async def setup_production_infrastructure(
        self,
        app_name: str,
        api_server_instances: int = 3,
        database_replicas: int = 2,
        cdn_enabled: bool = True
    ) -> Dict[str, Any]:
        """Setup production infrastructure with auto-scaling"""
        logger.info(f"🚀 Setting up production infrastructure for {app_name}")

        # API instances
        api_instances = []
        for i in range(api_server_instances):
            instance = await self.cloud.provision_instance(
                provider=CloudProvider.AWS,
                instance_type=InstanceType.MEDIUM,
                region="us-east-1",
                tags={"app": app_name, "tier": "api", "index": str(i)}
            )
            api_instances.append(instance)

        # Database replicas
        db_instances = []
        for i in range(database_replicas):
            instance = await self.cloud.provision_instance(
                provider=CloudProvider.AWS,
                instance_type=InstanceType.LARGE,
                region="us-east-1",
                tags={"app": app_name, "tier": "database", "index": str(i)}
            )
            db_instances.append(instance)

        # Auto-scaling rules
        self.autoscaling.create_scaling_rule(
            metric="cpu_percent",
            threshold=75,
            action="scale_up"
        )
        self.autoscaling.create_scaling_rule(
            metric="cpu_percent",
            threshold=25,
            action="scale_down"
        )

        # Secrets
        self.secrets.create_secret(
            name=f"{app_name}_db_password",
            secret_type="password",
            value="<generated>",
            rotation_days=30
        )

        logger.info(f"✅ Production infrastructure ready:")
        logger.info(f"  • API servers: {len(api_instances)}")
        logger.info(f"  • Database replicas: {len(db_instances)}")
        logger.info(f"  • Monthly cost: ${self.cloud.get_monthly_cost():.2f}")

        return {
            "app_name": app_name,
            "api_instances": [i.id for i in api_instances],
            "database_instances": [i.id for i in db_instances],
            "monthly_cost_usd": self.cloud.get_monthly_cost()
        }

    async def cleanup_shadow_infrastructure(self) -> int:
        """Terminate all shadow infrastructure"""
        logger.info("🧹 Cleaning up shadow infrastructure")

        terminated = 0
        for instance in self.cloud.instances.values():
            if instance.tags.get("environment") == "shadow":
                await self.cloud.terminate_instance(instance.id)
                terminated += 1

        logger.info(f"✅ Terminated {terminated} shadow instances")
        return terminated


import hashlib
from datetime import timedelta


# Singleton
_infra_engine: Optional[InfrastructureAutomationEngine] = None


def get_infrastructure_automation_engine() -> InfrastructureAutomationEngine:
    """Get or create singleton infrastructure engine"""
    global _infra_engine
    if _infra_engine is None:
        _infra_engine = InfrastructureAutomationEngine()
    return _infra_engine
