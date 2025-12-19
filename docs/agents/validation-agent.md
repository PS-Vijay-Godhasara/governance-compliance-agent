# Validation Agent Documentation

## Overview
The Validation Agent performs comprehensive data validation, KYC checks, risk assessment, and compliance verification.

## Core Actions

### `validate_data`
**Input:**
```json
{
  "data": {"email": "user@example.com", "age": 25},
  "rules": {
    "rules": [
      {"field": "email", "type": "email", "required": true},
      {"field": "age", "type": "integer", "required": true, "constraints": {"min": 18}}
    ]
  },
  "context": {"region": "US"}
}
```

**Output:**
```json
{
  "is_valid": true,
  "score": 1.0,
  "violations": [],
  "warnings": [],
  "total_checks": 2
}
```

### `kyc_validation`
**Input:**
```json
{
  "customer_data": {
    "identity_documents": [{"type": "passport", "expiry_date": "2025-12-31"}],
    "address_proof": {"type": "utility_bill"},
    "date_of_birth": "1990-05-15"
  }
}
```

**Output:**
```json
{
  "kyc_status": "approved",
  "kyc_score": 0.85,
  "issues": [],
  "recommendation": "Customer approved for onboarding"
}
```

### `risk_assessment`
**Input:**
```json
{
  "data": {
    "transaction_amount": 15000,
    "country": "US",
    "beneficiary_country": "CH"
  },
  "context": {
    "customer_history": {"previous_violations": 0}
  }
}
```

**Output:**
```json
{
  "risk_level": "medium",
  "risk_score": 0.6,
  "risk_factors": [
    {"factor": "high_value_transaction", "weight": 0.3}
  ],
  "recommendation": "Enhanced monitoring recommended"
}
```

### `compliance_check`
Checks data against regulatory requirements for specific jurisdictions.

## Usage Example

```python
from src.agents.validation_agent import ValidationAgent

validation_agent = ValidationAgent()
await validation_agent.initialize()

# Validate customer data
message = AgentMessage(
    sender="user",
    recipient="validation",
    action="validate_data",
    payload={
        "data": {
            "email": "john@example.com",
            "age": 25,
            "phone": "+1-555-0123"
        },
        "rules": {
            "rules": [
                {"field": "email", "type": "email", "required": True},
                {"field": "age", "type": "integer", "required": True, "constraints": {"min": 18}},
                {"field": "phone", "type": "phone", "required": True}
            ]
        }
    }
)

response = await validation_agent.process_message(message)
if response.data['is_valid']:
    print("Data is valid")
else:
    for violation in response.data['violations']:
        print(f"Issue: {violation['message']}")
```

## Validation Patterns
- **Email**: RFC-compliant email validation
- **Phone**: International phone number formats
- **SSN**: US Social Security Number format
- **Credit Card**: Standard credit card number format

## Risk Thresholds
- **High Risk**: Score ≥ 0.8
- **Medium Risk**: Score ≥ 0.5
- **Low Risk**: Score < 0.5