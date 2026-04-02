from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.config import Config
from app.api.routes import api_bp, limiter

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    CORS(app, origins=Config.ALLOWED_ORIGINS)
    limiter.init_app(app)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app