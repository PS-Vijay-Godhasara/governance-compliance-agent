# 🚀 Quick Start Guide

## Prerequisites
- Python 3.11+
- Docker & Docker Compose
- 8GB+ RAM (for local LLM)

## 1. Setup Environment

```bash
# Clone and navigate
cd governance-compliance-agent

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
```

## 2. Start Ollama + Models

### Option A: Docker (Recommended)
```bash
# Start full stack with Ollama
docker-compose -f docker-compose.ollama.yml up -d

# Pull free models
docker exec governance-compliance-agent-ollama-1 ollama pull mistral:7b
docker exec governance-compliance-agent-ollama-1 ollama pull llama3.2:3b
```

### Option B: Local Ollama
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
ollama serve

# Pull models (choose one)
ollama pull mistral:7b        # 4.1GB - Best balance
ollama pull llama3.2:3b       # 2.0GB - Fastest
ollama pull llama3.2:1b       # 1.3GB - Smallest
ollama pull codellama:7b      # 3.8GB - Code-focused
```

## 3. Run Application

```bash
# Start the governance agent
python -m src.main

# Or with uvicorn directly
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

## 4. Test Basic Functionality

```bash
# Run examples
python examples/basic_usage.py

# Run tests
pytest tests/ -v

# Health check
curl http://localhost:8000/health
```

## 5. API Usage

### Register Policy
```bash
curl -X POST "http://localhost:8000/policies" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "customer_validation",
    "content": "Customer must have valid email and age 18-65"
  }'
```

### Validate Data
```bash
curl -X POST "http://localhost:8000/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "policy_id": "customer_validation",
    "data": {"email": "test@example.com", "age": 25}
  }'
```

## Model Comparison

| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| mistral:7b | 4.1GB | Medium | High | Production |
| llama3.2:3b | 2.0GB | Fast | Good | Development |
| llama3.2:1b | 1.3GB | Fastest | Basic | Testing |
| codellama:7b | 3.8GB | Medium | High | Code validation |

## Troubleshooting

### Ollama Issues
```bash
# Check Ollama status
ollama list

# Restart Ollama
docker restart governance-compliance-agent-ollama-1

# Check logs
docker logs governance-compliance-agent-ollama-1
```

### Memory Issues
```bash
# Use smaller model
ollama pull llama3.2:1b

# Update .env
LLM_MODEL=llama3.2:1b
```

### Port Conflicts
```bash
# Check port usage
netstat -an | findstr :8000
netstat -an | findstr :11434

# Kill processes
taskkill /F /PID <pid>
```