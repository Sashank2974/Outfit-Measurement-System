"""
Mock AI Model Server for Testing
This provides fake measurements so you can test the UI while the real AI dependencies install
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'Mock AI Model Server',
        'message': 'This is a temporary mock server for testing'
    })

@app.route('/api/measure', methods=['POST'])
def measure():
    """Mock measurement endpoint - returns fake but realistic measurements"""
    try:
        data = request.json
        gender = data.get('gender', 'male')
        
        # Generate realistic fake measurements based on gender
        if gender == 'male':
            measurements = {
                'height': round(random.uniform(165, 185), 1),
                'chest': round(random.uniform(90, 110), 1),
                'waist': round(random.uniform(75, 95), 1),
                'hip': round(random.uniform(85, 105), 1),
                'shoulder_width': round(random.uniform(40, 50), 1),
                'arm_length': round(random.uniform(55, 65), 1),
                'inseam': round(random.uniform(75, 85), 1),
                'outseam': round(random.uniform(100, 110), 1)
            }
            size = random.choice(['S', 'M', 'L', 'XL'])
        else:  # female
            measurements = {
                'height': round(random.uniform(155, 175), 1),
                'bust': round(random.uniform(80, 100), 1),
                'under_bust': round(random.uniform(70, 85), 1),
                'waist': round(random.uniform(60, 80), 1),
                'hip': round(random.uniform(85, 105), 1),
                'shoulder_width': round(random.uniform(35, 45), 1),
                'arm_length': round(random.uniform(50, 60), 1)
            }
            size = random.choice(['XS', 'S', 'M', 'L', 'XL'])
        
        response = {
            'success': True,
            'measurements': measurements,
            'confidence': round(random.uniform(0.85, 0.95), 2),
            'size_recommendation': size,
            'gender': gender,
            'message': 'Mock measurements generated for testing. Real AI server will provide accurate measurements once dependencies finish installing.'
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🧪 MOCK AI Model Server Starting...")
    print("=" * 60)
    print("⚠️  This is a TEMPORARY mock server for testing")
    print("📍 Server running at: http://localhost:5000")
    print("🔧 Returns fake measurements for UI testing")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)
