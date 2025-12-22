# Multi-Agent Architecture Tests

Test suite for the multi-agent governance system.

## 🧪 Test Files

- **`test_runner.py`** - Async multi-agent test suite
- **`test_config.py`** - Test configuration and workflow data

## 🚀 Running Tests

### Automated Tests
```bash
cd multi-agent/tests
python test_runner.py
```

**Expected Output:**
```
🚀 Multi-Agent Governance Test Suite
==================================================
🤖 Running Orchestrator Tests...
  ✅ PASS Validation Workflow
  ✅ PASS KYC Workflow

🔍 Running RAG Tests...
  ✅ PASS Add Knowledge
  ✅ PASS Search Knowledge
  ✅ PASS Get Context

🔌 Running MCP Tests...
  ✅ PASS List Tools
  ✅ PASS Call Enhanced Tool
  ✅ PASS Multi-Policy Validation

🔄 Running Workflow Tests...
  ✅ PASS Risk Assessment Workflow
  ✅ PASS System Status

📊 Test Summary:
Total Tests: 9
Passed: 9 ✅
Failed: 0 ❌
Success Rate: 100.0%

🎉 All tests passed!
```

## 📋 Test Coverage

### Orchestrator Tests
- ✅ Multi-agent workflow execution
- ✅ Agent coordination
- ✅ Message routing
- ✅ System lifecycle management

### RAG Service Tests
- ✅ Knowledge addition (with/without database)
- ✅ Vector/text search functionality
- ✅ Context enhancement
- ✅ Fallback mechanisms

### MCP Server Tests
- ✅ Advanced tool execution
- ✅ Database logging (when available)
- ✅ Multi-policy validation
- ✅ Compliance auditing
- ✅ Workflow orchestration

### Workflow Tests
- ✅ Complex multi-step processes
- ✅ Agent communication patterns
- ✅ Error handling and recovery
- ✅ Performance monitoring

## 🔧 Test Configuration

Edit `test_config.py` to customize:

```python
TEST_CONFIG = {
    "use_database": False,  # Test without DB dependencies
    "test_timeout": 60,     # Async operation timeout
    "mock_agents": True,    # Use mock agents for testing
    "db_path": ":memory:"   # In-memory database
}
```

## 🤖 Agent Testing

### Mock Agent Configuration
```python
AGENT_CONFIG = {
    "policy_agent": {
        "agent_id": "policy_test_001",
        "capabilities": ["policy_interpretation", "rule_validation"]
    },
    "validation_agent": {
        "agent_id": "validation_test_001", 
        "capabilities": ["data_validation", "constraint_checking"]
    }
}
```

### Workflow Testing
```python
SAMPLE_WORKFLOWS = {
    "validation": {
        "policy_id": "customer_onboarding",
        "data": {"email": "test@example.com", "age": 25}
    },
    "kyc": {
        "customer_data": {
            "identity_documents": [{"type": "passport"}]
        }
    }
}
```

## 📊 Advanced Features Testing

### Database Integration Tests
```bash
# Test with database enabled
python -c "
from test_config import TEST_CONFIG
TEST_CONFIG['use_database'] = True
from test_runner import MultiAgentTestRunner
import asyncio
asyncio.run(MultiAgentTestRunner().run_all_tests())
"
```

### Performance Testing
```bash
# Measure async operation performance
python -c "
import time
import asyncio
from test_runner import MultiAgentTestRunner

async def perf_test():
    runner = MultiAgentTestRunner()
    start = time.time()
    await runner.run_all_tests()
    print(f'Total time: {time.time() - start:.2f}s')

asyncio.run(perf_test())
"
```

## 🔍 Debugging Tests

### Verbose Async Debugging
```bash
# Enable asyncio debug mode
python -X dev test_runner.py
```

### Individual Test Components
```bash
python -c "
import asyncio
from rag_service import MultiAgentRAGService

async def test_rag():
    rag = MultiAgentRAGService(use_database=False)
    await rag.add_knowledge('test', 'sample content')
    results = await rag.search('sample')
    print(f'RAG results: {len(results)}')

asyncio.run(test_rag())
"
```

## ✅ Success Criteria

All tests should pass with:
- **Async operations** complete within timeout
- **Agent communication** functions correctly
- **Database fallback** works when DB unavailable
- **Memory usage** scales appropriately
- **Error handling** graceful degradation

## 🔄 Continuous Integration

Add to CI/CD pipeline:

```yaml
# .github/workflows/test.yml
- name: Test Multi-Agent System
  run: |
    cd multi-agent/tests
    python test_runner.py
```

## 🚨 Common Issues

### Database Connection Errors
- Tests automatically fall back to file-based storage
- Check `use_database=False` in test config

### Async Timeout Issues
- Increase `test_timeout` in configuration
- Check for deadlocks in agent communication

### Agent Communication Failures
- Verify mock agent configuration
- Check message routing in orchestrator