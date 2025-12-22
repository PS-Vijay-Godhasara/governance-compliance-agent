# Simple Test Prompts for Governance Agent

Quick test prompts to verify the simplified governance agent is working correctly.

## 🚀 Quick Start Tests

### Test 1: Basic Validation
```python
from src.core.simple_orchestrator import SimpleOrchestrator
from src.core.simple_engine import SimpleGovernanceEngine

engine = SimpleGovernanceEngine()
orchestrator = SimpleOrchestrator(engine)

# Test valid data
result = orchestrator.validate("customer_onboarding", {
    "email": "test@example.com",
    "age": 25,
    "phone": "+1-555-0123"
})
print(f"Valid: {result['is_valid']}")
```

### Test 2: Invalid Data
```python
# Test invalid email
result = orchestrator.validate("customer_onboarding", {
    "email": "invalid-email",
    "age": 25
})
print(f"Valid: {result['is_valid']}")
print(f"Violations: {result['violations']}")
```

### Test 3: KYC Validation
```python
# Test KYC
kyc_result = orchestrator.perform_kyc_validation({
    "identity_documents": [{"type": "passport", "expiry_date": "2025-12-31"}],
    "date_of_birth": "1990-05-15"
})
print(f"KYC Status: {kyc_result['kyc_status']}")
```

### Test 4: Risk Assessment
```python
# Test risk assessment
risk = orchestrator.assess_risk({
    "amount": 15000,
    "country": "US"
})
print(f"Risk Level: {risk['risk_level']}")
```

## 🌐 API Tests (if using FastAPI server)

### Start Server
```bash
python src/simple_main.py
```

### Test Endpoints
```bash
# Test validation
curl -X POST "http://localhost:8000/validate" \
  -H "Content-Type: application/json" \
  -d '{"policy_id": "customer_onboarding", "data": {"email": "test@example.com", "age": 25}}'

# Test KYC
curl -X POST "http://localhost:8000/kyc/validate" \
  -H "Content-Type: application/json" \
  -d '{"identity_documents": [{"type": "passport", "expiry_date": "2025-12-31"}]}'

# Test risk assessment
curl -X POST "http://localhost:8000/risk/assess" \
  -H "Content-Type: application/json" \
  -d '{"amount": 15000, "country": "US"}'
```

## ✅ Expected Results

### Valid Data Response
```json
{
  "is_valid": true,
  "score": 1.0,
  "violations": [],
  "explanations": []
}
```

### Invalid Data Response
```json
{
  "is_valid": false,
  "score": 0.6,
  "violations": ["Email format is invalid"],
  "explanations": ["Please provide a valid email address"]
}
```

### KYC Response
```json
{
  "kyc_status": "APPROVED",
  "risk_level": "LOW",
  "documents_verified": true,
  "violations": []
}
```

### Risk Assessment Response
```json
{
  "risk_level": "HIGH",
  "risk_score": 0.8,
  "requires_approval": true,
  "risk_factors": ["High transaction amount"]
}
```

## 🏃‍♂️ Run All Tests
```bash
python test_runner.py --suite=all
```