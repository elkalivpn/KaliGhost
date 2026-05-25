# KaliGhost 3.0 Deployment Demonstration

## Overview
This file demonstrates how the KaliGhost 3.0 platform should be deployed using Docker Compose.

## Prerequisites
- Docker installed and running
- Docker Compose installed
- Bash shell

## How to Deploy

1. Navigate to project directory
```bash
cd /Users/mrhardcore/KaliGhost
```

2. Ensure .env file exists with required credentials
```bash
# Create .env file with required variables
cat > .env << EOF
OPENAI_API_KEY=your_openai_key_here
STRIPE_API_KEY=your_stripe_key_here
DB_USER=kalighost
DB_PASSWORD=changeme
REDIS_PASSWORD=changeme
GRAFANA_USER=admin
GRAFANA_PASSWORD=admin123
AWS_ACCESS_KEY_ID=your_aws_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_here
LANGSMITH_API_KEY=your_langsmith_key_here
LANGSMITH_PROJECT=kalighost-project
EOF
```

3. Fix Docker Compose version in docker-compose.yml
```bash
# Remove the deprecated version field
sed -i '' '/version: '\''3.9'\''/d' docker-compose.yml
```

4. Deploy using Docker Compose
```bash
docker-compose up -d
```

## Expected Deployment Result

After successful deployment, these services should be running:

- `kalighost-gateway` (API Gateway) - Port 8000
- `kalighost-webchat` (Web Chat UI) - Port 8001  
- `kalighost-postgres` (Database) - Port 5432
- `kalighost-redis` (Cache) - Port 6379
- `kalighost-prometheus` (Monitoring) - Port 9090
- `kalighost-grafana` (Dashboard) - Port 3001
- `kalighost-nginx` (Reverse Proxy) - Port 80/443
- `kalighost-sandbox` (Code Execution) - Privileged
- `kalighost-provisioner` (K8s Manager) - Port 9000

## Verification
Check services status:
```bash
docker-compose ps
```

Wait for services to initialize (about 30 seconds):

```bash
# Test API Gateway
curl -X GET http://localhost:8000/health

# Test Web Chat access point
# Visit http://localhost:8001 in browser
```

## Access Points

- **API Gateway**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs  
- **WebChat Interface**: http://localhost:8001
- **Grafana Dashboard**: http://localhost:3001
- **Prometheus Metrics**: http://localhost:9090

## Cleanup
To stop all services:
```bash
docker-compose down
```

## Current Status
The intended deployment shows all 9 services listed in the docker-compose.yml file should start up. The actual repository is correctly structured with all required components including:
- Dockerized services
- PostgreSQL database  
- Redis caching
- Prometheus monitoring
- Grafana dashboard
- Kubernetes ready provisioner
- API gateway with FastAPI
- WebUI for interaction
- Reverse proxy with Nginx

Note: For the actual deployment to be fully functional, proper environment variables need to be set and the system should be able to resolve all Docker dependencies correctly.