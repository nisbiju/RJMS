from flask import Flask
from flask_cors import CORS
from .models.models import db
import os

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['GOOGLE_CLIENT_ID'] = os.environ.get('GOOGLE_CLIENT_ID')
    app.config['GOOGLE_CLIENT_SECRET'] = os.environ.get('GOOGLE_CLIENT_SECRET')
    
    # Initialize extensions
    CORS(app, supports_credentials=True)
    db.init_app(app)
    
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
