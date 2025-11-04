from flask import Blueprint, request, jsonify, session
from google.oauth2 import id_token
from google.auth.transport import requests
from ..models.models import db, User
import os

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/google', methods=['POST'])
def google_auth():
    """Handle Google OAuth authentication"""
    try:
        data = request.get_json()
        token = data.get('token')
        role = data.get('role')  # 'student' or 'teacher'
        
        if not token or not role or role not in ['student', 'teacher']:
            return jsonify({'error': 'Invalid request'}), 400
        
        # Verify the Google token
        google_client_id = os.environ.get('GOOGLE_CLIENT_ID')
        
        # Ensure GOOGLE_CLIENT_ID is configured
        if not google_client_id:
            print('CRITICAL: GOOGLE_CLIENT_ID environment variable is not set')
            return jsonify({'error': 'Authentication service is not configured'}), 500
        
        # Verify the token with Google
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), google_client_id)
            
            # Explicitly verify the audience (client ID)
            if idinfo.get('aud') != google_client_id:
                print(f'Token audience mismatch: expected {google_client_id}, got {idinfo.get("aud")}')
                return jsonify({'error': 'Invalid token audience'}), 401
                
        except ValueError as e:
            print(f'Token verification failed: {str(e)}')
            return jsonify({'error': 'Invalid token'}), 401
        
        google_id = idinfo['sub']
        email = idinfo['email']
        name = idinfo.get('name', email.split('@')[0])
        picture = idinfo.get('picture', '')
        
        # Check if user exists by email (for demo mode compatibility)
        user = User.query.filter_by(email=email).first()
        
        if not user:
            # Create new user
            user = User(
                email=email,
                name=name,
                google_id=google_id,
                role=role,
                profile_image=picture
            )
            db.session.add(user)
            db.session.commit()
        elif user.role != role:
            return jsonify({'error': f'This account is registered as a {user.role}. Please use the {user.role} login page.'}), 403
        else:
            # Update google_id for existing user (in case it's a demo login)
            if user.google_id != google_id:
                user.google_id = google_id
                db.session.commit()
        
        # Set session
        session['user_id'] = user.id
        session['user_role'] = user.role
        
        return jsonify({
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'role': user.role,
                'profile_image': user.profile_image
            }
        }), 200
        
    except Exception as e:
        print(f'Auth error: {str(e)}')
        return jsonify({'error': 'Authentication failed'}), 401

@bp.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

@bp.route('/me', methods=['GET'])
def get_current_user():
    """Get current logged in user"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': user.role,
            'profile_image': user.profile_image,
            'department': user.department,
            'experience': user.experience,
            'area_of_interest': user.area_of_interest,
            'student_id': user.student_id,
            'year_of_joining': user.year_of_joining
        }
    }), 200

@bp.route('/profile', methods=['PUT'])
def update_profile():
    """Update user profile"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    # Update allowed fields
    if 'name' in data:
        user.name = data['name']
    if 'department' in data:
        user.department = data['department']
    if 'area_of_interest' in data:
        user.area_of_interest = data['area_of_interest']
    
    # Teacher-specific fields
    if user.role == 'teacher' and 'experience' in data:
        user.experience = data['experience']
    
    # Student-specific fields
    if user.role == 'student':
        if 'student_id' in data:
            user.student_id = data['student_id']
        if 'year_of_joining' in data:
            user.year_of_joining = data['year_of_joining']
    
    # Profile image (base64) - validate size
    if 'profile_image' in data:
        image_data = data['profile_image']
        if image_data:
            # Check if it's a valid base64 data URL
            if not image_data.startswith('data:image/'):
                return jsonify({'error': 'Invalid image format'}), 400
            
            # Estimate base64 size (approximately 4/3 of original)
            # Limit to ~2.7MB base64 (2MB original)
            if len(image_data) > 2.7 * 1024 * 1024:
                return jsonify({'error': 'Image too large. Maximum size is 2MB'}), 400
            
            user.profile_image = image_data
        else:
            # Allow null to remove image
            user.profile_image = None
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f'Error updating profile: {str(e)}')
        return jsonify({'error': 'Failed to update profile'}), 500
    
    return jsonify({
        'message': 'Profile updated successfully',
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': user.role,
            'profile_image': user.profile_image,
            'department': user.department,
            'experience': user.experience,
            'area_of_interest': user.area_of_interest,
            'student_id': user.student_id,
            'year_of_joining': user.year_of_joining
        }
    }), 200
