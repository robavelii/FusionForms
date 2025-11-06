# apps/analytics/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, F
from django.utils import timezone
from datetime import timedelta
from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.forms.models import Form
from apps.submissions.models import Submission
from .models import FormAnalytics, FieldAnalytics
from .serializers import FormAnalyticsSerializer, FieldAnalyticsSerializer

@extend_schema_view(
    list=extend_schema(tags=['Analytics']),
    retrieve=extend_schema(tags=['Analytics']),
)
class FormAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FormAnalyticsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self): #type: ignore[override]
        user = self.request.user
        if user.role == 'admin':
            return FormAnalytics.objects.all()
        else:
            # Users can only see analytics for their own forms
            return FormAnalytics.objects.filter(form__created_by=user)
    
    @extend_schema(tags=['Analytics'])
    @action(detail=True, methods=['get'])
    def submissions_over_time(self, request, pk=None):
        analytics = self.get_object()
        days = int(request.query_params.get('days', 30))
        
        start_date = timezone.now() - timedelta(days=days)
        submissions = Submission.objects.filter(
            form=analytics.form,
            created_at__gte=start_date
        ).extra(
            select={'day': 'date(created_at)'}
        ).values('day').annotate(count=Count('id')).order_by('day')
        
        return Response(list(submissions))
    
    @extend_schema(tags=['Analytics'])
    @action(detail=True, methods=['get'])
    def field_responses(self, request, pk=None):
        analytics = self.get_object()
        field_id = request.query_params.get('field_id')
        
        if not field_id:
            return Response(
                {'error': 'field_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get all submissions for this form
        submissions = Submission.objects.filter(form=analytics.form)
        
        # Extract values for the specified field
        field_values = []
        for submission in submissions:
            if field_id in submission.data:
                field_values.append(submission.data[field_id])
        
        # Count occurrences
        response_counts = {}
        for value in field_values:
            if value in response_counts:
                response_counts[value] += 1
            else:
                response_counts[value] = 1
        
        return Response({
            'field_id': field_id,
            'total_responses': len(field_values),
            'response_counts': response_counts
        })
    
    @extend_schema(tags=['Analytics'])
    @action(detail=True, methods=['post'])
    def track_view(self, request, pk=None):
        analytics = self.get_object()
        analytics.views += 1
        analytics.save()
        return Response({'status': 'view tracked'})
    
    @extend_schema(tags=['Analytics'])
    @action(detail=True, methods=['post'])
    def calculate_completion_rate(self, request, pk=None):
        analytics = self.get_object()
        form = analytics.form
        
        # Calculate completion rate
        total_views = analytics.views
        total_submissions = Submission.objects.filter(form=form).count()
        
        if total_views > 0:
            completion_rate = (total_submissions / total_views) * 100
        else:
            completion_rate = 0
        
        analytics.completion_rate = completion_rate
        analytics.submissions = total_submissions
        analytics.save()
        
        return Response({
            'completion_rate': completion_rate,
            'total_views': total_views,
            'total_submissions': total_submissions
        })