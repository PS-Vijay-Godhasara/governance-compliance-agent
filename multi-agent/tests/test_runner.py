"""Multi-Agent Test Runner"""

import asyncio
import sys
import os
from typing import Dict, Any

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from orchestrator import MultiAgentOrchestrator
from rag_service import MultiAgentRAGService
from mcp_server import MultiAgentMCPServer

class MultiAgentTestRunner:
    def __init__(self):
        self.orchestrator = MultiAgentOrchestrator()
        self.rag_service = MultiAgentRAGService(use_database=False)  # Test without DB
        self.mcp_server = MultiAgentMCPServer(use_database=False)
        self.results = []
    
    async def run_orchestrator_tests(self):
        """Test multi-agent orchestrator"""
        print("🤖 Running Orchestrator Tests...")
        
        # Test 1: Validation workflow
        result = await self.orchestrator.execute_workflow("validation", {
            "policy_id": "customer_onboarding",
            "data": {"email": "test@example.com", "age": 25}
        })
        self._assert_test("Validation Workflow", result["status"] == "completed")
        
        # Test 2: KYC workflow
        result = await self.orchestrator.execute_workflow("kyc", {
            "customer_data": {"identity_documents": [{"type": "passport"}]}
        })
        self._assert_test("KYC Workflow", result["status"] == "completed")
    
    async def run_rag_tests(self):
        """Test RAG service"""
        print("\n🔍 Running RAG Tests...")
        
        # Test 1: Add knowledge
        await self.rag_service.add_knowledge("test_doc", "GDPR compliance requirements", {"topic": "regulations"})
        self._assert_test("Add Knowledge", True)
        
        # Test 2: Search knowledge
        results = await self.rag_service.search("GDPR compliance")
        self._assert_test("Search Knowledge", len(results) > 0)
        
        # Test 3: Get context
        context = await self.rag_service.get_context("customer_onboarding", "GDPR")
        self._assert_test("Get Context", "policy_id" in context)
    
    async def run_mcp_tests(self):
        """Test MCP server"""
        print("\n🔌 Running MCP Tests...")
        
        # Test 1: List tools
        tools = self.mcp_server.list_tools()
        self._assert_test("List Tools", len(tools) >= 8)
        
        # Test 2: Call tool
        result = await self.mcp_server.call_tool("validate_data_enhanced", {
            "policy_id": "customer_onboarding",
            "data": {"email": "test@example.com", "age": 25}
        })
        self._assert_test("Call Enhanced Tool", result["success"] == True)
        
        # Test 3: Multi-policy validation
        result = await self.mcp_server.call_tool("multi_policy_validation", {
            "policy_ids": ["customer_onboarding", "kyc_validation"],
            "data": {"email": "test@example.com", "age": 25}
        })
        self._assert_test("Multi-Policy Validation", result["success"] == True)
    
    async def run_workflow_tests(self):
        """Test complex workflows"""
        print("\n🔄 Running Workflow Tests...")
        
        # Test 1: Risk assessment workflow
        result = await self.orchestrator.execute_workflow("risk_assessment", {
            "transaction_data": {"amount": 15000, "country": "US"}
        })
        self._assert_test("Risk Assessment Workflow", result["status"] == "completed")
        
        # Test 2: System status
        status = self.orchestrator.get_system_status()
        self._assert_test("System Status", "orchestrator_running" in status)
    
    def _assert_test(self, test_name: str, condition: bool):
        """Assert test result"""
        status = "✅ PASS" if condition else "❌ FAIL"
        print(f"  {status} {test_name}")
        self.results.append({"test": test_name, "passed": condition})
    
    async def run_all_tests(self):
        """Run all test suites"""
        print("🚀 Multi-Agent Governance Test Suite")
        print("=" * 50)
        
        await self.orchestrator.start()
        
        await self.run_orchestrator_tests()
        await self.run_rag_tests()
        await self.run_mcp_tests()
        await self.run_workflow_tests()
        
        await self.orchestrator.stop()
        
        # Summary
        total = len(self.results)
        passed = sum(1 for r in self.results if r["passed"])
        
        print(f"\n📊 Test Summary:")
        print(f"Total Tests: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {total - passed} ❌")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        return passed == total

async def main():
    runner = MultiAgentTestRunner()
    success = await runner.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n⚠️ Some tests failed!")
        return 1

if __name__ == "__main__":
    exit(asyncio.run(main()))