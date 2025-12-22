#!/usr/bin/env python3
"""
Interactive Test Script for Governance Agent
Provides interactive prompts to test different scenarios
"""

import sys
import os
import json
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.simple_engine import SimpleGovernanceEngine
from core.simple_orchestrator import SimpleOrchestrator

class InteractiveTestRunner:
    def __init__(self):
        self.engine = SimpleGovernanceEngine()
        self.orchestrator = SimpleOrchestrator(self.engine)
        
    def display_menu(self):
        """Display test menu"""
        print("\n" + "="*50)
        print("🤖 Governance Agent Interactive Test Suite")
        print("="*50)
        print("1. Basic Validation Tests")
        print("2. KYC Validation Tests") 
        print("3. Risk Assessment Tests")
        print("4. Error Handling Tests")
        print("5. Custom Data Test")
        print("6. Run All Quick Tests")
        print("0. Exit")
        print("-"*50)
        
    def test_basic_validation(self):
        """Test basic validation scenarios"""
        print("\n🧪 Basic Validation Tests")
        print("-"*30)
        
        test_cases = [
            {
                "name": "Valid Customer",
                "data": {
                    "email": "john.doe@example.com",
                    "phone": "+1-555-0123",
                    "age": 25,
                    "kyc_uploaded": "2024-01-15"
                }
            },
            {
                "name": "Invalid Email",
                "data": {
                    "email": "invalid-email",
                    "phone": "+1-555-0123",
                    "age": 25
                }
            },
            {
                "name": "Age Too Young",
                "data": {
                    "email": "young@example.com",
                    "age": 16
                }
            },
            {
                "name": "Missing Required Fields",
                "data": {
                    "email": "incomplete@example.com"
                }
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{i}. Testing: {test_case['name']}")
            print(f"   Data: {json.dumps(test_case['data'], indent=2)}")
            
            result = self.orchestrator.validate("customer_onboarding", test_case['data'])
            
            print(f"   Result: {'✅ VALID' if result['is_valid'] else '❌ INVALID'}")
            print(f"   Score: {result['score']}")
            
            if result['violations']:
                print(f"   Violations: {result['violations']}")
            if result['explanations']:
                print(f"   Explanations: {result['explanations']}")
                
        input("\nPress Enter to continue...")
    
    def test_kyc_validation(self):
        """Test KYC validation scenarios"""
        print("\n🔍 KYC Validation Tests")
        print("-"*30)
        
        test_cases = [
            {
                "name": "Valid KYC Documents",
                "data": {
                    "identity_documents": [
                        {"type": "passport", "expiry_date": "2025-12-31"},
                        {"type": "driver_license", "expiry_date": "2024-06-15"}
                    ],
                    "date_of_birth": "1990-05-15",
                    "address_proof": {"type": "utility_bill", "date": "2024-01-10"}
                }
            },
            {
                "name": "Expired Documents",
                "data": {
                    "identity_documents": [
                        {"type": "passport", "expiry_date": "2023-12-31"}
                    ],
                    "date_of_birth": "1990-05-15"
                }
            },
            {
                "name": "Missing Documents",
                "data": {
                    "date_of_birth": "1990-05-15"
                }
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{i}. Testing: {test_case['name']}")
            print(f"   Data: {json.dumps(test_case['data'], indent=2)}")
            
            result = self.orchestrator.perform_kyc_validation(test_case['data'])
            
            print(f"   KYC Status: {result['kyc_status']}")
            print(f"   Risk Level: {result['risk_level']}")
            
            if result['violations']:
                print(f"   Violations: {result['violations']}")
                
        input("\nPress Enter to continue...")
    
    def test_risk_assessment(self):
        """Test risk assessment scenarios"""
        print("\n💰 Risk Assessment Tests")
        print("-"*30)
        
        test_cases = [
            {
                "name": "High-Value Transaction",
                "data": {
                    "amount": 15000,
                    "currency": "USD",
                    "country": "US",
                    "customer_tier": "premium"
                }
            },
            {
                "name": "Low-Risk Transaction",
                "data": {
                    "amount": 500,
                    "currency": "USD",
                    "country": "US",
                    "customer_tier": "standard"
                }
            },
            {
                "name": "High-Risk Country",
                "data": {
                    "amount": 5000,
                    "currency": "USD",
                    "country": "XX",  # High-risk country
                    "customer_tier": "standard"
                }
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{i}. Testing: {test_case['name']}")
            print(f"   Data: {json.dumps(test_case['data'], indent=2)}")
            
            result = self.orchestrator.assess_risk(test_case['data'])
            
            print(f"   Risk Level: {result['risk_level']}")
            print(f"   Risk Score: {result['risk_score']}")
            print(f"   Requires Approval: {result['requires_approval']}")
            
            if result['risk_factors']:
                print(f"   Risk Factors: {result['risk_factors']}")
                
        input("\nPress Enter to continue...")
    
    def test_error_handling(self):
        """Test error handling scenarios"""
        print("\n🚨 Error Handling Tests")
        print("-"*30)
        
        test_cases = [
            {
                "name": "Invalid Policy ID",
                "policy_id": "non_existent_policy",
                "data": {"email": "test@example.com"}
            },
            {
                "name": "Empty Data",
                "policy_id": "customer_onboarding",
                "data": {}
            },
            {
                "name": "Invalid Data Types",
                "policy_id": "customer_onboarding",
                "data": {
                    "email": "test@example.com",
                    "age": "twenty-five",  # String instead of integer
                    "phone": 5550123       # Integer instead of string
                }
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{i}. Testing: {test_case['name']}")
            print(f"   Policy: {test_case['policy_id']}")
            print(f"   Data: {json.dumps(test_case['data'], indent=2)}")
            
            try:
                result = self.orchestrator.validate(test_case['policy_id'], test_case['data'])
                print(f"   Result: {'✅ VALID' if result['is_valid'] else '❌ INVALID'}")
                if result['violations']:
                    print(f"   Violations: {result['violations']}")
            except Exception as e:
                print(f"   Error: {str(e)}")
                
        input("\nPress Enter to continue...")
    
    def test_custom_data(self):
        """Allow user to input custom test data"""
        print("\n🎯 Custom Data Test")
        print("-"*30)
        
        print("Available policies:")
        print("1. customer_onboarding")
        print("2. kyc_validation")
        
        policy_choice = input("\nSelect policy (1 or 2): ").strip()
        policy_map = {"1": "customer_onboarding", "2": "kyc_validation"}
        policy_id = policy_map.get(policy_choice, "customer_onboarding")
        
        print(f"\nSelected policy: {policy_id}")
        print("Enter test data as JSON (or press Enter for sample):")
        
        user_input = input().strip()
        
        if not user_input:
            # Provide sample data
            if policy_id == "customer_onboarding":
                test_data = {
                    "email": "custom@example.com",
                    "age": 30,
                    "phone": "+1-555-9999"
                }
            else:
                test_data = {
                    "identity_documents": [{"type": "passport", "expiry_date": "2025-12-31"}],
                    "date_of_birth": "1985-03-20"
                }
        else:
            try:
                test_data = json.loads(user_input)
            except json.JSONDecodeError:
                print("Invalid JSON format. Using sample data.")
                test_data = {"email": "test@example.com", "age": 25}
        
        print(f"\nTesting with data: {json.dumps(test_data, indent=2)}")
        
        if policy_id == "kyc_validation":
            result = self.orchestrator.perform_kyc_validation(test_data)
            print(f"KYC Status: {result['kyc_status']}")
            print(f"Risk Level: {result['risk_level']}")
        else:
            result = self.orchestrator.validate(policy_id, test_data)
            print(f"Valid: {result['is_valid']}")
            print(f"Score: {result['score']}")
        
        if result.get('violations'):
            print(f"Violations: {result['violations']}")
        if result.get('explanations'):
            print(f"Explanations: {result['explanations']}")
            
        input("\nPress Enter to continue...")
    
    def run_quick_tests(self):
        """Run all quick tests"""
        print("\n🚀 Running All Quick Tests")
        print("-"*30)
        
        tests = [
            ("Valid Customer", "customer_onboarding", {"email": "test@example.com", "age": 25}),
            ("Invalid Email", "customer_onboarding", {"email": "invalid", "age": 25}),
            ("Valid KYC", "kyc", {"identity_documents": [{"type": "passport", "expiry_date": "2025-12-31"}]}),
            ("High Risk", "risk", {"amount": 20000, "country": "US"})
        ]
        
        for name, test_type, data in tests:
            print(f"\n• {name}:")
            
            if test_type == "kyc":
                result = self.orchestrator.perform_kyc_validation(data)
                print(f"  Status: {result['kyc_status']}")
            elif test_type == "risk":
                result = self.orchestrator.assess_risk(data)
                print(f"  Risk: {result['risk_level']}")
            else:
                result = self.orchestrator.validate(test_type, data)
                print(f"  Valid: {result['is_valid']}")
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main interactive loop"""
        while True:
            self.display_menu()
            choice = input("Select option (0-6): ").strip()
            
            if choice == "0":
                print("\n👋 Goodbye!")
                break
            elif choice == "1":
                self.test_basic_validation()
            elif choice == "2":
                self.test_kyc_validation()
            elif choice == "3":
                self.test_risk_assessment()
            elif choice == "4":
                self.test_error_handling()
            elif choice == "5":
                self.test_custom_data()
            elif choice == "6":
                self.run_quick_tests()
            else:
                print("❌ Invalid choice. Please try again.")

def main():
    """Main function"""
    try:
        runner = InteractiveTestRunner()
        runner.run()
    except KeyboardInterrupt:
        print("\n\n👋 Test session interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()