# Sample Test Data for Policy Validation

This document provides sample test data that corresponds to each policy document for comprehensive validation testing.

## 1. Customer Onboarding Comprehensive Policy

### Valid Customer Data
```json
{
  "email": "john.doe@example.com",
  "phone": "+1-555-0123",
  "age": 28,
  "full_name": "John Michael Doe",
  "address": {
    "street": "123 Main Street Apt 4B",
    "city": "New York",
    "country": "US",
    "postal_code": "10001"
  },
  "date_of_birth": "1995-06-15",
  "employment_status": "employed",
  "annual_income": 75000,
  "identity_verification": {
    "document_type": "passport",
    "document_number": "AB1234567",
    "expiry_date": "2026-12-31"
  },
  "consent": {
    "terms_accepted": true,
    "privacy_policy_accepted": true,
    "marketing_consent": false
  }
}
```

### Invalid Customer Data (Multiple Violations)
```json
{
  "email": "invalid-email-format",
  "phone": "555-0123",
  "age": 16,
  "full_name": "J",
  "address": {
    "street": "123",
    "city": "NY",
    "country": "XX",
    "postal_code": "1"
  },
  "date_of_birth": "2010-01-01",
  "employment_status": "unknown",
  "identity_verification": {
    "document_type": "passport",
    "document_number": "123",
    "expiry_date": "2023-01-01"
  },
  "consent": {
    "terms_accepted": false,
    "privacy_policy_accepted": false
  }
}
```

## 2. Financial Transaction Policy

### Valid Transaction
```json
{
  "transaction_id": "TXN1234567890",
  "amount": 1250.50,
  "currency": "USD",
  "payment_method": {
    "type": "credit_card",
    "last_four": "4567",
    "expiry_month": 12,
    "expiry_year": 2026
  },
  "merchant_info": {
    "merchant_id": "MERCH12345",
    "category": "retail",
    "country": "US"
  },
  "customer_id": "CUST12345678",
  "timestamp": "2024-01-15T14:30:00Z",
  "risk_indicators": {
    "velocity_check": true,
    "geolocation_match": true,
    "device_fingerprint": "fp_abc123def456"
  }
}
```

### High-Risk Transaction
```json
{
  "transaction_id": "TXN9876543210",
  "amount": 25000.00,
  "currency": "USD",
  "payment_method": {
    "type": "bank_transfer",
    "last_four": "9999"
  },
  "merchant_info": {
    "merchant_id": "MERCH99999",
    "category": "online",
    "country": "XX"
  },
  "customer_id": "CUST87654321",
  "timestamp": "2024-01-15T23:45:00Z",
  "risk_indicators": {
    "velocity_check": false,
    "geolocation_match": false
  }
}
```

## 3. GDPR Compliance Policy

### Valid GDPR Data
```json
{
  "data_subject_consent": {
    "consent_given": true,
    "consent_date": "2024-01-15T10:00:00Z",
    "consent_method": "explicit",
    "purpose_specified": true
  },
  "personal_data": {
    "data_categories": ["identity", "contact"],
    "processing_purpose": "contract",
    "retention_period": 1095
  },
  "data_subject_rights": {
    "right_to_access": true,
    "right_to_rectification": true,
    "right_to_erasure": true,
    "right_to_portability": true
  },
  "data_protection_measures": {
    "encryption_at_rest": true,
    "encryption_in_transit": true,
    "access_controls": true,
    "audit_logging": true
  },
  "breach_notification": {
    "notification_procedure": true,
    "72_hour_notification": true,
    "data_subject_notification": true
  }
}
```

### GDPR Violation Data
```json
{
  "data_subject_consent": {
    "consent_given": false,
    "consent_date": "2024-01-15T10:00:00Z",
    "consent_method": "implied",
    "purpose_specified": false
  },
  "personal_data": {
    "data_categories": ["sensitive", "behavioral"],
    "processing_purpose": "marketing",
    "retention_period": 3650
  },
  "data_protection_measures": {
    "encryption_at_rest": false,
    "encryption_in_transit": false,
    "access_controls": false,
    "audit_logging": false
  }
}
```

## 4. HIPAA Compliance Policy

### Valid HIPAA Data
```json
{
  "patient_info": {
    "patient_id": "PAT12345678",
    "medical_record_number": "MRN987654",
    "date_of_birth": "1985-03-20",
    "ssn_last_four": "1234"
  },
  "phi_categories": ["demographic", "treatment_records"],
  "access_controls": {
    "user_authentication": true,
    "role_based_access": true,
    "minimum_necessary": true,
    "audit_trail": true
  },
  "data_security": {
    "encryption_required": true,
    "secure_transmission": true,
    "backup_encryption": true,
    "device_controls": true
  },
  "patient_rights": {
    "right_to_access": true,
    "right_to_amend": true,
    "right_to_accounting": true,
    "right_to_restrict": true
  },
  "breach_response": {
    "incident_response_plan": true,
    "risk_assessment_process": true,
    "notification_procedures": true,
    "documentation_requirements": true
  }
}
```

## 5. Employee Data Validation Policy

### Valid Employee Data
```json
{
  "employee_id": "EMP123456",
  "personal_info": {
    "first_name": "Sarah",
    "last_name": "Johnson",
    "email": "sarah.johnson@company.com",
    "phone": "+1-555-0199",
    "date_of_birth": "1990-08-12"
  },
  "employment_details": {
    "hire_date": "2023-01-15",
    "department": "Engineering",
    "position": "Senior Software Engineer",
    "employment_type": "full_time",
    "manager_id": "EMP654321",
    "salary": 95000
  },
  "security_clearance": {
    "level": "confidential",
    "granted_date": "2023-02-01",
    "expiry_date": "2025-02-01",
    "background_check_completed": true
  },
  "emergency_contact": {
    "name": "Michael Johnson",
    "relationship": "spouse",
    "phone": "+1-555-0188",
    "email": "michael.j@email.com"
  },
  "compliance_training": [
    {
      "training_name": "Security Awareness",
      "completion_date": "2023-01-20",
      "expiry_date": "2024-01-20",
      "status": "completed"
    }
  ]
}
```

## 6. API Security Validation Policy

### Valid API Request
```json
{
  "authentication": {
    "method": "jwt",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiry": "2024-01-15T15:30:00Z",
    "scope": ["read", "write"]
  },
  "request_metadata": {
    "client_id": "CLIENT_ABC12345",
    "user_agent": "MyApp/1.0 (Windows NT 10.0)",
    "ip_address": "192.168.1.100",
    "timestamp": "2024-01-15T14:25:00Z"
  },
  "rate_limiting": {
    "requests_per_minute": 50,
    "requests_per_hour": 1000,
    "burst_limit": 10,
    "concurrent_requests": 5
  },
  "data_validation": {
    "input_sanitization": true,
    "sql_injection_check": true,
    "xss_protection": true,
    "data_size_limit_mb": 10
  },
  "encryption_requirements": {
    "tls_version": "1.3",
    "cipher_suite": "TLS_AES_256_GCM_SHA384",
    "certificate_valid": true,
    "hsts_enabled": true
  },
  "audit_logging": {
    "request_logged": true,
    "response_logged": true,
    "error_logged": true,
    "retention_days": 365
  },
  "access_control": {
    "resource_permissions": ["users:read", "data:write"],
    "ip_whitelist": ["192.168.1.0/24"],
    "geo_restrictions": ["US", "CA"]
  }
}
```

## Test Execution Commands

```bash
# Test comprehensive customer onboarding
python test_runner.py --policy=customer_onboarding_comprehensive --data=valid_customer.json

# Test financial transaction validation
python test_runner.py --policy=financial_transaction --data=high_risk_transaction.json

# Test GDPR compliance
python test_runner.py --policy=gdpr_compliance --data=gdpr_violation.json

# Test all policies with sample data
python test_runner.py --suite=all --use-sample-data

# Interactive testing with policy selection
python interactive_test.py --load-policies
```