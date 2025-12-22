"""Interactive Test Script for Simple Governance Agent"""

import sys
import os
import json

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from orchestrator import SimpleOrchestrator

class InteractiveTestRunner:
    def __init__(self):
        self.orchestrator = SimpleOrchestrator(use_llm=False)
        
    def display_menu(self):
        """Display test menu"""
        print("\n" + "="*50)
        print("🤖 Simple Governance Agent Interactive Tests")
        print("="*50)
        print("1. Basic Validation Tests")
        print("2. RAG Knowledge Tests") 
        print("3. MCP Tool Tests")
        print("4. KYC Validation Tests")
        print("5. Risk Assessment Tests")
        print("6. Custom Data Test")
        print("7. Run All Quick Tests")
        print("0. Exit")
        print("-"*50)
        
    def test_basic_validation(self):
        """Test basic validation scenarios"""
        print("\n🧪 Basic Validation Tests")
        print("-"*30)
        
        test_cases = [
            {
                "name": "Valid Customer",
                "data": {"email": "john@example.com", "age": 25, "phone": "+1-555-0123"}
            },
            {
                "name": "Invalid Email",
                "data": {"email": "invalid-email", "age": 25}
            },
            {
                "name": "Age Too Young",
                "data": {"email": "young@example.com", "age": 16}
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{i}. Testing: {test_case['name']}")
            result = self.orchestrator.validate("customer_onboarding", test_case['data'])
            print(f"   Result: {'✅ VALID' if result['is_valid'] else '❌ INVALID'}")
            print(f"   Score: {result['score']}")
            if result['violations']:
                print(f"   Issues: {result['violations']}")
                
        input("\nPress Enter to continue...")
    
    def test_rag_knowledge(self):
        """Test RAG knowledge search"""
        print("\n🔍 RAG Knowledge Tests")
        print("-"*30)
        
        queries = ["GDPR", "KYC requirements", "compliance"]
        
        for query in queries:
            print(f"\nSearching for: '{query}'")
            results = self.orchestrator.search_knowledge(query)
            print(f"Found {len(results)} results:")
            for result in results[:2]:
                print(f"  - Topic: {result.get('topic', 'N/A')}")
                print(f"    Relevance: {result.get('relevance', 0):.2f}")
        
        input("\nPress Enter to continue...")
    
    def test_mcp_tools(self):
        """Test MCP tool execution"""
        print("\n🔌 MCP Tool Tests")
        print("-"*30)
        
        # List available tools
        tools = self.orchestrator.list_mcp_tools()
        print(f"Available tools: {len(tools)}")
        for tool in tools[:3]:
            print(f"  - {tool['name']}: {tool['description']}")
        
        # Test tool execution
        print("\nTesting validate_data tool:")
        result = self.orchestrator.call_mcp_tool("validate_data", {
            "policy_id": "customer_onboarding",
            "data": {"email": "test@example.com", "age": 25}
        })
        print(f"Tool result: {result.get('result', {}).get('is_valid', 'N/A')}")
        
        input("\nPress Enter to continue...")
    
    def test_custom_data(self):
        """Allow user to input custom test data"""
        print("\n🎯 Custom Data Test")
        print("-"*30)
        
        print("Enter test data as JSON (or press Enter for sample):")
        user_input = input().strip()
        
        if not user_input:
            test_data = {"email": "custom@example.com", "age": 30, "phone": "+1-555-9999"}
        else:
            try:
                test_data = json.loads(user_input)
            except json.JSONDecodeError:
                print("Invalid JSON. Using sample data.")
                test_data = {"email": "test@example.com", "age": 25}
        
        print(f"\nTesting with: {json.dumps(test_data, indent=2)}")
        
        result = self.orchestrator.validate("customer_onboarding", test_data)
        print(f"Valid: {result['is_valid']}")
        print(f"Score: {result['score']}")
        if result['violations']:
            print(f"Issues: {result['violations']}")
            
        input("\nPress Enter to continue...")
    
    def run_quick_tests(self):
        """Run all quick tests"""
        print("\n🚀 Running All Quick Tests")
        print("-"*30)
        
        tests = [
            ("Valid Customer", {"email": "test@example.com", "age": 25}),
            ("Invalid Email", {"email": "invalid", "age": 25}),
            ("RAG Search", "GDPR"),
            ("MCP Tool", "validate_data")
        ]
        
        for name, test_input in tests:
            print(f"\n• {name}:")
            
            if name == "RAG Search":
                results = self.orchestrator.search_knowledge(test_input)
                print(f"  Found: {len(results)} results")
            elif name == "MCP Tool":
                result = self.orchestrator.call_mcp_tool(test_input, {
                    "policy_id": "customer_onboarding",
                    "data": {"email": "test@example.com", "age": 25}
                })
                print(f"  Success: {result.get('success', False)}")
            else:
                result = self.orchestrator.validate("customer_onboarding", test_input)
                print(f"  Valid: {result['is_valid']}")
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main interactive loop"""
        while True:
            self.display_menu()
            choice = input("Select option (0-7): ").strip()
            
            if choice == "0":
                print("\n👋 Goodbye!")
                break
            elif choice == "1":
                self.test_basic_validation()
            elif choice == "2":
                self.test_rag_knowledge()
            elif choice == "3":
                self.test_mcp_tools()
            elif choice == "4":
                print("\n📋 KYC test - using basic validation for demo")
                self.test_basic_validation()
            elif choice == "5":
                print("\n💰 Risk test - using basic validation for demo")
                self.test_basic_validation()
            elif choice == "6":
                self.test_custom_data()
            elif choice == "7":
                self.run_quick_tests()
            else:
                print("❌ Invalid choice. Please try again.")

def main():
    try:
        runner = InteractiveTestRunner()
        runner.run()
    except KeyboardInterrupt:
        print("\n\n👋 Test session interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()