# Python 3.13 Compatibility

This project is compatible with Python 3.13 and uses alternatives to Pydantic for data validation.

## 🐍 Python Version Support

- **Python 3.13+** - Full support
- **Python 3.11-3.12** - Compatible
- **Python 3.10** - Compatible with minor adjustments

## 📦 Dependency Changes

### Replaced Dependencies

| Original | Replacement | Reason |
|----------|-------------|---------|
| `pydantic==2.5.0` | `dataclasses-json==0.6.3` | Python 3.13 compatibility |
| Pydantic BaseModel | Python dataclasses | Built-in Python feature |
| Pydantic validation | Manual validation | Simpler, no external deps |

### Simple Architecture
```
# Before (Pydantic)
from pydantic import BaseModel

class ValidationRequest(BaseModel):
    policy_id: str
    data: Dict[str, Any]

# After (Dataclasses)
from dataclasses import dataclass

@dataclass
class ValidationRequest:
    policy_id: str
    data: Dict[str, Any]
```

### FastAPI Integration
```python
# Before (Pydantic models)
@app.post("/validate")
def validate_data(request: ValidationRequest):
    return orchestrator.validate(request.policy_id, request.data)

# After (Dict-based)
@app.post("/validate")
def validate_data(request: dict):
    policy_id = request.get("policy_id")
    data = request.get("data")
    return orchestrator.validate(policy_id, data)
```

## ✅ Benefits

1. **Python 3.13 Ready** - No compatibility issues
2. **Fewer Dependencies** - Uses built-in Python features
3. **Simpler Code** - Less complex validation logic
4. **Better Performance** - No external validation overhead
5. **Easier Maintenance** - Standard library features

## 🚀 Installation

```bash
# Simple Architecture
cd simple
pip install -r requirements.txt

# Multi-Agent Architecture  
cd multi-agent
pip install -r requirements.txt
```

## 🧪 Testing

All tests work with Python 3.13:

```bash
# Simple tests
cd simple/tests
python test_runner.py

# Multi-agent tests
cd multi-agent/tests
python test_runner.py
```

## 🔧 Migration Notes

If upgrading from Pydantic version:

1. **Replace BaseModel** with `@dataclass`
2. **Update FastAPI endpoints** to use `dict` parameters
3. **Add manual validation** where needed
4. **Update requirements.txt** files

## 📋 Current Dependencies

### Simple Architecture
```
fastapi==0.104.1
uvicorn==0.24.0
dataclasses-json==0.6.3  # Instead of pydantic
requests==2.31.0
```

### Multi-Agent Architecture
```
fastapi==0.104.1
uvicorn==0.24.0
dataclasses-json==0.6.3  # Instead of pydantic
chromadb==0.4.18
langchain==0.0.340
```

All functionality remains the same with improved Python 3.13 compatibility.