# Simple Test Prompts with LLM Integration

Quick test prompts to verify the governance agent with natural language capabilities.

## 🚀 Quick Start Tests with LLM

### Test 1: Basic Validation with Natural Language Explanations
```python
from src.core.simple_orchestrator import SimpleOrchestrator

# Initialize with LLM support
orchestrator = SimpleOrchestrator(use_llm=True)

# Test with invalid data
result = orchestrator.validate("customer_onboarding", {
    "email": "invalid-email",
    "age": 16
})

print(f"Valid: {result['is_valid']}")
print(f"Natural Summary: {result['natural_language_summary']}")
print(f"LLM Explanations: {result['explanations']}")
```

### Test 2: Create Policy from Natural Language
```python
# Create policy using natural language
policy_text = """
Premium customers must have:
- Account balance over $50,000
- Account age over 12 months
- Clean transaction history
"""

new_policy = orchestrator.create_policy_from_text(policy_text, "premium_policy")
print(f"Policy created: {new_policy}")
```

### Test 3: Enhanced KYC with LLM Analysis
```python
# KYC validation with LLM explanations
kyc_result = orchestrator.perform_kyc_validation({
    "identity_documents": [{"type": "passport", "expiry_date": "2025-12-31"}],
    "date_of_birth": "1990-05-15"
})

print(f"KYC Status: {kyc_result['kyc_status']}")
print(f"LLM Explanation: {kyc_result['explanation']}")
```

### Test 4: Intelligent Risk Assessment
```python
# Risk assessment with LLM analysis
risk = orchestrator.assess_risk({
    "amount": 25000,
    "country": "US",
    "customer_age": 22,
    "transaction_type": "wire_transfer"
})

print(f"Risk Level: {risk['risk_level']}")
print(f"LLM Analysis: {risk.get('explanation', 'No explanation')}")
```

### Test 5: Policy Explanation
```python
# Get natural language policy explanation
explanation = orchestrator.explain_policy("customer_onboarding")
print(f"Policy Explanation: {explanation}")
```

### Test 6: Compliance Report Generation
```python
# Generate natural language compliance report
results = [
    {"is_valid": True, "policy_name": "Customer Policy", "score": 1.0},
    {"is_valid": False, "policy_name": "KYC Policy", "score": 0.6}
]

report = orchestrator.generate_compliance_report(results)
print(f"Compliance Report:\n{report}")
```

## 🌐 API Tests with LLM Features

### Start Server with LLM
```bash
python src/simple_main.py
```

### Test LLM-Enhanced Endpoints
```bash
# Test validation with natural language response
curl -X POST "http://localhost:8000/validate" \
  -H "Content-Type: application/json" \
  -d '{"policy_id": "customer_onboarding", "data": {"email": "invalid", "age": 16}}'

# Create policy from natural language
curl -X POST "http://localhost:8000/policies/create" \
  -H "Content-Type: application/json" \
  -d '{"policy_text": "Users must be 21+ with valid ID", "policy_id": "age_verification"}'

# Get policy explanation
curl "http://localhost:8000/policies/customer_onboarding/explain"

# Generate compliance report
curl -X POST "http://localhost:8000/compliance/report" \
  -H "Content-Type: application/json" \
  -d '{"results": [{"is_valid": true, "policy_name": "Test Policy"}]}'
```

## ✅ Expected LLM-Enhanced Results

### Validation with Natural Language
```json
{
  "is_valid": false,
  "score": 0.6,
  "violations": ["Email format is invalid", "Age below minimum requirement"],
  "explanations": [
    "The email address format is not valid. Please provide a proper email with @ symbol and domain.",
    "Customer age of 16 is below the required minimum of 18 years for account creation."
  ],
  "natural_language_summary": "Customer data has 2 validation issues that need to be resolved before approval."
}
```

### KYC with LLM Analysis
```json
{
  "kyc_status": "APPROVED",
  "risk_level": "LOW",
  "documents_verified": true,
  "explanation": "Customer provided valid passport with future expiry date. All identity verification requirements are met for low-risk approval."
}
```

### Risk Assessment with LLM
```json
{
  "risk_level": "HIGH",
  "risk_score": 0.8,
  "requires_approval": true,
  "risk_factors": ["High transaction amount", "Young customer profile"],
  "explanation": "Large wire transfer of $25,000 from a 22-year-old customer presents elevated risk. Manual review recommended due to amount threshold and customer age profile."
}
```

### Policy Explanation
```
The Customer Onboarding Policy ensures new customers meet basic requirements for account creation. It validates email format for communication, verifies customers are at least 18 years old for legal compliance, and requires a valid phone number for security purposes. This policy helps maintain data quality and regulatory compliance.
```

### Compliance Report
```
COMPLIANCE REPORT SUMMARY

Overall Status: 2 of 3 validations passed (67% compliance rate)

Key Findings:
- Customer Policy: PASSED - All requirements met
- KYC Policy: FAILED - Missing required documentation  
- Risk Assessment: PASSED - Low risk profile confirmed

Recommendations:
1. Address KYC documentation gaps before account activation
2. Implement enhanced monitoring for failed validations
3. Review policy requirements for completeness

Risk Level: MEDIUM - Manual review recommended for failed KYC validation.
```

## 🔧 LLM Setup Requirements

### Install Ollama
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
ollama serve

# Pull recommended model
ollama pull llama3.2:3b
```

### Alternative Models
```bash
# Faster, smaller model
ollama pull llama3.2:1b

# Better quality, larger model  
ollama pull llama3.2:7b

# Code-focused model
ollama pull codellama:7b
```

## 🏃♂️ Run All Tests
```bash
# Test with LLM integration
python simple_usage_llm.py

# Interactive testing with LLM
python interactive_test.py

# Automated tests with LLM features
python test_runner.py --suite=all --use-llm
```

## 📝 Notes

- LLM features require Ollama running locally
- Falls back to rule-based processing if LLM unavailable
- Natural language explanations improve user experience
- Policy creation from text enables business users
- Compliance reports provide executive summaries