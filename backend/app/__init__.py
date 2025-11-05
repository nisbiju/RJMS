from flask import Flask, send_from_directory
from flask_cors import CORS
from .models.models import db
from dotenv import load_dotenv
import os


def create_app():
    # Load variables from backend/.env
    load_dotenv()

    app = Flask(__name__)

    # ----- Core config -----
    app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')

    db_uri = os.environ.get('DATABASE_URL')
    if not db_uri:
        # Helpful error if .env is missing or key is wrong
        raise RuntimeError(
            "DATABASE_URL not set. Create backend/.env and set:\n"
            "DATABASE_URL=postgresql://... ?sslmode=require"
        )

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Optional Google OAuth
    app.config['GOOGLE_CLIENT_ID'] = os.environ.get('GOOGLE_CLIENT_ID')
    app.config['GOOGLE_CLIENT_SECRET'] = os.environ.get('GOOGLE_CLIENT_SECRET')

    # Cookies (adjust for prod/HTTPS)
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = False  # True in production with HTTPS

    # ----- CORS -----
    CORS(
        app,
        supports_credentials=True,
        origins=[
            
	    'http://localhost:5001',      
            'http://127.0.0.1:5001',
            'http://localhost:8080',       # Vite default
            'http://127.0.0.1:8080',
            'https://*.replit.app',
            'https://*.replit.dev',
        ],
        allow_headers=['Content-Type', 'Authorization'],
        expose_headers=['Set-Cookie'],
        methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    )

    # Init DB
    db.init_app(app)

    # Health Check Route
    @app.route('/api/health')
    def health():
        return {'status': 'ok', 'message': 'RJMS API and Frontend running'}

    # Blueprints
    from .routes import auth, courses, students, teacher, reflections
    app.register_blueprint(auth.bp)
    app.register_blueprint(courses.bp)
    app.register_blueprint(students.bp)
    app.register_blueprint(teacher.bp)
    app.register_blueprint(reflections.bp)

    # Create tables
    with app.app_context():
        db.create_all()

    # ----- Serve Built Vue Frontend -----
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_vue(path):
        
        static_folder = os.path.join(app.root_path, '../static')
        file_path = os.path.join(static_folder, path)

        if path != "" and os.path.exists(file_path):
            return send_from_directory(static_folder, path)
        else:
            # ---- Fallback to index.html for Vue Router paths ----
            return send_from_directory(static_folder, 'index.html')


    return app
