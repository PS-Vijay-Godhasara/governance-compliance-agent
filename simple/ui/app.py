import os
import sys
import json
from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename
import uuid

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.orchestrator import SimpleOrchestrator

app = Flask(__name__)
app.secret_key = 'governance-agent-ui-key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize orchestrator
orchestrator = SimpleOrchestrator(use_llm=True)

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
        return jsonify({'error': f'Error processing message: {str(e)}'}), 500

@app.route('/api/validate', methods=['POST'])
def validate_data():
    """Handle data validation requests"""
    try:
        data = request.json
        validation_data = data.get('data', {})
        policy_name = data.get('policy', 'customer_onboarding')
        
        # Validate using orchestrator
        result = orchestrator.validate_data(validation_data, policy_name)
        
        return jsonify({
            'valid': result.valid,
            'score': result.score,
            'violations': result.violations,
            'explanation': result.explanation
        })
    
    except Exception as e:
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
            
            # Process file based on type
            if filename.endswith('.json'):
                with open(filepath, 'r') as f:
                    file_data = json.load(f)
                
                # Validate JSON data
                policy_name = request.form.get('policy', 'customer_onboarding')
                result = orchestrator.validate_data(file_data, policy_name)
                
                # Clean up file
                os.remove(filepath)
                
                return jsonify({
                    'filename': filename,
                    'valid': result.valid,
                    'score': result.score,
                    'violations': result.violations,
                    'explanation': result.explanation
                })
            
            elif filename.endswith(('.txt', '.csv')):
                with open(filepath, 'r') as f:
                    content = f.read()
                
                # Process text through LLM
                response = orchestrator.process_natural_language(
                    f"Please analyze this file content for compliance: {content[:1000]}..."
                )
                
                # Clean up file
                os.remove(filepath)
                
                return jsonify({
                    'filename': filename,
                    'analysis': response
                })
            
            else:
                os.remove(filepath)
                return jsonify({'error': 'Unsupported file type. Use JSON, TXT, or CSV'}), 400
    
    except Exception as e:
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)