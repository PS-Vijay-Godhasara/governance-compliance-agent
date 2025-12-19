# Agent-Based Governance System Usage Guide

## Quick Start

### 1. Installation
```bash
# Clone and setup
git clone <repository>
cd governance-compliance-agent

# Install dependencies
pip install -r requirements.txt

# Setup Ollama (for local LLM)
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
ollama pull mistral:7b
```

### 2. Basic Usage

```python
from src.core.engine import GovernanceEngine
from src.agents.orchestrator import AgentOrchestrator

# Initialize system
engine = GovernanceEngine()
orchestrator = AgentOrchestrator(engine)
await orchestrator.start_agents()

# Register a policy
policy_id = await orchestrator.register_policy(
    name="Customer Policy",
    content="All customers must be over 18 and provide valid email"
)

# Validate data
result = await orchestrator.validate(policy_id, {
    "email": "user@example.com",
    "age": 25
})

print(f"Valid: {result['data']['is_valid']}")
```

## Agent Architecture

### Available Agents

1. **Policy Agent** - Natural language policy parsing
2. **RAG Agent** - Knowledge retrieval and context management
3. **Validation Agent** - Data validation and compliance checking
4. **Schema Agent** - Database/API schema evolution management
5. **Explanation Agent** - Human-readable explanations and remediation

### Agent Communication

Agents communicate through standardized messages:

```python
from src.agents.base_agent import AgentMessage

message = AgentMessage(
    sender="orchestrator",
    recipient="policy",
    action="parse_policy",
    payload={"policy_text": "Your policy here"}
)
```

## Core Workflows

### 1. Policy Management

```python
# Register policy
policy_id = await orchestrator.register_policy(
    name="KYC Policy",
    content="""
    Customer verification requirements:
    1. Valid government-issued ID
    2. Proof of address (utility bill, bank statement)
    3. Age verification (18+ years)
    4. Phone number verification
    """,
    metadata={"jurisdiction": "US", "regulation": "BSA"}
)

# Retrieve policy
policy = await orchestrator.get_policy(policy_id)
```

### 2. Data Validation

```python
# Comprehensive validation
customer_data = {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 25,
    "phone": "+1-555-0123",
    "documents": ["passport", "utility_bill"]
}

result = await orchestrator.validate(policy_id, customer_data)

if not result['data']['is_valid']:
    for violation in result['data']['violations']:
        print(f"Issue: {violation['description']}")
        print(f"Fix: {violation.get('remediation', 'Contact support')}")
```

### 3. KYC Validation

```python
# Specialized KYC validation
kyc_data = {
    "customer_id": "CUST_001",
    "identity_documents": [
        {"type": "passport", "number": "P123456", "expiry_date": "2025-12-31"}
    ],
    "address_proof": {"type": "utility_bill", "date": "2024-01-01"},
    "date_of_birth": "1990-05-15"
}

kyc_result = await orchestrator.perform_kyc_validation(kyc_data)
print(f"KYC Status: {kyc_result['kyc_status']}")
print(f"Recommendation: {kyc_result['recommendation']}")
```

### 4. Risk Assessment

```python
# Risk assessment with context
transaction_data = {
    "amount": 15000,
    "currency": "USD",
    "country": "US",
    "beneficiary_country": "CH"
}

context = {
    "customer_history": {
        "previous_violations": 0,
        "account_age_months": 24
    }
}

risk_result = await orchestrator.assess_risk(transaction_data, context)
print(f"Risk Level: {risk_result['risk_level']}")
print(f"Mitigation: {risk_result.get('explanation', {}).get('mitigation_strategies', [])}")
```

### 5. Schema Evolution

```python
# Detect schema changes
old_schema = {
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"}
    },
    "required": ["name", "email"]
}

new_schema = {
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"},
        "phone": {"type": "string"}  # New field
    },
    "required": ["name", "email", "phone"]  # Phone now required
}

drift_result = await orchestrator.detect_schema_drift(old_schema, new_schema)
print(f"Changes: {drift_result['total_changes']}")
print(f"Risk: {drift_result['risk_level']}")
```

### 6. Knowledge Search

```python
# Search policy knowledge base
search_result = await orchestrator.search_knowledge(
    query="customer age requirements",
    doc_type="policy",
    limit=5
)

for result in search_result['context']:
    print(f"Relevance: {result['score']:.2f}")
    print(f"Content: {result['content'][:100]}...")
```

## MCP Server Integration

### Starting MCP Server

```python
from src.mcp.mcp_server import MCPServer

# Initialize and start MCP server
mcp_server = MCPServer()
await mcp_server.start_server(host="localhost", port=8001)
```

### Available MCP Tools

1. **parse_policy** - Parse natural language policies
2. **validate_policy** - Validate policy structure
3. **get_policy** - Retrieve policy by ID
4. **store_knowledge** - Store knowledge in vector DB
5. **retrieve_context** - Retrieve relevant context
6. **semantic_search** - Semantic search across knowledge
7. **validate_data** - Validate data against rules
8. **kyc_validation** - Perform KYC validation
9. **risk_assessment** - Assess risk levels
10. **compliance_check** - Check regulatory compliance

### Using MCP Tools

```python
# Call MCP tool
response = await mcp_server.call_tool("validate_data", {
    "data": {"email": "test@example.com", "age": 25},
    "rules": {
        "rules": [
            {"field": "email", "type": "email", "required": True},
            {"field": "age", "type": "integer", "required": True}
        ]
    }
})

if response.success:
    print(f"Validation result: {response.data}")
else:
    print(f"Error: {response.error}")
```

## Configuration

### Environment Variables

```bash
# LLM Configuration
LLM_PROVIDER=ollama
LLM_MODEL=mistral:7b
LLM_BASE_URL=http://localhost:11434

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/governance
REDIS_URL=redis://localhost:6379

# Monitoring
LOG_LEVEL=INFO
ENABLE_TRACING=true
```

### Model Selection

Choose based on your needs:

- **mistral:7b** (4.1GB) - Best balance of speed/quality
- **llama3.2:3b** (2.0GB) - Fast, good quality  
- **llama3.2:1b** (1.3GB) - Fastest, basic quality
- **codellama:7b** (3.8GB) - Code-focused validation

## Production Deployment

### Docker Deployment

```bash
# Build and run
docker build -t governance-agent .
docker run -p 8000:8000 governance-agent

# Or use docker-compose
docker-compose up -d
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
        - containerPort: 8000
        env:
        - name: LLM_PROVIDER
          value: "ollama"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
```

## Monitoring and Observability

### Metrics Collection

```python
from prometheus_client import Counter, Histogram

# Custom metrics
validation_counter = Counter('validations_total', 'Total validations')
validation_duration = Histogram('validation_duration_seconds', 'Validation duration')

# Use in your code
validation_counter.inc()
with validation_duration.time():
    result = await orchestrator.validate(policy_id, data)
```

### Logging

```python
import logging
from src.core.logger import setup_logging

# Setup structured logging
setup_logging()
logger = logging.getLogger(__name__)

# Log with context
logger.info("Policy validation started", extra={
    "policy_id": policy_id,
    "data_size": len(data),
    "correlation_id": "req_123"
})
```

## Error Handling

### Common Error Patterns

```python
try:
    result = await orchestrator.validate(policy_id, data)
    if not result['success']:
        # Handle validation failure
        logger.error(f"Validation failed: {result['error']}")
        return {"error": "Validation failed", "details": result['error']}
    
except ValueError as e:
    # Handle policy not found, invalid data, etc.
    logger.error(f"Value error: {e}")
    return {"error": "Invalid input", "message": str(e)}
    
except Exception as e:
    # Handle unexpected errors
    logger.error(f"Unexpected error: {e}")
    return {"error": "Internal error", "message": "Please try again"}
```

### Retry Logic

```python
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def robust_validation(policy_id, data):
    return await orchestrator.validate(policy_id, data)
```

## Performance Optimization

### Batch Processing

```python
# Process multiple validations
async def batch_validate(policy_id, data_list):
    tasks = [
        orchestrator.validate(policy_id, data)
        for data in data_list
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

### Caching

```python
from functools import lru_cache
import redis

# Redis caching
redis_client = redis.Redis(host='localhost', port=6379, db=0)

async def cached_policy_lookup(policy_id):
    # Check cache first
    cached = redis_client.get(f"policy:{policy_id}")
    if cached:
        return json.loads(cached)
    
    # Fetch and cache
    policy = await orchestrator.get_policy(policy_id)
    redis_client.setex(f"policy:{policy_id}", 3600, json.dumps(policy))
    return policy
```

## Testing

### Unit Tests

```python
import pytest
from src.agents.policy_agent import PolicyAgent

@pytest.mark.asyncio
async def test_policy_parsing():
    agent = PolicyAgent()
    await agent.initialize()
    
    message = AgentMessage(
        sender="test",
        recipient="policy",
        action="parse_policy",
        payload={"policy_text": "Users must be over 18"}
    )
    
    response = await agent.process_message(message)
    assert response.success
    assert "rules" in response.data["parsed_rules"]
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_full_validation_workflow():
    engine = GovernanceEngine()
    orchestrator = AgentOrchestrator(engine)
    await orchestrator.start_agents()
    
    # Register policy
    policy_id = await orchestrator.register_policy(
        "Test Policy",
        "Users must provide valid email"
    )
    
    # Validate data
    result = await orchestrator.validate(policy_id, {
        "email": "test@example.com"
    })
    
    assert result['success']
    assert result['data']['is_valid']
```

## Troubleshooting

### Common Issues

1. **Ollama Connection Failed**
   ```bash
   # Check if Ollama is running
   curl http://localhost:11434/api/tags
   
   # Restart Ollama
   ollama serve
   ```

2. **ChromaDB Initialization Error**
   ```bash
   # Install missing dependencies
   pip install chromadb sentence-transformers
   
   # Clear ChromaDB data
   rm -rf ./chroma_db
   ```

3. **Agent Communication Timeout**
   ```python
   # Increase timeout in agent configuration
   agent.timeout = 30  # seconds
   ```

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable agent debug mode
orchestrator.debug_mode = True
```

## Best Practices

1. **Policy Design**
   - Use clear, specific language
   - Include business justification
   - Version your policies
   - Test with sample data

2. **Data Validation**
   - Validate early and often
   - Provide clear error messages
   - Log validation results
   - Handle edge cases

3. **Performance**
   - Cache frequently accessed policies
   - Use batch processing for bulk operations
   - Monitor agent performance
   - Scale horizontally when needed

4. **Security**
   - Sanitize input data
   - Use secure communication channels
   - Audit all policy changes
   - Implement proper access controls

## Support

- **Documentation**: See `/docs` folder
- **Examples**: See `/examples` folder
- **Issues**: GitHub Issues
- **Community**: GitHub Discussions