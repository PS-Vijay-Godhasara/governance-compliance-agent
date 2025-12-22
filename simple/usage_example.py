#!/usr/bin/env python3
"""Simple Governance Agent Usage Examples"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from orchestrator import SimpleOrchestrator

def main():
    print("Simple Governance Agent Examples")
    print("=" * 40)
    
    # Initialize orchestrator
    orchestrator = SimpleOrchestrator(use_llm=False)
    
    # Example 1: Basic validation
    print("\n1. Basic Customer Validation")
    result = orchestrator.validate("customer_onboarding", {
        "email": "john@example.com",
        "age": 25,
        "phone": "+1-555-0123"
    })
    print(f"   Valid: {result['is_valid']}")
    print(f"   Score: {result['score']}")
    
    # Example 2: Invalid data
    print("\n2. Invalid Data Validation")
    result = orchestrator.validate("customer_onboarding", {
        "email": "invalid-email",
        "age": 16
    })
    print(f"   Valid: {result['is_valid']}")
    print(f"   Violations: {result['violations']}")
    
    # Example 3: KYC validation
    print("\n3. KYC Validation")
    kyc_result = orchestrator.validate_kyc({
        "identity_documents": [{"type": "passport", "expiry_date": "2025-12-31"}],
        "date_of_birth": "1990-05-15"
    })
    print(f"   KYC Status: {kyc_result['kyc_status']}")
    print(f"   Risk Level: {kyc_result['risk_level']}")
    
    # Example 4: Risk assessment
    print("\n4. Risk Assessment")
    risk_result = orchestrator.assess_risk({
        "amount": 15000,
        "country": "US",
        "age": 22
    })
    print(f"   Risk Level: {risk_result['risk_level']}")
    print(f"   Requires Approval: {risk_result['requires_approval']}")
    
    # Example 5: Policy management
    print("\n5. Policy Management")
    policies = orchestrator.list_policies()
    print(f"   Available Policies: {policies}")
    
    print("\nExamples completed!")

if __name__ == "__main__":
    main()