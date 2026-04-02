from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.config import Config
from app.api.routes import api_bp, limiter
from app.api.middleware import SecurityMiddleware, CorsMiddleware
import logging
import sys

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Setup logging
    setup_logging(app)
    
    # Initialize extensions
    CORS(app, origins=Config.ALLOWED_ORIGINS, supports_credentials=True)
    limiter.init_app(app)
    
    # Initialize middleware
    security_middleware = SecurityMiddleware()
    cors_middleware = CorsMiddleware(Config.ALLOWED_ORIGINS)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Add middleware
    app.after_request(security_middleware.add_security_headers)
    app.after_request(cors_middleware.add_cors_headers)
    
    # Error handlers
    register_error_handlers(app)
    
    return app

def setup_logging(app):
    """Configure logging for the application"""
    # Remove default handler
    if app.logger.hasHandlers():
        app.logger.handlers.clear()
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Add handler to app logger
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)
    
    # Also set up loggers for key modules
    logging.getLogger('flask_cors').setLevel(logging.INFO)
    logging.getLogger('werkzeug').setLevel(logging.INFO)

def register_error_handlers(app):
    """Register error handlers for common HTTP errors"""
    
    @app.errorhandler(400)
    def bad_request(error):
        app.logger.warning(f'Bad request: {error}')
        return jsonify({'error': 'Bad request'}), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        app.logger.warning(f'Rate limit exceeded')
        return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Internal server error: {error}', exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500
