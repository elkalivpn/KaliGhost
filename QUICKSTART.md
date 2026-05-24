# 🐉 KaliGhost 3.0 - Quick Start Guide

## ⚡ 5-Minute Setup

### 1. Clone & Install

```bash
git clone https://github.com/yourusername/KaliGhost.git
cd KaliGhost

# Make startup script executable
chmod +x start.sh

# Run setup
./start.sh
```

The script will:
- ✅ Check Python 3 & Docker
- ✅ Install dependencies
- ✅ Create directories
- ✅ Build Docker images
- ✅ Start services
- ✅ Verify all systems

### 2. Access Interfaces

**🌐 WebChat Interface (3D Dragon)**
```
http://localhost:8001
```
Type natural language tasks, watch the dragon animate!

**⚙️ API Gateway**
```
http://localhost:8000/docs
```
Interactive Swagger documentation for all endpoints

**📊 Monitoring**
- Grafana: http://localhost:3001 (admin/admin123)
- Prometheus: http://localhost:9090

### 3. Your First Task

#### Option A: WebChat
1. Open http://localhost:8001
2. Type: "Create a Node.js REST API with authentication"
3. Watch the dragon execute!

#### Option B: CLI
```bash
kalighost orchestrate execute "Create a Go microservice"
```

#### Option C: Python
```python
from backend.orchestrator import get_orchestrator, AgentMode
import asyncio

async def main():
    orchestrator = get_orchestrator()
    plan = await orchestrator.decompose_task(
        "Build a Python data pipeline",
        thread_id="demo",
        mode=AgentMode.ULTRA
    )
    result = await orchestrator.execute_plan(plan)
    print(f"✅ Completed: {result['status']}")

asyncio.run(main())
```

---

## 📚 10-Module Cheat Sheet

### 1️⃣ ORCHESTRATOR - Multi-Agent Execution
```bash
kalighost orchestrate execute "Your task here" --mode ultra
```
**Modes**: flash (fast), standard, pro (planning), ultra (multi-agent)

### 2️⃣ MEMORY - Persistent Context
```bash
# Add memory
kalighost memory add preference "I prefer TypeScript and Go"

# Search
kalighost memory search "backend preferences"

# View profile
kalighost memory profile
```

### 3️⃣ ELITE SKILLS - Pre-built Workflows
```bash
# List skills
kalighost skills list

# Find skill for task
# (Automatic in orchestrator)
```

### 4️⃣ SECURITY HARDENER - Code Audit
```bash
kalighost security audit ./src --language python
```
Returns: vulnerabilities, patches, security score

### 5️⃣ MONETIZATION - Stripe + Licensing
```bash
# Create pricing tier
kalighost monetize tier "Professional" 29 \
  --features "5K API calls" "Priority support"

# Generate license
kalighost monetize license cust_001 tier_pro_123

# Revenue analytics
kalighost monetize revenue --days 30
```

### 6️⃣ THREAT INTELLIGENCE - OSINT
```bash
kalighost threats recon example.com
```
Returns: subdomains, emails, cloud services, vulnerabilities

### 7️⃣ INFRASTRUCTURE - Cloud & Auto-scaling
```bash
# Provision instances
kalighost infra provision myapp --provider digitalocean --count 3

# Check costs
kalighost infra cost
```

### 8️⃣ GUI GENERATOR - CLI → Web UI
```python
from backend.gui_generator import get_gui_automation_engine
gui = get_gui_automation_engine()
await gui.cli_to_web_ui(Path("my_tool.py"), Path("./ui/"))
```

### 9️⃣ COMPLIANCE - Legal + Ethics
```bash
kalighost compliance audit-compliance "MyStartup Inc" \
  --jurisdiction us \
  --standards gdpr ccpa
```

### 🔟 IM CHANNELS - Telegram/Slack
Configure in `.env`:
```env
TELEGRAM_BOT_TOKEN=your_token_here
SLACK_BOT_TOKEN=xoxb-your-token
```

Then send Slack/Telegram messages directly to KaliGhost!

---

## 🔧 Configuration

### .env File
```env
# API Keys
OPENAI_API_KEY=sk-...
STRIPE_API_KEY=sk_live_...
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...

# IM Channels
TELEGRAM_BOT_TOKEN=...
SLACK_BOT_TOKEN=...

# Database
DB_USER=kalighost
DB_PASSWORD=changeme
REDIS_PASSWORD=changeme

# Environment
ENVIRONMENT=production
LOG_LEVEL=INFO
```

### Config Files
- `config/config.yaml` - Main configuration
- `docker/nginx.conf` - Reverse proxy
- `docker/prometheus.yml` - Monitoring
- `docker/grafana/provisioning/` - Dashboards

---

## 📖 Example Workflows

### Example 1: Build & Deploy SaaS (2-3 hours)

```bash
# Step 1: Generate full-stack SaaS
kalighost orchestrate execute \
  "Create React + Go + Stripe SaaS for API monitoring" \
  --mode ultra

# Step 2: Security audit
kalighost security audit . --language go

# Step 3: Setup monetization
kalighost monetize tier "Starter" 0 --features "10 API calls"
kalighost monetize tier "Pro" 29 --features "10K API calls"

# Step 4: Provision infrastructure
kalighost infra provision myapi --provider aws --count 3

# Step 5: Compliance check
kalighost compliance audit-compliance "MyCompany" --standards gdpr ccpa

# Result: Live, secure, monetized SaaS! 🚀
```

### Example 2: Security Audit & Remediation (30 min)

```bash
# Audit code
kalighost security audit ./backend --language python

# Auto-fixes generated for vulnerabilities
# Check logs for detailed findings
# Patches committed to git

# Fuzzing API endpoints
# (Simulates 5000 attack attempts)

# Final security score: 92/100 ✅
```

### Example 3: OSINT Investigation (20 min)

```bash
# Reconnaissance
kalighost threats recon competitor.com

# Results include:
# - 12 subdomains discovered
# - 3 exposed S3 buckets
# - 5 vulnerable dependencies
# - Email list
# - Dark web monitoring started

# Dark web alerts: Real-time notifications if code leaks
```

---

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f gateway

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Rebuild specific service
docker-compose up -d --build gateway

# Execute command in container
docker-compose exec gateway python -m backend.orchestrator
```

---

## 📊 Monitoring Dashboard

After setup, access:
- **Grafana**: http://localhost:3001
  - Login: admin / admin123
  - Pre-built dashboards for KaliGhost metrics
  - CPU, memory, request rates, execution times

- **Prometheus**: http://localhost:9090
  - Raw metrics data
  - Time-series queries

---

## 🆘 Troubleshooting

### Gateway Won't Start
```bash
# Check logs
docker-compose logs gateway

# Common issue: Port 8000 already in use
# Solution: Change in docker-compose.yml or kill process
lsof -i :8000
kill -9 <PID>
```

### Memory Issues
```bash
# Increase memory limit in docker-compose.yml
# gateway:
#   ... 
#   mem_limit: 2g  # Increase this
```

### Database Connection Error
```bash
# Reset database
docker-compose exec postgres psql -U kalighost -d kalighost -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# Restart postgres
docker-compose restart postgres
```

### WebSocket Connection Failed
```bash
# Check if webchat service is running
docker-compose ps webchat

# Start it
docker-compose up -d webchat
```

---

## 📈 Performance Tuning

### Production Setup

```bash
# Increase workers
WORKERS=8 docker-compose up -d gateway

# Enable caching
REDIS_CACHE=1 docker-compose up -d

# Monitor resources
docker stats

# Scale infrastructure
kalighost infra provision myapp --count 5
```

---

## 🎓 Learning Resources

### Documentation
- `/ARCHITECTURE_3_0.md` - Complete architecture
- `/COMPLETE_SUITE_3_0.md` - Full workflow guide
- `/examples/complete_examples.py` - Code examples

### Videos (Create These!)
- 🎥 5-min setup
- 🎥 Building your first SaaS
- 🎥 Security audit walkthrough

### Community
- GitHub Issues: Report bugs
- Discussions: Ask questions
- Contributing: Help develop!

---

## 🚀 Next Steps

1. **Deploy**: `./start.sh`
2. **Test**: `python examples/complete_examples.py`
3. **Build**: Create your first SaaS
4. **Monitor**: Check Grafana dashboards
5. **Scale**: Add more instances
6. **Monetize**: Launch with Stripe
7. **Share**: Tell the world!

---

## 💡 Pro Tips

✅ Use `--mode ultra` for complex multi-agent tasks  
✅ Save frequently used tasks in memory  
✅ Monitor costs with `kalighost infra cost`  
✅ Check security score before launch  
✅ Use dark web monitoring for competitive research  
✅ Integrate with Slack for team collaboration  
✅ Set up CI/CD for auto-deployment  

---

**You're ready! 🐉 Let's build something amazing.**

Questions? Check the docs or open a GitHub issue!
