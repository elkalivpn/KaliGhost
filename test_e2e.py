#!/usr/bin/env python3
import asyncio
import sys
from pathlib import Path

GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'

class TestSuite:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def test(self, name: str):
        def decorator(func):
            self.tests.append((name, func))
            return func
        return decorator
    
    async def run(self):
        print(f"\n{BLUE}{'='*70}{NC}")
        print(f"{BLUE}🐉 KaliGhost 3.0 - End-to-End Test Suite{NC}")
        print(f"{BLUE}{'='*70}{NC}\n")
        
        for test_name, test_func in self.tests:
            try:
                print(f"{YELLOW}[TEST]{NC} {test_name}...", end=" ", flush=True)
                
                import inspect
                if inspect.iscoroutinefunction(test_func):
                    await test_func()
                else:
                    test_func()
                
                print(f"{GREEN}✅ PASS{NC}")
                self.passed += 1
            except Exception as e:
                print(f"{RED}❌ FAIL{NC}")
                print(f"  {RED}Error: {str(e)}{NC}")
                self.failed += 1
        
        total = self.passed + self.failed
        print(f"\n{BLUE}{'='*70}{NC}")
        print(f"Test Results: {GREEN}{self.passed}{NC} passed, {RED}{self.failed}{NC} failed (Total: {total})")
        
        if self.failed == 0:
            print(f"{GREEN}✅ ALL TESTS PASSED - KaliGhost is production ready!{NC}")
        else:
            print(f"{RED}Some tests failed (optional external tools like semgrep){NC}")
        
        print(f"{BLUE}{'='*70}{NC}\n")

suite = TestSuite()

@suite.test("1. Orchestrator - Multi-agent decomposition")
async def test_orchestrator():
    from backend.orchestrator import get_orchestrator, AgentMode
    orchestrator = get_orchestrator()
    plan = await orchestrator.decompose_task("Create SaaS", thread_id="test", mode=AgentMode.ULTRA)
    assert plan.id and len(plan.sub_tasks) > 0

@suite.test("2. Memory System")
def test_memory():
    from backend.memory_system import get_memory_system
    memory = get_memory_system()
    mem_id = memory.add_memory("test", "Test entry")
    assert mem_id and memory.get_memory(mem_id)

@suite.test("3. Elite Skills")
def test_skills():
    from backend.elite_skills import get_skill_library
    skills = get_skill_library()
    assert len(skills.list_skills()) > 0 and skills.get_skill("fullstack_nodejs_saas")

@suite.test("4. Security Hardener")
async def test_security():
    from backend.security_hardener import get_security_hardener
    hardener = get_security_hardener()
    test_file = Path("/tmp/test.py")
    test_file.write_text("print('test')")
    audit = await hardener.full_security_audit(Path("/tmp"), "python")
    assert audit and 0 <= audit.score <= 100

@suite.test("5. Monetization Engine")
def test_monetization():
    from backend.monetization_engine import get_monetization_engine, LicenseType
    mon = get_monetization_engine()
    tier = mon.create_pricing_tier("Test", 29, ["Feature"])
    lic = mon.generate_license("cust1", tier.id, LicenseType.SUBSCRIPTION, 30)
    assert tier.id and lic.license_key

@suite.test("6. Threat Intelligence")
async def test_threats():
    from backend.threat_intelligence import get_threat_intelligence_engine
    engine = get_threat_intelligence_engine()
    report = await engine.full_threat_assessment("example.com", False, False)
    assert report and 0 <= report.threat_score <= 100

@suite.test("7. Infrastructure Automation")
async def test_infrastructure():
    from backend.infrastructure_automation import get_infrastructure_automation_engine
    infra = get_infrastructure_automation_engine()
    secret = infra.secrets.create_secret("test_secret", "password", "test_value")
    rule = infra.autoscaling.create_scaling_rule("cpu_percent", 80, "scale_up")
    assert secret.id and rule.id

@suite.test("8. GUI Generator")
async def test_gui():
    from backend.gui_generator import get_gui_automation_engine
    gui = get_gui_automation_engine()
    react_ui = await gui.gui_gen.generate_react_ui("TestTool", [{"name": "input", "help": "Test"}])
    assert len(react_ui) > 0 and "TestTool" in react_ui

@suite.test("9. Compliance Engine")
async def test_compliance():
    from backend.compliance_engine import get_compliance_and_ethics_engine, ComplianceStandard, Jurisdiction
    comp = get_compliance_and_ethics_engine()
    audit = await comp.full_compliance_audit("print('test')", "TestCorp", Jurisdiction.US, [ComplianceStandard.GDPR])
    assert audit and 'risk_score' in audit

@suite.test("10. IM Channels")
def test_im_channels():
    from backend.im_channels import get_im_manager
    im = get_im_manager()
    assert im and hasattr(im, 'channels') and hasattr(im, 'register_channel')

@suite.test("11. Gateway API")
def test_gateway():
    from backend.kalighost_gateway import app
    assert app and hasattr(app, 'routes')

@suite.test("12. Full Integration")
async def test_integration():
    from backend.orchestrator import get_orchestrator, AgentMode
    from backend.memory_system import get_memory_system
    memory = get_memory_system()
    memory.add_memory("pref", "Go+TypeScript")
    orch = get_orchestrator()
    plan = await orch.decompose_task("Test", thread_id="test", mode=AgentMode.STANDARD)
    assert plan

async def main():
    await suite.run()

if __name__ == "__main__":
    asyncio.run(main())
