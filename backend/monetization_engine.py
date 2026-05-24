#!/usr/bin/env python3
"""
🐉 KaliGhost Monetization Engine
Stripe integration, licensing, usage tracking, billing automation
Complete SaaS monetization stack
"""

import json
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging
import hashlib
import uuid

logger = logging.getLogger(__name__)


class PricingModel(Enum):
    """Pricing models"""
    FLAT_RATE = "flat_rate"
    TIERED = "tiered"
    USAGE_BASED = "usage_based"
    FREEMIUM = "freemium"


class LicenseType(Enum):
    """License types"""
    PERPETUAL = "perpetual"
    SUBSCRIPTION = "subscription"
    TRIAL = "trial"
    SITE = "site"  # Single machine
    FLOATING = "floating"  # N concurrent users


@dataclass
class PricingTier:
    """Single pricing tier"""
    id: str
    name: str
    price_usd: float
    billing_interval: str  # "month", "year", "one_time"
    features: List[str]
    stripe_product_id: Optional[str] = None
    stripe_price_id: Optional[str] = None


@dataclass
class License:
    """Single customer license"""
    id: str
    customer_id: str
    license_key: str
    type: LicenseType
    tier: str
    issued_at: str
    expires_at: Optional[str] = None
    max_activations: int = 1
    active_activations: int = 0
    is_valid: bool = True


@dataclass
class UsageEvent:
    """Track customer usage (for metering)"""
    id: str
    customer_id: str
    license_id: str
    event_type: str  # "api_call", "file_processed", "computation", etc
    quantity: int
    timestamp: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class Invoice:
    """Customer invoice"""
    id: str
    customer_id: str
    stripe_invoice_id: str
    amount_usd: float
    currency: str
    status: str  # "draft", "open", "paid", "void"
    issued_at: str
    due_at: str
    paid_at: Optional[str] = None
    items: List[Dict[str, Any]] = None


class MonetizationEngine:
    """Complete monetization stack"""

    def __init__(self, stripe_api_key: Optional[str] = None):
        self.stripe_api_key = stripe_api_key or self._get_from_env("STRIPE_API_KEY")
        self.pricing_tiers: Dict[str, PricingTier] = {}
        self.licenses: Dict[str, License] = {}
        self.usage_events: List[UsageEvent] = []
        self.invoices: Dict[str, Invoice] = {}
        
        # Initialize Stripe client if available
        if self.stripe_api_key:
            try:
                import stripe
                stripe.api_key = self.stripe_api_key
                self.stripe = stripe
                logger.info("✅ Stripe client initialized")
            except ImportError:
                logger.warning("⚠️  stripe-python not installed")
                self.stripe = None
        else:
            logger.warning("⚠️  STRIPE_API_KEY not set")
            self.stripe = None

    def _get_from_env(self, key: str) -> Optional[str]:
        """Get from environment"""
        import os
        return os.getenv(key)

    # ============================================================================
    # Pricing Management
    # ============================================================================

    def create_pricing_tier(
        self,
        name: str,
        price_usd: float,
        features: List[str],
        billing_interval: str = "month"
    ) -> PricingTier:
        """Create a pricing tier"""
        tier_id = f"tier_{uuid.uuid4().hex[:8]}"
        
        tier = PricingTier(
            id=tier_id,
            name=name,
            price_usd=price_usd,
            billing_interval=billing_interval,
            features=features
        )
        
        self.pricing_tiers[tier_id] = tier
        logger.info(f"✅ Pricing tier created: {name} (${price_usd}/{billing_interval})")
        
        # Create in Stripe if available
        if self.stripe:
            try:
                product = self.stripe.Product.create(
                    name=name,
                    description="\n".join(features),
                    type="service"
                )
                tier.stripe_product_id = product.id
                
                price = self.stripe.Price.create(
                    product=product.id,
                    unit_amount=int(price_usd * 100),
                    currency="usd",
                    recurring={"interval": billing_interval}
                )
                tier.stripe_price_id = price.id
                logger.info(f"  📊 Synced to Stripe: {product.id}")
            except Exception as e:
                logger.error(f"  ❌ Stripe sync failed: {e}")
        
        return tier

    def list_pricing_tiers(self) -> List[PricingTier]:
        """List all pricing tiers"""
        return list(self.pricing_tiers.values())

    # ============================================================================
    # License Management
    # ============================================================================

    def generate_license(
        self,
        customer_id: str,
        tier_id: str,
        license_type: LicenseType = LicenseType.SUBSCRIPTION,
        duration_days: Optional[int] = None
    ) -> License:
        """Generate a new license for customer"""
        license_id = f"lic_{uuid.uuid4().hex[:12]}"
        license_key = self._generate_license_key()
        
        expires_at = None
        if license_type in [LicenseType.SUBSCRIPTION, LicenseType.TRIAL] and duration_days:
            expires_at = (datetime.now() + timedelta(days=duration_days)).isoformat()
        
        license = License(
            id=license_id,
            customer_id=customer_id,
            license_key=license_key,
            type=license_type,
            tier=tier_id,
            issued_at=datetime.now().isoformat(),
            expires_at=expires_at
        )
        
        self.licenses[license_id] = license
        logger.info(f"✅ License generated: {license_key[:8]}... ({license_type.value})")
        
        return license

    def validate_license(self, license_key: str) -> Dict[str, Any]:
        """Validate license key"""
        # Find license by key
        license = None
        for lic in self.licenses.values():
            if lic.license_key == license_key:
                license = lic
                break
        
        if not license:
            return {"valid": False, "error": "License not found"}
        
        if not license.is_valid:
            return {"valid": False, "error": "License revoked"}
        
        # Check expiration
        if license.expires_at:
            if datetime.fromisoformat(license.expires_at) < datetime.now():
                return {"valid": False, "error": "License expired"}
        
        # Check activations
        if license.active_activations >= license.max_activations:
            return {"valid": False, "error": "Max activations reached"}
        
        logger.info(f"✅ License valid: {license_key[:8]}...")
        return {
            "valid": True,
            "license_id": license.id,
            "tier": license.tier,
            "customer_id": license.customer_id,
            "expires_at": license.expires_at
        }

    def activate_license(self, license_key: str, device_id: str) -> bool:
        """Activate license on a device"""
        for license in self.licenses.values():
            if license.license_key == license_key:
                if license.active_activations < license.max_activations:
                    license.active_activations += 1
                    logger.info(f"✅ License activated on {device_id}")
                    return True
        
        logger.error(f"❌ Could not activate license")
        return False

    def revoke_license(self, license_key: str) -> bool:
        """Revoke a license"""
        for license in self.licenses.values():
            if license.license_key == license_key:
                license.is_valid = False
                logger.info(f"🚫 License revoked: {license_key[:8]}...")
                return True
        return False

    # ============================================================================
    # Usage Tracking & Metering
    # ============================================================================

    def track_usage(
        self,
        customer_id: str,
        event_type: str,
        quantity: int = 1,
        metadata: Optional[Dict[str, Any]] = None
    ) -> UsageEvent:
        """Track customer usage for metered billing"""
        event = UsageEvent(
            id=str(uuid.uuid4()),
            customer_id=customer_id,
            license_id="",  # Would be linked in real scenario
            event_type=event_type,
            quantity=quantity,
            timestamp=datetime.now().isoformat(),
            metadata=metadata
        )
        
        self.usage_events.append(event)
        logger.info(f"📊 Usage tracked: {customer_id} - {event_type} (+{quantity})")
        
        return event

    def get_usage_summary(self, customer_id: str, days: int = 30) -> Dict[str, Any]:
        """Get usage summary for customer"""
        cutoff = datetime.now() - timedelta(days=days)
        
        events = [
            e for e in self.usage_events
            if e.customer_id == customer_id and datetime.fromisoformat(e.timestamp) > cutoff
        ]
        
        by_type = {}
        for event in events:
            by_type[event.event_type] = by_type.get(event.event_type, 0) + event.quantity
        
        return {
            "customer_id": customer_id,
            "period_days": days,
            "events_count": len(events),
            "by_type": by_type,
            "total_quantity": sum(e.quantity for e in events)
        }

    # ============================================================================
    # Billing & Invoicing
    # ============================================================================

    def create_invoice(
        self,
        customer_id: str,
        tier_id: str,
        amount_usd: float
    ) -> Invoice:
        """Create and send invoice to customer"""
        invoice_id = f"inv_{uuid.uuid4().hex[:8]}"
        
        invoice = Invoice(
            id=invoice_id,
            customer_id=customer_id,
            stripe_invoice_id="",
            amount_usd=amount_usd,
            currency="usd",
            status="draft",
            issued_at=datetime.now().isoformat(),
            due_at=(datetime.now() + timedelta(days=14)).isoformat(),
            items=[{"tier_id": tier_id, "amount": amount_usd}]
        )
        
        self.invoices[invoice_id] = invoice
        logger.info(f"✅ Invoice created: {invoice_id} (${amount_usd} for {customer_id})")
        
        # Create in Stripe if available
        if self.stripe:
            try:
                tier = self.pricing_tiers.get(tier_id)
                if tier and tier.stripe_product_id:
                    stripe_invoice = self.stripe.Invoice.create(
                        customer=customer_id,
                        auto_advance=False
                    )
                    invoice.stripe_invoice_id = stripe_invoice.id
                    logger.info(f"  📊 Synced to Stripe: {stripe_invoice.id}")
            except Exception as e:
                logger.error(f"  ❌ Stripe sync failed: {e}")
        
        return invoice

    def mark_invoice_paid(self, invoice_id: str) -> bool:
        """Mark invoice as paid"""
        if invoice_id in self.invoices:
            invoice = self.invoices[invoice_id]
            invoice.status = "paid"
            invoice.paid_at = datetime.now().isoformat()
            logger.info(f"✅ Invoice marked paid: {invoice_id}")
            return True
        return False

    def get_revenue_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get revenue summary"""
        cutoff = datetime.now() - timedelta(days=days)
        
        paid_invoices = [
            inv for inv in self.invoices.values()
            if inv.status == "paid" and datetime.fromisoformat(inv.paid_at or inv.issued_at) > cutoff
        ]
        
        total_revenue = sum(inv.amount_usd for inv in paid_invoices)
        
        return {
            "period_days": days,
            "total_revenue_usd": total_revenue,
            "invoice_count": len(paid_invoices),
            "avg_invoice_usd": total_revenue / len(paid_invoices) if paid_invoices else 0,
            "customer_count": len(set(inv.customer_id for inv in paid_invoices))
        }

    # ============================================================================
    # Checkout & Subscription Management
    # ============================================================================

    def create_checkout_session(
        self,
        customer_id: str,
        tier_id: str,
        success_url: str,
        cancel_url: str
    ) -> Optional[str]:
        """Create Stripe checkout session"""
        if not self.stripe:
            logger.error("❌ Stripe not configured")
            return None
        
        try:
            tier = self.pricing_tiers.get(tier_id)
            if not tier or not tier.stripe_price_id:
                logger.error(f"❌ Tier not found or not in Stripe: {tier_id}")
                return None
            
            session = self.stripe.checkout.Session.create(
                customer=customer_id,
                line_items=[{
                    "price": tier.stripe_price_id,
                    "quantity": 1
                }],
                mode="subscription" if tier.billing_interval != "one_time" else "payment",
                success_url=success_url,
                cancel_url=cancel_url
            )
            
            logger.info(f"✅ Checkout session created: {session.id}")
            return session.id
        except Exception as e:
            logger.error(f"❌ Checkout creation failed: {e}")
            return None

    # ============================================================================
    # Utilities
    # ============================================================================

    def _generate_license_key(self) -> str:
        """Generate a unique license key"""
        import random
        import string
        
        chars = string.ascii_uppercase + string.digits
        segments = [
            ''.join(random.choices(chars, k=4))
            for _ in range(5)
        ]
        return '-'.join(segments)

    def export_monetization_config(self, output_path: Path) -> bool:
        """Export pricing and licensing config as JSON"""
        try:
            config = {
                "pricing_tiers": [asdict(t) for t in self.pricing_tiers.values()],
                "exported_at": datetime.now().isoformat()
            }
            
            with open(output_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            logger.info(f"✅ Monetization config exported: {output_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Export failed: {e}")
            return False


# Singleton
_monetization_engine: Optional[MonetizationEngine] = None


def get_monetization_engine(stripe_api_key: Optional[str] = None) -> MonetizationEngine:
    """Get or create singleton monetization engine"""
    global _monetization_engine
    if _monetization_engine is None:
        _monetization_engine = MonetizationEngine(stripe_api_key)
    return _monetization_engine
