"""Basic tests for the Governance & Compliance Agent"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock

from src.core.engine import GovernanceEngine
from src.agents.orchestrator import AgentOrchestrator


class TestGovernanceEngine:
    """Test cases for the GovernanceEngine"""
    
    @pytest.fixture
    async def engine(self):
        """Create a test engine instance"""
        engine = GovernanceEngine()
        yield engine
        await engine.shutdown()
    
    @pytest.mark.asyncio
    async def test_engine_initialization(self, engine):
        """Test engine initializes correctly"""
        assert engine is not None
        assert hasattr(engine, 'policy_store')
        assert hasattr(engine, 'schema_store')
    
    @pytest.mark.asyncio
    async def test_policy_registration(self, engine):
        """Test policy registration"""
        orchestrator = AgentOrchestrator(engine)
        
        policy_content = "Test policy: All users must have valid email"
        policy_id = await orchestrator.register_policy("test_policy", policy_content)
        
        assert policy_id is not None
        assert isinstance(policy_id, str)
    
    @pytest.mark.asyncio
    async def test_basic_validation(self, engine):
        """Test basic data validation"""
        orchestrator = AgentOrchestrator(engine)
        
        # Register a simple policy
        policy_content = "Email must be valid format"
        policy_id = await orchestrator.register_policy("email_policy", policy_content)
        
        # Test valid data
        valid_data = {"email": "test@example.com"}
        result = await orchestrator.validate(policy_id, valid_data)
        
        assert result is not None
        assert hasattr(result, 'is_valid')
        assert hasattr(result, 'violations')
    
    @pytest.mark.asyncio
    async def test_invalid_data_validation(self, engine):
        """Test validation with invalid data"""
        orchestrator = AgentOrchestrator(engine)
        
        policy_content = "Age must be between 18 and 65"
        policy_id = await orchestrator.register_policy("age_policy", policy_content)
        
        # Test invalid data
        invalid_data = {"age": 150}
        result = await orchestrator.validate(policy_id, invalid_data)
        
        assert result is not None
        # Should have violations for invalid age
        assert len(result.violations) > 0


class TestSchemaHandling:
    """Test cases for schema drift detection"""
    
    @pytest.fixture
    async def engine(self):
        """Create a test engine instance"""
        engine = GovernanceEngine()
        yield engine
        await engine.shutdown()
    
    @pytest.mark.asyncio
    async def test_schema_drift_detection(self, engine):
        """Test schema drift detection"""
        orchestrator = AgentOrchestrator(engine)
        
        old_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            }
        }
        
        new_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "string"},  # Type changed
                "email": {"type": "string"}  # New field
            }
        }
        
        drift_result = await orchestrator.detect_schema_drift(old_schema, new_schema)
        
        assert drift_result is not None
        assert hasattr(drift_result, 'changes')
        assert len(drift_result.changes) > 0


class TestPolicyInterpretation:
    """Test cases for policy interpretation"""
    
    @pytest.fixture
    async def engine(self):
        """Create a test engine instance"""
        engine = GovernanceEngine()
        yield engine
        await engine.shutdown()
    
    @pytest.mark.asyncio
    async def test_natural_language_policy(self, engine):
        """Test natural language policy interpretation"""
        orchestrator = AgentOrchestrator(engine)
        
        policy_content = """
        Customer registration requires:
        - Valid email address
        - Age between 18 and 100
        - Phone number with country code
        """
        
        policy_id = await orchestrator.register_policy("registration", policy_content)
        
        # Test with complete valid data
        valid_data = {
            "email": "user@example.com",
            "age": 25,
            "phone": "+1-555-0123"
        }
        
        result = await orchestrator.validate(policy_id, valid_data)
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_complex_business_rules(self, engine):
        """Test complex business rule interpretation"""
        orchestrator = AgentOrchestrator(engine)
        
        policy_content = """
        Financial transactions must follow these rules:
        - Amounts over $10,000 require manager approval
        - International transfers need compliance review
        - Weekend transactions are restricted to $5,000
        """
        
        policy_id = await orchestrator.register_policy("financial", policy_content)
        
        # Test high-value transaction
        transaction_data = {
            "amount": 15000,
            "type": "domestic",
            "manager_approval": True,
            "timestamp": "2024-01-15T14:30:00Z"
        }
        
        result = await orchestrator.validate(policy_id, transaction_data)
        assert result is not None


@pytest.mark.asyncio
async def test_end_to_end_workflow():
    """Test complete end-to-end workflow"""
    engine = GovernanceEngine()
    orchestrator = AgentOrchestrator(engine)
    
    try:
        # 1. Register policy
        policy_content = "All users must provide valid contact information"
        policy_id = await orchestrator.register_policy("contact_policy", policy_content)
        
        # 2. Validate data
        test_data = {
            "email": "test@example.com",
            "phone": "+1-555-0123",
            "address": "123 Main St, City, 12345"
        }
        
        result = await orchestrator.validate(policy_id, test_data)
        
        # 3. Check results
        assert result is not None
        assert hasattr(result, 'is_valid')
        assert hasattr(result, 'violations')
        assert hasattr(result, 'explanations')
        
    finally:
        await engine.shutdown()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])