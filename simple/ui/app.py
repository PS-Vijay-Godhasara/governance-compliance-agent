import os
import sys
import json
from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.orchestrator import SimpleOrchestrator

app = Flask(__name__)
app.secret_key = 'governance-agent-ui-key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configuration from environment
USE_LLM = os.getenv('USE_LLM', 'false').lower() == 'true'
POLICIES_DIR = os.getenv('POLICIES_DIR', '../policies')
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('DEBUG', 'true').lower() == 'true'

# Governance Features
AUTO_VALIDATION = os.getenv('AUTO_VALIDATION', 'true').lower() == 'true'
AUTO_POLICY_DETECTION = os.getenv('AUTO_POLICY_DETECTION', 'true').lower() == 'true'
RISK_ASSESSMENT = os.getenv('RISK_ASSESSMENT', 'true').lower() == 'true'
COMPLIANCE_CHECKING = os.getenv('COMPLIANCE_CHECKING', 'true').lower() == 'true'
AML_SCREENING = os.getenv('AML_SCREENING', 'true').lower() == 'true'
KYC_VALIDATION = os.getenv('KYC_VALIDATION', 'true').lower() == 'true'
GDPR_ANALYSIS = os.getenv('GDPR_ANALYSIS', 'true').lower() == 'true'
SANCTIONS_SCREENING = os.getenv('SANCTIONS_SCREENING', 'false').lower() == 'true'
PEP_SCREENING = os.getenv('PEP_SCREENING', 'false').lower() == 'true'

# Validation Thresholds
HIGH_RISK_AMOUNT = float(os.getenv('HIGH_RISK_AMOUNT', 50000))
AML_THRESHOLD = float(os.getenv('AML_THRESHOLD', 10000))
KYC_EXPIRY_DAYS = int(os.getenv('KYC_EXPIRY_DAYS', 30))
RISK_SCORE_THRESHOLD = float(os.getenv('RISK_SCORE_THRESHOLD', 0.7))

# File Processing
MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 16777216))
ALLOWED_FILE_TYPES = os.getenv('ALLOWED_FILE_TYPES', 'json,txt,csv,pdf').split(',')
AUTO_FILE_ANALYSIS = os.getenv('AUTO_FILE_ANALYSIS', 'true').lower() == 'true'
FILE_CONTENT_PREVIEW = os.getenv('FILE_CONTENT_PREVIEW', 'true').lower() == 'true'

# Logging and Audit
AUDIT_LOGGING = os.getenv('AUDIT_LOGGING', 'true').lower() == 'true'
COMPLIANCE_REPORTING = os.getenv('COMPLIANCE_REPORTING', 'true').lower() == 'true'
VIOLATION_ALERTS = os.getenv('VIOLATION_ALERTS', 'true').lower() == 'true'
PERFORMANCE_MONITORING = os.getenv('PERFORMANCE_MONITORING', 'false').lower() == 'true'

# Initialize orchestrator with error handling
try:
    orchestrator = SimpleOrchestrator(use_llm=USE_LLM, policies_dir=POLICIES_DIR)
    print(f"Orchestrator initialized successfully (LLM: {USE_LLM})")
except Exception as e:
    print(f"Error initializing orchestrator: {e}")
    print("Falling back to basic mode without LLM")
    try:
        orchestrator = SimpleOrchestrator(use_llm=False, policies_dir=POLICIES_DIR)
        USE_LLM = False
        print("Orchestrator initialized in basic mode")
    except Exception as e2:
        print(f"Failed to initialize orchestrator: {e2}")
        orchestrator = None

@app.route('/')
def index():
    """Main chat interface"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        if orchestrator is None:
            return jsonify({'error': 'Orchestrator not initialized'}), 500
            
        data = request.json
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Process message through orchestrator
        response = orchestrator.process_natural_language(message)
        
        return jsonify({
            'response': response,
            'session_id': session['session_id']
        })
    
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({'error': f'Error processing message: {str(e)}'}), 500

@app.route('/api/validate', methods=['POST'])
def validate_data():
    """Handle data validation requests"""
    try:
        if orchestrator is None:
            return jsonify({'error': 'Orchestrator not initialized'}), 500
            
        data = request.json
        validation_data = data.get('data', {})
        policy_name = data.get('policy', 'customer_onboarding')
        
        # Validate using orchestrator
        result = orchestrator.validate_data(validation_data, policy_name)
        
        return jsonify({
            'valid': result.is_valid,
            'score': result.score,
            'violations': result.violations,
            'explanation': result.summary
        })
    
    except Exception as e:
        print(f"Validation error: {e}")
        return jsonify({'error': f'Validation error: {str(e)}'}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file uploads for validation"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Get user prompt if provided
            user_prompt = request.form.get('prompt', '').strip()
            policy_name = request.form.get('policy', 'customer_onboarding')
            
            # Process file based on type
            if filename.endswith('.json'):
                with open(filepath, 'r') as f:
                    file_data = json.load(f)
                
                # Validate JSON data
                result = orchestrator.validate_data(file_data, policy_name)
                
                response_data = {
                    'filename': filename,
                    'valid': result.is_valid,
                    'score': result.score,
                    'violations': result.violations,
                    'explanation': result.summary
                }
                
                # Process user prompt if provided
                if user_prompt and orchestrator:
                    prompt_context = f"File: {filename}\nData: {json.dumps(file_data, indent=2)}\nValidation Result: {result.summary}\nUser Question: {user_prompt}"
                    prompt_response = orchestrator.process_natural_language(prompt_context)
                    response_data['prompt'] = user_prompt
                    response_data['prompt_response'] = prompt_response
                
                # Clean up file
                os.remove(filepath)
                return jsonify(response_data)
            
            elif filename.endswith(('.txt', '.csv')):
                with open(filepath, 'r') as f:
                    content = f.read()
                
                # Process text through LLM or basic analysis
                if user_prompt:
                    analysis_prompt = f"Document: {filename}\nContent: {content[:2000]}...\nUser Question: {user_prompt}"
                else:
                    analysis_prompt = f"Please analyze this document for compliance: {content[:1000]}..."
                
                analysis = orchestrator.process_natural_language(analysis_prompt) if orchestrator else "File uploaded successfully"
                
                response_data = {
                    'filename': filename,
                    'analysis': analysis
                }
                
                if user_prompt:
                    response_data['prompt'] = user_prompt
                    response_data['prompt_response'] = analysis
                
                # Clean up file
                os.remove(filepath)
                return jsonify(response_data)
            
            else:
                os.remove(filepath)
                return jsonify({'error': 'Unsupported file type. Use JSON, TXT, or CSV'}), 400
    
    except Exception as e:
        print(f"File upload error: {e}")
        return jsonify({'error': f'File processing error: {str(e)}'}), 500

@app.route('/api/policies')
def get_policies():
    """Get available policies"""
    try:
        policies_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'policies')
        policies = []
        
        for filename in os.listdir(policies_dir):
            if filename.endswith('.json'):
                policy_name = filename.replace('.json', '')
                policies.append(policy_name)
        
        return jsonify({'policies': policies})
    
    except Exception as e:
        return jsonify({'error': f'Error loading policies: {str(e)}'}), 500

@app.route('/api/unified', methods=['POST'])
def unified_interface():
    """Handle unified chat, validation, and file upload"""
    try:
        if orchestrator is None:
            return jsonify({'error': 'Orchestrator not initialized'}), 500
        
        # Handle file upload
        if 'file' in request.files:
            file = request.files['file']
            message = request.form.get('message', '').strip()
            
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                if filename.endswith('.json'):
                    with open(filepath, 'r') as f:
                        file_data = json.load(f)
                    
                    if message:
                        # Chat about the uploaded data
                        context = f"User uploaded file '{filename}' with data: {json.dumps(file_data, indent=2)}\n\nUser question: {message}"
                        response = orchestrator.process_natural_language(context)
                        
                        # Also try validation if it looks like customer data
                        validation_result = None
                        if any(key in file_data for key in ['email', 'age', 'name', 'phone']):
                            try:
                                validation_result = orchestrator.validate_data(file_data, 'basic_validation')
                            except:
                                pass
                        
                        result = {
                            'type': 'file_chat',
                            'filename': filename,
                            'response': response,
                            'data': file_data
                        }
                        
                        if validation_result:
                            result['validation'] = {
                                'valid': validation_result.is_valid,
                                'score': validation_result.score,
                                'violations': validation_result.violations,
                                'explanation': validation_result.summary
                            }
                        
                        os.remove(filepath)
                        return jsonify(result)
                    
                elif filename.endswith(('.txt', '.csv')):
                    with open(filepath, 'r') as f:
                        content = f.read()
                    
                    if message:
                        context = f"User uploaded document '{filename}' with content: {content[:2000]}...\n\nUser question: {message}"
                    else:
                        context = f"Analyze this document for compliance and governance: {content[:1000]}..."
                    
                    response = orchestrator.process_natural_language(context)
                    
                    os.remove(filepath)
                    return jsonify({
                        'type': 'document_analysis',
                        'filename': filename,
                        'response': response,
                        'content_preview': content[:500] + '...' if len(content) > 500 else content
                    })
                
            except Exception as e:
                os.remove(filepath)
                return jsonify({'error': f'File processing error: {str(e)}'}), 500
        
        # Handle JSON data in message
        data = request.json
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Try to extract JSON from message
        json_data = None
        try:
            # Look for JSON patterns in the message
            import re
            json_match = re.search(r'\{[^{}]*\}', message)
            if json_match:
                json_str = json_match.group()
                json_data = json.loads(json_str)
        except:
            pass
        
        if json_data:
            # Message contains JSON data - provide validation and chat
            validation_result = None
            if any(key in json_data for key in ['email', 'age', 'name', 'phone', 'amount', 'transaction_type']):
                try:
                    # Auto-detect policy based on data fields
                    policy = 'basic_validation'
                    if 'amount' in json_data and 'currency' in json_data:
                        policy = 'transaction_validation'
                    elif 'identity_documents' in json_data:
                        policy = 'kyc_validation'
                    elif 'balance' in json_data and json_data.get('balance', 0) >= 50000:
                        policy = 'premium_customer'
                    
                    validation_result = orchestrator.validate_data(json_data, policy)
                except:
                    pass
            
            # Generate contextual response
            context = f"User provided data: {json.dumps(json_data, indent=2)}\n\nUser message: {message}"
            response = orchestrator.process_natural_language(context)
            
            result = {
                'type': 'data_chat',
                'response': response,
                'data': json_data
            }
            
            if validation_result:
                result['validation'] = {
                    'valid': validation_result.is_valid,
                    'score': validation_result.score,
                    'violations': validation_result.violations,
                    'explanation': validation_result.summary,
                    'policy_used': policy
                }
            
            return jsonify(result)
        
        # Regular chat message
        response = orchestrator.process_natural_language(message)
        return jsonify({
            'type': 'chat',
            'response': response,
            'session_id': session['session_id']
        })
    
    except Exception as e:
        print(f"Unified interface error: {e}")
        return jsonify({'error': f'Error processing request: {str(e)}'}), 500

@app.route('/api/config', methods=['GET', 'POST'])
def manage_config():
    """Get or update system configuration"""
    if request.method == 'GET':
        return jsonify({
            'llm_features': {
                'use_llm': USE_LLM,
                'ollama_host': os.getenv('OLLAMA_HOST', 'http://localhost:11434'),
                'ollama_model': os.getenv('OLLAMA_MODEL', 'llama3.2:3b')
            },
            'governance_features': {
                'auto_validation': AUTO_VALIDATION,
                'auto_policy_detection': AUTO_POLICY_DETECTION,
                'risk_assessment': RISK_ASSESSMENT,
                'compliance_checking': COMPLIANCE_CHECKING,
                'aml_screening': AML_SCREENING,
                'kyc_validation': KYC_VALIDATION,
                'gdpr_analysis': GDPR_ANALYSIS,
                'sanctions_screening': SANCTIONS_SCREENING,
                'pep_screening': PEP_SCREENING
            },
            'validation_thresholds': {
                'high_risk_amount': HIGH_RISK_AMOUNT,
                'aml_threshold': AML_THRESHOLD,
                'kyc_expiry_days': KYC_EXPIRY_DAYS,
                'risk_score_threshold': RISK_SCORE_THRESHOLD
            },
            'file_processing': {
                'max_file_size': MAX_FILE_SIZE,
                'allowed_file_types': ALLOWED_FILE_TYPES,
                'auto_file_analysis': AUTO_FILE_ANALYSIS,
                'file_content_preview': FILE_CONTENT_PREVIEW
            },
            'logging_audit': {
                'audit_logging': AUDIT_LOGGING,
                'compliance_reporting': COMPLIANCE_REPORTING,
                'violation_alerts': VIOLATION_ALERTS,
                'performance_monitoring': PERFORMANCE_MONITORING
            },
            'system': {
                'port': PORT,
                'debug': DEBUG,
                'policies_dir': POLICIES_DIR
            }
        })
    
    elif request.method == 'POST':
        # Update configuration (would require restart to take effect)
        config_updates = request.json
        
        # For demo purposes, we'll just return what would be updated
        # In production, this would update the .env file
        return jsonify({
            'message': 'Configuration updated successfully',
            'note': 'Restart required for changes to take effect',
            'updated_config': config_updates
        })

@app.route('/api/status')
def get_status():
    """Get system status"""
    return jsonify({
        'llm_enabled': USE_LLM,
        'orchestrator_ready': orchestrator is not None,
        'policies_dir': POLICIES_DIR,
        'features_enabled': {
            'auto_validation': AUTO_VALIDATION,
            'risk_assessment': RISK_ASSESSMENT,
            'aml_screening': AML_SCREENING,
            'kyc_validation': KYC_VALIDATION,
            'gdpr_analysis': GDPR_ANALYSIS
        }
    })

if __name__ == '__main__':
    print(f"Starting Governance Agent UI on port {PORT}")
    print(f"LLM enabled: {USE_LLM}")
    print(f"Auto validation: {AUTO_VALIDATION}")
    print(f"Risk assessment: {RISK_ASSESSMENT}")
    print(f"AML screening: {AML_SCREENING}")
    print(f"Policies directory: {POLICIES_DIR}")
    app.run(debug=DEBUG, host='0.0.0.0', port=PORT)