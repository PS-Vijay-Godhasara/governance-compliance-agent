"""Multi-Agent Workflow Examples"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from orchestrator import MultiAgentOrchestrator

async def basic_multi_agent_workflow():
    """Basic multi-agent workflow example"""
    print("Multi-Agent Workflow Examples")
    print("=" * 30)
    
    orchestrator = MultiAgentOrchestrator()
    await orchestrator.start()
    
    try:
        # Example 1: Validation workflow
        print("\n1. Multi-Agent Validation Workflow:")
        result = await orchestrator.execute_workflow("validation", {
            "policy_id": "customer_onboarding",
            "data": {
                "email": "customer@example.com",
                "age": 30,
                "phone": "+1-555-0123"
            }
        })
        print(f"   Workflow Status: {result['status']}")
        print(f"   Result: {result['result']}")
        
        # Example 2: KYC workflow
        print("\n2. Multi-Agent KYC Workflow:")
        result = await orchestrator.execute_workflow("kyc", {
            "customer_data": {
                "identity_documents": [{"type": "passport", "expiry_date": "2025-12-31"}],
                "date_of_birth": "1990-05-15"
            }
        })
        print(f"   Workflow Status: {result['status']}")
        print(f"   KYC Result: {result['result']}")
        
        # Example 3: Risk assessment workflow
        print("\n3. Multi-Agent Risk Assessment Workflow:")
        result = await orchestrator.execute_workflow("risk_assessment", {
            "transaction_data": {
                "amount": 15000,
                "currency": "USD",
                "country": "US"
            }
        })
        print(f"   Workflow Status: {result['status']}")
        print(f"   Risk Result: {result['result']}")
        
        # System status
        print("\n4. System Status:")
        status = orchestrator.get_system_status()
        print(f"   Orchestrator Running: {status['orchestrator_running']}")
        print(f"   Registered Agents: {status['registered_agents']}")
        
    finally:
        await orchestrator.stop()

async def advanced_agent_coordination():
    """Advanced agent coordination examples"""
    print("\n\nAdvanced Agent Coordination")
    print("=" * 27)
    
    orchestrator = MultiAgentOrchestrator()
    await orchestrator.start()
    
    try:
        # Complex workflow with multiple agents
        print("\n1. Complex Multi-Step Workflow:")
        
        # Step 1: Policy interpretation
        print("   Step 1: Policy Agent - Interpreting requirements")
        
        # Step 2: Data validation
        print("   Step 2: Validation Agent - Checking data quality")
        
        # Step 3: Knowledge enhancement
        print("   Step 3: RAG Agent - Adding context")
        
        # Step 4: Explanation generation
        print("   Step 4: Explanation Agent - Creating summaries")
        
        # Execute coordinated workflow
        workflow_result = await orchestrator.execute_workflow("validation", {
            "policy_id": "comprehensive_validation",
            "data": {
                "customer_type": "premium",
                "transaction_amount": 50000,
                "region": "EU"
            },
            "require_explanations": True,
            "include_context": True
        })
        
        print(f"   Final Result: {workflow_result['status']}")
        
    finally:
        await orchestrator.stop()

async def enterprise_scenarios():
    """Enterprise-level scenarios"""
    print("\n\nEnterprise Scenarios")
    print("=" * 19)
    
    orchestrator = MultiAgentOrchestrator()
    await orchestrator.start()
    
    try:
        # Scenario 1: Bulk processing
        print("\n1. Bulk Customer Processing:")
        customers = [
            {"email": f"customer{i}@example.com", "age": 25 + i}
            for i in range(5)
        ]
        
        for i, customer in enumerate(customers):
            result = await orchestrator.execute_workflow("validation", {
                "policy_id": "customer_onboarding",
                "data": customer
            })
            print(f"   Customer {i+1}: {result['status']}")
        
        # Scenario 2: Multi-jurisdiction compliance
        print("\n2. Multi-Jurisdiction Compliance:")
        jurisdictions = ["US", "EU", "UK"]
        
        for jurisdiction in jurisdictions:
            result = await orchestrator.execute_workflow("validation", {
                "policy_id": f"{jurisdiction.lower()}_compliance",
                "data": {
                    "email": f"customer@{jurisdiction.lower()}.com",
                    "age": 30,
                    "region": jurisdiction
                }
            })
            print(f"   {jurisdiction} Compliance: {result['status']}")
        
    finally:
        await orchestrator.stop()

if __name__ == "__main__":
    print("Running Multi-Agent Examples...")
    
    # Run async examples
    asyncio.run(basic_multi_agent_workflow())
    asyncio.run(advanced_agent_coordination())
    asyncio.run(enterprise_scenarios())
    
    print("\nMulti-agent examples completed!")