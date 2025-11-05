# apps/core/caching.py
from django.core.cache import cache as django_cache
from functools import wraps
import hashlib
import json


def cache_result(timeout=300, key_prefix=''):
    """Decorator to cache function results"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            try:
                kwargs_str = json.dumps(kwargs, sort_keys=True, default=str)
            except TypeError:
                kwargs_str = str(kwargs)
            cache_key = f"{key_prefix}:{func.__name__}:{hashlib.md5(kwargs_str.encode()).hexdigest()}"
            
            # Try to get from cache
            result = django_cache.get(cache_key)
            if result is not None:
                return result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            django_cache.set(cache_key, result, timeout)
            return result
        return wrapper
    return decorator


def invalidate_cache(pattern):
    """Invalidate cache keys matching pattern"""
    # Note: This is a simplified version. For production, consider using django-redis with pattern deletion
    try:
        from django_redis import get_redis_connection
        redis_conn = get_redis_connection("default")
        keys = redis_conn.keys(f"fusionforms:{pattern}*")
        if keys:
            redis_conn.delete(*keys)
    except ImportError:
        pass


def get_or_set_cache(key, callback, timeout=300):
    """Get value from cache or set it using callback"""
    value = django_cache.get(key)
    if value is None:
        value = callback()
        django_cache.set(key, value, timeout)
    return value

