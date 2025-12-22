# Governance Agent API Documentation

## Base URL
```
http://localhost:5000
```

## Authentication
No authentication required for local development.

---

## Endpoints

### 1. System Status
**GET** `/api/status`

Get system status and configuration information.

**Response:**
```json
{
  "llm_enabled": true,
  "orchestrator_ready": true,
  "policies_dir": "../policies"
}
```

**Example:**
```bash
curl -X GET http://localhost:5000/api/status
```

---

### 2. Chat Interface
**POST** `/api/chat`

Send messages to the governance agent for natural language processing.

**Request Body:**
```json
{
  "message": "What is GDPR and how does it affect customer validation?"
}
```

**Response:**
```json
{
  "response": "GDPR is the EU General Data Protection Regulation that requires...",
  "session_id": "uuid-session-id"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain KYC requirements"}'
```

**Error Response:**
```json
{
  "error": "Message cannot be empty"
}
```

---

### 3. Data Validation
**POST** `/api/validate`

Validate data against specified policies.

**Request Body:**
```json
{
  "data": {
    "email": "user@example.com",
    "age": 25,
    "country": "US",
    "balance": 50000
  },
  "policy": "basic_validation"
}
```

**Response:**
```json
{
  "valid": true,
  "score": 1.0,
  "violations": [],
  "explanation": "Validation passed with no issues"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/validate \
  -H "Content-Type: application/json" \
  -d '{
    "data": {"email": "test@example.com", "age": 25},
    "policy": "customer_onboarding"
  }'
```

**Error Response:**
```json
{
  "valid": false,
  "score": 0.6,
  "violations": ["Missing required field: phone", "Age below minimum 18"],
  "explanation": "Validation failed with 2 issues"
}
```

---

### 4. File Upload & Analysis
**POST** `/api/upload`

Upload files for validation or analysis with optional custom prompts.

**Request (Form Data):**
- `file`: File to upload (JSON, TXT, CSV)
- `policy`: Policy name for validation (optional)
- `prompt`: Custom question about the file (optional)

**Response for JSON Validation:**
```json
{
  "filename": "customer_data.json",
  "valid": true,
  "score": 0.85,
  "violations": ["Age below minimum for premium services"],
  "explanation": "Customer meets most requirements",
  "prompt": "Is this customer eligible for premium services?",
  "prompt_response": "Based on the data, the customer meets most requirements but..."
}
```

**Response for Text Analysis:**
```json
{
  "filename": "privacy_policy.txt",
  "analysis": "This privacy policy covers most GDPR requirements...",
  "prompt": "Is this policy GDPR compliant?",
  "prompt_response": "The policy addresses key GDPR requirements including..."
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/upload \
  -F "file=@customer_data.json" \
  -F "policy=premium_customer" \
  -F "prompt=What validation errors exist?"
```

**Error Response:**
```json
{
  "error": "Unsupported file type. Use JSON, TXT, or CSV"
}
```

---

### 5. Available Policies
**GET** `/api/policies`

Get list of available validation policies.

**Response:**
```json
{
  "policies": [
    "basic_validation",
    "customer_onboarding", 
    "premium_customer",
    "kyc_validation",
    "transaction_validation",
    "aml_compliance"
  ]
}
```

**Example:**
```bash
curl -X GET http://localhost:5000/api/policies
```

---

## Policy Types

### Available Policies

| Policy Name | Description | Required Fields |
|-------------|-------------|-----------------|
| `basic_validation` | Minimal customer validation | email, age |
| `customer_onboarding` | Complete customer profile | email, age, phone, full_name |
| `premium_customer` | High-value customer validation | email, age, full_name, phone, balance, country |
| `kyc_validation` | Identity verification | identity_documents, date_of_birth |
| `transaction_validation` | Financial transaction checks | amount, currency, recipient_account, transaction_type |
| `aml_compliance` | Anti-money laundering screening | customer_id, transaction_amount, source_of_funds, sanctions_check |

---

## Error Codes

| HTTP Code | Description |
|-----------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid input data |
| 500 | Internal Server Error - System error |

**Common Error Messages:**
- `"Message cannot be empty"` - Chat message is required
- `"Policy not found"` - Invalid policy name
- `"No file uploaded"` - File is required for upload endpoint
- `"Orchestrator not initialized"` - System initialization error
- `"Validation error: [details]"` - Data validation failed

---

## Sample Requests

### 1. Basic Customer Validation
```javascript
fetch('/api/validate', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    data: {
      email: "user@example.com",
      age: 25,
      country: "US",
      balance: 50000
    },
    policy: "basic_validation"
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

### 2. Chat Interaction
```javascript
fetch('/api/chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    message: "What are the KYC requirements for new customers?"
  })
})
.then(response => response.json())
.then(data => console.log(data.response));
```

### 3. File Upload with Prompt
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('policy', 'customer_onboarding');
formData.append('prompt', 'What validation errors exist in this data?');

fetch('/api/upload', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## Python SDK Example

```python
import requests
import json

class GovernanceAgentClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
    
    def chat(self, message):
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={"message": message}
        )
        return response.json()
    
    def validate(self, data, policy):
        response = requests.post(
            f"{self.base_url}/api/validate",
            json={"data": data, "policy": policy}
        )
        return response.json()
    
    def upload_file(self, file_path, policy=None, prompt=None):
        files = {'file': open(file_path, 'rb')}
        data = {}
        if policy:
            data['policy'] = policy
        if prompt:
            data['prompt'] = prompt
        
        response = requests.post(
            f"{self.base_url}/api/upload",
            files=files,
            data=data
        )
        return response.json()
    
    def get_policies(self):
        response = requests.get(f"{self.base_url}/api/policies")
        return response.json()

# Usage
client = GovernanceAgentClient()

# Chat
result = client.chat("What is GDPR?")
print(result['response'])

# Validate data
customer_data = {
    "email": "user@example.com",
    "age": 25,
    "country": "US"
}
validation = client.validate(customer_data, "basic_validation")
print(f"Valid: {validation['valid']}, Score: {validation['score']}")

# Upload file
file_result = client.upload_file(
    "customer_data.json", 
    policy="customer_onboarding",
    prompt="What validation errors exist?"
)
print(file_result['prompt_response'])
```

---

## Rate Limits
No rate limits currently implemented for local development.

## CORS
CORS is enabled for all origins in development mode.

## File Upload Limits
- Maximum file size: 16MB
- Supported formats: JSON, TXT, CSV
- Files are automatically deleted after processing

---

## Integration Examples

### React/JavaScript
```javascript
const GovernanceAPI = {
  baseURL: 'http://localhost:5000',
  
  async chat(message) {
    const response = await fetch(`${this.baseURL}/api/chat`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message})
    });
    return response.json();
  },
  
  async validate(data, policy) {
    const response = await fetch(`${this.baseURL}/api/validate`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({data, policy})
    });
    return response.json();
  }
};

// Usage
const result = await GovernanceAPI.chat("Explain GDPR requirements");
console.log(result.response);
```

### cURL Examples
```bash
# System status
curl -X GET http://localhost:5000/api/status

# Chat
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is KYC?"}'

# Validation
curl -X POST http://localhost:5000/api/validate \
  -H "Content-Type: application/json" \
  -d '{"data": {"email": "test@example.com", "age": 25}, "policy": "basic_validation"}'

# File upload
curl -X POST http://localhost:5000/api/upload \
  -F "file=@data.json" \
  -F "policy=customer_onboarding" \
  -F "prompt=What errors exist?"

# Get policies
curl -X GET http://localhost:5000/api/policies
```