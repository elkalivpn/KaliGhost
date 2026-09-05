# Core Configuration
KALIGHOST_VERSION="4.0-ULTIMATE"
MODE="hybrid"  # ghost, legitimate, hybrid

# Security & Encryption
MASTER_KEY=""  # Generate with: openssl rand -hex 32
ENCRYPTION_ALGORITHM="AES-256-GCM"
HASH_ROUNDS=100000

# Database
DATABASE_URL="sqlite+aiosqlite:///data/kalighost.db"
REDIS_URL="redis://localhost:6379/0"
CVE_DB_PATH="data/cve_db/cve_database.sqlite"

# RAM Execution
RAM_DISK_SIZE="2G"
RAM_EXECUTION_ENABLED=true
AUTO_WIPE=true

# Network & Stealth
DEFAULT_ROUTING_MODE="isolated"
TOR_ENABLED=false
PROXY_CHAIN_ENABLED=false
VPN_CONFIG_PATH=""

# Steganography
STEGANOGRAPHY_ALGORITHM="lsb_advanced"
CLEAN_METADATA_AUTO=true

# Emergency Response
DEAD_MAN_SWITCH_ENABLED=true
DEAD_MAN_TIMEOUT_MINUTES=30
SHAMIR_N_PARTS=5
SHAMIR_K_THRESHOLD=3
EMERGENCY_WIPE_METHOD="secure_delete_7pass"

# AI & Agents
AI_MODEL_ENDPOINT="http://localhost:11434"  # Ollama local
AI_MODEL_NAME="mistral-large"
RAG_ENABLED=true
AUTONOMOUS_MODE_MAX_AGENTS=8

# Sandbox
SANDBOX_TYPE="docker_kubernetes_hybrid"
SANDBOX_TIMEOUT_SECONDS=300
FORENSICS_CAPTURE=true

# Purple Team
PURPLE_TEAM_REPORT_PATH="data/reports/purple_team"
RED_TEAM_OPS_LOG="data/logs/redteam_ops.log"
GREY_TEAM_COLLAB_ENABLED=true

# API & Web
API_HOST="0.0.0.0"
API_PORT=8000
WEBCHAT_PORT=8001
DEBUG_MODE=false
SECRET_KEY=""  # Generate with: openssl rand -hex 32

# Monitoring
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000

# GitHub Integration (for auto-push after ops)
GITHUB_TOKEN=""
GITHUB_REPO_URL=""
