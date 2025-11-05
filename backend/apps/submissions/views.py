# apps/submissions/views.py
from rest_framework import viewsets, permissions, status, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q, QuerySet
from .models import Submission, SavedForm
from .serializers import SubmissionSerializer, SavedFormSerializer
from apps.forms.models import Form
from apps.analytics.models import FormAnalytics
from apps.webhooks.tasks import process_webhook
from jsonschema import validate as jsonschema_validate, ValidationError
import csv
from django.http import HttpResponse
import os
import requests

class SubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = 'submissions'
    
    def get_queryset(self) -> QuerySet[Submission]:  # type: ignore[override]
        user = self.request.user
        if user.role == 'admin':
            return Submission.objects.all()
        else:
            # Users can only see submissions for their own forms
            return Submission.objects.filter(form__created_by=user)

    def perform_create(self, serializer):
        form_id = self.request.data.get('form')
        form = get_object_or_404(Form, id=form_id)
        
        # Validate against schema if provided
        schema = form.schema.get('jsonSchema') or form.schema.get('schema') or None
        if schema:
            try:
                jsonschema_validate(instance=self.request.data.get('data', {}), schema=schema)
            except ValidationError as exc:
                raise exceptions.ValidationError({'data': f'Invalid data: {exc.message}'})

        # Optional reCAPTCHA verification
        recaptcha_secret = os.getenv('RECAPTCHA_SECRET')
        recaptcha_token = self.request.data.get('recaptchaToken')
        if recaptcha_secret:
            if not recaptcha_token:
                raise exceptions.ValidationError({'recaptchaToken': 'Missing reCAPTCHA token'})
            try:
                verify_resp = requests.post(
                    'https://www.google.com/recaptcha/api/siteverify',
                    data={'secret': recaptcha_secret, 'response': recaptcha_token}, timeout=5
                ).json()
                if not verify_resp.get('success'):
                    raise exceptions.ValidationError({'recaptcha': 'Verification failed'})
            except Exception:
                raise exceptions.ValidationError({'recaptcha': 'Verification error'})

        submission = serializer.save(
            form=form,
            ip_address=self.request.META.get('REMOTE_ADDR'),
            user_agent=self.request.META.get('HTTP_USER_AGENT', ''),
        )
        # Update analytics counters lazily
        analytics, _ = FormAnalytics.objects.get_or_create(form=form)
        analytics.submissions += 1
        analytics.save()
        # Fire webhooks asynchronously
        process_webhook.delay(str(form.id), 'submission.created', serializer.data)
        return submission
    
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

        if format_type == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="submissions.csv"'
            writer = csv.writer(response)
            writer.writerow(['id', 'created_at', 'ip_address', 'user_agent', 'data'])
            for s in submissions:
                writer.writerow([str(s.id), s.created_at.isoformat(), s.ip_address or '', s.user_agent[:100], s.data])
            return response
        else:
            return Response({'error': 'Unsupported format'}, status=status.HTTP_400_BAD_REQUEST)

class PublicSubmissionView(APIView):
    """Public endpoint for submitting forms (no auth required)"""
    permission_classes = [permissions.AllowAny]
    throttle_scope = 'submissions'
    
    def post(self, request, form_id):
        form = get_object_or_404(Form, id=form_id, status='published')
        
        # Validate against schema
        schema = form.schema.get('jsonSchema') or form.schema.get('schema') or None
        if schema:
            try:
                jsonschema_validate(instance=request.data.get('data', {}), schema=schema)
            except ValidationError as exc:
                raise exceptions.ValidationError({'data': f'Invalid data: {exc.message}'})
        
        # Optional reCAPTCHA verification
        recaptcha_secret = os.getenv('RECAPTCHA_SECRET')
        recaptcha_token = request.data.get('recaptchaToken')
        if recaptcha_secret and recaptcha_token:
            try:
                verify_resp = requests.post(
                    'https://www.google.com/recaptcha/api/siteverify',
                    data={'secret': recaptcha_secret, 'response': recaptcha_token}, timeout=5
                ).json()
                if not verify_resp.get('success'):
                    raise exceptions.ValidationError({'recaptcha': 'Verification failed'})
            except Exception:
                raise exceptions.ValidationError({'recaptcha': 'Verification error'})
        
        # Create submission
        submission = Submission.objects.create(
            form=form,
            data=request.data.get('data', {}),
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
        )
        
        # Update analytics
        analytics, _ = FormAnalytics.objects.get_or_create(form=form)
        analytics.submissions += 1
        analytics.save()
        
        # Fire webhooks asynchronously
        process_webhook.delay(str(form.id), 'submission.created', SubmissionSerializer(submission).data)
        
        return Response({
            'status': 'success',
            'submission_id': str(submission.id)
        }, status=status.HTTP_201_CREATED)


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