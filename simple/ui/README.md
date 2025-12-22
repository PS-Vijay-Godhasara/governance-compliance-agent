# Governance Agent Web UI

Web-based chat interface for the Governance & Compliance Agent with file upload and validation capabilities.

## 🚀 Quick Start

1. **Install dependencies:**
```bash
cd simple/ui
pip install -r requirements.txt
```

2. **Configure LLM (Optional):**
```bash
# For advanced AI responses, start Ollama
ollama serve
ollama pull llama3.2:3b

# Edit .env file
USE_LLM=true
```

3. **Start the web server:**
```bash
python app.py
```

4. **Open browser:** `http://localhost:5000`

## 🎯 Complete Usage Examples

### 1. Chat Interface Examples

**Basic Questions:**
- "What is GDPR and how does it affect customer validation?"
- "Explain KYC requirements for financial services"
- "Why did my customer validation fail?"
- "Create a policy for premium customers with minimum $50,000 balance"

**Expected Responses:**
- **With LLM:** Detailed, contextual explanations
- **Without LLM:** Rule-based responses with key information

### 2. Quick Validation Examples

**Valid Customer Data:**
```json
{
  "email": "john.doe@company.com",
  "age": 28,
  "phone": "+1234567890",
  "country": "US",
  "balance": 75000
}
```
**Result:** ✅ Status: VALID (Score: 1.0)

**Invalid Customer Data:**
```json
{
  "email": "invalid-email",
  "age": 16,
  "country": "US",
  "balance": 1000
}
```
**Result:** ❌ Status: INVALID (Score: 0.6)
**Violations:** Email format invalid, Age below minimum 18

**KYC Validation:**
```json
{
  "identity_documents": [
    {"type": "passport", "number": "A12345678", "expiry": "2025-12-31"}
  ],
  "date_of_birth": "1990-05-15",
  "full_name": "John Smith"
}
```
**Policy:** KYC Validation
**Result:** ✅ Complete documentation provided

### 3. File Upload & Analysis

**JSON File Validation:**
1. Upload `valid_customer.json` (provided in sample_data/)
2. Select "Customer Onboarding" policy
3. Get instant validation results with explanations

**Text File Compliance Analysis:**
1. Upload `privacy_policy.txt` (provided in sample_data/)
2. Get AI-powered compliance analysis
3. Receive GDPR/CCPA compliance recommendations

**CSV Data Processing:**
1. Upload customer data CSV
2. Get bulk validation insights
3. Identify compliance gaps

### 4. Interactive Workflows

**Scenario 1: Customer Onboarding Review**
1. **Chat:** "I need to validate a new customer application"
2. **Agent:** "I can help! Please provide the customer data or upload a file"
3. **Upload:** customer_data.json
4. **Result:** Validation report with specific recommendations
5. **Follow-up Chat:** "Why was the email validation flagged?"
6. **Agent:** Detailed explanation of email format requirements

**Scenario 2: Policy Creation**
1. **Chat:** "Create a policy for high-value transactions over $100,000"
2. **Agent:** Generates policy structure with validation rules
3. **Validation:** Test the new policy with sample data
4. **Refinement:** Ask for modifications based on results

**Scenario 3: Compliance Audit**
1. **Upload:** privacy_policy.txt
2. **Analysis:** GDPR compliance assessment
3. **Chat:** "What are the main compliance risks identified?"
4. **Agent:** Prioritized list of compliance gaps and solutions

## 📊 Expected Results

### Validation Results Format
```json
{
  "valid": true,
  "score": 0.85,
  "violations": ["Age below minimum 21 for premium account"],
  "explanation": "Customer meets most requirements but age restriction applies for premium services"
}
```

### Chat Response Examples

**GDPR Question:**
```
User: What is GDPR?
Agent: GDPR (General Data Protection Regulation) is EU legislation that:
• Requires explicit consent for data processing
• Grants individuals rights to access, correct, and delete data
• Mandates data breach notifications within 72 hours
• Applies to any organization processing EU residents' data
• Penalties up to 4% of annual revenue for violations
```

**Policy Creation:**
```
User: Create a policy for premium customers
Agent: I'll create a premium customer policy with these requirements:
• Minimum age: 21
• Minimum balance: $50,000
• Valid government ID required
• Credit score above 700
• Enhanced KYC documentation
Would you like me to add specific validation rules?
```

## 🔧 Configuration Options

### Environment Variables (.env)
```bash
# LLM Configuration
USE_LLM=true                    # Enable/disable AI responses
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b

# System Configuration
POLICIES_DIR=../policies        # Policy files location
KNOWLEDGE_DIR=../knowledge      # Knowledge base location
PORT=5000                       # Web server port
DEBUG=true                      # Debug mode
```

### Policy Selection
- **Customer Onboarding:** Basic customer validation
- **KYC Validation:** Identity verification requirements
- **Risk Assessment:** Transaction risk evaluation
- **Custom Policies:** Create via chat or file upload

## 🎨 UI Features

### Status Indicators
- 🤖 **LLM Mode:** Advanced AI responses enabled
- ⚡ **Basic Mode:** Rule-based responses (LLM disabled)
- ✅ **Valid:** Data passes all validation rules
- ❌ **Invalid:** Data has violations requiring attention

### Interactive Elements
- **Real-time chat** with typing indicators
- **File drag-and-drop** upload area
- **Policy dropdown** with descriptions
- **Validation scores** with color coding
- **Expandable results** with detailed explanations

## 🔍 Troubleshooting

### Common Issues

**"Failed to fetch" Error:**
- Check if server is running on port 5000
- Verify policies directory exists
- Check console for initialization errors

**LLM Not Working:**
```bash
# Check Ollama status
ollama list

# Restart Ollama service
ollama serve

# Pull required model
ollama pull llama3.2:3b
```

**Validation Errors:**
- Verify JSON format in quick validation
- Check policy exists in policies directory
- Ensure required fields are provided

**File Upload Issues:**
- Max file size: 16MB
- Supported formats: JSON, TXT, CSV
- Check file permissions

### Debug Mode
Enable debug logging:
```bash
DEBUG=true python app.py
```

## 📁 Sample Data

Use provided sample files in `sample_data/`:
- `valid_customer.json` - Complete customer data
- `invalid_customer.json` - Data with validation errors
- `kyc_complete.json` - KYC documentation example
- `privacy_policy.txt` - Compliance analysis sample

## 🚀 Advanced Usage

### API Integration
```javascript
// Chat API
fetch('/api/chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({message: 'What is GDPR?'})
})

// Validation API
fetch('/api/validate', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    data: {email: 'test@example.com', age: 25},
    policy: 'customer_onboarding'
  })
})
```

### Custom Policy Creation
1. **Via Chat:** "Create a policy for international transfers"
2. **Via File:** Upload policy JSON structure
3. **Via API:** POST to `/api/policies` endpoint

The UI provides a complete governance and compliance validation experience with both basic and advanced AI-powered features!