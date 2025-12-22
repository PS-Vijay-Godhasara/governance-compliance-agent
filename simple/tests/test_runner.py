"""Simple Test Runner for Governance Agent"""

import sys
import os
import json
from typing import Dict, Any

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from orchestrator import SimpleOrchestrator

class SimpleTestRunner:
    def __init__(self):
        self.orchestrator = SimpleOrchestrator(use_llm=False)
        self.results = []
    
    def run_basic_tests(self):
        """Run basic validation tests"""
        print("🧪 Running Basic Tests...")
        
        # Test 1: Valid customer data
        result = self.orchestrator.validate("customer_onboarding", {
            "email": "test@example.com",
            "age": 25,
            "phone": "+1-555-0123"
        })
        self._assert_test("Valid Customer Data", result["is_valid"] == True)
        
        # Test 2: Invalid email
        result = self.orchestrator.validate("customer_onboarding", {
            "email": "invalid-email",
            "age": 25,
            "phone": "+1-555-0123"
        })
        self._assert_test("Invalid Email", result["is_valid"] == False)
        
        # Test 3: Age too young
        result = self.orchestrator.validate("customer_onboarding", {
            "email": "test@example.com",
            "age": 16,
            "phone": "+1-555-0123"
        })
        self._assert_test("Age Too Young", result["is_valid"] == False)
    
    def run_rag_tests(self):
        """Run RAG service tests"""
        print("\n🔍 Running RAG Tests...")
        
        # Test 1: Knowledge search
        results = self.orchestrator.search_knowledge("GDPR")
        self._assert_test("Knowledge Search", len(results) > 0)
        
        # Test 2: Context retrieval
        context = self.orchestrator.get_context("customer_onboarding")
        self._assert_test("Context Retrieval", "policy_id" in context)
    
    def run_mcp_tests(self):
        """Run MCP server tests"""
        print("\n🔌 Running MCP Tests...")
        
        # Test 1: List tools
        tools = self.orchestrator.list_mcp_tools()
        self._assert_test("List MCP Tools", len(tools) >= 5)
        
        # Test 2: Call tool
        result = self.orchestrator.call_mcp_tool("validate_data", {
            "policy_id": "customer_onboarding",
            "data": {"email": "test@example.com", "age": 25}
        })
        self._assert_test("Call MCP Tool", "result" in result)
    
    def run_kyc_tests(self):
        """Run KYC validation tests"""
        print("\n📋 Running KYC Tests...")
        
        # Test 1: Valid KYC
        result = self.orchestrator.validate_kyc({
            "identity_documents": [{"type": "passport", "expiry_date": "2025-12-31"}],
            "date_of_birth": "1990-05-15"
        })
        self._assert_test("Valid KYC", result["kyc_status"] in ["APPROVED", "REVIEW_REQUIRED"])
    
    def run_risk_tests(self):
        """Run risk assessment tests"""
        print("\n💰 Running Risk Tests...")
        
        # Test 1: High-value transaction
        result = self.orchestrator.assess_risk({
            "amount": 15000,
            "country": "US",
            "age": 25
        })
        self._assert_test("High-Value Risk", result["risk_level"] in ["MEDIUM", "HIGH"])
    
    def _assert_test(self, test_name: str, condition: bool):
        """Assert test result"""
        status = "✅ PASS" if condition else "❌ FAIL"
        print(f"  {status} {test_name}")
        self.results.append({"test": test_name, "passed": condition})
    
    def run_all_tests(self):
        """Run all test suites"""
        print("🚀 Simple Governance Agent Test Suite")
        print("=" * 50)
        
        self.run_basic_tests()
        self.run_rag_tests()
        self.run_mcp_tests()
        self.run_kyc_tests()
        self.run_risk_tests()
        
        # Summary
        total = len(self.results)
        passed = sum(1 for r in self.results if r["passed"])
        
        print(f"\n📊 Test Summary:")
        print(f"Total Tests: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {total - passed} ❌")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        return passed == total

def main():
    runner = SimpleTestRunner()
    success = runner.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n⚠️ Some tests failed!")
        return 1

if __name__ == "__main__":
    exit(main())