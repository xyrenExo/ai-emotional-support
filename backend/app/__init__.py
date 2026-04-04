from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.config import Config
import logging
import sys

# Configure logging at module level BEFORE anything else
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

from app.api.routes import api_bp, limiter
from app.api.middleware import SecurityMiddleware, CorsMiddleware

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    logger.info("Flask app creating...")
    
    # Initialize extensions
    CORS(app, origins=Config.ALLOWED_ORIGINS, supports_credentials=True)
    limiter.init_app(app)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Error handlers
    register_error_handlers(app)
    
    return app

def setup_logging(app):
    """Configure logging for the application"""
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
    
    # Set app-specific loggers to DEBUG
    logging.getLogger('app').setLevel(logging.DEBUG)
    
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
