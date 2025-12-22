"""Test Configuration for Multi-Agent Governance System"""

import os

# Test Configuration
TEST_CONFIG = {
    "use_database": False,  # Disable database for testing
    "test_timeout": 60,  # seconds for async operations
    "verbose_output": True,
    "mock_agents": True,  # Use mock agents for testing
    "db_path": ":memory:",  # In-memory database for tests
}

# Agent Configuration
AGENT_CONFIG = {
    "policy_agent": {
        "agent_id": "policy_test_001",
        "capabilities": ["policy_interpretation", "rule_validation"]
    },
    "validation_agent": {
        "agent_id": "validation_test_001", 
        "capabilities": ["data_validation", "constraint_checking"]
    },
    "rag_agent": {
        "agent_id": "rag_test_001",
        "capabilities": ["knowledge_search", "context_enhancement"]
    }
}

# Sample workflow data
SAMPLE_WORKFLOWS = {
    "validation": {
        "policy_id": "customer_onboarding",
        "data": {
            "email": "test@example.com",
            "age": 25,
            "phone": "+1-555-0123"
        }
    },
    "kyc": {
        "customer_data": {
            "identity_documents": [{"type": "passport", "expiry_date": "2025-12-31"}],
            "date_of_birth": "1990-05-15"
        }
    },
    "risk_assessment": {
        "transaction_data": {
            "amount": 15000,
            "currency": "USD",
            "country": "US"
        }
    }
}

# MCP Tool Test Data
MCP_TEST_TOOLS = [
    "validate_data_enhanced",
    "multi_policy_validation", 
    "compliance_audit",
    "risk_scoring_advanced",
    "workflow_orchestration"
]

# Expected workflow results
EXPECTED_WORKFLOW_RESULTS = {
    "validation": {"status": "completed", "workflow": "validation"},
    "kyc": {"status": "completed", "workflow": "kyc"},
    "risk_assessment": {"status": "completed", "workflow": "risk_assessment"}
}