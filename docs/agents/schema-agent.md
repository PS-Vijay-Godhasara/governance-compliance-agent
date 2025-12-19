# Schema Agent Documentation

## Overview
The Schema Agent handles database/API schema evolution, drift detection, and migration planning.

## Core Actions

### `detect_drift`
**Input:**
```json
{
  "old_schema": {
    "properties": {
      "name": {"type": "string"},
      "email": {"type": "string"}
    },
    "required": ["name", "email"]
  },
  "new_schema": {
    "properties": {
      "name": {"type": "string"},
      "email": {"type": "string"},
      "phone": {"type": "string"}
    },
    "required": ["name", "email", "phone"]
  }
}
```

**Output:**
```json
{
  "changes": [
    {
      "type": "field_added",
      "field": "phone",
      "description": "New field 'phone' added",
      "impact": "medium",
      "migration_strategy": "Add default value for required field 'phone'"
    }
  ],
  "total_changes": 1,
  "risk_level": "medium",
  "compatibility": "breaking"
}
```

### `generate_migration`
**Input:**
```json
{
  "changes": [...],
  "target_system": "database"
}
```

**Output:**
```json
{
  "migration_plan": {
    "steps": [
      {
        "step": "ADD_COLUMN_phone",
        "sql": "ALTER TABLE main_table ADD COLUMN phone VARCHAR(255)",
        "description": "Add new column phone",
        "order": 1
      }
    ],
    "rollback_steps": [...],
    "estimated_duration": "5 minutes"
  }
}
```

### `validate_compatibility`
Checks backward compatibility between schema versions.

### `register_schema`
Registers new schema version with metadata.

## Usage Example

```python
from src.agents.schema_agent import SchemaAgent

schema_agent = SchemaAgent()
await schema_agent.initialize()

# Detect schema drift
message = AgentMessage(
    sender="user",
    recipient="schema",
    action="detect_drift",
    payload={
        "old_schema": {
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"}
            }
        },
        "new_schema": {
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "email": {"type": "string"}
            },
            "required": ["id", "name", "email"]
        }
    }
)

response = await schema_agent.process_message(message)
print(f"Changes detected: {response.data['total_changes']}")
print(f"Risk level: {response.data['risk_level']}")
```

## Change Types
- **field_added**: New field in schema
- **field_removed**: Field removed from schema
- **type_changed**: Field data type modified
- **required_changed**: Field requirement status changed

## Impact Levels
- **High**: Breaking changes requiring immediate attention
- **Medium**: Changes requiring migration planning
- **Low**: Non-breaking changes with minimal impact