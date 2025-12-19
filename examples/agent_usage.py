"""Example usage of the agent-based governance system"""

import asyncio
import json
from src.core.engine import GovernanceEngine
from src.agents.orchestrator import AgentOrchestrator
from src.mcp.mcp_server import MCPServer


async def demo_policy_management():
    """Demonstrate policy management capabilities"""
    print("=== Policy Management Demo ===")
    
    # Initialize system
    engine = GovernanceEngine()
    orchestrator = AgentOrchestrator(engine)
    await orchestrator.start_agents()
    
    # Register a policy
    policy_text = """
    Customer onboarding policy:
    1. All customers must provide a valid email address
    2. Customers must be at least 18 years old
    3. Phone number with country code is required
    4. Identity documents must be uploaded within 30 days
    5. High-value customers (>$50,000) require additional verification
    """
    
    policy_id = await orchestrator.register_policy(
        name="Customer Onboarding Policy",
        content=policy_text,
        metadata={"version": "1.0", "jurisdiction": "US"}
    )
    
    print(f"Policy registered with ID: {policy_id}")
    
    # Retrieve policy
    policy = await orchestrator.get_policy(policy_id)
    print(f"Retrieved policy: {policy.get('name', 'Unknown')}")
    
    return orchestrator, policy_id


async def demo_data_validation():
    """Demonstrate data validation capabilities"""
    print("\n=== Data Validation Demo ===")
    
    orchestrator, policy_id = await demo_policy_management()
    
    # Test data - valid customer
    valid_customer = {
        "email": "john.doe@example.com",
        "age": 25,
        "phone": "+1-555-0123",
        "identity_documents": ["passport", "driver_license"],
        "account_value": 75000
    }
    
    # Validate valid customer
    result = await orchestrator.validate(policy_id, valid_customer)
    print(f"Valid customer validation: {result['data']['is_valid']}")
    print(f"Validation score: {result['data']['score']:.2f}")
    
    # Test data - invalid customer
    invalid_customer = {
        "email": "invalid-email",
        "age": 16,  # Too young
        "phone": "555-0123",  # Missing country code
        # Missing identity_documents
        "account_value": 75000
    }
    
    # Validate invalid customer
    result = await orchestrator.validate(policy_id, invalid_customer)
    print(f"\nInvalid customer validation: {result['data']['is_valid']}")
    print(f"Validation score: {result['data']['score']:.2f}")
    print(f"Violations found: {len(result['data']['violations'])}")
    
    # Print explanations if available
    if 'explanations' in result['data']:
        print("\nExplanations:")
        for explanation in result['data']['explanations']:
            print(f"- {explanation['field']}: {explanation['explanation'][:100]}...")
    
    return orchestrator


async def demo_kyc_validation():
    """Demonstrate KYC validation capabilities"""
    print("\n=== KYC Validation Demo ===")
    
    orchestrator = await demo_data_validation()
    
    # KYC test data
    kyc_data = {
        "customer_id": "CUST_001",
        "full_name": "John Doe",
        "date_of_birth": "1990-05-15",
        "identity_documents": [
            {"type": "passport", "number": "P123456789", "expiry_date": "2025-12-31"},
            {"type": "driver_license", "number": "DL987654321", "expiry_date": "2024-08-15"}
        ],
        "address_proof": {
            "type": "utility_bill",
            "date": "2024-01-01"
        },
        "phone": "+1-555-0123",
        "email": "john.doe@example.com"
    }
    
    # Perform KYC validation
    kyc_result = await orchestrator.perform_kyc_validation(kyc_data)
    print(f"KYC Status: {kyc_result['kyc_status']}")
    print(f"KYC Score: {kyc_result['kyc_score']:.2f}")
    print(f"Issues found: {len(kyc_result['issues'])}")
    
    if kyc_result['issues']:
        print("\nKYC Issues:")
        for issue in kyc_result['issues']:
            print(f"- {issue['type']}: {issue['message']}")
    
    return orchestrator


async def demo_risk_assessment():
    """Demonstrate risk assessment capabilities"""
    print("\n=== Risk Assessment Demo ===")
    
    orchestrator = await demo_kyc_validation()
    
    # Risk assessment data
    risk_data = {
        "transaction_amount": 15000,
        "country": "US",
        "customer_id": "CUST_001",
        "transaction_type": "wire_transfer",
        "beneficiary_country": "CH"
    }
    
    risk_context = {
        "customer_history": {
            "previous_violations": 0,
            "account_age_months": 24,
            "average_transaction": 5000
        }
    }
    
    # Perform risk assessment
    risk_result = await orchestrator.assess_risk(risk_data, risk_context)
    print(f"Risk Level: {risk_result['risk_level']}")
    print(f"Risk Score: {risk_result['risk_score']:.2f}")
    print(f"Risk Factors: {len(risk_result['risk_factors'])}")
    
    if 'explanation' in risk_result:
        print(f"\nRisk Explanation: {risk_result['explanation']['explanation'][:200]}...")
    
    return orchestrator


async def demo_schema_drift():
    """Demonstrate schema drift detection"""
    print("\n=== Schema Drift Detection Demo ===")
    
    orchestrator = await demo_risk_assessment()
    
    # Old schema
    old_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "email": {"type": "string"},
            "age": {"type": "integer"}
        },
        "required": ["name", "email"]
    }
    
    # New schema with changes
    new_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "email": {"type": "string"},
            "age": {"type": "integer"},
            "phone": {"type": "string"},  # New field
            "middle_name": {"type": "string"}  # New optional field
        },
        "required": ["name", "email", "phone"]  # Phone now required
    }
    
    # Detect schema drift
    drift_result = await orchestrator.detect_schema_drift(old_schema, new_schema)
    print(f"Schema changes detected: {drift_result['total_changes']}")
    print(f"Risk level: {drift_result['risk_level']}")
    print(f"Compatibility: {drift_result['compatibility']}")
    
    print("\nChanges:")
    for change in drift_result['changes']:
        print(f"- {change['type']}: {change['description']}")
        print(f"  Impact: {change['impact']}")
        print(f"  Strategy: {change['migration_strategy']}")
    
    return orchestrator


async def demo_knowledge_search():
    """Demonstrate knowledge search capabilities"""
    print("\n=== Knowledge Search Demo ===")
    
    orchestrator = await demo_schema_drift()
    
    # Search for policy information
    search_queries = [
        "customer age requirements",
        "identity document validation",
        "high value customer verification",
        "email validation rules"
    ]
    
    for query in search_queries:
        print(f"\nSearching for: '{query}'")
        search_result = await orchestrator.search_knowledge(query, "policy", 3)
        
        if search_result['context']:
            print(f"Found {len(search_result['context'])} relevant results:")
            for i, result in enumerate(search_result['context'][:2], 1):
                print(f"  {i}. Score: {result['score']:.2f}")
                print(f"     Content: {result['content'][:100]}...")
        else:
            print("No relevant results found")
    
    return orchestrator


async def demo_mcp_server():
    """Demonstrate MCP server capabilities"""
    print("\n=== MCP Server Demo ===")
    
    # Initialize MCP server
    mcp_server = MCPServer()
    
    # Test policy parsing through MCP
    policy_response = await mcp_server.call_tool("parse_policy", {
        "policy_text": "All users must be over 21 and provide valid ID",
        "policy_id": "age_verification_policy"
    })
    
    print(f"MCP Policy Parsing: {policy_response.success}")
    if policy_response.success:
        print(f"Parsed rules: {len(policy_response.data.get('parsed_rules', {}).get('rules', []))}")
    
    # Test knowledge storage through MCP
    knowledge_response = await mcp_server.call_tool("store_knowledge", {
        "content": "GDPR Article 6 requires lawful basis for processing personal data",
        "type": "regulation",
        "id": "gdpr_article_6",
        "metadata": {"regulation": "GDPR", "article": "6"}
    })
    
    print(f"MCP Knowledge Storage: {knowledge_response.success}")
    
    # Test data validation through MCP
    validation_response = await mcp_server.call_tool("validate_data", {
        "data": {"email": "test@example.com", "age": 25},
        "rules": {
            "rules": [
                {"field": "email", "type": "email", "required": True},
                {"field": "age", "type": "integer", "required": True, "constraints": {"min": 18}}
            ]
        }
    })
    
    print(f"MCP Data Validation: {validation_response.success}")
    if validation_response.success:
        print(f"Validation result: {validation_response.data['is_valid']}")
    
    # Get available tools
    tools_schema = mcp_server.get_tools_schema()
    print(f"\nAvailable MCP tools: {len(tools_schema)}")
    for tool in tools_schema[:3]:  # Show first 3 tools
        print(f"- {tool['name']}: {tool['description']}")
    
    await mcp_server.shutdown()


async def main():
    """Run all demos"""
    print("🤖 Governance & Compliance Agent Demo")
    print("=" * 50)
    
    try:
        # Run all demos in sequence
        await demo_policy_management()
        await demo_data_validation()
        await demo_kyc_validation()
        await demo_risk_assessment()
        await demo_schema_drift()
        await demo_knowledge_search()
        await demo_mcp_server()
        
        print("\n✅ All demos completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())