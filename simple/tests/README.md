# Simple Architecture Tests

Test suite for the simple governance agent architecture.

## 🧪 Test Files

- **`test_runner.py`** - Automated test suite
- **`interactive_test.py`** - Interactive testing interface  
- **`test_config.py`** - Test configuration and sample data

## 🚀 Running Tests

### Automated Tests
```bash
cd simple/tests
python test_runner.py
```

**Expected Output:**
```
🚀 Simple Governance Agent Test Suite
==================================================
🧪 Running Basic Tests...
  ✅ PASS Valid Customer Data
  ✅ PASS Invalid Email
  ✅ PASS Age Too Young

🔍 Running RAG Tests...
  ✅ PASS Knowledge Search
  ✅ PASS Context Retrieval

🔌 Running MCP Tests...
  ✅ PASS List MCP Tools
  ✅ PASS Call MCP Tool

📊 Test Summary:
Total Tests: 8
Passed: 8 ✅
Failed: 0 ❌
Success Rate: 100.0%

🎉 All tests passed!
```

### Interactive Tests
```bash
cd simple/tests
python interactive_test.py
```

**Interactive Menu:**
```
🤖 Simple Governance Agent Interactive Tests
==================================================
1. Basic Validation Tests
2. RAG Knowledge Tests
3. MCP Tool Tests
4. KYC Validation Tests
5. Risk Assessment Tests
6. Custom Data Test
7. Run All Quick Tests
0. Exit
```

## 📋 Test Coverage

### Basic Validation Tests
- ✅ Valid customer data
- ✅ Invalid email format
- ✅ Age boundary testing
- ✅ Missing required fields

### RAG Service Tests
- ✅ Knowledge search functionality
- ✅ Context retrieval for policies
- ✅ Topic-based filtering

### MCP Server Tests
- ✅ Tool listing
- ✅ Tool execution
- ✅ Parameter validation
- ✅ Error handling

### KYC Workflow Tests
- ✅ Document validation
- ✅ Status determination
- ✅ Risk level assessment

### Risk Assessment Tests
- ✅ High-value transactions
- ✅ Geographic risk factors
- ✅ Age-based risk scoring

## 🔧 Test Configuration

Edit `test_config.py` to customize:

```python
TEST_CONFIG = {
    "use_llm": False,  # Disable for consistent testing
    "test_timeout": 30,
    "verbose_output": True
}
```

## 📊 Sample Test Data

```python
# Valid customer data
{
    "email": "john.doe@example.com",
    "age": 28,
    "phone": "+1-555-0123",
    "full_name": "John Doe"
}

# Invalid test cases
{
    "email": "invalid-email-format",  # Bad email
    "age": 16,                       # Too young
    "phone": "555-0123"             # Missing country code
}
```

## 🐛 Debugging Tests

### Verbose Output
```bash
python test_runner.py --verbose
```

### Single Test Category
```bash
python -c "
from test_runner import SimpleTestRunner
runner = SimpleTestRunner()
runner.run_basic_tests()
"
```

### Custom Test Data
```bash
python interactive_test.py
# Select option 6 for custom data input
```

## ✅ Success Criteria

All tests should pass with:
- **Response time** < 100ms per validation
- **Memory usage** < 50MB additional overhead
- **No external dependencies** required
- **Consistent results** across runs

## 🔄 Continuous Testing

Add to your development workflow:

```bash
# Before committing changes
cd simple/tests && python test_runner.py

# Quick validation check
cd simple/tests && python -c "
from test_runner import SimpleTestRunner
runner = SimpleTestRunner()
runner.run_basic_tests()
"
```