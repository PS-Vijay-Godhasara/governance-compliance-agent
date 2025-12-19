"""Basic usage examples for the Governance & Compliance Agent"""

import asyncio
from src.core.engine import GovernanceEngine
from src.agents.orchestrator import AgentOrchestrator


async def basic_policy_example():
    """Example: Basic policy registration and validation"""
    
    # Initialize engine and orchestrator
    engine = GovernanceEngine()
    orchestrator = AgentOrchestrator(engine)
    
    # Define a customer onboarding policy
    policy_content = """
    Customer data must include:
    - Valid email address
    - Phone number with country code
    - Age between 18 and 120 years
    - KYC documents uploaded within 30 days
    - Address with postal code
    """
    
    # Register the policy
    policy_id = await orchestrator.register_policy(
        name="customer_onboarding",
        content=policy_content,
        metadata={"version": "1.0", "jurisdiction": "US"}
    )
    
    print(f"Policy registered with ID: {policy_id}")
    
    # Test data - valid customer
    valid_customer = {
        "email": "john.doe@example.com",
        "phone": "+1-555-0123",
        "age": 25,
        "kyc_uploaded": "2024-01-15",
        "address": {
            "street": "123 Main St",
            "city": "New York",
            "postal_code": "10001"
        }
    }
    
    # Validate valid customer
    result = await orchestrator.validate(policy_id, valid_customer)
    print(f"\nValid customer validation:")
    print(f"Is valid: {result.is_valid}")
    print(f"Score: {result.score}")
    
    # Test data - invalid customer
    invalid_customer = {
        "email": "invalid-email",
        "phone": "555-0123",  # Missing country code
        "age": 150,  # Invalid age
        "kyc_uploaded": "2023-01-15",  # Too old
        "address": {
            "street": "456 Oak Ave",
            "city": "Boston"
            # Missing postal_code
        }
    }
    
    # Validate invalid customer
    result = await orchestrator.validate(policy_id, invalid_customer)
    print(f"\nInvalid customer validation:")
    print(f"Is valid: {result.is_valid}")
    print(f"Score: {result.score}")
    print(f"Violations: {len(result.violations)}")
    
    for violation in result.violations:
        print(f"  - {violation.field}: {violation.description}")
        print(f"    Fix: {violation.remediation}")
    
    await engine.shutdown()


async def schema_drift_example():
    """Example: Schema drift detection and handling"""
    
    engine = GovernanceEngine()
    orchestrator = AgentOrchestrator(engine)
    
    # Original schema
    old_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "email": {"type": "string"}
        },
        "required": ["name", "age", "email"]
    }
    
    # New schema with changes
    new_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "string"},  # Type changed
            "email": {"type": "string"},
            "phone": {"type": "string"}  # New field
        },
        "required": ["name", "age", "email", "phone"]  # New required field
    }
    
    # Detect schema drift
    drift_result = await orchestrator.detect_schema_drift(old_schema, new_schema)
    
    print("Schema drift detected:")
    for change in drift_result.changes:
        print(f"  - {change.type}: {change.description}")
        print(f"    Impact: {change.impact}")
        print(f"    Migration: {change.migration_strategy}")
    
    await engine.shutdown()


async def financial_compliance_example():
    """Example: Financial compliance validation"""
    
    engine = GovernanceEngine()
    orchestrator = AgentOrchestrator(engine)
    
    # Financial transaction policy
    policy_content = """
    Financial transactions must comply with:
    - Transactions over $10,000 require manager approval
    - International transfers need compliance review
    - High-risk countries require additional documentation
    - All transactions must have valid beneficiary information
    - AML screening must be completed within 24 hours
    """
    
    policy_id = await orchestrator.register_policy(
        name="financial_transactions",
        content=policy_content,
        metadata={"regulation": "BSA", "jurisdiction": "US"}
    )
    
    # Test transaction
    transaction = {
        "amount": 15000,
        "currency": "USD",
        "beneficiary": {
            "name": "ABC Corp",
            "account": "123456789",
            "country": "US"
        },
        "purpose": "Business payment",
        "manager_approval": True,
        "aml_screening": {
            "completed": True,
            "timestamp": "2024-01-15T10:30:00Z",
            "risk_score": 0.2
        }
    }
    
    result = await orchestrator.validate(
        policy_id, 
        transaction,
        context={"user_role": "trader", "region": "US"}
    )
    
    print(f"Transaction validation:")
    print(f"Is valid: {result.is_valid}")
    print(f"Risk score: {result.risk_score}")
    
    if result.violations:
        print("Violations found:")
        for violation in result.violations:
            print(f"  - {violation.description}")
    
    await engine.shutdown()


if __name__ == "__main__":
    print("=== Basic Policy Example ===")
    asyncio.run(basic_policy_example())
    
    print("\n=== Schema Drift Example ===")
    asyncio.run(schema_drift_example())
    
    print("\n=== Financial Compliance Example ===")
    asyncio.run(financial_compliance_example())