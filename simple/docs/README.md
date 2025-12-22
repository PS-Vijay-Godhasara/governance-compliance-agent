# Simple Governance Agent Architecture

A lightweight, file-based governance and compliance validation system with RAG and MCP integration.

## 🏗️ Architecture Overview

```
simple/
├── src/
│   ├── engine.py          # Core validation engine
│   ├── orchestrator.py    # Workflow orchestrator  
│   ├── llm_service.py     # Optional LLM integration
│   ├── rag_service.py     # File-based RAG service
│   ├── mcp_server.py      # MCP protocol server
│   └── main.py           # FastAPI server
├── tests/
│   └── test_runner.py    # Test suite
├── docs/
│   └── README.md         # This documentation
├── policies/             # JSON policy files
└── knowledge/            # RAG knowledge base (JSON files)
```

## 🔧 Core Components

### 1. SimpleGovernanceEngine (`engine.py`)
- **File-based policies** - JSON configuration files
- **Rule validation** - Type checking, constraints, patterns
- **LLM integration** - Optional natural language processing
- **Policy creation** - Generate policies from text

### 2. SimpleOrchestrator (`orchestrator.py`)
- **Validation workflows** - Customer, KYC, risk assessment
- **Business logic** - Status determination, scoring
- **RAG integration** - Knowledge-enhanced validation
- **MCP coordination** - Tool execution management

### 3. SimpleRAGService (`rag_service.py`)
- **File-based knowledge** - JSON knowledge storage
- **Text search** - Simple keyword matching
- **Context enhancement** - Policy-relevant information
- **No database dependencies** - Pure file-based operation

### 4. SimpleMCPServer (`mcp_server.py`)
- **Tool registry** - Governance-specific tools
- **Parameter validation** - Type and constraint checking
- **Execution logging** - In-memory operation history
- **Resource management** - File-based resource storage

## 📋 RAG Knowledge Structure

```json
{
  "gdpr": {
    "description": "EU General Data Protection Regulation",
    "key_requirements": ["consent", "data_minimization"],
    "penalties": "Up to 4% of annual revenue"
  },
  "kyc": {
    "description": "Know Your Customer requirements",
    "documents_required": ["government_id", "proof_of_address"]
  }
}
```

## 🛠️ MCP Tools Available

| Tool | Description | Parameters |
|------|-------------|------------|
| `validate_data` | Validate against policy | policy_id, data |
| `assess_risk` | Risk factor analysis | data |
| `validate_kyc` | KYC workflow | customer_data |
| `search_knowledge` | RAG knowledge search | query, topic |
| `list_policies` | Available policies | none |
| `create_policy` | Policy from text | policy_text, policy_id |

## 🚀 Quick Start

### 1. Basic Usage with RAG
```python
from orchestrator import SimpleOrchestrator

# Initialize with RAG
orchestrator = SimpleOrchestrator(use_llm=False)

# Search knowledge base
results = orchestrator.search_knowledge("GDPR consent requirements")
print(results)
# [{"topic": "regulations", "content": "GDPR consent...", "relevance": 0.8}]

# Get policy context
context = orchestrator.get_context("customer_onboarding")
print(context["related_info"])
```

### 2. MCP Tool Usage
```python
# Call MCP tools
result = orchestrator.call_mcp_tool("validate_data", {
    "policy_id": "customer_onboarding",
    "data": {"email": "user@example.com", "age": 25}
})

# List available tools
tools = orchestrator.list_mcp_tools()
print([tool["name"] for tool in tools])
```

### 3. Enhanced API Endpoints
```bash
# Start server
python src/main.py

# Search knowledge
curl "http://localhost:8000/knowledge/search?query=GDPR&topic=regulations"

# List MCP tools
curl "http://localhost:8000/mcp/tools"

# Call MCP tool
curl -X POST "http://localhost:8000/mcp/call" \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "validate_data", "parameters": {"policy_id": "customer_onboarding", "data": {"email": "test@example.com"}}}'
```

## 🔍 RAG Features

### File-Based Knowledge Storage
- **JSON files** - Human-readable knowledge format
- **Topic organization** - Separate files per domain
- **Simple search** - Keyword-based matching
- **No dependencies** - No vector database required

### Knowledge Enhancement
```python
# Add new knowledge
orchestrator.rag_service.add_knowledge("compliance", {
    "sox": "Sarbanes-Oxley Act requirements for financial reporting"
})

# Search with context
results = orchestrator.search_knowledge("financial reporting compliance")
```

## 🔌 MCP Integration

### Tool Registration
```python
# Tools are automatically registered
tools = [
    "validate_data", "assess_risk", "validate_kyc",
    "search_knowledge", "list_policies", "create_policy"
]
```

### Execution Logging
```python
# All tool executions are logged in memory
server = orchestrator.mcp_server
print(f"Executed {len(server.execution_log)} tools")
```

## 📊 Validation with RAG Enhancement

```python
# Enhanced validation workflow
result = orchestrator.validate("customer_onboarding", {
    "email": "user@example.com",
    "age": 25
})

# Includes RAG context automatically
print(result["summary"])  # "Validation passed with GDPR compliance noted"
```

## 🧪 Testing RAG and MCP

```bash
cd simple/tests
python test_runner.py

# Tests include:
# ✅ RAG knowledge search
# ✅ MCP tool execution  
# ✅ Enhanced validation
# ✅ Context retrieval
```

## 📈 Performance

- **RAG Search**: <10ms for file-based lookup
- **MCP Tools**: <50ms per tool execution
- **Memory Usage**: <50MB additional overhead
- **No Database**: Zero database setup or maintenance

## 🔧 Configuration

### Knowledge Directory
```python
# Custom knowledge location
orchestrator = SimpleOrchestrator(policies_dir="./custom_policies")
orchestrator.rag_service = SimpleRAGService("./custom_knowledge")
```

### MCP Server Settings
```python
# Access MCP server directly
mcp_server = orchestrator.mcp_server
server_info = mcp_server.get_server_info()
print(server_info["capabilities"])
```

## 🎯 Use Cases

### Enhanced Validation
- **Context-aware validation** - RAG provides regulatory context
- **Compliance checking** - Knowledge base includes requirements
- **Policy explanation** - Natural language policy descriptions

### Tool Integration
- **External systems** - MCP tools for system integration
- **Workflow automation** - Standardized tool interface
- **API consistency** - Uniform tool parameter validation

### Knowledge Management
- **Regulatory updates** - Easy knowledge file updates
- **Domain expertise** - Structured compliance information
- **Search capabilities** - Quick information retrieval

## 🔄 Extensibility

### Adding Knowledge
```python
# Add new regulatory information
new_regulation = {
    "ccpa": {
        "description": "California Consumer Privacy Act",
        "requirements": ["opt-out rights", "data deletion"]
    }
}
orchestrator.rag_service.add_knowledge("regulations", new_regulation)
```

### Custom MCP Tools
```python
# Register custom tool
orchestrator.mcp_server.tools["custom_validation"] = {
    "name": "custom_validation",
    "description": "Custom business validation",
    "parameters": {"data": {"type": "object", "required": True}}
}
```

This simple architecture provides RAG and MCP capabilities without database complexity, maintaining the lightweight, file-based approach while adding powerful knowledge retrieval and tool integration features.