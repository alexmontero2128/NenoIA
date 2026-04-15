from flask import Flask, render_template, request, jsonify
import cv2
import base64
import numpy as np
from models import DatabaseManager
from face_utils import FaceRecognitionManager
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Initialize managers
db = DatabaseManager('access_control.db')
face_manager = FaceRecognitionManager()

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')

@app.route('/api/enroll', methods=['POST'])
def enroll_user():
    """Enroll a new user with face data"""
    try:
        data = request.json
        user_id = data.get('user_id')
        name = data.get('name')
        email = data.get('email')
        image_data = data.get('image')
        
        # Decode image from base64
        image_bytes = base64.b64decode(image_data.split(',')[1])
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Get face encoding
        face_encoding = face_manager.get_face_encoding(image)
        
        if face_encoding is None:
            return jsonify({'success': False, 'message': 'No face detected'}), 400
        
        # Convert to bytes for storage
        encoding_bytes = face_manager.encode_face_to_bytes(face_encoding)
        
        # Add to database
        success = db.add_user(user_id, name, email, encoding_bytes)
        
        if success:
            return jsonify({'success': True, 'message': 'User enrolled successfully'})
        else:
            return jsonify({'success': False, 'message': 'User already exists'}), 400
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/verify', methods=['POST'])
def verify_face():
    """Verify a face against enrolled users"""
    try:
        data = request.json
        image_data = data.get('image')
        
        # Decode image from base64
        image_bytes = base64.b64decode(image_data.split(',')[1])
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Get face encoding
        test_encoding = face_manager.get_face_encoding(image)
        
        if test_encoding is None:
            return jsonify({'success': False, 'message': 'No face detected'}), 400
        
        # Get all users
        users = db.get_all_users()
        
        best_match = None
        best_confidence = 0
        
        for user in users:
            user_id, name, email = user[1], user[2], user[3]
            stored_encoding = face_manager.decode_face_from_bytes(user[4])
            
            match, confidence = face_manager.recognize_face(image, [stored_encoding])
            
            if match and confidence > best_confidence:
                best_match = (user_id, name, confidence)
                best_confidence = confidence
        
        if best_match:
            user_id, name, confidence = best_match
            db.log_access(user_id, True, confidence)
            return jsonify({
                'success': True,
                'message': f'Access granted to {name}',
                'user': name,
                'confidence': float(confidence)
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Face not recognized',
                'confidence': float(best_confidence)
            }), 403
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/access-logs', methods=['GET'])
def get_access_logs():
    """Retrieve access logs"""
    try:
        limit = request.args.get('limit', 100, type=int)
        logs = db.get_access_logs(limit)
        
        logs_list = []
        for log in logs:
            logs_list.append({
                'id': log[0],
                'user_id': log[1],
                'timestamp': log[2],
                'access_granted': log[3],
                'confidence': log[4]
            })
        
        return jsonify({'success': True, 'logs': logs_list})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    """Retrieve all enrolled users"""
    try:
        users = db.get_all_users()
        
        users_list = []
        for user in users:
            users_list.append({
                'user_id': user[1],
                'name': user[2],
                'email': user[3],
                'enrollment_date': user[5]
            })
        
        return jsonify({'success': True, 'users': users_list})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000