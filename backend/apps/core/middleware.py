# apps/core/middleware.py
import time
import logging
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(MiddlewareMixin):
    """Middleware to log all requests for monitoring and debugging"""
    
    def process_request(self, request):
        request.start_time = time.time()
        return None
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            # Log slow requests
            if duration > 1.0:  # Log requests taking more than 1 second
                logger.warning(
                    f"Slow request: {request.method} {request.path} took {duration:.2f}s",
                    extra={
                        'method': request.method,
                        'path': request.path,
                        'duration': duration,
                        'status_code': response.status_code,
                    }
                )
            
            # Add timing header
            response['X-Process-Time'] = f"{duration:.3f}"
        
        return response


class MetricsMiddleware(MiddlewareMixin):
    """Middleware to track API metrics"""
    
    def process_response(self, request, response):
        # Track request metrics in cache (for basic metrics)
        if request.path.startswith('/api/'):
            try:
                cache_key = f"metrics:requests:{request.method}"
                cache.incr(cache_key, timeout=3600)  # Increment counter, expire in 1 hour
            except:
                pass  # Ignore cache errors
        
        return response

