<<<<<<< HEAD
from functools import wraps
from flask import request, jsonify
import time
import re
from typing import Dict, Any

class SecurityMiddleware:
    """Security middleware for request validation and sanitization"""
    
    @staticmethod
    def sanitize_input(data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize all string inputs in request data"""
        sanitized = {}
        for key, value in data.items():
            if isinstance(value, str):
                # Remove any script tags or dangerous patterns
                cleaned = re.sub(r'<[^>]*>', '', value)
                cleaned = re.sub(r'[<>{}]', '', cleaned)
                sanitized[key] = cleaned[:2000]  # Limit length
            elif isinstance(value, dict):
                sanitized[key] = SecurityMiddleware.sanitize_input(value)
            elif isinstance(value, list):
                sanitized[key] = [
                    SecurityMiddleware.sanitize_input(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                sanitized[key] = value
        return sanitized
    
    @staticmethod
    def validate_content_type(content_type: str) -> bool:
        """Validate request content type"""
        allowed_types = ['application/json']
        return content_type in allowed_types
    
    @staticmethod
    def add_security_headers(response):
        """Add security headers to response"""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        return response

class RateLimitMiddleware:
    """Rate limiting middleware with Redis support"""
    
    def __init__(self, redis_client=None):
        self.redis_client = redis_client
        self.in_memory_store = {}
        
    def check_rate_limit(self, key: str, limit: int, window: int) -> bool:
        """Check if request is within rate limit"""
        current_time = time.time()
        
        if self.redis_client:
            # Use Redis for distributed rate limiting
            pipe = self.redis_client.pipeline()
            pipe.zremrangebyscore(key, 0, current_time - window)
            pipe.zadd(key, {str(current_time): current_time})
            pipe.zcard(key)
            pipe.expire(key, window)
            _, _, count, _ = pipe.execute()
            return count <= limit
        else:
            # Fallback to in-memory store
            if key not in self.in_memory_store:
                self.in_memory_store[key] = []
            
            # Clean old requests
            self.in_memory_store[key] = [
                t for t in self.in_memory_store[key] 
                if t > current_time - window
            ]
            
            if len(self.in_memory_store[key]) >= limit:
                return False
            
            self.in_memory_store[key].append(current_time)
            return True

def rate_limit(limit=100, window=60):
    """Decorator for rate limiting endpoints"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get client identifier (IP address)
            client_ip = request.remote_addr
            
            # Create rate limit key
            key = f"ratelimit:{client_ip}:{f.__name__}"
            
            # Initialize rate limiter (would be configured in app)
            if not hasattr(request, 'rate_limiter'):
                request.rate_limiter = RateLimitMiddleware()
            
            # Check rate limit
            if not request.rate_limiter.check_rate_limit(key, limit, window):
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'message': f'Too many requests. Please wait {window} seconds.',
                    'limit': limit,
                    'window': window
                }), 429
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_api_key(f):
    """Decorator to require API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({'error': 'API key required'}), 401
        
        # Check against environment variable
        from app.config import Config
        if api_key != Config.API_KEY:
            return jsonify({'error': 'Invalid API key'}), 401
        
        return f(*args, **kwargs)
    return decorated_function

class CorsMiddleware:
    """CORS middleware with configurable origins"""
    
    def __init__(self, allowed_origins=None):
        self.allowed_origins = allowed_origins or ['http://localhost:3000']
    
    def add_cors_headers(self, response):
        """Add CORS headers to response"""
        origin = request.headers.get('Origin')
        
        if origin in self.allowed_origins or '*' in self.allowed_origins:
            response.headers['Access-Control-Allow-Origin'] = origin or '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-API-Key'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
        
        return response

def handle_options_request(f):
    """Handle CORS preflight requests"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'OPTIONS':
            response = jsonify({})
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            return response
        return f(*args, **kwargs)
=======
from functools import wraps
from flask import request, jsonify
import time
import re
from typing import Dict, Any

class SecurityMiddleware:
    """Security middleware for request validation and sanitization"""
    
    @staticmethod
    def sanitize_input(data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize all string inputs in request data"""
        sanitized = {}
        for key, value in data.items():
            if isinstance(value, str):
                # Remove any script tags or dangerous patterns
                cleaned = re.sub(r'<[^>]*>', '', value)
                cleaned = re.sub(r'[<>{}]', '', cleaned)
                sanitized[key] = cleaned[:2000]  # Limit length
            elif isinstance(value, dict):
                sanitized[key] = SecurityMiddleware.sanitize_input(value)
            elif isinstance(value, list):
                sanitized[key] = [
                    SecurityMiddleware.sanitize_input(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                sanitized[key] = value
        return sanitized
    
    @staticmethod
    def validate_content_type(content_type: str) -> bool:
        """Validate request content type"""
        allowed_types = ['application/json']
        return content_type in allowed_types
    
    @staticmethod
    def add_security_headers(response):
        """Add security headers to response"""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        return response

class RateLimitMiddleware:
    """Rate limiting middleware with Redis support"""
    
    def __init__(self, redis_client=None):
        self.redis_client = redis_client
        self.in_memory_store = {}
        
    def check_rate_limit(self, key: str, limit: int, window: int) -> bool:
        """Check if request is within rate limit"""
        current_time = time.time()
        
        if self.redis_client:
            # Use Redis for distributed rate limiting
            pipe = self.redis_client.pipeline()
            pipe.zremrangebyscore(key, 0, current_time - window)
            pipe.zadd(key, {str(current_time): current_time})
            pipe.zcard(key)
            pipe.expire(key, window)
            _, _, count, _ = pipe.execute()
            return count <= limit
        else:
            # Fallback to in-memory store
            if key not in self.in_memory_store:
                self.in_memory_store[key] = []
            
            # Clean old requests
            self.in_memory_store[key] = [
                t for t in self.in_memory_store[key] 
                if t > current_time - window
            ]
            
            if len(self.in_memory_store[key]) >= limit:
                return False
            
            self.in_memory_store[key].append(current_time)
            return True

def rate_limit(limit=100, window=60):
    """Decorator for rate limiting endpoints"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get client identifier (IP address)
            client_ip = request.remote_addr
            
            # Create rate limit key
            key = f"ratelimit:{client_ip}:{f.__name__}"
            
            # Initialize rate limiter (would be configured in app)
            if not hasattr(request, 'rate_limiter'):
                request.rate_limiter = RateLimitMiddleware()
            
            # Check rate limit
            if not request.rate_limiter.check_rate_limit(key, limit, window):
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'message': f'Too many requests. Please wait {window} seconds.',
                    'limit': limit,
                    'window': window
                }), 429
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_api_key(f):
    """Decorator to require API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({'error': 'API key required'}), 401
        
        # Check against environment variable
        from app.config import Config
        if api_key != Config.API_KEY:
            return jsonify({'error': 'Invalid API key'}), 401
        
        return f(*args, **kwargs)
    return decorated_function

class CorsMiddleware:
    """CORS middleware with configurable origins"""
    
    def __init__(self, allowed_origins=None):
        self.allowed_origins = allowed_origins or ['http://localhost:3000']
    
    def add_cors_headers(self, response):
        """Add CORS headers to response"""
        origin = request.headers.get('Origin')
        
        if origin in self.allowed_origins or '*' in self.allowed_origins:
            response.headers['Access-Control-Allow-Origin'] = origin or '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-API-Key'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
        
        return response

def handle_options_request(f):
    """Handle CORS preflight requests"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'OPTIONS':
            response = jsonify({})
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            return response
        return f(*args, **kwargs)
>>>>>>> 6a97c5ff1caff98b22d3c35a1de0b0b2e5252662
    return decorated_function