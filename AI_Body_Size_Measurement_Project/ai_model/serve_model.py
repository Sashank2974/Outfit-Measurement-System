"""
AI Model Inference Server
Serves pose estimation and measurement models
"""

from flask import Flask, request, jsonify
import cv2
import mediapipe as mp
import numpy as np
from typing import Dict, List, Tuple
import base64
import io
from PIL import Image

app = Flask(__name__)

# Initialize MediaPipe
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(
    static_image_mode=True,
    model_complexity=2,
    enable_segmentation=True,
    min_detection_confidence=0.5
)

class BodyMeasurementAI:
    """AI model for body measurement"""
    
    def __init__(self):
        self.pose_estimator = pose
        self.reference_card_width_cm = 8.56  # Standard credit card width
        
    def decode_image(self, base64_string: str) -> np.ndarray:
        """Decode base64 image to numpy array"""
        img_data = base64.b64decode(base64_string)
        img = Image.open(io.BytesIO(img_data))
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
    def detect_pose(self, image: np.ndarray) -> Dict:
        """Detect pose landmarks"""
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose_estimator.process(image_rgb)
        
        if not results.pose_landmarks:
            return None
        
        landmarks = []
        for landmark in results.pose_landmarks.landmark:
            landmarks.append({
                'x': landmark.x,
                'y': landmark.y,
                'z': landmark.z,
                'visibility': landmark.visibility
            })
        
        return {
            'landmarks': landmarks,
            'segmentation_mask': results.segmentation_mask is not None
        }
    
    def calculate_distance(self, point1: Dict, point2: Dict, image_height: int) -> float:
        """Calculate Euclidean distance between two points"""
        x1, y1 = point1['x'], point1['y']
        x2, y2 = point2['x'], point2['y']
        
        pixel_distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2) * image_height
        return pixel_distance
    
    def estimate_measurements(self, landmarks: List[Dict], gender: str, 
                            image_height: int, reference_scale: float = 1.0) -> Dict:
        """Estimate body measurements from landmarks"""
        
        # Key landmark indices (MediaPipe Pose)
        NOSE = 0
        LEFT_SHOULDER = 11
        RIGHT_SHOULDER = 12
        LEFT_HIP = 23
        RIGHT_HIP = 24
        LEFT_KNEE = 25
        RIGHT_KNEE = 26
        LEFT_ANKLE = 27
        RIGHT_ANKLE = 28
        LEFT_WRIST = 15
        RIGHT_WRIST = 16
        LEFT_ELBOW = 13
        RIGHT_ELBOW = 14
        
        measurements = {}
        
        # Height (nose to ankle)
        height_pixels = self.calculate_distance(
            landmarks[NOSE], 
            landmarks[LEFT_ANKLE], 
            image_height
        )
        measurements['height'] = height_pixels * reference_scale
        
        # Shoulder width
        shoulder_width_pixels = self.calculate_distance(
            landmarks[LEFT_SHOULDER],
            landmarks[RIGHT_SHOULDER],
            image_height
        )
        measurements['shoulder_width'] = shoulder_width_pixels * reference_scale
        
        # Hip width
        hip_width_pixels = self.calculate_distance(
            landmarks[LEFT_HIP],
            landmarks[RIGHT_HIP],
            image_height
        )
        measurements['hip'] = hip_width_pixels * reference_scale * 3.14  # Approximate circumference
        
        # Arm length (shoulder to wrist)
        arm_length_pixels = self.calculate_distance(
            landmarks[LEFT_SHOULDER],
            landmarks[LEFT_WRIST],
            image_height
        )
        measurements['arm_length'] = arm_length_pixels * reference_scale
        
        # Gender-specific measurements
        if gender == 'male':
            # Chest approximation (shoulder width * 2.5)
            measurements['chest'] = measurements['shoulder_width'] * 2.5
        else:  # female
            # Bust approximation (shoulder width * 2.3)
            measurements['bust'] = measurements['shoulder_width'] * 2.3
            measurements['under_bust'] = measurements['bust'] * 0.85
        
        # Waist approximation (hip * 0.75)
        measurements['waist'] = measurements['hip'] * 0.75
        
        # Calculate confidence scores
        avg_visibility = np.mean([lm['visibility'] for lm in landmarks])
        measurements['overall_confidence'] = avg_visibility * 100
        
        return measurements

# Initialize AI model
ai_model = BodyMeasurementAI()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'AI Model Server',
        'version': '1.0.0'
    })

@app.route('/api/measure', methods=['POST'])
def measure_body():
    """Process image and return measurements"""
    try:
        data = request.json
        
        # Validate input
        if 'image' not in data:
            return jsonify({'error': 'No image provided'}), 400
        
        gender = data.get('gender', 'male')
        if gender not in ['male', 'female']:
            return jsonify({'error': 'Invalid gender'}), 400
        
        # Decode image
        image = ai_model.decode_image(data['image'])
        image_height = image.shape[0]
        
        # Detect pose
        pose_result = ai_model.detect_pose(image)
        
        if not pose_result:
            return jsonify({
                'error': 'No person detected in image',
                'confidence': 0
            }), 400
        
        # Calculate measurements
        measurements = ai_model.estimate_measurements(
            pose_result['landmarks'],
            gender,
            image_height,
            reference_scale=data.get('reference_scale', 1.0)
        )
        
        return jsonify({
            'success': True,
            'measurements': measurements,
            'pose_detected': True,
            'processing_time_ms': 0  # Add actual timing
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/detect-pose', methods=['POST'])
def detect_pose_endpoint():
    """Detect pose landmarks only"""
    try:
        data = request.json
        image = ai_model.decode_image(data['image'])
        
        pose_result = ai_model.detect_pose(image)
        
        if not pose_result:
            return jsonify({
                'pose_detected': False,
                'landmarks': []
            })
        
        return jsonify({
            'pose_detected': True,
            'landmarks': pose_result['landmarks'],
            'has_segmentation': pose_result['segmentation_mask']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🤖 Starting AI Model Server...")
    print("📊 MediaPipe Pose initialized")
    app.run(host='0.0.0.0', port=5000, debug=True)
