# Simplified Governance & Compliance Agent

## 🎯 Overview
A lightweight governance and compliance validation system using file-based policies and simple validation rules.

## 🏗️ Simplified Architecture

```
┌─────────────────┐
│ FastAPI Server  │
│ (REST API)      │
└─────────┬───────┘
          │
┌─────────────────┐
│ Simple          │
│ Orchestrator    │
└─────────┬───────┘
          │
┌─────────────────┐    ┌─────────────────┐
│ Simple Engine   │───▶│ File-based      │
│ (Validation)    │    │ Policies        │
└─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Installation
```bash
# Install minimal dependencies
pip install -r requirements-simple.txt

# Run the server
python -m src.simple_main
```

### Basic Usage
```python
from src.core.simple_orchestrator import SimpleOrchestrator

# Initialize
orchestrator = SimpleOrchestrator()

# Validate customer data
result = orchestrator.validate("customer_onboarding", {
    "email": "user@example.com",
    "age": 25,
    "phone": "+1-555-0123"
})

print(f"Valid: {result['is_valid']}")
```

## 📁 File Structure

```
governance-compliance-agent/
├── src/
│   ├── core/
│   │   ├── simple_engine.py      # Core validation logic
│   │   └── simple_orchestrator.py # Workflow orchestration
│   └── simple_main.py            # FastAPI server
├── policies/                     # JSON policy files
│   ├── customer_onboarding.json
│   └── kyc_validation.json
├── examples/
│   └── simple_usage.py          # Usage examples
└── requirements-simple.txt      # Minimal dependencies
```

## 📋 Policy Format

Policies are stored as JSON files in the `./policies` directory:

```json
{
  "name": "Customer Onboarding Policy",
  "rules": [
    {
      "field": "email",
      "type": "email", 
      "required": true
    },
    {
      "field": "age",
      "type": "integer",
      "required": true,
      "min": 18
    }
  ]
}
```

## 🔧 Core Features

### 1. Data Validation
```python
# Validate against policy
result = orchestrator.validate("customer_onboarding", customer_data)

# Check result
if result['is_valid']:
    print("✅ Data is compliant")
else:
    for violation in result['violations']:
        print(f"❌ {violation['message']}")
```

### 2. KYC Validation
```python
# KYC validation
kyc_result = orchestrator.validate_kyc({
    "identity_documents": [{"type": "passport"}],
    "address_proof": {"type": "utility_bill"},
    "date_of_birth": "1990-05-15"
})

print(f"KYC Status: {kyc_result['kyc_status']}")
```

### 3. Risk Assessment
```python
# Risk assessment
risk_result = orchestrator.assess_risk({
    "transaction_amount": 15000,
    "country": "US"
})

print(f"Risk Level: {risk_result['risk_level']}")
```

## 🌐 API Endpoints

### GET /policies
List available policies

### GET /policies/{policy_id}
Get policy details

### POST /validate
```json
{
  "policy_id": "customer_onboarding",
  "data": {
    "email": "user@example.com",
    "age": 25
  }
}
```

### POST /kyc
```json
{
  "customer_data": {
    "identity_documents": [...],
    "address_proof": {...}
  }
}
```

### POST /risk
```json
{
  "data": {
    "transaction_amount": 15000,
    "country": "US"
  }
}
```

## 📊 Validation Rules

### Supported Types
- `string` - Text values
- `integer` - Whole numbers
- `number` - Numbers (int/float)
- `email` - Email addresses (basic validation)
- `array` - Lists
- `object` - Dictionaries
- `boolean` - True/false values

### Supported Constraints
- `required` - Field must be present
- `min` - Minimum value (numbers)
- `max` - Maximum value (numbers)
- `min_items` - Minimum array length
- `max_items` - Maximum array length

## 🎯 Use Cases

### Customer Onboarding
```python
customer = {
    "email": "john@example.com",
    "age": 25,
    "phone": "+1-555-0123"
}

result = orchestrator.validate("customer_onboarding", customer)
```

### KYC Compliance
```python
kyc_data = {
    "identity_documents": [{"type": "passport", "number": "P123456"}],
    "address_proof": {"type": "utility_bill"},
    "date_of_birth": "1990-05-15"
}

kyc_result = orchestrator.validate_kyc(kyc_data)
```

### Transaction Risk
```python
transaction = {
    "transaction_amount": 25000,
    "country": "CH",
    "age": 30
}

risk_result = orchestrator.assess_risk(transaction)
```

## 🔄 Adding New Policies

1. Create JSON file in `./policies` directory
2. Define validation rules
3. Restart application (policies loaded on startup)

Example policy file (`./policies/new_policy.json`):
```json
{
  "name": "New Policy",
  "rules": [
    {"field": "name", "type": "string", "required": true},
    {"field": "score", "type": "number", "min": 0, "max": 100}
  ]
}
```

## 🧪 Testing

```bash
# Run examples
python examples/simple_usage.py

# Test API (server must be running)
curl http://localhost:8000/health
curl http://localhost:8000/policies
```

## 📈 Benefits of Simplified Approach

- **No Database Required** - File-based policies
- **Minimal Dependencies** - Only FastAPI and Pydantic
- **Easy Deployment** - Single Python process
- **Simple Configuration** - JSON policy files
- **Fast Startup** - No complex initialization
- **Easy Testing** - Direct function calls

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Change policies directory
POLICIES_DIR=./custom_policies

# Optional: Change server port
PORT=8080
```

### Policy Directory Structure
```
policies/
├── customer_onboarding.json
├── kyc_validation.json
├── transaction_limits.json
└── data_quality.json
```

This simplified version removes the complexity of multi-agent communication, database dependencies, and heavy frameworks while maintaining core governance functionality.