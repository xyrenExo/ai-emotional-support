import time
import threading
from functools import wraps
from flask import request, jsonify
from typing import Dict, Tuple, Optional
import redis
from app.config import Config

class RateLimiter:
    """Advanced rate limiter with multiple strategies"""
    
    def __init__(self, redis_url: Optional[str] = None):
        self.redis_client = None
        if redis_url:
            try:
                self.redis_client = redis.from_url(redis_url)
            except:
                pass
        
        # In-memory store as fallback
        self.memory_store: Dict[str, list] = {}
        self.lock = threading.Lock()
    
    def _get_redis_key(self, key: str, window: int) -> str:
        """Generate Redis key for rate limiting"""
        current_window = int(time.time() / window)
        return f"ratelimit:{key}:{current_window}"
    
    def _check_redis(self, key: str, limit: int, window: int) -> Tuple[bool, Dict]:
        """Check rate limit using Redis"""
        redis_key = self._get_redis_key(key, window)
        
        pipe = self.redis_client.pipeline()
        pipe.incr(redis_key)
        pipe.expire(redis_key, window)
        count, _ = pipe.execute()
        
        is_allowed = count <= limit
        headers = {
            'X-RateLimit-Limit': str(limit),
            'X-RateLimit-Remaining': str(max(0, limit - count)),
            'X-RateLimit-Reset': str(int(time.time() + window))
        }
        
        return is_allowed, headers
    
    def _check_memory(self, key: str, limit: int, window: int) -> Tuple[bool, Dict]:
        """Check rate limit using in-memory store"""
        current_time = time.time()
        
        with self.lock:
            if key not in self.memory_store:
                self.memory_store[key] = []
            
            # Clean old requests
            self.memory_store[key] = [
                t for t in self.memory_store[key] 
                if t > current_time - window
            ]
            
            current_count = len(self.memory_store[key])
            is_allowed = current_count < limit
            
            if is_allowed:
                self.memory_store[key].append(current_time)
            
            headers = {
                'X-RateLimit-Limit': str(limit),
                'X-RateLimit-Remaining': str(max(0, limit - current_count - (1 if is_allowed else 0))),
                'X-RateLimit-Reset': str(int(current_time + window))
            }
            
            return is_allowed, headers
    
    def check_rate_limit(self, key: str, limit: int = 100, window: int = 60) -> Tuple[bool, Dict]:
        """Check if request is within rate limits"""
        if self.redis_client:
            return self._check_redis(key, limit, window)
        else:
            return self._check_memory(key, limit, window)
    
    def get_remaining(self, key: str, limit: int, window: int) -> int:
        """Get remaining requests allowed"""
        if self.redis_client:
            redis_key = self._get_redis_key(key, window)
            count = self.redis_client.get(redis_key) or 0
            return max(0, limit - int(count))
        else:
            current_time = time.time()
            with self.lock:
                if key not in self.memory_store:
                    return limit
                valid_requests = [
                    t for t in self.memory_store[key] 
                    if t > current_time - window
                ]
                return max(0, limit - len(valid_requests))

class RateLimitDecorator:
    """Decorator for applying rate limits to Flask routes"""
    
    def __init__(self, limiter: RateLimiter):
        self.limiter = limiter
    
    def limit(self, limit: int = 100, window: int = 60, key_func=None):
        """Rate limit decorator"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # Get rate limit key
                if key_func:
                    key = key_func()
                else:
                    # Default to IP address
                    key = f"ip:{request.remote_addr}:{f.__name__}"
                
                # Check rate limit
                is_allowed, headers = self.limiter.check_rate_limit(key, limit, window)
                
                # Add rate limit headers to response
                def add_headers(response):
                    for header_name, header_value in headers.items():
                        response.headers[header_name] = header_value
                    return response
                
                if not is_allowed:
                    response = jsonify({
                        'error': 'Rate limit exceeded',
                        'message': f'Too many requests. Limit is {limit} requests per {window} seconds.',
                        'retry_after': headers.get('X-RateLimit-Reset', window)
                    }), 429
                    return add_headers(response)
                
                result = f(*args, **kwargs)
                
                # If result is a tuple (response, status_code)
                if isinstance(result, tuple):
                    response = result[0]
                    if hasattr(response, 'headers'):
                        for header_name, header_value in headers.items():
                            response.headers[header_name] = header_value
                    return result
                
                # If result is a response object
                if hasattr(result, 'headers'):
                    for header_name, header_value in headers.items():
                        result.headers[header_name] = header_value
                
                return result
            
            return decorated_function
        return decorator

# Global rate limiter instance
rate_limiter = RateLimiter()
rate_limit_decorator = RateLimitDecorator(rate_limiter)

# Predefined rate limit configurations
RATE_LIMITS = {
    'strict': {'limit': 10, 'window': 60},      # 10 requests per minute
    'normal': {'limit': 30, 'window': 60},      # 30 requests per minute
    'liberal': {'limit': 100, 'window': 60},    # 100 requests per minute
    'api': {'limit': 1000, 'window': 3600}      # 1000 requests per hour
}

def apply_rate_limit(level: str = 'normal'):
    """Apply predefined rate limit by level"""
    config = RATE_LIMITS.get(level, RATE_LIMITS['normal'])
    return rate_limit_decorator.limit(**config)