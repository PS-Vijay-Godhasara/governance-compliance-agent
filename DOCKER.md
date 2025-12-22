# Docker Deployment Guide

## 🐳 Quick Start with Docker

### Option 1: Docker Compose (Recommended)

1. **Basic Deployment (without LLM):**
```bash
docker-compose up -d
```

2. **With LLM Support:**
```bash
docker-compose --profile llm up -d
```

3. **Access the application:**
```
http://localhost:5000
```

### Option 2: Docker Build & Run

1. **Build the image:**
```bash
docker build -f simple/Dockerfile -t governance-agent .
```

2. **Run the container:**
```bash
docker run -d \
  --name governance-agent \
  -p 5000:5000 \
  -e USE_LLM=false \
  -e AUTO_VALIDATION=true \
  -e RISK_ASSESSMENT=true \
  -v $(pwd)/simple/policies:/app/policies \
  governance-agent
```

## 🔧 Configuration

### Environment Variables
All configuration options can be set via environment variables:

```yaml
environment:
  # AI Features
  - USE_LLM=false
  - AUTO_VALIDATION=true
  - AUTO_POLICY_DETECTION=true
  
  # Compliance Features
  - RISK_ASSESSMENT=true
  - AML_SCREENING=true
  - KYC_VALIDATION=true
  - GDPR_ANALYSIS=true
  
  # Validation Thresholds
  - HIGH_RISK_AMOUNT=50000
  - AML_THRESHOLD=10000
  - RISK_SCORE_THRESHOLD=0.7
```

### Volume Mounts
- **Policies**: `./simple/policies:/app/policies`
- **Knowledge**: `./simple/knowledge:/app/knowledge`
- **Uploads**: `governance_uploads:/app/ui/uploads`

## 🚀 Production Deployment

### Docker Compose Production
```yaml
version: '3.8'
services:
  governance-agent:
    image: governance-agent:latest
    ports:
      - "80:5000"
    environment:
      - USE_LLM=true
      - DEBUG=false
      - AUDIT_LOGGING=true
      - COMPLIANCE_REPORTING=true
    volumes:
      - /opt/governance/policies:/app/policies
      - /opt/governance/knowledge:/app/knowledge
      - /opt/governance/uploads:/app/ui/uploads
    restart: always
    
  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - governance-agent
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: governance-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: governance-agent
  template:
    metadata:
      labels:
        app: governance-agent
    spec:
      containers:
      - name: governance-agent
        image: governance-agent:latest
        ports:
        - containerPort: 5000
        env:
        - name: USE_LLM
          value: "true"
        - name: AUTO_VALIDATION
          value: "true"
        - name: RISK_ASSESSMENT
          value: "true"
        volumeMounts:
        - name: policies
          mountPath: /app/policies
        - name: knowledge
          mountPath: /app/knowledge
      volumes:
      - name: policies
        configMap:
          name: governance-policies
      - name: knowledge
        configMap:
          name: governance-knowledge
---
apiVersion: v1
kind: Service
metadata:
  name: governance-agent-service
spec:
  selector:
    app: governance-agent
  ports:
  - port: 80
    targetPort: 5000
  type: LoadBalancer
```

## 🔍 Monitoring & Health Checks

### Health Check Endpoint
```bash
curl http://localhost:5000/api/status
```

### Docker Health Check
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/status || exit 1
```

### Monitoring with Prometheus
```yaml
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
```

## 🛡️ Security Considerations

### Production Security
```yaml
environment:
  # Disable debug mode
  - DEBUG=false
  
  # Enable audit logging
  - AUDIT_LOGGING=true
  - COMPLIANCE_REPORTING=true
  - VIOLATION_ALERTS=true
  
  # Secure file processing
  - MAX_FILE_SIZE=16777216
  - ALLOWED_FILE_TYPES=json,txt,csv
```

### Network Security
```yaml
networks:
  governance-net:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

### Secrets Management
```yaml
secrets:
  ollama_api_key:
    external: true
  database_password:
    external: true

services:
  governance-agent:
    secrets:
      - ollama_api_key
      - database_password
```

## 📊 Scaling & Performance

### Horizontal Scaling
```yaml
deploy:
  replicas: 3
  update_config:
    parallelism: 1
    delay: 10s
  restart_policy:
    condition: on-failure
```

### Resource Limits
```yaml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 1G
    reservations:
      cpus: '0.5'
      memory: 512M
```

## 🔧 Troubleshooting

### Common Issues

1. **Container won't start:**
```bash
docker logs governance-agent
```

2. **Configuration not loading:**
```bash
docker exec -it governance-agent env | grep -E "(USE_LLM|AUTO_VALIDATION)"
```

3. **File permissions:**
```bash
docker exec -it governance-agent ls -la /app/policies
```

4. **Health check failing:**
```bash
docker exec -it governance-agent curl -f http://localhost:5000/api/status
```

### Debug Mode
```bash
docker run -it --rm \
  -p 5000:5000 \
  -e DEBUG=true \
  -e USE_LLM=false \
  governance-agent
```

## 🚀 Deployment Commands

### Development
```bash
# Start with basic features
docker-compose up -d

# View logs
docker-compose logs -f governance-agent

# Stop services
docker-compose down
```

### Production
```bash
# Build and deploy
docker-compose -f docker-compose.prod.yml up -d

# Update configuration
docker-compose -f docker-compose.prod.yml up -d --force-recreate

# Backup data
docker run --rm -v governance_uploads:/data -v $(pwd):/backup alpine tar czf /backup/governance-backup.tar.gz /data
```

### With LLM Support
```bash
# Start Ollama service
docker-compose --profile llm up -d ollama

# Pull LLM model
docker exec -it governance-compliance-agent-ollama-1 ollama pull llama3.2:3b

# Start governance agent with LLM
docker-compose up -d governance-agent
```

The Docker deployment provides a complete, scalable solution for running the Governance & Compliance Agent in any environment.