# Examples for Governance Agent

This directory contains practical examples for both simple and multi-agent architectures.

## 🚀 Simple Architecture Examples

### Basic Usage (`basic_usage.py`)
```bash
cd simple/examples
python basic_usage.py
```
**Covers:**
- Basic validation examples
- RAG knowledge search
- MCP tool execution

### Interactive LLM Agent (`interactive_llm.py`)
```bash
cd simple/examples
python interactive_llm.py --interactive
```
**Features:**
- Natural language conversation with governance agent
- Real-time validation explanations
- Policy creation from text
- Context-aware responses

**Sample Interaction:**
```
You: What is GDPR and how does it affect customer validation?
Agent: GDPR is the EU General Data Protection Regulation that requires...

You: validate
Agent: I can help you validate data! Here are some examples...

You: explain why email validation failed
Agent: Email validation failed because the format doesn't match...
```

### Business Scenarios (`business_scenarios.py`)
```bash
cd simple/examples
python business_scenarios.py
```
**Scenarios:**
- Customer onboarding workflows
- KYC compliance checks
- Risk assessment examples
- Regulatory compliance validation

### Sample Prompts (`sample_prompts.py`)
```bash
cd simple/examples
python sample_prompts.py
```
**Categories:**
- 70+ sample prompts across 9 categories
- Validation, policy, compliance questions
- Natural language policy creation
- Troubleshooting scenarios

## 🏢 Multi-Agent Architecture Examples

### Multi-Agent Workflows (`multi_agent_workflows.py`)
```bash
cd multi-agent/examples
python multi_agent_workflows.py
```
**Features:**
- Agent coordination examples
- Complex workflow orchestration
- Enterprise-level scenarios
- Bulk processing examples

## 📋 Usage Guide

### 1. Interactive LLM Communication

**Start Interactive Mode:**
```bash
cd simple/examples
python interactive_llm.py --interactive
```

**Available Commands:**
- `validate` - Learn about data validation
- `policy` - Get policy information
- `explain` - Get violation explanations
- `help` - Show available commands
- `quit` - Exit the chat

**Natural Language Features:**
- Ask questions in plain English
- Get contextual explanations
- Create policies from descriptions
- Receive actionable suggestions

### 2. Sample Prompts for Testing

**Validation Questions:**
- "How do I validate customer email addresses?"
- "What are the age requirements for customer onboarding?"
- "Why is my customer validation failing?"

**Policy Questions:**
- "Explain the customer onboarding policy"
- "How do I create a new policy?"
- "What are the KYC validation requirements?"

**Compliance Questions:**
- "What is GDPR and how does it affect customer data?"
- "Explain KYC requirements for financial services"
- "What are AML compliance obligations?"

**Natural Language Policy Creation:**
- "Create a policy for premium customers with minimum $50,000 balance"
- "I need a policy for international wire transfers over $10,000"
- "Make a policy for high-risk country transactions"

### 3. Business Scenarios

**Customer Onboarding:**
- Valid new customer approval
- Underage customer rejection
- Invalid email format handling
- Missing required fields

**KYC Compliance:**
- Complete documentation approval
- Expired document rejection
- Missing identity documents

**Risk Assessment:**
- Low-risk standard transactions
- High-value transaction approval
- High-risk geography flagging
- Young customer large transactions

### 4. LLM Integration Requirements

**Setup Ollama:**
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start service
ollama serve

# Pull model
ollama pull llama3.2:3b
```

**Without LLM:**
- Basic rule-based validation
- Simple explanations
- File-based knowledge search

**With LLM:**
- Natural language explanations
- Policy creation from text
- Context-aware responses
- Interactive conversations

## 🔧 Configuration

### Environment Setup
```bash
# Simple architecture
cd simple
pip install -r requirements.txt

# Multi-agent architecture
cd multi-agent
pip install -r requirements.txt
```

### LLM Configuration
```python
# Enable LLM features
orchestrator = SimpleOrchestrator(use_llm=True)

# Disable for testing
orchestrator = SimpleOrchestrator(use_llm=False)
```

## 📊 Expected Outputs

### Basic Validation
```
Basic Validation Examples
=========================

1. Valid Customer:
   Valid: True
   Score: 1.0

2. Invalid Customer:
   Valid: False
   Violations: ['Email format is invalid', 'Age below minimum requirement']
```

### Interactive LLM
```
Interactive Governance Agent with LLM
====================================
Ask questions about policies, validation, or compliance!

You: What is GDPR?
Agent: GDPR is the EU General Data Protection Regulation that establishes 
strict rules for how organizations collect, process, and store personal data...
```

### Business Scenarios
```
Customer Onboarding Scenarios
============================

1. Valid New Customer:
   Status: APPROVED
   Score: 1.00

2. Underage Customer:
   Status: REJECTED
   Score: 0.80
   Issues:
   - Age below minimum 18
```

## 🎯 Use Cases

### Development & Testing
- **Prototype validation** - Quick testing of validation logic
- **Policy development** - Create and test new policies
- **Integration testing** - API and workflow testing

### Business Operations
- **Staff training** - Interactive learning about compliance
- **Customer support** - Understanding rejection reasons
- **Process optimization** - Workflow efficiency analysis

### Compliance & Audit
- **Regulatory testing** - GDPR, KYC, AML compliance
- **Documentation** - Policy explanations and justifications
- **Audit preparation** - Compliance evidence generation

Run the examples to see the governance agent in action with real-world scenarios and interactive capabilities!