# Explanation Agent Documentation

## Overview
The Explanation Agent generates human-readable explanations for policy violations, decisions, and risk assessments.

## Core Actions

### `explain_violation`
**Input:**
```json
{
  "violations": [
    {
      "field": "age",
      "type": "constraint_violation",
      "severity": "high"
    }
  ],
  "context": {"region": "US"},
  "policy_name": "Customer Onboarding Policy"
}
```

**Output:**
```json
{
  "explanations": [
    {
      "field": "age",
      "violation_type": "constraint_violation",
      "severity": "high",
      "explanation": "The age field violates business constraints...",
      "business_impact": "Critical compliance failure",
      "urgency": "Immediate action required",
      "stakeholders": ["Compliance Team", "Legal Department"]
    }
  ],
  "summary": "Found 1 violations, 1 of which are high severity",
  "next_steps": ["Address high-severity violations immediately"]
}
```

### `generate_remediation`
**Input:**
```json
{
  "violations": [...],
  "context": {...}
}
```

**Output:**
```json
{
  "remediation_plan": {
    "immediate_actions": ["Fix data validation", "Update records"],
    "short_term_actions": ["Implement monitoring", "Train staff"],
    "long_term_actions": ["Improve processes", "Automate checks"],
    "preventive_measures": ["Regular audits", "Enhanced training"]
  },
  "estimated_effort": "Medium effort (1-2 weeks)",
  "timeline": {
    "immediate_actions": "Within 24 hours",
    "short_term_actions": "Within 1 week"
  }
}
```

### `explain_decision`
Explains automated compliance decisions in business terms.

### `risk_explanation`
Provides detailed explanations for risk assessment results.

## Usage Example

```python
from src.agents.explanation_agent import ExplanationAgent

explanation_agent = ExplanationAgent()
await explanation_agent.initialize()

# Explain violations
message = AgentMessage(
    sender="user",
    recipient="explanation",
    action="explain_violation",
    payload={
        "violations": [
            {
                "field": "email",
                "type": "pattern_mismatch",
                "severity": "medium"
            }
        ],
        "context": {"customer_type": "premium"},
        "policy_name": "Data Quality Policy"
    }
)

response = await explanation_agent.process_message(message)
for explanation in response.data['explanations']:
    print(f"Field: {explanation['field']}")
    print(f"Issue: {explanation['explanation']}")
    print(f"Impact: {explanation['business_impact']}")
```

## Explanation Templates
- **missing_required**: Required field explanations
- **invalid_type**: Data type mismatch explanations
- **constraint_violation**: Business constraint violations
- **pattern_mismatch**: Format validation failures
- **business_rule_violation**: Business logic violations

## Stakeholder Mapping
- **Email issues**: Data Quality Team, Customer Service
- **Age verification**: Compliance Team, Legal Department
- **Transaction amounts**: Risk Management, Finance Team
- **Identity documents**: KYC Team, Compliance Officer