#!/usr/bin/env python3
"""
Test Runner for Governance Agent
Executes test prompts and verifies results automatically
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Any
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.simple_engine import SimpleGovernanceEngine
from core.simple_orchestrator import SimpleOrchestrator

class TestRunner:
    def __init__(self):
        self.engine = SimpleGovernanceEngine()
        self.orchestrator = SimpleOrchestrator(self.engine)
        self.results = []
        
    def run_test(self, test_name: str, test_func, expected: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single test and compare with expected results"""
        print(f"Running {test_name}...")
        
        start_time = time.time()
        try:
            result = test_func()
            execution_time = time.time() - start_time
            
            # Compare with expected results
            passed = self._compare_results(result, expected)
            
            test_result = {
                "test_name": test_name,
                "passed": passed,
                "execution_time_ms": round(execution_time * 1000, 2),
                "result": result,
                "expected": expected,
                "timestamp": datetime.now().isoformat()
            }
            
            self.results.append(test_result)
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{status} {test_name} ({execution_time*1000:.1f}ms)")
            
            return test_result
            
        except Exception as e:
            test_result = {
                "test_name": test_name,
                "passed": False,
                "error": str(e),
                "execution_time_ms": round((time.time() - start_time) * 1000, 2),
                "timestamp": datetime.now().isoformat()
            }
            self.results.append(test_result)
            print(f"❌ ERROR {test_name}: {e}")
            return test_result
    
    def _compare_results(self, actual: Dict, expected: Dict) -> bool:
        """Compare actual results with expected results"""
        for key, expected_value in expected.items():
            if key not in actual:
                return False
            
            actual_value = actual[key]
            
            # Handle different comparison types
            if isinstance(expected_value, bool):
                if actual_value != expected_value:
                    return False
            elif isinstance(expected_value, str):
                if expected_value.startswith("contains:"):
                    search_term = expected_value.replace("contains:", "").strip()
                    if search_term.lower() not in str(actual_value).lower():
                        return False
                elif actual_value != expected_value:
                    return False
            elif isinstance(expected_value, (int, float)):
                if abs(actual_value - expected_value) > 0.01:
                    return False
            elif isinstance(expected_value, list):
                if len(actual_value) != len(expected_value):
                    return False
        
        return True
    
    def run_basic_tests(self):
        """Run basic validation tests"""
        print("\n🧪 Running Basic Validation Tests...")
        
        # Test 1: Valid Customer Data
        def test_valid_customer():
            customer_data = {
                "email": "john.doe@example.com",
                "phone": "+1-555-0123",
                "age": 25,
                "kyc_uploaded": "2024-01-15"
            }
            return self.orchestrator.validate("customer_onboarding", customer_data)
        
        self.run_test(
            "Test 1: Valid Customer Data",
            test_valid_customer,
            {"is_valid": True, "score": 1.0}
        )
        
        # Test 2: Invalid Email Format
        def test_invalid_email():
            customer_data = {
                "email": "invalid-email",
                "phone": "+1-555-0123",
                "age": 25,
                "kyc_uploaded": "2024-01-15"
            }
            return self.orchestrator.validate("customer_onboarding", customer_data)
        
        self.run_test(
            "Test 2: Invalid Email Format",
            test_invalid_email,
            {"is_valid": False}
        )
        
        # Test 3: Age Boundary Testing
        def test_age_boundaries():
            # Test minimum age
            customer_data = {"email": "test@example.com", "age": 17}
            result1 = self.orchestrator.validate("customer_onboarding", customer_data)
            
            # Test maximum age  
            customer_data = {"email": "test@example.com", "age": 121}
            result2 = self.orchestrator.validate("customer_onboarding", customer_data)
            
            return {
                "min_age_valid": result1["is_valid"],
                "max_age_valid": result2["is_valid"]
            }
        
        self.run_test(
            "Test 3: Age Boundary Testing",
            test_age_boundaries,
            {"min_age_valid": False, "max_age_valid": False}
        )
    
    def run_kyc_tests(self):
        """Run KYC validation tests"""
        print("\n🔍 Running KYC Validation Tests...")
        
        # Test 4: Valid KYC Documents
        def test_valid_kyc():
            kyc_data = {
                "identity_documents": [
                    {"type": "passport", "expiry_date": "2025-12-31"},
                    {"type": "driver_license", "expiry_date": "2024-06-15"}
                ],
                "date_of_birth": "1990-05-15",
                "address_proof": {"type": "utility_bill", "date": "2024-01-10"}
            }
            return self.orchestrator.perform_kyc_validation(kyc_data)
        
        self.run_test(
            "Test 4: Valid KYC Documents",
            test_valid_kyc,
            {"kyc_status": "APPROVED", "risk_level": "LOW"}
        )
        
        # Test 5: Expired Documents
        def test_expired_documents():
            kyc_data = {
                "identity_documents": [
                    {"type": "passport", "expiry_date": "2023-12-31"}
                ],
                "date_of_birth": "1990-05-15"
            }
            return self.orchestrator.perform_kyc_validation(kyc_data)
        
        self.run_test(
            "Test 5: Expired Documents",
            test_expired_documents,
            {"kyc_status": "REJECTED"}
        )
    
    def run_risk_tests(self):
        """Run risk assessment tests"""
        print("\n💰 Running Risk Assessment Tests...")
        
        # Test 6: High-Value Transaction
        def test_high_value_transaction():
            transaction_data = {
                "amount": 15000,
                "currency": "USD",
                "country": "US",
                "customer_tier": "premium"
            }
            return self.orchestrator.assess_risk(transaction_data)
        
        self.run_test(
            "Test 6: High-Value Transaction",
            test_high_value_transaction,
            {"requires_approval": True}
        )
        
        # Test 7: Low-Risk Transaction
        def test_low_risk_transaction():
            transaction_data = {
                "amount": 500,
                "currency": "USD",
                "country": "US",
                "customer_tier": "standard"
            }
            return self.orchestrator.assess_risk(transaction_data)
        
        self.run_test(
            "Test 7: Low-Risk Transaction",
            test_low_risk_transaction,
            {"risk_level": "LOW", "requires_approval": False}
        )
    
    def run_error_handling_tests(self):
        """Run error handling tests"""
        print("\n🚨 Running Error Handling Tests...")
        
        # Test 11: Missing Required Fields
        def test_missing_fields():
            incomplete_data = {
                "email": "test@example.com"
                # Missing required fields: phone, age
            }
            return self.orchestrator.validate("customer_onboarding", incomplete_data)
        
        self.run_test(
            "Test 11: Missing Required Fields",
            test_missing_fields,
            {"is_valid": False}
        )
        
        # Test 12: Invalid Data Types
        def test_invalid_types():
            invalid_data = {
                "email": "test@example.com",
                "age": "twenty-five",  # String instead of integer
                "phone": 5550123       # Integer instead of string
            }
            return self.orchestrator.validate("customer_onboarding", invalid_data)
        
        self.run_test(
            "Test 12: Invalid Data Types",
            test_invalid_types,
            {"is_valid": False}
        )
    
    def run_performance_tests(self):
        """Run performance tests"""
        print("\n📊 Running Performance Tests...")
        
        # Test 15: Bulk Validation
        def test_bulk_validation():
            customers = [
                {"email": f"user{i}@example.com", "age": 20+i, "phone": f"+1-555-{i:04d}"} 
                for i in range(100)  # Reduced from 1000 for faster testing
            ]
            
            start_time = time.time()
            results = []
            for customer in customers:
                result = self.orchestrator.validate("customer_onboarding", customer)
                results.append(result)
            
            processing_time = time.time() - start_time
            
            return {
                "records_processed": len(results),
                "processing_time_seconds": processing_time,
                "records_per_second": len(results) / processing_time
            }
        
        self.run_test(
            "Test 15: Bulk Validation",
            test_bulk_validation,
            {"records_processed": 100}
        )
    
    def generate_report(self):
        """Generate test report"""
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r["passed"])
        failed_tests = total_tests - passed_tests
        
        avg_execution_time = sum(r["execution_time_ms"] for r in self.results) / total_tests
        
        report = {
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "success_rate": round((passed_tests / total_tests) * 100, 1),
                "average_execution_time_ms": round(avg_execution_time, 2)
            },
            "results": self.results,
            "generated_at": datetime.now().isoformat()
        }
        
        # Save report
        with open("test_results.json", "w") as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print(f"\n📋 Test Summary:")
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {report['summary']['success_rate']}%")
        print(f"Average Execution Time: {avg_execution_time:.1f}ms")
        print(f"\nDetailed report saved to: test_results.json")
        
        return report

def main():
    """Main test runner"""
    runner = TestRunner()
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        suite = sys.argv[1].replace("--suite=", "")
        
        if suite == "basic":
            runner.run_basic_tests()
        elif suite == "kyc":
            runner.run_kyc_tests()
        elif suite == "risk":
            runner.run_risk_tests()
        elif suite == "error":
            runner.run_error_handling_tests()
        elif suite == "performance":
            runner.run_performance_tests()
        elif suite == "all":
            runner.run_basic_tests()
            runner.run_kyc_tests()
            runner.run_risk_tests()
            runner.run_error_handling_tests()
            runner.run_performance_tests()
        else:
            print(f"Unknown test suite: {suite}")
            return
    else:
        # Run all tests by default
        runner.run_basic_tests()
        runner.run_kyc_tests()
        runner.run_risk_tests()
        runner.run_error_handling_tests()
        runner.run_performance_tests()
    
    # Generate report
    runner.generate_report()

if __name__ == "__main__":
    main()