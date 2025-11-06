# fusionforms/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.shortcuts import redirect
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from apps.core.health import HealthCheckView, ReadinessCheckView, LivenessCheckView
from apps.core.monitoring import MetricsView


def root_view(request):
    """Root endpoint that provides API information"""
    return JsonResponse({
        'message': 'Welcome to FusionForms API',
        'version': '1.0.0',
        'documentation': {
            'swagger': request.build_absolute_uri('/api/docs/'),
            'redoc': request.build_absolute_uri('/api/redoc/'),
            'schema': request.build_absolute_uri('/api/schema/'),
        },
        'endpoints': {
            'api_v1': request.build_absolute_uri('/api/v1/'),
            'health': request.build_absolute_uri('/health/'),
            'admin': request.build_absolute_uri('/admin/'),
        }
    })


urlpatterns = [
    # Root endpoint
    path('', root_view, name='root'),
    
    path('admin/', admin.site.urls),
    
    # Health check endpoints
    path('health/', HealthCheckView.as_view(), name='health'),
    path('health/ready/', ReadinessCheckView.as_view(), name='readiness'),
    path('health/live/', LivenessCheckView.as_view(), name='liveness'),
    path('health/metrics/', MetricsView.as_view(), name='metrics'),
    
    # API v1
    path('api/v1/accounts/', include('apps.accounts.urls')),
    path('api/v1/forms/', include('apps.forms.urls')),
    path('api/v1/submissions/', include('apps.submissions.urls')),
    path('api/v1/analytics/', include('apps.analytics.urls')),
    path('api/v1/webhooks/', include('apps.webhooks.urls')),
    
    # Backward compatibility (redirect to v1)
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/forms/', include('apps.forms.urls')),
    path('api/submissions/', include('apps.submissions.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    path('api/webhooks/', include('apps.webhooks.urls')),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]