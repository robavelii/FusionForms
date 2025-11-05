# apps/core/throttling.py
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle


class SubmissionRateThrottle(UserRateThrottle):
    """Custom throttle for form submissions - stricter limits"""
    scope = 'submissions'


class AuthRateThrottle(AnonRateThrottle):
    """Throttle for authentication endpoints to prevent brute force"""
    scope = 'auth'


class PublicFormRateThrottle(AnonRateThrottle):
    """Throttle for public form access"""
    scope = 'anon'


class WebhookRateThrottle(UserRateThrottle):
    """Throttle for webhook testing/triggering"""
    scope = 'webhooks'

