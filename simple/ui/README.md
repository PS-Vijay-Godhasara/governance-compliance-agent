# Governance Agent Web UI

Web-based chat interface for the Governance & Compliance Agent with file upload and validation capabilities.

## Features

- **💬 Interactive Chat**: Natural language conversation with the governance agent
- **🔍 Quick Validation**: JSON data validation with policy selection
- **📁 File Upload**: Upload and analyze JSON, TXT, or CSV files
- **📋 Policy Management**: Select from available validation policies
- **🎯 Real-time Results**: Instant validation feedback with explanations

## Setup

1. Install dependencies:
```bash
cd simple/ui
pip install -r requirements.txt
```

2. Start the web server:
```bash
python app.py
```

3. Open browser to: `http://localhost:5000`

## Usage

### Chat Interface
- Ask questions about policies, validation, or compliance
- Get natural language explanations
- Request policy creation or modifications
- Troubleshoot validation issues

**Example Questions:**
- "What is GDPR and how does it affect customer validation?"
- "Why did my customer validation fail?"
- "Create a policy for premium customers"
- "Explain KYC requirements"

### Quick Validation
- Enter JSON data in the textarea
- Select validation policy
- Click "Validate Data" for instant results
- View validation score, violations, and explanations

**Example JSON:**
```json
{
  "email": "user@example.com",
  "age": 25,
  "country": "US",
  "balance": 50000
}
```

### File Upload
- Upload JSON files for validation
- Upload TXT/CSV files for compliance analysis
- Get detailed analysis and recommendations
- Automatic file cleanup after processing

**Supported Files:**
- `.json` - Data validation against policies
- `.txt` - Text analysis for compliance
- `.csv` - Structured data analysis

## API Endpoints

### POST /api/chat
Chat with the governance agent
```json
{
  "message": "What is GDPR?"
}
```

### POST /api/validate
Validate data against policies
```json
{
  "data": {"email": "test@example.com", "age": 25},
  "policy": "customer_onboarding"
}
```

### POST /api/upload
Upload files for analysis
- Form data with file and policy parameters

### GET /api/policies
Get available validation policies

## Configuration

- **Port**: 5000 (configurable in app.py)
- **Upload Limit**: 16MB max file size
- **LLM**: Enabled by default (requires Ollama)
- **Policies**: Loaded from `../policies/` directory

## Security Features

- Secure filename handling
- File size limits
- Automatic file cleanup
- Session management
- Input validation

## Troubleshooting

### LLM Not Available
If Ollama is not running, the chat will use basic responses:
```bash
# Start Ollama
ollama serve
ollama pull llama3.2:3b
```

### File Upload Issues
- Check file size (max 16MB)
- Verify file format (JSON, TXT, CSV)
- Ensure proper JSON formatting

### Policy Not Found
- Verify policy files exist in `../policies/`
- Check policy name spelling
- Use GET /api/policies to list available policies

## Development

### Adding New Features
1. Add route to `app.py`
2. Update HTML template
3. Add JavaScript handlers
4. Test with sample data

### Custom Styling
- Modify CSS in `templates/index.html`
- Add new components as needed
- Maintain responsive design

### API Extensions
- Add new validation endpoints
- Implement batch processing
- Add export functionality

Run the UI to interact with your governance agent through a user-friendly web interface!