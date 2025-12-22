"""Test Configuration for Simple Governance Agent"""

import os

# Test Configuration
TEST_CONFIG = {
    "use_llm": False,  # Disable LLM for consistent testing
    "policies_dir": os.path.join(os.path.dirname(__file__), "..", "policies"),
    "knowledge_dir": os.path.join(os.path.dirname(__file__), "..", "knowledge"),
    "test_timeout": 30,  # seconds
    "verbose_output": True
}

# Sample test data
SAMPLE_CUSTOMER_DATA = {
    "valid": {
        "email": "john.doe@example.com",
        "age": 28,
        "phone": "+1-555-0123",
        "full_name": "John Doe"
    },
    "invalid_email": {
        "email": "invalid-email-format",
        "age": 25,
        "phone": "+1-555-0123"
    },
    "age_too_young": {
        "email": "young@example.com",
        "age": 16,
        "phone": "+1-555-0123"
    },
    "missing_required": {
        "email": "incomplete@example.com"
    }
}

SAMPLE_KYC_DATA = {
    "valid": {
        "identity_documents": [
            {"type": "passport", "expiry_date": "2025-12-31"}
        ],
        "date_of_birth": "1990-05-15"
    },
    "missing_documents": {
        "date_of_birth": "1990-05-15"
    }
}

SAMPLE_RISK_DATA = {
    "high_risk": {
        "amount": 25000,
        "country": "XX",
        "age": 20
    },
    "low_risk": {
        "amount": 500,
        "country": "US",
        "age": 35
    }
}

# Expected test results
EXPECTED_RESULTS = {
    "valid_customer": {"is_valid": True, "score": 1.0},
    "invalid_email": {"is_valid": False},
    "age_too_young": {"is_valid": False},
    "missing_required": {"is_valid": False}
}