# Governance Agent - Unified Interface

Intelligent governance and compliance assistant with automatic data detection, validation, and contextual analysis.

## 🎆 Revolutionary Features

### 🤖 Smart Auto-Detection
- **Automatic Data Recognition**: Paste JSON anywhere in your message - I'll detect and validate it
- **Intelligent Policy Matching**: Auto-selects the best validation policy based on data fields
- **Context-Aware Responses**: Combines chat, validation, and analysis in one seamless experience
- **File Intelligence**: Upload any document and ask specific questions about it

### 💬 Natural Conversation Flow
- Chat naturally about compliance topics
- Paste data directly in messages for instant analysis
- Upload files and ask questions in the same interface
- Get comprehensive responses with validation results

## 🚀 Quick Start

1. **Install dependencies:**
```bash
cd simple/ui
pip install -r requirements.txt
```

2. **Start the server:**
```bash
python app.py
```

3. **Open browser:** `http://localhost:5000`

## 🎯 Complete Test Scenarios

### 1. Natural Chat Examples

**Basic Compliance Questions:**
```
💬 "What is GDPR and how does it affect customer data processing?"
💬 "Explain KYC requirements for financial institutions"
💬 "What are the penalties for AML violations?"
💬 "How do I handle a GDPR data deletion request?"
```

**Policy Creation Requests:**
```
💬 "Create a policy for premium customers with minimum $100,000 balance"
💬 "I need validation rules for international wire transfers"
💬 "Design a KYC policy for high-risk customers"
```

### 2. Smart Data Validation

**Simple Customer Data:**
```
{"email": "john@example.com", "age": 28, "country": "US"} - Is this customer data valid?
```
**Auto-detects**: Basic customer validation policy
**Result**: ✅ Validation + contextual explanation

**Premium Customer:**
```
{"email": "premium@example.com", "age": 35, "balance": 75000, "full_name": "Jane Smith", "phone": "+1234567890"} - Can this customer access premium services?
```
**Auto-detects**: Premium customer policy
**Result**: ✅ Validation + premium eligibility analysis

**Transaction Data:**
```
{"amount": 25000, "currency": "USD", "recipient_account": "ACC123", "transaction_type": "wire_transfer", "country": "SG"} - Does this need AML screening?
```
**Auto-detects**: Transaction validation policy
**Result**: ⚠️ Validation + AML risk assessment

**KYC Documentation:**
```
{"identity_documents": [{"type": "passport", "expiry": "2025-12-31"}], "date_of_birth": "1990-05-15", "full_name": "John Smith"} - Is KYC complete?
```
**Auto-detects**: KYC validation policy
**Result**: ✅ Validation + completeness check

### 3. Advanced File Analysis

**Complex Customer Profile:**
1. **Upload**: `complex_customer.json`
2. **Ask**: "What compliance risks does this customer profile present?"
3. **Get**: Comprehensive risk analysis with specific recommendations

**High-Risk Transaction:**
1. **Upload**: `high_risk_transaction.json`
2. **Ask**: "Should this transaction be approved or flagged for review?"
3. **Get**: Detailed risk assessment with regulatory guidance

**Policy Document Review:**
1. **Upload**: `aml_policy.txt`
2. **Ask**: "Is this AML policy compliant with current regulations?"
3. **Get**: Gap analysis with improvement recommendations

### 4. Multi-Modal Scenarios

**Scenario A: Customer Onboarding Review**
```
Step 1: Upload customer_data.json
Step 2: Ask "Is this customer eligible for our premium services?"
Step 3: Get validation + eligibility analysis
Step 4: Follow up: "What additional documentation do we need?"
Step 5: Get specific KYC requirements
```

**Scenario B: Transaction Risk Assessment**
```
Step 1: Paste transaction JSON in chat
Step 2: Ask "What are the AML risks for this transaction?"
Step 3: Get automatic validation + risk analysis
Step 4: Upload supporting policy document
Step 5: Ask "Does our policy cover this scenario?"
Step 6: Get policy gap analysis
```

**Scenario C: Compliance Audit Preparation**
```
Step 1: Upload privacy_policy.txt
Step 2: Ask "What GDPR compliance gaps exist?"
Step 3: Get detailed gap analysis
Step 4: Paste sample customer data
Step 5: Ask "How should we handle data deletion requests?"
Step 6: Get procedural guidance
```

## 📋 Sample Data Files

### JSON Validation Files
- `basic_customer.json` - Simple customer for basic validation
- `complex_customer.json` - Complete customer profile with KYC, risk assessment
- `high_risk_transaction.json` - Cross-border high-value transaction
- `premium_customer.json` - High-value customer profile
- `transaction_sample.json` - Standard transaction data
- `aml_sample.json` - AML compliance screening data
- `kyc_complete.json` - Complete KYC documentation
- `gdpr_complaint.json` - GDPR deletion request scenario

### Policy Documents
- `aml_policy.txt` - Comprehensive AML policy document
- `data_retention_policy.txt` - Data retention compliance policy
- `privacy_policy.txt` - Privacy policy for GDPR analysis

## 🎆 Advanced Use Cases

### 1. Regulatory Change Impact Analysis
```
Upload: current_policy.txt
Ask: "How will the new EU AI Act affect this policy?"
Get: Impact analysis with required changes
```

### 2. Cross-Jurisdictional Compliance
```
Paste: {"customer_country": "DE", "transaction_country": "US", "amount": 50000}
Ask: "What compliance requirements apply to this cross-border transaction?"
Get: Multi-jurisdiction analysis
```

### 3. Risk Scoring and Mitigation
```
Upload: customer_profile.json
Ask: "Calculate the risk score and suggest mitigation measures"
Get: Quantitative risk assessment with actionable recommendations
```

### 4. Policy Optimization
```
Upload: existing_policy.txt
Ask: "How can we optimize this policy for better efficiency while maintaining compliance?"
Get: Optimization recommendations with risk-benefit analysis
```

### 5. Incident Response Planning
```
Paste: {"incident_type": "data_breach", "affected_records": 1000, "countries": ["US", "EU"]}
Ask: "What are our notification obligations and timeline?"
Get: Step-by-step incident response plan
```

## 🔍 Testing Checklist

### Basic Functionality
- [ ] Natural language chat responses
- [ ] JSON data auto-detection in messages
- [ ] File upload with contextual questions
- [ ] Automatic policy selection
- [ ] Validation result display

### Data Validation
- [ ] Customer data validation (basic, premium, KYC)
- [ ] Transaction validation (domestic, international)
- [ ] AML compliance screening
- [ ] Document completeness checks
- [ ] Risk assessment calculations

### File Analysis
- [ ] JSON file validation with custom questions
- [ ] Text document compliance analysis
- [ ] Policy gap identification
- [ ] Regulatory mapping
- [ ] Multi-document comparison

### Edge Cases
- [ ] Invalid JSON handling
- [ ] Large file processing
- [ ] Multiple data types in one message
- [ ] Conflicting validation results
- [ ] Missing required fields

## 📊 Expected Results

### Chat Response Format
```
User: What is GDPR?
Agent: GDPR (General Data Protection Regulation) is EU legislation that...
       • Requires explicit consent for data processing
       • Grants individuals rights to access and delete data
       • Mandates breach notifications within 72 hours
       • Applies to any organization processing EU residents' data
```

### Data Validation Format
```
User: {"email": "test@example.com", "age": 25} - Is this valid?
Agent: I've analyzed your customer data and here's what I found:
       • Email format is valid
       • Age meets minimum requirements
       • Missing required phone number for full onboarding

📋 Validation Result: VALID ✅ (Score: 0.8)
Policy Used: Basic Customer Validation
Recommendation: Add phone number to complete profile
```

### File Analysis Format
```
User: [Uploads policy.txt] "Is this GDPR compliant?"
Agent: I've analyzed your policy document for GDPR compliance:
       • Covers most GDPR requirements effectively
       • Strong data subject rights section
       • Clear retention periods specified
       ⚠️ Gap: Missing explicit consent mechanisms
       ⚠️ Gap: No data breach notification procedures

📁 File: policy.txt
Compliance Level: 85% - Good with minor gaps
Priority Actions: Add consent management, breach procedures
```

## 🔧 Configuration

### Environment Variables (.env)
```bash
USE_LLM=true                    # Enable AI responses
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
POLICIES_DIR=../policies        # Policy files location
PORT=5000                       # Web server port
DEBUG=true                      # Debug mode
```

### Auto-Detection Rules
- **Basic Customer**: email, age fields present
- **Premium Customer**: balance >= 50000
- **Transaction**: amount, currency fields present
- **KYC**: identity_documents field present
- **AML**: transaction_amount, source_of_funds present

## 📚 API Documentation

### Unified Endpoint
**POST** `/api/unified`

Handles all interactions - chat, data validation, file upload:

```javascript
// Chat message
fetch('/api/unified', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({message: 'What is GDPR?'})
})

// Message with JSON data
fetch('/api/unified', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({message: '{"email": "test@example.com"} - Is this valid?'})
})

// File upload with question
const formData = new FormData();
formData.append('file', file);
formData.append('message', 'Is this policy compliant?');
fetch('/api/unified', {method: 'POST', body: formData})
```

## 🎆 Why This Approach is Revolutionary

### Traditional Approach
- Separate tools for chat, validation, file analysis
- Manual policy selection
- Disconnected workflows
- Context switching between interfaces

### Our Unified Approach
- **Single Interface**: Everything in one chat window
- **Auto-Detection**: Intelligent recognition of data types
- **Contextual Analysis**: Combines multiple analysis types
- **Natural Workflow**: Chat naturally, get comprehensive results

### Benefits
- **50% Faster**: No interface switching
- **Higher Accuracy**: Auto-policy selection
- **Better UX**: Natural conversation flow
- **Comprehensive**: Multiple analysis types in one response

The unified interface represents the future of governance and compliance tools - intelligent, contextual, and effortlessly integrated into natural workflows.

## 🎯 Complete Validation Examples

### 1. Basic Customer Validation ✅
**Use Case:** Quick signup with minimal requirements

**Sample Data:**
```json
{
  "email": "user@example.com",
  "age": 25,
  "country": "US",
  "balance": 50000
}
```
**Policy:** Basic Customer Validation
**Result:** ✅ Status: VALID (Score: 1.0)
**Why it works:** Only email and age are required

### 2. Customer Onboarding (Full) ⚠️
**Use Case:** Complete account setup with all details

**Sample Data (Invalid):**
```json
{
  "email": "user@example.com",
  "age": 25,
  "country": "US",
  "balance": 50000
}
```
**Policy:** Customer Onboarding (Full)
**Result:** ❌ Status: INVALID (Score: 0.6)
**Violations:** Missing required field: phone, Missing required field: full_name

**Sample Data (Valid):**
```json
{
  "email": "john.doe@company.com",
  "age": 28,
  "phone": "+1234567890",
  "full_name": "John Doe",
  "country": "US",
  "balance": 75000
}
```
**Result:** ✅ Status: VALID (Score: 1.0)

### 3. Premium Customer Validation 💎
**Use Case:** High-value customer with enhanced requirements

**Sample Data:**
```json
{
  "email": "premium@example.com",
  "age": 35,
  "full_name": "Jane Premium Customer",
  "phone": "+1234567890",
  "balance": 75000,
  "country": "US"
}
```
**Policy:** Premium Customer
**Result:** ✅ Status: VALID (Score: 1.0)
**Requirements:** Age 21+, $50K+ balance, full contact info

### 4. Transaction Validation 💸
**Use Case:** Financial transaction compliance

**Sample Data:**
```json
{
  "amount": 15000,
  "currency": "USD",
  "recipient_account": "ACC123456789",
  "transaction_type": "transfer",
  "country": "CA"
}
```
**Policy:** Transaction Validation
**Result:** ✅ Status: VALID (Score: 1.0)
**Checks:** Amount limits, currency format, account validity

### 5. KYC Validation 🆔
**Use Case:** Identity verification for compliance

**Sample Data:**
```json
{
  "identity_documents": [
    {"type": "passport", "number": "A12345678", "expiry": "2025-12-31"}
  ],
  "date_of_birth": "1990-05-15",
  "full_name": "John Smith",
  "address": "123 Main St, City, State 12345"
}
```
**Policy:** KYC Validation
**Result:** ✅ Status: VALID (Score: 1.0)
**Requirements:** Valid ID documents, personal information

### 6. AML Compliance Check 🛡️
**Use Case:** Anti-Money Laundering screening

**Sample Data:**
```json
{
  "customer_id": "CUST001",
  "transaction_amount": 25000,
  "source_of_funds": "salary",
  "risk_country": false,
  "pep_status": false,
  "sanctions_check": true
}
```
**Policy:** AML Compliance
**Result:** ✅ Status: VALID (Score: 1.0)
**Checks:** Source of funds, sanctions screening, PEP status

## 📋 Policy Comparison

| Policy | Required Fields | Min Age | Special Requirements |
|--------|----------------|---------|---------------------|
| **Basic Validation** | email, age | 18 | Minimal signup |
| **Customer Onboarding** | email, age, phone, full_name | 18 | Complete profile |
| **Premium Customer** | email, age, full_name, phone, balance, country | 21 | $50K+ balance |
| **Transaction** | amount, currency, recipient_account, transaction_type | - | Valid transaction data |
| **KYC** | identity_documents, date_of_birth | - | Identity verification |
| **AML** | customer_id, transaction_amount, source_of_funds, sanctions_check | - | Compliance screening |

## 📝 File Upload with Custom Prompts

### Interactive Document Analysis
Upload any document and ask specific questions about it:

**Example 1: Policy Document Analysis**
1. **Upload:** `data_retention_policy.txt`
2. **Prompt:** "Is this policy GDPR compliant? What are the potential risks?"
3. **Expected Response:** Detailed GDPR compliance analysis with specific recommendations

**Example 2: Customer Data Validation**
1. **Upload:** `gdpr_complaint.json`
2. **Prompt:** "How should we handle this GDPR deletion request? What data can we legally retain?"
3. **Expected Response:** Step-by-step guidance on GDPR compliance and data retention

**Example 3: Transaction Analysis**
1. **Upload:** `transaction_sample.json`
2. **Prompt:** "Does this transaction require additional AML screening? What are the risk factors?"
3. **Expected Response:** Risk assessment with AML compliance recommendations

### Sample Prompts by Use Case

**📊 Validation Questions:**
- "What validation errors exist in this data?"
- "Is this customer eligible for premium services?"
- "Does this transaction meet compliance requirements?"
- "What fields are missing for complete KYC?"

**🛡️ Compliance Questions:**
- "Is this document GDPR compliant?"
- "What are the data retention requirements?"
- "How should we handle this privacy request?"
- "What are the AML risks in this transaction?"

**📝 Policy Questions:**
- "What policy violations are present?"
- "How can we improve this policy document?"
- "What regulatory requirements are missing?"
- "Is this policy up to date with current regulations?"

**🔍 Risk Assessment Questions:**
- "What are the main risk factors?"
- "Should this transaction be flagged for review?"
- "What additional documentation is needed?"
- "How can we mitigate these compliance risks?"

### Advanced Prompt Examples

**Multi-part Analysis:**
```
Prompt: "Analyze this customer data for: 1) GDPR compliance, 2) KYC completeness, 3) Risk factors, 4) Required actions"
```

**Comparative Analysis:**
```
Prompt: "Compare this policy against GDPR Article 5 requirements and identify gaps"
```

**Scenario-based Questions:**
```
Prompt: "If this customer requests data deletion, what can we legally retain and why?"
```

**Regulatory Mapping:**
```
Prompt: "Map this transaction data to AML reporting requirements and identify missing fields"
```

## 📋 Sample Files for Testing

### JSON Validation Files
- `basic_customer.json` - Simple customer data for basic validation
- `premium_customer.json` - Complete premium customer profile
- `transaction_sample.json` - Financial transaction data
- `aml_sample.json` - AML compliance screening data
- `kyc_complete.json` - Complete KYC documentation
- `gdpr_complaint.json` - GDPR deletion request scenario

### Text Analysis Files
- `privacy_policy.txt` - Privacy policy for GDPR analysis
- `data_retention_policy.txt` - Data retention policy document

### Sample Prompt Combinations

**File + Prompt Examples:**

1. **`gdpr_complaint.json`** + "How should we handle this GDPR deletion request?"
2. **`data_retention_policy.txt`** + "Is this policy compliant with current regulations?"
3. **`premium_customer.json`** + "What additional verification is needed for this customer?"
4. **`transaction_sample.json`** + "Does this transaction require AML reporting?"
5. **`privacy_policy.txt`** + "What are the main compliance gaps in this policy?"

### Quick Prompt Suggestions
The UI now includes a dropdown with common prompts:
- "What validation errors exist?"
- "Is this GDPR compliant?"
- "What are the compliance risks?"
- "Does this meet KYC requirements?"
- "What documentation is needed?"
- "How to handle this issue?"
- "What are regulatory requirements?"
- "Is screening required?"

### Complete Prompt Library
See **[PROMPT_LIBRARY.md](PROMPT_LIBRARY.md)** for 100+ categorized prompts covering:
- Validation questions
- Policy analysis
- Risk assessment
- Compliance scenarios
- Process improvement

### API Documentation
See **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** for complete API reference including:
- All endpoints with examples
- Request/response formats
- Error handling
- Python SDK
- Integration examples

### Expected Workflow
1. **Upload** any sample file
2. **Write** a specific question in the prompt box
3. **Get** contextual analysis combining file content with your question
4. **Follow up** in chat for additional clarification

## 🎨 UI Testing Guide

### Quick Test Scenarios

**✅ Success Cases:**
- Basic validation with minimal data
- Premium customer with complete profile
- Valid transaction within limits
- Complete KYC documentation

**❌ Failure Cases:**
- Underage customer (age < 18)
- Invalid email format
- Missing required phone number
- Transaction amount exceeding limits
- Incomplete KYC documents

**⚠️ Edge Cases:**
- Exactly minimum age (18/21)
- Maximum transaction amounts
- International phone numbers
- Multiple identity documents
- High-risk country transactions

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