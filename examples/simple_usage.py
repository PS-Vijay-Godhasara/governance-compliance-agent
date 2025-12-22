"""Simple usage examples for the governance agent"""

import asyncio
import requests
import json
from src.core.simple_orchestrator import SimpleOrchestrator


def test_direct_usage():
    """Test direct usage without API"""
    print("=== Direct Usage Test ===")
    
    # Initialize orchestrator
    orchestrator = SimpleOrchestrator()
    
    # Test customer validation
    customer_data = {
        "email": "john@example.com",
        "age": 25,
        "phone": "+1-555-0123"
    }
    
    result = orchestrator.validate("customer_onboarding", customer_data)
    print(f"Customer validation: {result['is_valid']}")
    print(f"Score: {result['score']:.2f}")
    
    if result['violations']:
        print("Violations:")
        for violation in result['violations']:
            print(f"  - {violation['field']}: {violation['message']}")
    
    # Test KYC validation
    kyc_data = {
        "identity_documents": [{"type": "passport", "number": "P123456"}],
        "address_proof": {"type": "utility_bill", "date": "2024-01-01"},
        "date_of_birth": "1990-05-15"
    }
    
    kyc_result = orchestrator.validate_kyc(kyc_data)
    print(f"\nKYC Status: {kyc_result['kyc_status']}")
    print(f"KYC Score: {kyc_result['kyc_score']:.2f}")
    
    # Test risk assessment
    risk_data = {
        "transaction_amount": 15000,
        "country": "US",
        "age": 25
    }
    
    risk_result = orchestrator.assess_risk(risk_data)
    print(f"\nRisk Level: {risk_result['risk_level']}")
    print(f"Risk Score: {risk_result['risk_score']:.2f}")
    print(f"Recommendation: {risk_result['recommendation']}")


def test_api_usage():
    """Test API usage (requires server to be running)"""
    print("\n=== API Usage Test ===")
    
    base_url = "http://localhost:8000"
    
    try:
        # Test health check
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.json()}")
        
        # List policies
        response = requests.get(f"{base_url}/policies")
        policies = response.json()["policies"]
        print(f"Available policies: {policies}")
        
        # Validate customer data
        validation_request = {
            "policy_id": "customer_onboarding",
            "data": {
                "email": "test@example.com",
                "age": 30,
                "phone": "+1-555-0123"
            }
        }
        
        response = requests.post(f"{base_url}/validate", json=validation_request)
        result = response.json()
        print(f"API validation result: {result['is_valid']}")
        
        # KYC validation
        kyc_request = {
            "customer_data": {
                "identity_documents": [{"type": "passport"}],
                "address_proof": {"type": "utility_bill"},
                "date_of_birth": "1985-03-15"
            }
        }
        
        response = requests.post(f"{base_url}/kyc", json=kyc_request)
        kyc_result = response.json()
        print(f"API KYC status: {kyc_result['kyc_status']}")
        
    except requests.exceptions.ConnectionError:
        print("API server not running. Start with: python -m src.simple_main")


def demo_business_scenarios():
    """Demo common business scenarios"""
    print("\n=== Business Scenarios Demo ===")
    
    orchestrator = SimpleOrchestrator()
    
    # Scenario 1: Valid customer onboarding
    print("\n1. Valid Customer Onboarding:")
    valid_customer = {
        "email": "alice@company.com",
        "age": 28,
        "phone": "+1-555-0199"
    }
    
    result = orchestrator.validate("customer_onboarding", valid_customer)
    print(f"   Result: {'✅ Approved' if result['is_valid'] else '❌ Rejected'}")
    
    # Scenario 2: Invalid customer (missing email)
    print("\n2. Invalid Customer (Missing Email):")
    invalid_customer = {
        "age": 17,  # Also underage
        "phone": "+1-555-0199"
    }
    
    result = orchestrator.validate("customer_onboarding", invalid_customer)
    print(f"   Result: {'✅ Approved' if result['is_valid'] else '❌ Rejected'}")
    if result['explanations']:
        for explanation in result['explanations']:
            print(f"   Issue: {explanation['explanation']}")
    
    # Scenario 3: High-risk transaction
    print("\n3. High-Risk Transaction:")
    high_risk_transaction = {
        "transaction_amount": 25000,
        "country": "XX",  # High-risk country
        "age": 19
    }
    
    risk_result = orchestrator.assess_risk(high_risk_transaction)
    print(f"   Risk Level: {risk_result['risk_level']}")
    print(f"   Action: {risk_result['recommendation']}")
    
    # Scenario 4: KYC with missing documents
    print("\n4. KYC with Missing Documents:")
    incomplete_kyc = {
        "date_of_birth": "1990-01-01"
        # Missing identity_documents and address_proof
    }
    
    kyc_result = orchestrator.validate_kyc(incomplete_kyc)
    print(f"   KYC Status: {kyc_result['kyc_status']}")
    print(f"   Recommendation: {kyc_result['recommendation']}")


if __name__ == "__main__":
    # Run all tests
    test_direct_usage()
    test_api_usage()
    demo_business_scenarios()