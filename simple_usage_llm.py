#!/usr/bin/env python3
"""
Simple Usage Examples with LLM Integration
Demonstrates governance agent with natural language capabilities
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.simple_engine import SimpleGovernanceEngine
from core.simple_orchestrator import SimpleOrchestrator

def main():
    print("🤖 Governance Agent with LLM Integration")
    print("="*50)
    
    # Initialize with LLM support
    print("\n1. Initializing governance engine with LLM...")
    engine = SimpleGovernanceEngine(use_llm=True)
    orchestrator = SimpleOrchestrator(engine, use_llm=True)
    
    # Test 1: Basic validation with natural language explanations
    print("\n2. Testing customer validation with LLM explanations...")
    customer_data = {
        "email": "invalid-email",
        "age": 16,
        "phone": "+1-555-0123"
    }
    
    result = orchestrator.validate("customer_onboarding", customer_data)
    print(f"Valid: {result['is_valid']}")
    print(f"Score: {result['score']}")
    print(f"Natural Language Summary: {result['natural_language_summary']}")
    if result['explanations']:
        print("LLM Explanations:")
        for explanation in result['explanations']:
            print(f"  - {explanation}")
    
    # Test 2: Create policy from natural language
    print("\n3. Creating policy from natural language...")
    policy_text = """
    Premium customers must have:
    - Minimum account balance of $50,000
    - Account age of at least 12 months
    - No more than 1 failed transaction in last 90 days
    - Valid premium membership status
    """
    
    new_policy = orchestrator.create_policy_from_text(policy_text, "premium_customer_policy")
    print(f"Created policy: {new_policy.get('description', 'Policy created')}")
    
    # Test 3: Enhanced KYC validation
    print("\n4. Testing KYC validation with LLM analysis...")
    kyc_data = {
        "identity_documents": [
            {"type": "passport", "expiry_date": "2025-12-31"}
        ],
        "date_of_birth": "1990-05-15",
        "address_proof": {"type": "utility_bill", "date": "2024-01-10"}
    }
    
    kyc_result = orchestrator.perform_kyc_validation(kyc_data)
    print(f"KYC Status: {kyc_result['kyc_status']}")
    print(f"Risk Level: {kyc_result['risk_level']}")
    print(f"Explanation: {kyc_result['explanation']}")
    
    # Test 4: Enhanced risk assessment
    print("\n5. Testing risk assessment with LLM analysis...")
    transaction_data = {
        "amount": 25000,
        "currency": "USD",
        "country": "US",
        "customer_age": 22,
        "transaction_type": "wire_transfer"
    }
    
    risk_result = orchestrator.assess_risk(transaction_data)
    print(f"Risk Level: {risk_result['risk_level']}")
    print(f"Risk Score: {risk_result['risk_score']}")
    print(f"Requires Approval: {risk_result.get('requires_approval', False)}")
    if 'explanation' in risk_result:
        print(f"Risk Analysis: {risk_result['explanation']}")
    
    # Test 5: Policy explanation
    print("\n6. Getting natural language policy explanation...")
    policy_explanation = orchestrator.explain_policy("customer_onboarding")
    print(f"Policy Explanation: {policy_explanation}")
    
    # Test 6: Compliance report generation
    print("\n7. Generating compliance report...")
    validation_results = [
        {"is_valid": True, "policy_name": "Customer Onboarding", "score": 1.0},
        {"is_valid": False, "policy_name": "KYC Validation", "score": 0.6, "violations": ["Missing documents"]},
        {"is_valid": True, "policy_name": "Risk Assessment", "score": 0.8}
    ]
    
    compliance_report = orchestrator.generate_compliance_report(validation_results)
    print("Compliance Report:")
    print(compliance_report)
    
    print("\n✅ All tests completed!")
    print("\nNote: LLM features require Ollama running with a model like 'llama3.2:3b'")
    print("If LLM is not available, the system falls back to rule-based processing.")

if __name__ == "__main__":
    main()