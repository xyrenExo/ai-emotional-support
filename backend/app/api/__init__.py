<<<<<<< HEAD
from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.config import Config
from app.api.routes import api_bp
from app.api.middleware import SecurityMiddleware, CorsMiddleware
import logging
import sys

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Setup logging
    setup_logging(app)
    
    # Initialize extensions
    CORS(app, origins=Config.ALLOWED_ORIGINS, supports_credentials=True)
    limiter.init_app(app)
    
    # Initialize middleware
    cors_middleware = CorsMiddleware(Config.ALLOWED_ORIGINS)
    security_middleware = SecurityMiddleware()
    
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
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

def register_error_handlers(app):
    """Register error handlers for common HTTP errors"""
    
    @app.errorhandler(400)
    def bad_request(error):
        return {'error': 'Bad request', 'message': str(error)}, 400
    
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found', 'message': 'The requested resource was not found'}, 404
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        return {'error': 'Rate limit exceeded', 'message': 'Too many requests. Please try again later.'}, 429
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Internal server error: {error}')
        return {'error': 'Internal server error', 'message': 'An unexpected error occurred'}, 500

# Export important classes and functions
=======
from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.config import Config
from app.api.routes import api_bp
from app.api.middleware import SecurityMiddleware, CorsMiddleware
import logging
import sys

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Setup logging
    setup_logging(app)
    
    # Initialize extensions
    CORS(app, origins=Config.ALLOWED_ORIGINS, supports_credentials=True)
    limiter.init_app(app)
    
    # Initialize middleware
    cors_middleware = CorsMiddleware(Config.ALLOWED_ORIGINS)
    security_middleware = SecurityMiddleware()
    
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
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

def register_error_handlers(app):
    """Register error handlers for common HTTP errors"""
    
    @app.errorhandler(400)
    def bad_request(error):
        return {'error': 'Bad request', 'message': str(error)}, 400
    
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found', 'message': 'The requested resource was not found'}, 404
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        return {'error': 'Rate limit exceeded', 'message': 'Too many requests. Please try again later.'}, 429
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Internal server error: {error}')
        return {'error': 'Internal server error', 'message': 'An unexpected error occurred'}, 500

# Export important classes and functions
>>>>>>> 6a97c5ff1caff98b22d3c35a1de0b0b2e5252662
__all__ = ['create_app', 'limiter']