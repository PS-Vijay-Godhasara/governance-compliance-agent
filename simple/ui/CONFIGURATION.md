# Governance Agent Configuration Guide

## 🎛️ Available Configuration Options

### 🤖 AI Features
- **Advanced LLM Responses** (`USE_LLM`): Enable/disable AI-powered natural language processing
- **Auto Data Validation** (`AUTO_VALIDATION`): Automatically validate JSON data found in messages
- **Auto Policy Detection** (`AUTO_POLICY_DETECTION`): Automatically select best validation policy based on data

### 🛡️ Compliance Features
- **Risk Assessment** (`RISK_ASSESSMENT`): Enable comprehensive risk scoring and analysis
- **AML Screening** (`AML_SCREENING`): Anti-Money Laundering transaction screening
- **KYC Validation** (`KYC_VALIDATION`): Know Your Customer identity verification
- **GDPR Analysis** (`GDPR_ANALYSIS`): EU data protection regulation compliance checking
- **Sanctions Screening** (`SANCTIONS_SCREENING`): Check against sanctions lists (requires external API)
- **PEP Screening** (`PEP_SCREENING`): Politically Exposed Person screening (requires external API)

### 📊 Validation Thresholds
- **High Risk Amount** (`HIGH_RISK_AMOUNT`): Transaction amount threshold for high-risk classification (default: $50,000)
- **AML Threshold** (`AML_THRESHOLD`): Amount requiring AML reporting (default: $10,000)
- **KYC Expiry Days** (`KYC_EXPIRY_DAYS`): Days before KYC documents expire (default: 30)
- **Risk Score Threshold** (`RISK_SCORE_THRESHOLD`): Minimum score for risk flagging (default: 0.7)

### 📁 File Processing
- **Max File Size** (`MAX_FILE_SIZE`): Maximum upload size in bytes (default: 16MB)
- **Allowed File Types** (`ALLOWED_FILE_TYPES`): Comma-separated list of allowed extensions
- **Auto File Analysis** (`AUTO_FILE_ANALYSIS`): Automatically analyze uploaded files
- **File Content Preview** (`FILE_CONTENT_PREVIEW`): Show file content previews in responses

### 📋 Logging & Audit
- **Audit Logging** (`AUDIT_LOGGING`): Log all validation and compliance activities
- **Compliance Reporting** (`COMPLIANCE_REPORTING`): Generate compliance reports
- **Violation Alerts** (`VIOLATION_ALERTS`): Send alerts for policy violations
- **Performance Monitoring** (`PERFORMANCE_MONITORING`): Monitor system performance metrics

## 🔧 Configuration Methods

### 1. Environment Variables (.env file)
```bash
# AI Features
USE_LLM=true
AUTO_VALIDATION=true
AUTO_POLICY_DETECTION=true

# Compliance Features
RISK_ASSESSMENT=true
AML_SCREENING=true
KYC_VALIDATION=true
GDPR_ANALYSIS=true
SANCTIONS_SCREENING=false
PEP_SCREENING=false

# Validation Thresholds
HIGH_RISK_AMOUNT=50000
AML_THRESHOLD=10000
RISK_SCORE_THRESHOLD=0.7

# File Processing
MAX_FILE_SIZE=16777216
ALLOWED_FILE_TYPES=json,txt,csv,pdf
AUTO_FILE_ANALYSIS=true

# Logging & Audit
AUDIT_LOGGING=true
COMPLIANCE_REPORTING=true
VIOLATION_ALERTS=true
```

### 2. Web UI Settings Panel
- Click the ⚙️ Settings button in the header
- Toggle features on/off with checkboxes
- Adjust thresholds with number inputs
- Save configuration (requires restart)

### 3. API Configuration
```javascript
// Get current configuration
fetch('/api/config')
  .then(response => response.json())
  .then(config => console.log(config));

// Update configuration
fetch('/api/config', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    governance_features: {
      aml_screening: false,
      risk_assessment: true
    }
  })
});
```

## 🎯 Recommended Configurations

### Development Environment
```bash
USE_LLM=true
AUTO_VALIDATION=true
RISK_ASSESSMENT=true
AML_SCREENING=false
SANCTIONS_SCREENING=false
PEP_SCREENING=false
AUDIT_LOGGING=false
DEBUG=true
```

### Production Environment
```bash
USE_LLM=true
AUTO_VALIDATION=true
RISK_ASSESSMENT=true
AML_SCREENING=true
KYC_VALIDATION=true
GDPR_ANALYSIS=true
SANCTIONS_SCREENING=true
PEP_SCREENING=true
AUDIT_LOGGING=true
COMPLIANCE_REPORTING=true
VIOLATION_ALERTS=true
DEBUG=false
```

### High-Security Environment
```bash
USE_LLM=false
AUTO_VALIDATION=true
RISK_ASSESSMENT=true
AML_SCREENING=true
KYC_VALIDATION=true
SANCTIONS_SCREENING=true
PEP_SCREENING=true
HIGH_RISK_AMOUNT=25000
AML_THRESHOLD=5000
RISK_SCORE_THRESHOLD=0.5
AUDIT_LOGGING=true
VIOLATION_ALERTS=true
```

### Minimal Configuration
```bash
USE_LLM=false
AUTO_VALIDATION=true
AUTO_POLICY_DETECTION=false
RISK_ASSESSMENT=false
AML_SCREENING=false
KYC_VALIDATION=true
GDPR_ANALYSIS=false
AUDIT_LOGGING=false
```

## 🔄 Configuration Impact

### When AUTO_VALIDATION is enabled:
- JSON data in messages is automatically validated
- Appropriate policies are selected based on data fields
- Validation results appear in chat responses

### When RISK_ASSESSMENT is enabled:
- Transaction amounts are evaluated against thresholds
- Risk scores are calculated for customers and transactions
- High-risk indicators are flagged in responses

### When AML_SCREENING is enabled:
- Transactions above AML_THRESHOLD are flagged
- Source of funds validation is required
- Suspicious activity patterns are detected

### When GDPR_ANALYSIS is enabled:
- Personal data processing is evaluated
- Data retention requirements are checked
- Privacy rights compliance is assessed

## 🚨 Important Notes

### Security Considerations
- **Sanctions/PEP Screening**: Requires external API keys and should only be enabled with proper credentials
- **Audit Logging**: Stores sensitive validation data - ensure proper data protection
- **File Processing**: Large files can impact performance - adjust MAX_FILE_SIZE accordingly

### Performance Impact
- **LLM Features**: Require Ollama service and impact response times
- **Auto Validation**: Adds processing overhead to all messages
- **Risk Assessment**: Complex calculations may slow down responses
- **Audit Logging**: Increases storage requirements

### Compliance Requirements
- **AML Screening**: May be legally required for financial institutions
- **KYC Validation**: Required for customer onboarding in regulated industries
- **GDPR Analysis**: Mandatory for EU data processing
- **Audit Logging**: Often required for regulatory compliance

## 🔧 Troubleshooting

### Configuration Not Loading
1. Check .env file syntax
2. Verify file permissions
3. Restart the application
4. Check console logs for errors

### Features Not Working
1. Verify feature is enabled in configuration
2. Check external service dependencies (Ollama for LLM)
3. Review API keys for external services
4. Check system logs for error messages

### Performance Issues
1. Disable non-essential features
2. Reduce file size limits
3. Adjust validation thresholds
4. Monitor system resources

The configuration system provides fine-grained control over all governance and compliance features, allowing you to customize the system for your specific requirements and regulatory environment.