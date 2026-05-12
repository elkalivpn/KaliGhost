#!/bin/bash

# KaliGhost Pre-Release Validation Script
# Ejecuta antes de ./release.sh para verificar que todo está listo

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PASS=0
FAIL=0
WARN=0

check() {
    echo -n "Checking $1... "
    if eval "$2" &>/dev/null; then
        echo -e "${GREEN}✓${NC}"
        ((PASS++))
        return 0
    else
        echo -e "${RED}✗${NC}"
        ((FAIL++))
        return 1
    fi
}

check_warn() {
    echo -n "Checking $1... "
    if eval "$2" &>/dev/null; then
        echo -e "${GREEN}✓${NC}"
        ((PASS++))
        return 0
    else
        echo -e "${YELLOW}⚠${NC}"
        ((WARN++))
        return 1
    fi
}

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║   KaliGhost Pre-Release Validator v1.0  ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# ─── Project structure ─────────────────────────
echo "📁 Project Structure"
echo "─────────────────────"
check "Root directory (README.md)" "test -f README.md"
check "web_monetizacion/index.html" "test -f web_monetizacion/index.html"
check "CSS styles" "test -f web_monetizacion/css/style.css"
check "JS main.js" "test -f web_monetizacion/js/main.js"
check "boot/boot.sh" "test -f boot/boot.sh && test -x boot/boot.sh"
check "YrYs-Agent config" "test -f YrYs-Agent/yrays_config.yaml"
check "AUTO_MODE.md" "test -f YrYs-Agent/AUTO_MODE.md"
check "CORE_PRINCIPLES.md" "test -f YrYs-Agent/CORE_PRINCIPLES.md"
check "release_manifest.json" "test -f release_manifest.json"
check ".github/workflows/release.yml" "test -f .github/workflows/release.yml"

echo ""

# ─── Documentation ─────────────────────────────
echo "📚 Documentation"
echo "─────────────────"
check "README.md" "test -s README.md"
check_warn "CHANGELOG.md" "test -f CHANGELOG.md"
check_warn "docs/INSTALLATION.md" "test -f docs/INSTALLATION.md"
check_warn "docs/TROUBLESHOOTING.md" "test -f docs/TROUBLESHOOTING.md"
check_warn "docs/AGENT.md" "test -f docs/AGENT.md"
check "LICENSE" "test -f LICENSE"
check "CONTRIBUTING.md" "test -f CONTRIBUTING.md"
check "SECURITY.md" "test -f SECURITY.md"
check "CODE_OF_CONDUCT.md" "test -f CODE_OF_CONDUCT.md"

echo ""

# ─── Examples ───────────────────────────────────
echo "📂 Examples"
echo "────────────"
check "examples/auto-tasks/" "test -d examples/auto-tasks"
check "examples/aws/" "test -d examples/aws"
check "examples/scripts/" "test -d examples/scripts"
check "Example: network_scan.yaml" "test -f examples/auto-tasks/network_scan.yaml"
check "Example: deploy_ec2_instance.py" "test -f examples/aws/deploy_ec2_instance.py"
check "Example: scripts utilities" "test -f examples/scripts/vuln_scorer.py"

echo ""

# ─── HTML validation ───────────────────────────
echo "🌐 HTML Validation"
echo "───────────────────"
if command -v tidy &>/dev/null; then
    check_warn "HTML tidy" "tidy -q -e web_monetizacion/index.html"
else
    echo "  tidy not installed – skip HTML validation (install: brew install tidy-html5)"
    ((WARN++))
fi

# Basic checks
check_warn "DOCTYPE present" "grep -q '<!DOCTYPE html>' web_monetizacion/index.html"
check_warn "UTF-8 charset" "grep -q 'charset=\"UTF-8\"' web_monetizacion/index.html"
check_warn "Starter plan exists" "grep -q 'Starter' web_monetizacion/index.html"
check_warn "Pro plan exists" "grep -q 'Pro' web_monetizacion/index.html"
check_warn "Enterprise plan exists" "grep -q 'Enterprise' web_monetizacion/index.html"
check_warn "Gumroad links present" "grep -q 'gumroad.com' web_monetizacion/index.html"

echo ""

# ─── Git status ─────────────────────────────────
echo "📦 Git Status"
echo "──────────────"
if command -v git &>/dev/null; then
    check "Git repo initialized" "test -d .git"
    check_warn "No uncommitted changes" "test -z \"\$(git status --porcelain)\""
    
    # Check if on main branch
    CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "")
    if [ "$CURRENT_BRANCH" = "main" ]; then
        echo -e "  Current branch: ${GREEN}main${NC}"
    else
        echo -e "  Current branch: ${YELLOW}$CURRENT_BRANCH${NC} (recommended: main)"
        ((WARN++))
    fi
    
    # Check remote
    if git remote get-url origin &>/dev/null; then
        echo -e "  Remote: ${GREEN}origin${NC} ✓"
    else
        echo -e "  Remote: ${RED}not set${NC}"
        ((FAIL++))
    fi
else
    echo "  ${RED}Git not installed${NC}"
    ((FAIL++))
fi

echo ""

# ─── Docker availability ────────────────────────
echo "🐳 Docker"
echo "──────────"
check_warn "Docker installed" "command -v docker"
if command -v docker &>/dev/null; then
    check_warn "Docker daemon running" "docker ps >/dev/null 2>&1"
fi

echo ""

# ─── Python environment ─────────────────────────
echo "🐍 Python"
echo "──────────"
check "Python 3.11+" "python3 --version | grep -E 'Python 3\.(1[1-9]|[2-9][0-9])'"
check_warn "pip available" "python3 -m pip --version"
check_warn "venv module" "python3 -c 'import venv'"

echo ""

# ─── AWS credentials (optional) ─────────────────
echo "☁️  AWS (Optional)"
echo "─────────────────"
if [ -f ~/.aws/credentials ] || env | grep -q AWS_ACCESS_KEY_ID; then
    echo -e "  ${GREEN}AWS credentials found${NC} ✓"
    check_warn "AWS CLI" "command -v aws"
else
    echo "  ${YELLOW}AWS credentials not configured${NC} (optional for AWS features)"
fi

echo ""

# ─── File counts ────────────────────────────────
echo "📊 File Statistics"
echo "────────────────────"
echo "  HTML files:      $(find . -name '*.html' | wc -l) | expected: ≥1"
echo "  CSS files:       $(find . -name '*.css' | wc -l) | expected: ≥1"
echo "  JS files:        $(find . -name '*.js' | wc -l) | expected: ≥1"
echo "  Markdown docs:   $(find . -name '*.md' | wc -l) | expected: ≥8"
echo "  Python scripts:  $(find . -name '*.py' | wc -l) | expected: ≥5"
echo "  Shell scripts:   $(find . -name '*.sh' | wc -l) | expected: ≥1"

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  Results: $PASS passed, $FAIL failed, $WARN warnings"
echo "╚══════════════════════════════════════════╝"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✅ Pre-release check PASSED${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Commit all changes: git add . && git commit -m 'feat: prepare v1.0.0 release'"
    echo "  2. Tag release: git tag -a v1.0.0 -m 'KaliGhost v1.0.0'"
    echo "  3. Push: git push origin main --tags"
    echo "  4. Or run: ./release.sh patch"
    echo ""
    exit 0
else
    echo -e "${RED}❌ Pre-release check FAILED${NC}"
    echo "Fix failed checks before release."
    echo ""
    exit 1
fi