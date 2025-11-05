# apps/core/exceptions.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """Custom exception handler for consistent error responses"""
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # Now add the custom error formatting
    if response is not None:
        custom_response_data = {
            'error': {
                'status_code': response.status_code,
                'message': 'An error occurred',
                'details': response.data
            }
        }
        response.data = custom_response_data
        
        # Log errors
        if response.status_code >= 500:
            logger.error(f"Server error: {exc}", exc_info=True)
        elif response.status_code >= 400:
            logger.warning(f"Client error: {exc}")
    
    return response


class ValidationError(Exception):
    """Custom validation error"""
    pass


class RateLimitExceeded(Exception):
    """Custom rate limit exception"""
    pass

