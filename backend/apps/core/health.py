# apps/core/health.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from django.core.cache import cache
from django.conf import settings
import redis
import logging

logger = logging.getLogger(__name__)


class HealthCheckView(APIView):
    """Health check endpoint for load balancers and monitoring"""
    permission_classes = []
    
    def get(self, request):
        return Response({
            'status': 'healthy',
            'service': 'fusionforms-api'
        })


class ReadinessCheckView(APIView):
    """Readiness check - verifies all dependencies are available"""
    permission_classes = []
    
    def get(self, request):
        checks = {
            'database': False,
            'cache': False,
            'celery': False,
        }
        
        # Check database
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                checks['database'] = True
        except Exception as e:
            logger.error(f"Database check failed: {e}")
        
        # Check cache (Redis)
        try:
            cache.set('health_check', 'ok', 10)
            if cache.get('health_check') == 'ok':
                checks['cache'] = True
        except Exception as e:
            logger.error(f"Cache check failed: {e}")
        
        # Check Celery broker (basic check)
        try:
            broker_url = settings.CELERY_BROKER_URL
            if broker_url and broker_url.startswith('redis://'):
                # Try to connect to Redis
                import redis
                from urllib.parse import urlparse
                parsed = urlparse(broker_url)
                r = redis.Redis(
                    host=parsed.hostname or 'localhost',
                    port=parsed.port or 6379,
                    password=parsed.password,
                    socket_connect_timeout=1,
                    decode_responses=False
                )
                r.ping()
                checks['celery'] = True
        except Exception as e:
            logger.warning(f"Celery broker check failed: {e}")
        
        all_healthy = all(checks.values())
        
        return Response({
            'status': 'ready' if all_healthy else 'not ready',
            'checks': checks
        }, status=status.HTTP_200_OK if all_healthy else status.HTTP_503_SERVICE_UNAVAILABLE)


class LivenessCheckView(APIView):
    """Liveness check - simple endpoint to verify service is running"""
    permission_classes = []
    
    def get(self, request):
        return Response({
            'status': 'alive',
            'service': 'fusionforms-api'
        })

