# MCP Integration Guide

## Overview
The Model Context Protocol (MCP) server exposes all agent capabilities as standardized tools for external integration.

## Available MCP Tools

### Policy Management Tools

#### `parse_policy`
**Description**: Parse natural language policy into structured rules
**Schema**:
```json
{
  "type": "object",
  "properties": {
    "policy_text": {"type": "string", "description": "Natural language policy text"},
    "policy_id": {"type": "string", "description": "Optional policy identifier"}
  },
  "required": ["policy_text"]
}
```

#### `validate_policy`
**Description**: Validate policy structure and completeness
**Schema**:
```json
{
  "type": "object", 
  "properties": {
    "rules": {"type": "object", "description": "Policy rules to validate"}
  },
  "required": ["rules"]
}
```

#### `get_policy`
**Description**: Retrieve policy by ID
**Schema**:
```json
{
  "type": "object",
  "properties": {
    "policy_id": {"type": "string", "description": "Policy identifier"}
  },
  "required": ["policy_id"]
}
```

### Knowledge Management Tools

#### `store_knowledge`
**Description**: Store knowledge in vector database
**Schema**:
```json
{
  "type": "object",
  "properties": {
    "content": {"type": "string", "description": "Content to store"},
    "type": {"type": "string", "description": "Document type (policy/regulation)"},
    "id": {"type": "string", "description": "Document identifier"},
    "metadata": {"type": "object", "description": "Additional metadata"}
  },
  "required": ["content"]
}
```

#### `retrieve_context`
**Description**: Retrieve relevant context for a query
**Schema**:
```json
{
  "type": "object",
  "properties": {
    "query": {"type": "string", "description": "Search query"},
    "type": {"type": "string", "description": "Document type to search"},
    "limit": {"type": "integer", "description": "Maximum results to return"}
  },
  "required": ["query"]
}
```

#### `semantic_search`
**Description**: Perform semantic search across knowledge base
**Schema**:
```json
{
  "type": "object",
  "properties": {
    "query": {"type": "string", "description": "Search query"},
    "threshold": {"type": "number", "description": "Similarity threshold"}
  },
  "required": ["query"]
}
```

### Validation Tools

#### `validate_data`
**Description**: Validate data against policy rules
**Schema**:
```json
{
  "type": "object",
  "properties": {
    "data": {"type": "object", "description": "Data to validate"},
    "rules": {"type": "object", "description": "Validation rules"},
    "context": {"type": "object", "description": "Additional context"}
  },
  "required": ["data", "rules"]
}
```

#### `kyc_validation`
**Description**: Perform KYC validation
**Schema**:
```json
{
  "type": "object",
  "properties": {
    "customer_data": {"type": "object", "description": "Customer data"},
    "requirements": {"type": "object", "description": "KYC requirements"}
  },
  "required": ["customer_data"]
}
```

#### `risk_assessment`
**Description**: Perform risk assessment
**Schema**:
```json
{
  "type": "object",
  "properties": {
    "data": {"type": "object", "description": "Data for risk assessment"},
    "context": {"type": "object", "description": "Additional context"}
  },
  "required": ["data"]
}
```

#### `compliance_check`
**Description**: Check compliance against regulations
**Schema**:
```json
{
  "type": "object",
  "properties": {
    "data": {"type": "object", "description": "Data to check"},
    "regulations": {"type": "array", "description": "Regulations to check against"},
    "jurisdiction": {"type": "string", "description": "Legal jurisdiction"}
  },
  "required": ["data", "regulations"]
}
```

## Usage Examples

### Starting MCP Server
```python
from src.mcp.mcp_server import MCPServer

# Initialize MCP server
mcp_server = MCPServer()

# Start server (in production, this would be HTTP/WebSocket)
await mcp_server.start_server(host="localhost", port=8001)
```

### Calling MCP Tools
```python
# Parse a policy
policy_response = await mcp_server.call_tool("parse_policy", {
    "policy_text": "All customers must be over 18 and provide valid email",
    "policy_id": "customer_policy_1"
})

if policy_response.success:
    print(f"Policy parsed: {policy_response.data['policy_id']}")
else:
    print(f"Error: {policy_response.error}")

# Validate data
validation_response = await mcp_server.call_tool("validate_data", {
    "data": {"email": "test@example.com", "age": 25},
    "rules": {
        "rules": [
            {"field": "email", "type": "email", "required": True},
            {"field": "age", "type": "integer", "required": True, "constraints": {"min": 18}}
        ]
    }
})

print(f"Valid: {validation_response.data['is_valid']}")
```

### Getting Tool Schema
```python
# Get all available tools and their schemas
tools_schema = mcp_server.get_tools_schema()

for tool in tools_schema:
    print(f"Tool: {tool['name']}")
    print(f"Description: {tool['description']}")
    print(f"Schema: {tool['input_schema']}")
```

## Integration Patterns

### IDE Integration
```python
# Example IDE plugin integration
class GovernancePlugin:
    def __init__(self):
        self.mcp_server = MCPServer()
    
    async def validate_code_policy(self, code_snippet):
        return await self.mcp_server.call_tool("validate_data", {
            "data": {"code": code_snippet},
            "rules": self.get_code_policy_rules()
        })
    
    async def explain_violation(self, violation):
        return await self.mcp_server.call_tool("explain_violation", {
            "violations": [violation]
        })
```

### API Gateway Integration
```python
# FastAPI integration
from fastapi import FastAPI
from src.mcp.mcp_server import MCPServer

app = FastAPI()
mcp_server = MCPServer()

@app.post("/validate")
async def validate_endpoint(request: ValidationRequest):
    response = await mcp_server.call_tool("validate_data", {
        "data": request.data,
        "rules": request.rules
    })
    return response.data if response.success else {"error": response.error}
```

### Message Queue Integration
```python
# Redis/RabbitMQ integration
import asyncio
import json

async def process_validation_queue():
    while True:
        message = await queue.get()
        
        response = await mcp_server.call_tool("validate_data", 
                                            json.loads(message))
        
        await result_queue.put(json.dumps(response.data))
```

## Error Handling

### MCP Response Format
```python
@dataclass
class MCPResponse:
    success: bool
    data: Any
    error: Optional[str] = None
```

### Error Types
- **Tool Not Found**: Requested tool doesn't exist
- **Invalid Parameters**: Missing or invalid required parameters
- **Agent Error**: Internal agent processing error
- **System Error**: Infrastructure or communication error

### Error Handling Example
```python
async def safe_mcp_call(tool_name, parameters):
    try:
        response = await mcp_server.call_tool(tool_name, parameters)
        
        if response.success:
            return response.data
        else:
            logger.error(f"MCP tool error: {response.error}")
            return None
            
    except Exception as e:
        logger.error(f"MCP communication error: {e}")
        return None
```

## Performance Considerations

### Async Processing
```python
# Process multiple tools concurrently
async def batch_validation(data_list):
    tasks = [
        mcp_server.call_tool("validate_data", {"data": data, "rules": rules})
        for data in data_list
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

### Caching
```python
# Cache frequently used tools
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_policy(policy_id):
    return asyncio.run(mcp_server.call_tool("get_policy", {"policy_id": policy_id}))
```

## Security Considerations

### Input Validation
```python
def validate_mcp_input(tool_name, parameters):
    schema = mcp_server.tools[tool_name].input_schema
    # Validate parameters against schema
    # Sanitize input data
    # Check permissions
    return validated_parameters
```

### Access Control
```python
class SecureMCPServer(MCPServer):
    def __init__(self, auth_provider):
        super().__init__()
        self.auth_provider = auth_provider
    
    async def call_tool(self, tool_name, parameters, user_context=None):
        if not self.auth_provider.can_access_tool(user_context, tool_name):
            return MCPResponse(success=False, error="Access denied")
        
        return await super().call_tool(tool_name, parameters)
```

## Monitoring and Observability

### Metrics Collection
```python
from prometheus_client import Counter, Histogram

mcp_calls_total = Counter('mcp_calls_total', 'Total MCP calls', ['tool_name', 'status'])
mcp_duration = Histogram('mcp_duration_seconds', 'MCP call duration', ['tool_name'])

async def monitored_call_tool(self, tool_name, parameters):
    with mcp_duration.labels(tool_name=tool_name).time():
        response = await self.call_tool(tool_name, parameters)
        
        status = 'success' if response.success else 'error'
        mcp_calls_total.labels(tool_name=tool_name, status=status).inc()
        
        return response
```

### Logging
```python
import structlog

logger = structlog.get_logger()

async def logged_call_tool(self, tool_name, parameters):
    logger.info("MCP tool called", tool=tool_name, params_size=len(str(parameters)))
    
    response = await self.call_tool(tool_name, parameters)
    
    logger.info("MCP tool completed", 
                tool=tool_name, 
                success=response.success,
                error=response.error)
    
    return response
```