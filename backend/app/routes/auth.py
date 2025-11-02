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
        
        # In development, we'll skip actual Google verification
        # In production, uncomment the following:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request(), google_client_id)
        
        # For development/demo purposes, we'll mock the response
        # Replace this with actual Google verification in production
        idinfo = {
            'sub': token,  # Using token as unique ID for demo
            'email': data.get('email', 'demo@example.com'),
            'name': data.get('name', 'Demo User'),
            'picture': data.get('picture', '')
        }
        
        google_id = idinfo['sub']
        email = idinfo['email']
        name = idinfo['name']
        picture = idinfo.get('picture', '')
        
        # Check if user exists
        user = User.query.filter_by(google_id=google_id).first()
        
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
            return jsonify({'error': f'This account is registered as a {user.role}'}), 403
        
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
            'profile_image': user.profile_image
        }
    }), 200
