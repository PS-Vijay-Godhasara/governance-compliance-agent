# Test Prompts for Governance Agent Verification

This document provides specific test prompts and expected outcomes to verify the governance agent is working correctly.

## 🧪 Basic Validation Tests

### Test 1: Valid Customer Data
**Prompt:**
```python
customer_data = {
    "email": "john.doe@example.com",
    "phone": "+1-555-0123",
    "age": 25,
    "kyc_uploaded": "2024-01-15"
}
result = orchestrator.validate("customer_onboarding", customer_data)
```

**Expected Result:**
- `is_valid`: True
- `violations`: []
- `score`: 1.0

### Test 2: Invalid Email Format
**Prompt:**
```python
customer_data = {
    "email": "invalid-email",
    "phone": "+1-555-0123",
    "age": 25,
    "kyc_uploaded": "2024-01-15"
}
result = orchestrator.validate("customer_onboarding", customer_data)
```

**Expected Result:**
- `is_valid`: False
- `violations`: Contains email format violation
- `explanations`: "Email format is invalid"

### Test 3: Age Boundary Testing
**Prompt:**
```python
# Test minimum age
customer_data = {"email": "test@example.com", "age": 17}
result = orchestrator.validate("customer_onboarding", customer_data)

# Test maximum age
customer_data = {"email": "test@example.com", "age": 121}
result = orchestrator.validate("customer_onboarding", customer_data)
```

**Expected Result:**
- Age 17: `is_valid`: False, violation for minimum age
- Age 121: `is_valid`: False, violation for maximum age

## 🔍 KYC Validation Tests

### Test 4: Valid KYC Documents
**Prompt:**
```python
kyc_data = {
    "identity_documents": [
        {"type": "passport", "expiry_date": "2025-12-31"},
        {"type": "driver_license", "expiry_date": "2024-06-15"}
    ],
    "date_of_birth": "1990-05-15",
    "address_proof": {"type": "utility_bill", "date": "2024-01-10"}
}
result = orchestrator.perform_kyc_validation(kyc_data)
```

**Expected Result:**
- `kyc_status`: "APPROVED"
- `risk_level`: "LOW"
- `documents_verified`: True

### Test 5: Expired Documents
**Prompt:**
```python
kyc_data = {
    "identity_documents": [
        {"type": "passport", "expiry_date": "2023-12-31"}  # Expired
    ],
    "date_of_birth": "1990-05-15"
}
result = orchestrator.perform_kyc_validation(kyc_data)
```

**Expected Result:**
- `kyc_status`: "REJECTED"
- `violations`: Contains expired document violation
- `explanations`: "Passport has expired"

## 💰 Risk Assessment Tests

### Test 6: High-Value Transaction
**Prompt:**
```python
transaction_data = {
    "amount": 15000,
    "currency": "USD",
    "country": "US",
    "customer_tier": "premium"
}
result = orchestrator.assess_risk(transaction_data)
```

**Expected Result:**
- `risk_level`: "MEDIUM" or "HIGH"
- `requires_approval`: True
- `risk_factors`: Contains high amount factor

### Test 7: Low-Risk Transaction
**Prompt:**
```python
transaction_data = {
    "amount": 500,
    "currency": "USD",
    "country": "US",
    "customer_tier": "standard"
}
result = orchestrator.assess_risk(transaction_data)
```

**Expected Result:**
- `risk_level`: "LOW"
- `requires_approval`: False
- `auto_approved`: True

## 📋 Policy Management Tests

### Test 8: Dynamic Policy Creation
**Prompt:**
```python
new_policy = """
Premium customers must have:
- Minimum account balance of $10,000
- Account age of at least 6 months
- No more than 2 failed transactions in last 30 days
"""
policy_id = orchestrator.register_policy("premium_validation", new_policy)
```

**Expected Result:**
- Policy successfully created
- Returns valid policy_id
- Policy rules parsed correctly

### Test 9: Policy Validation
**Prompt:**
```python
premium_data = {
    "account_balance": 15000,
    "account_age_months": 8,
    "failed_transactions_30d": 1
}
result = orchestrator.validate("premium_validation", premium_data)
```

**Expected Result:**
- `is_valid`: True
- All premium criteria met

## 🔄 Schema Drift Tests

### Test 10: Schema Change Detection
**Prompt:**
```python
old_schema = {"email": "string", "age": "integer"}
new_schema = {"email": "string", "age": "integer", "phone": "string"}
drift = orchestrator.detect_schema_drift(old_schema, new_schema)
```

**Expected Result:**
- Detects new field addition
- Suggests migration strategy
- Backward compatibility analysis

## 🚨 Error Handling Tests

### Test 11: Missing Required Fields
**Prompt:**
```python
incomplete_data = {
    "email": "test@example.com"
    # Missing required fields: phone, age
}
result = orchestrator.validate("customer_onboarding", incomplete_data)
```

**Expected Result:**
- `is_valid`: False
- Multiple violations for missing fields
- Clear explanations for each missing field

### Test 12: Invalid Data Types
**Prompt:**
```python
invalid_data = {
    "email": "test@example.com",
    "age": "twenty-five",  # String instead of integer
    "phone": 5550123       # Integer instead of string
}
result = orchestrator.validate("customer_onboarding", invalid_data)
```

**Expected Result:**
- `is_valid`: False
- Type validation violations
- Suggestions for correct formats

## 🌍 Multi-Jurisdiction Tests

### Test 13: GDPR Compliance (EU)
**Prompt:**
```python
eu_customer = {
    "email": "user@example.com",
    "age": 25,
    "region": "EU",
    "consent_given": True,
    "data_processing_consent": "2024-01-15"
}
result = orchestrator.validate_with_jurisdiction("customer_onboarding", eu_customer, "EU")
```

**Expected Result:**
- GDPR-specific validations applied
- Consent requirements checked
- Data retention policies enforced

### Test 14: US Compliance
**Prompt:**
```python
us_customer = {
    "email": "user@example.com",
    "age": 25,
    "region": "US",
    "ssn_provided": True
}
result = orchestrator.validate_with_jurisdiction("customer_onboarding", us_customer, "US")
```

**Expected Result:**
- US-specific validations applied
- Different age verification rules
- SSN validation if applicable

## 📊 Performance Tests

### Test 15: Bulk Validation
**Prompt:**
```python
customers = [
    {"email": f"user{i}@example.com", "age": 20+i} 
    for i in range(1000)
]
results = orchestrator.bulk_validate("customer_onboarding", customers)
```

**Expected Result:**
- All 1000 records processed
- Processing time < 5 seconds
- Detailed results for each record

### Test 16: Concurrent Validation
**Prompt:**
```python
import asyncio

async def validate_concurrent():
    tasks = [
        orchestrator.validate_async("customer_onboarding", customer_data)
        for _ in range(100)
    ]
    return await asyncio.gather(*tasks)

results = asyncio.run(validate_concurrent())
```

**Expected Result:**
- All concurrent validations complete
- No race conditions
- Consistent results

## 🔍 Explanation Quality Tests

### Test 17: Detailed Violation Explanations
**Prompt:**
```python
complex_violation = {
    "email": "invalid-email",
    "age": 15,
    "phone": "123",
    "kyc_uploaded": "2020-01-01"  # Too old
}
result = orchestrator.validate("customer_onboarding", complex_violation)
```

**Expected Result:**
- Multiple clear explanations
- Business impact described
- Remediation steps provided
- Prioritized by severity

### Test 18: Contextual Explanations
**Prompt:**
```python
result = orchestrator.explain_policy_violation(
    policy_id="customer_onboarding",
    field="age",
    value=15,
    context={"product": "credit_card", "region": "US"}
)
```

**Expected Result:**
- Context-aware explanation
- Legal/regulatory references
- Business justification
- Alternative solutions

## ✅ Success Criteria

For each test, verify:

1. **Correctness**: Results match expected outcomes
2. **Performance**: Response time < 200ms for single validations
3. **Explanations**: Clear, actionable violation descriptions
4. **Consistency**: Same input produces same output
5. **Error Handling**: Graceful handling of invalid inputs
6. **Logging**: Proper audit trail generation

## 🚀 Quick Test Runner

```python
# Run all basic tests
python test_runner.py --suite=basic

# Run specific test
python test_runner.py --test="Test 1: Valid Customer Data"

# Run performance tests
python test_runner.py --suite=performance

# Generate test report
python test_runner.py --report
```

## 📋 Test Checklist

- [ ] All basic validation tests pass
- [ ] KYC validation works correctly
- [ ] Risk assessment provides accurate scores
- [ ] Policy management functions properly
- [ ] Schema drift detection works
- [ ] Error handling is robust
- [ ] Multi-jurisdiction support works
- [ ] Performance meets requirements
- [ ] Explanations are clear and helpful
- [ ] Concurrent operations work correctly

Use these test prompts to systematically verify your governance agent implementation and ensure all features work as expected.