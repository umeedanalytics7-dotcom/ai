import os
import google.generativeai as genai
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Configure Gemini API (free)
# Get API key from: https://aistudio.google.com/apikey
API_KEY = os.environ.get('GEMINI_API_KEY', 'YOUR_API_KEY_HERE')
genai.configure(api_key=API_KEY)

# Select the model
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def serve_index():
    """Serve the main HTML file"""
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages and return AI response"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Generate response from Gemini
        response = model.generate_content(user_message)
        
        return jsonify({
            'response': response.text,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Render"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    # Important: Use 0.0.0.0 and environment port for Render [citation:5]
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
