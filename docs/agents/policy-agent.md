# Policy Agent Documentation

## Overview
The Policy Agent converts natural language policies into structured, executable rules.

## Core Actions

### `parse_policy`
**Input:**
```json
{
  "policy_text": "All customers must provide valid email and be over 18",
  "policy_id": "customer_policy_1"
}
```

**Output:**
```json
{
  "policy_id": "customer_policy_1",
  "parsed_rules": {
    "rules": [
      {"field": "email", "type": "email", "required": true},
      {"field": "age", "type": "integer", "required": true, "constraints": {"min": 18}}
    ]
  }
}
```

### `validate_policy`
Validates policy structure and completeness.

### `get_policy`
Retrieves stored policy by ID.

## Usage Example

```python
from src.agents.policy_agent import PolicyAgent
from src.agents.base_agent import AgentMessage

policy_agent = PolicyAgent()
await policy_agent.initialize()

message = AgentMessage(
    sender="user",
    recipient="policy",
    action="parse_policy",
    payload={
        "policy_text": "Customers must be 18+ with valid email",
        "policy_id": "simple_policy"
    }
)

response = await policy_agent.process_message(message)
print(f"Success: {response.success}")
```

## Best Practices
- Use clear, specific language in policies
- Include data types and constraints
- Define compliance requirements
- Test with sample data