from flask import Flask, redirect
from flask_cors import CORS
from .models.models import db
import os

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['GOOGLE_CLIENT_ID'] = os.environ.get('GOOGLE_CLIENT_ID')
    app.config['GOOGLE_CLIENT_SECRET'] = os.environ.get('GOOGLE_CLIENT_SECRET')
    
    # Session configuration for cross-origin cookies
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
    
    # Initialize extensions
    CORS(app, 
         supports_credentials=True,
         origins=['http://localhost:5000', 'http://127.0.0.1:5000', 'https://*.replit.app', 'https://*.replit.dev'],
         allow_headers=['Content-Type', 'Authorization'],
         expose_headers=['Set-Cookie'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    db.init_app(app)
    
    # Root route - API health check
    @app.route('/')
    def index():
        return {'status': 'ok', 'message': 'RJMS API is running'}
    
    # Register blueprints
    from .routes import auth, courses, students, teacher, reflections
    app.register_blueprint(auth.bp)
    app.register_blueprint(courses.bp)
    app.register_blueprint(students.bp)
    app.register_blueprint(teacher.bp)
    app.register_blueprint(reflections.bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
