# apps/core/monitoring.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.db import connection
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from apps.forms.models import Form
from apps.submissions.models import Submission
import logging

logger = logging.getLogger(__name__)


class MetricsView(APIView):
    """Endpoint to expose application metrics for monitoring"""
    permission_classes = []  # Make this protected in production
    
    def get(self, request):
        metrics = {
            'timestamp': timezone.now().isoformat(),
            'database': {},
            'cache': {},
            'application': {},
        }
        
        # Database metrics
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM pg_stat_activity")
                metrics['database']['active_connections'] = cursor.fetchone()[0]
        except Exception as e:
            logger.error(f"Error getting database metrics: {e}")
        
        # Cache metrics
        try:
            test_key = 'metrics:test'
            cache.set(test_key, 'test', 60)
            metrics['cache']['status'] = 'ok' if cache.get(test_key) == 'test' else 'error'
            cache.delete(test_key)
        except Exception as e:
            metrics['cache']['status'] = 'error'
            logger.error(f"Error getting cache metrics: {e}")
        
        # Application metrics
        try:
            metrics['application']['total_forms'] = Form.objects.count()
            metrics['application']['total_submissions'] = Submission.objects.count()
            metrics['application']['submissions_last_24h'] = Submission.objects.filter(
                created_at__gte=timezone.now() - timedelta(hours=24)
            ).count()
        except Exception as e:
            logger.error(f"Error getting application metrics: {e}")
        
        return Response(metrics, status=status.HTTP_200_OK)

