"""Basic Usage Examples for Simple Governance Agent"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from orchestrator import SimpleOrchestrator

def basic_validation_examples():
    """Basic validation examples"""
    print("Basic Validation Examples")
    print("=" * 30)
    
    orchestrator = SimpleOrchestrator(use_llm=False)
    
    # Example 1: Valid customer
    print("\n1. Valid Customer:")
    result = orchestrator.validate("customer_onboarding", {
        "email": "john@example.com",
        "age": 25,
        "phone": "+1-555-0123"
    })
    print(f"   Valid: {result['is_valid']}")
    print(f"   Score: {result['score']}")
    
    # Example 2: Invalid customer
    print("\n2. Invalid Customer:")
    result = orchestrator.validate("customer_onboarding", {
        "email": "invalid-email",
        "age": 16
    })
    print(f"   Valid: {result['is_valid']}")
    print(f"   Violations: {result['violations']}")
    
    # Example 3: KYC validation
    print("\n3. KYC Validation:")
    kyc_result = orchestrator.validate_kyc({
        "identity_documents": [{"type": "passport", "expiry_date": "2025-12-31"}],
        "date_of_birth": "1990-05-15"
    })
    print(f"   Status: {kyc_result['kyc_status']}")
    print(f"   Risk: {kyc_result['risk_level']}")
    
    # Example 4: Risk assessment
    print("\n4. Risk Assessment:")
    risk = orchestrator.assess_risk({
        "amount": 15000,
        "country": "US",
        "age": 22
    })
    print(f"   Risk Level: {risk['risk_level']}")
    print(f"   Approval Required: {risk['requires_approval']}")

def rag_examples():
    """RAG service examples"""
    print("\n\nRAG Service Examples")
    print("=" * 20)
    
    orchestrator = SimpleOrchestrator(use_llm=False)
    
    # Search knowledge
    print("\n1. Knowledge Search:")
    results = orchestrator.search_knowledge("GDPR compliance")
    print(f"   Found {len(results)} results")
    for result in results[:2]:
        print(f"   - {result.get('topic', 'N/A')}: {result.get('relevance', 0):.2f}")
    
    # Get context
    print("\n2. Policy Context:")
    context = orchestrator.get_context("customer_onboarding")
    print(f"   Policy: {context['policy_id']}")
    print(f"   Related info: {len(context['related_info'])} items")

def mcp_examples():
    """MCP tool examples"""
    print("\n\nMCP Tool Examples")
    print("=" * 17)
    
    orchestrator = SimpleOrchestrator(use_llm=False)
    
    # List tools
    print("\n1. Available Tools:")
    tools = orchestrator.list_mcp_tools()
    for tool in tools[:3]:
        print(f"   - {tool['name']}: {tool['description']}")
    
    # Call tool
    print("\n2. Tool Execution:")
    result = orchestrator.call_mcp_tool("validate_data", {
        "policy_id": "customer_onboarding",
        "data": {"email": "test@example.com", "age": 25}
    })
    print(f"   Success: {result.get('success', False)}")
    print(f"   Result: {result.get('result', {}).get('is_valid', 'N/A')}")

if __name__ == "__main__":
    basic_validation_examples()
    rag_examples()
    mcp_examples()
    print("\nBasic examples completed!")