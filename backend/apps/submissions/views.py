# apps/submissions/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, QuerySet
from .models import Submission, SavedForm
from .serializers import SubmissionSerializer, SavedFormSerializer

class SubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self) -> QuerySet[Submission]:  # type: ignore[override]
        user = self.request.user
        if user.role == 'admin':
            return Submission.objects.all()
        else:
            # Users can only see submissions for their own forms
            return Submission.objects.filter(form__created_by=user)
    
    @action(detail=False, methods=['get'])
    def export(self, request):
        form_id = request.query_params.get('form_id')
        format_type = request.query_params.get('format', 'csv')
        
        if not form_id:
            return Response(
                {'error': 'form_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        submissions = self.get_queryset().filter(form_id=form_id)
        
        # This is a simplified version - in a real implementation, 
        # you would generate and return the actual file
        return Response({
            'message': f'Exporting {len(submissions)} submissions in {format_type} format',
            'count': len(submissions)
        })

class SavedFormViewSet(viewsets.ModelViewSet):
    serializer_class = SavedFormSerializer
    permission_classes = [permissions.AllowAny]  # Allow anonymous users to save forms
    
    def get_queryset(self):  # type: ignore[override]
        # Use session key to identify the user
        session_key = self.request.session.session_key or self.request.session.create()
        return SavedForm.objects.filter(session_key=session_key)
    
    def perform_create(self, serializer):
        session_key = self.request.session.session_key or self.request.session.create()
        serializer.save(session_key=session_key)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        saved_form = self.get_object()
        saved_form.is_completed = True
        saved_form.save()
        
        # Create a submission from the saved form
        Submission.objects.create(
            form=saved_form.form,
            data=saved_form.data,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return Response({'status': 'form completed'})