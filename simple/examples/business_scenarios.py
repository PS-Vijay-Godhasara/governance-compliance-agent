"""Business Scenarios Examples"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from orchestrator import SimpleOrchestrator

def customer_onboarding_scenarios():
    """Customer onboarding business scenarios"""
    print("Customer Onboarding Scenarios")
    print("=" * 30)
    
    orchestrator = SimpleOrchestrator(use_llm=False)
    
    scenarios = [
        {
            "name": "Valid New Customer",
            "data": {
                "email": "alice.smith@company.com",
                "age": 28,
                "phone": "+1-555-0199",
                "full_name": "Alice Smith"
            }
        },
        {
            "name": "Underage Customer",
            "data": {
                "email": "teen@example.com",
                "age": 16,
                "phone": "+1-555-0123"
            }
        },
        {
            "name": "Invalid Email Format",
            "data": {
                "email": "not-an-email",
                "age": 25,
                "phone": "+1-555-0123"
            }
        },
        {
            "name": "Missing Required Fields",
            "data": {
                "email": "incomplete@example.com"
            }
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. {scenario['name']}:")
        result = orchestrator.validate("customer_onboarding", scenario['data'])
        
        status = "APPROVED" if result['is_valid'] else "REJECTED"
        print(f"   Status: {status}")
        print(f"   Score: {result['score']:.2f}")
        
        if result['violations']:
            print("   Issues:")
            for violation in result['violations']:
                print(f"   - {violation}")

def kyc_compliance_scenarios():
    """KYC compliance scenarios"""
    print("\n\nKYC Compliance Scenarios")
    print("=" * 24)
    
    orchestrator = SimpleOrchestrator(use_llm=False)
    
    scenarios = [
        {
            "name": "Complete KYC Documentation",
            "data": {
                "identity_documents": [
                    {"type": "passport", "expiry_date": "2025-12-31"},
                    {"type": "driver_license", "expiry_date": "2024-08-15"}
                ],
                "date_of_birth": "1990-05-15",
                "address_proof": {"type": "utility_bill", "date": "2024-01-10"}
            }
        },
        {
            "name": "Expired Documents",
            "data": {
                "identity_documents": [
                    {"type": "passport", "expiry_date": "2023-01-01"}
                ],
                "date_of_birth": "1985-03-20"
            }
        },
        {
            "name": "Missing Identity Documents",
            "data": {
                "date_of_birth": "1992-08-10",
                "address_proof": {"type": "bank_statement", "date": "2024-01-05"}
            }
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. {scenario['name']}:")
        result = orchestrator.validate_kyc(scenario['data'])
        
        print(f"   KYC Status: {result['kyc_status']}")
        print(f"   Risk Level: {result['risk_level']}")
        print(f"   Explanation: {result['explanation']}")

def risk_assessment_scenarios():
    """Risk assessment scenarios"""
    print("\n\nRisk Assessment Scenarios")
    print("=" * 25)
    
    orchestrator = SimpleOrchestrator(use_llm=False)
    
    scenarios = [
        {
            "name": "Low-Risk Standard Transaction",
            "data": {
                "amount": 500,
                "country": "US",
                "age": 35,
                "customer_tier": "standard"
            }
        },
        {
            "name": "High-Value Transaction",
            "data": {
                "amount": 25000,
                "country": "US",
                "age": 45,
                "customer_tier": "premium"
            }
        },
        {
            "name": "High-Risk Geography",
            "data": {
                "amount": 5000,
                "country": "XX",  # High-risk country
                "age": 30,
                "customer_tier": "standard"
            }
        },
        {
            "name": "Young Customer Large Transaction",
            "data": {
                "amount": 15000,
                "country": "US",
                "age": 19,
                "customer_tier": "standard"
            }
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. {scenario['name']}:")
        result = orchestrator.assess_risk(scenario['data'])
        
        print(f"   Risk Level: {result['risk_level']}")
        print(f"   Risk Score: {result['risk_score']:.2f}")
        print(f"   Requires Approval: {result['requires_approval']}")
        print(f"   Explanation: {result['explanation']}")

def compliance_workflow_scenarios():
    """End-to-end compliance workflow scenarios"""
    print("\n\nCompliance Workflow Scenarios")
    print("=" * 29)
    
    orchestrator = SimpleOrchestrator(use_llm=False)
    
    # Scenario: Complete customer onboarding workflow
    print("\n1. Complete Customer Onboarding Workflow:")
    
    # Step 1: Customer data validation
    customer_data = {
        "email": "newcustomer@example.com",
        "age": 30,
        "phone": "+1-555-0150",
        "full_name": "John Customer"
    }
    
    validation_result = orchestrator.validate("customer_onboarding", customer_data)
    print(f"   Step 1 - Data Validation: {'PASS' if validation_result['is_valid'] else 'FAIL'}")
    
    if validation_result['is_valid']:
        # Step 2: KYC verification
        kyc_data = {
            "identity_documents": [{"type": "passport", "expiry_date": "2025-06-30"}],
            "date_of_birth": "1993-04-12",
            "address_proof": {"type": "utility_bill", "date": "2024-01-15"}
        }
        
        kyc_result = orchestrator.validate_kyc(kyc_data)
        print(f"   Step 2 - KYC Verification: {kyc_result['kyc_status']}")
        
        if kyc_result['kyc_status'] == "APPROVED":
            # Step 3: Risk assessment for first transaction
            transaction_data = {
                "amount": 2500,
                "country": "US",
                "age": 30,
                "customer_tier": "standard"
            }
            
            risk_result = orchestrator.assess_risk(transaction_data)
            print(f"   Step 3 - Risk Assessment: {risk_result['risk_level']}")
            
            # Final decision
            if risk_result['risk_level'] in ["LOW", "MEDIUM"]:
                print("   Final Decision: CUSTOMER APPROVED FOR ONBOARDING")
            else:
                print("   Final Decision: REQUIRES MANUAL REVIEW")
        else:
            print("   Final Decision: KYC VERIFICATION FAILED")
    else:
        print("   Final Decision: DATA VALIDATION FAILED")

def regulatory_compliance_examples():
    """Regulatory compliance examples"""
    print("\n\nRegulatory Compliance Examples")
    print("=" * 30)
    
    orchestrator = SimpleOrchestrator(use_llm=False)
    
    # GDPR compliance check
    print("\n1. GDPR Compliance Check:")
    gdpr_data = {
        "email": "eu.customer@example.com",
        "age": 25,
        "region": "EU",
        "consent_given": True,
        "data_processing_consent": "2024-01-15"
    }
    
    # Search for GDPR requirements
    gdpr_info = orchestrator.search_knowledge("GDPR consent requirements")
    print(f"   GDPR Knowledge Found: {len(gdpr_info)} items")
    
    # Validate with context
    result = orchestrator.validate("customer_onboarding", gdpr_data)
    print(f"   GDPR Compliance: {'COMPLIANT' if result['is_valid'] else 'NON-COMPLIANT'}")
    
    # AML compliance check
    print("\n2. AML Compliance Check:")
    aml_transaction = {
        "amount": 12000,  # Above reporting threshold
        "country": "US",
        "transaction_type": "cash_deposit"
    }
    
    aml_info = orchestrator.search_knowledge("AML reporting threshold")
    print(f"   AML Knowledge Found: {len(aml_info)} items")
    
    risk_result = orchestrator.assess_risk(aml_transaction)
    print(f"   AML Risk Level: {risk_result['risk_level']}")
    print(f"   Reporting Required: {risk_result['requires_approval']}")

if __name__ == "__main__":
    customer_onboarding_scenarios()
    kyc_compliance_scenarios()
    risk_assessment_scenarios()
    compliance_workflow_scenarios()
    regulatory_compliance_examples()
    
    print("\nBusiness scenarios completed!")