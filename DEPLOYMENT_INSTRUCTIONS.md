# 🐉 KaliGhost 3.0 Complete Deployment Instructions

## 📋 Requirements
- macOS/Linux computer with Docker installed
- At least 8GB RAM recommended
- 20GB free disk space
- Terminal access

## 🔧 Step-by-Step Deployment

### 1. Prepare Environment
```bash
# Navigate to project directory
cd /Users/mrhardcore/KaliGhost

# Make deployment scripts executable
chmod +x start.sh
```

### 2. Set Up Environment Variables
```bash
# Create .env file with required credentials
cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
STRIPE_API_KEY=your_stripe_api_key_here
DB_USER=kalighost
DB_PASSWORD=changeme
REDIS_PASSWORD=changeme
GRAFANA_USER=admin
GRAFANA_PASSWORD=admin123
AWS_ACCESS_KEY_ID=your_aws_access_key_id_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key_here
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=kalighost-project
EOF
```

### 3. Fix Configuration Issues (if any)
In the current repository there's a small issue:

```bash
# Remove the deprecated version field from docker-compose.yml 
sed -i '' '/version: '\''3.9'\''/d' docker-compose.yml
```

### 4. Deploy Services (Manual Approach)
```bash
# Launch all services with Docker Compose
docker-compose up -d
```

### 5. Verify Deployment
Wait 30 seconds for services to initialize, then verify:

```bash
# Check running services
docker-compose ps

# Verify gateway health
curl -X GET http://localhost:8000/health

# Verify API documentation is accessible
# Open http://localhost:8000/docs in browser
```

### 6. Access KaliGhost
Once deployed, access the following URLs:

| Service | URL |
|---------|-----|
| API Gateway | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| WebChat UI | http://localhost:8001 |
| Grafana Dashboard | http://localhost:3001 |
| Prometheus | http://localhost:9090 |

## 🚀 Quick Start Commands

Start everything:
```bash
docker-compose up -d
```

Check status:
```bash
docker-compose ps
```

View logs:
```bash
docker-compose logs -f gateway
```

Stop all services:
```bash
docker-compose down
```

## 🛠️ Services Included

1. **Gateway** (FastAPI) - Port 8000
2. **WebChat** - Port 8001
3. **PostgreSQL** - Port 5432
4. **Redis** - Port 6379
5. **Prometheus** - Port 9090 
6. **Grafana** - Port 3001
7. **Nginx** - Port 80/443
8. **Sandbox** - Docker-in-Docker
9. **Provisioner** - Kubernetes Manager

## ⚠️ Troubleshooting

**Issue: Docker credential error**
Solution: Restart Docker Desktop or run:
```bash
sudo ln -sf /Applications/Docker.app/Contents/Resources/etc/docker-compose.yml /usr/local/bin/docker-compose
```

**Issue: Ports already in use**
Solution: Kill existing processes or modify docker-compose.yml ports.

**Issue: Python dependencies**
Ensure all requirements from requirements.txt are installed.

## 📈 Monitoring

After deployment:
1. Visit http://localhost:3001 (Grafana)
2. Login with admin/admin123
3. Set up dashboards for monitoring

## 🧪 Testing

Run end-to-end tests:
```bash
python test_e2e.py
```

## 📄 Documentation

Full documentation is available in:
- README.md
- ARCHITECTURE_3_0.md
- QUICKSTART.md
- CUSTOMIZATION_GUIDE.md

## 🎯 Deployment Success

Upon successful deployment, KaliGhost 3.0 will:
- Run 9 interconnected containers
- Provide enterprise-ready API gateway
- Offer real-time monitoring through Grafana
- Deliver 3D dragon UI via WebChat
- Enable autonomous application development
- Support multi-agent orchestration
- Include comprehensive security features