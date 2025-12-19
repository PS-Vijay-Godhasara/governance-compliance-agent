# End User Guide - Governance & Compliance Agent

## Quick Start for Business Users

### 1. Policy Creation Flow

**Step 1: Write Policy in Natural Language**
```text
Customer Onboarding Policy:
- All customers must provide a valid email address
- Customer age must be 18 years or older
- Phone number with country code is required
- Identity documents must be uploaded within 30 days
```

**Step 2: Register Policy**
```python
policy_id = await orchestrator.register_policy(
    name="Customer Onboarding v1.0",
    content=policy_text,
    metadata={"jurisdiction": "US", "regulation": "BSA"}
)
```

**Step 3: Test Policy**
```python
test_customer = {
    "email": "john.doe@example.com",
    "age": 25,
    "phone": "+1-555-0123",
    "documents_uploaded": True
}

result = await orchestrator.validate(policy_id, test_customer)
```

### 2. Data Validation Flow

**Submit Data → Validate → Review Results → Take Action**

```python
# Step 1: Submit data
customer_data = {
    "email": "john@example.com",
    "age": 25,
    "phone": "+1-555-0123"
}

# Step 2: Validate
result = await orchestrator.validate(policy_id, customer_data)

# Step 3: Review results
if result['data']['is_valid']:
    print("✅ Customer data is compliant")
else:
    print("❌ Issues found:")
    for violation in result['data']['violations']:
        print(f"- {violation['field']}: {violation['message']}")
```

### 3. KYC Validation Flow

```python
# Prepare KYC data
kyc_data = {
    "identity_documents": [{"type": "passport", "expiry_date": "2025-12-31"}],
    "address_proof": {"type": "utility_bill"},
    "date_of_birth": "1990-05-15"
}

# Run KYC validation
kyc_result = await orchestrator.perform_kyc_validation(kyc_data)

# Handle results
if kyc_result['kyc_status'] == "approved":
    print("✅ Customer approved")
elif kyc_result['kyc_status'] == "rejected":
    print("❌ Customer rejected")
else:
    print("⚠️ Manual review required")
```

### 4. Risk Assessment Flow

```python
# Transaction data
transaction = {
    "amount": 25000,
    "currency": "USD",
    "country": "US",
    "beneficiary_country": "CH"
}

# Assess risk
risk_result = await orchestrator.assess_risk(transaction)

# Take action based on risk
if risk_result['risk_level'] == "low":
    await approve_transaction()
elif risk_result['risk_level'] == "medium":
    await flag_for_monitoring()
else:  # high risk
    await queue_for_manual_review()
```

## Common Business Scenarios

### Scenario 1: Customer Onboarding
```python
async def onboard_customer(customer_data):
    # Validate against policy
    validation = await orchestrator.validate("onboarding_policy", customer_data)
    
    if not validation['data']['is_valid']:
        return {"status": "rejected", "reasons": validation['data']['violations']}
    
    # KYC validation
    kyc_result = await orchestrator.perform_kyc_validation(customer_data)
    
    if kyc_result['kyc_status'] != "approved":
        return {"status": "kyc_pending", "result": kyc_result}
    
    return {"status": "approved"}
```

### Scenario 2: Transaction Processing
```python
async def process_transaction(transaction_data):
    risk = await orchestrator.assess_risk(transaction_data)
    
    if risk['risk_level'] == "low":
        return await process_immediately(transaction_data)
    elif risk['risk_level'] == "medium":
        return await process_with_monitoring(transaction_data)
    else:
        return await queue_for_review(transaction_data)
```

## Error Handling

```python
try:
    result = await orchestrator.validate(policy_id, data)
    if not result['success']:
        print(f"Validation failed: {result['error']}")
except Exception as e:
    print(f"System error: {e}")
```

## Best Practices

1. **Policy Writing**: Use clear, specific language
2. **Data Validation**: Validate early in the process
3. **Risk Management**: Set appropriate thresholds
4. **Compliance**: Regular policy reviews