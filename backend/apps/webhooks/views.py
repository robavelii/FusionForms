# apps/webhooks/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import requests
import json
import hmac
import hashlib
from .models import Webhook, WebhookLog
from .serializers import WebhookSerializer, WebhookLogSerializer

class WebhookViewSet(viewsets.ModelViewSet):
    serializer_class = WebhookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Webhook.objects.all()
        else:
            # Users can only see webhooks for their own forms
            return Webhook.objects.filter(form__created_by=user)
    
    @action(detail=True, methods=['post'])
    def test(self, request, pk=None):
        webhook = self.get_object()
        
        # Create a test payload
        payload = {
            'event': 'test',
            'form_id': str(webhook.form.id),
            'form_title': webhook.form.title,
            'timestamp': webhook.created_at.isoformat()
        }
        
        # Send the test webhook
        headers = {
            'Content-Type': 'application/json',
        }
        
        if webhook.secret:
            signature = hmac.new(
                webhook.secret.encode(),
                json.dumps(payload).encode(),
                hashlib.sha256
            ).hexdigest()
            headers['X-Webhook-Signature'] = f'sha256={signature}'
        
        try:
            response = requests.post(
                webhook.url,
                json=payload,
                headers=headers,
                timeout=10
            )
            
            # Log the test
            WebhookLog.objects.create(
                webhook=webhook,
                event_type='test',
                response_code=response.status_code,
                response_body=response.text[:500]  # Limit response body size
            )
            
            return Response({
                'status': 'success',
                'response_code': response.status_code,
                'response_body': response.text[:500]
            })
        except Exception as e:
            # Log the error
            WebhookLog.objects.create(
                webhook=webhook,
                event_type='test',
                response_code=None,
                response_body=str(e)[:500]
            )
            
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def logs(self, request, pk=None):
        webhook = self.get_object()
        logs = webhook.logs.all()
        serializer = WebhookLogSerializer(logs, many=True)
        return Response(serializer.data)

def trigger_webhooks(form_id, event_type, data):
    """Trigger all webhooks for a form when an event occurs"""
    from apps.forms.models import Form
    
    try:
        form = Form.objects.get(id=form_id)
        webhooks = Webhook.objects.filter(form=form, is_active=True)
        
        for webhook in webhooks:
            if event_type in webhook.events:
                # Create the payload
                payload = {
                    'event': event_type,
                    'form_id': str(form.id),
                    'form_title': form.title,
                    'data': data,
                    'timestamp': webhook.created_at.isoformat()
                }
                
                # Send the webhook
                headers = {
                    'Content-Type': 'application/json',
                }
                
                if webhook.secret:
                    signature = hmac.new(
                        webhook.secret.encode(),
                        json.dumps(payload).encode(),
                        hashlib.sha256
                    ).hexdigest()
                    headers['X-Webhook-Signature'] = f'sha256={signature}'
                
                try:
                    response = requests.post(
                        webhook.url,
                        json=payload,
                        headers=headers,
                        timeout=10
                    )
                    
                    # Log the webhook call
                    WebhookLog.objects.create(
                        webhook=webhook,
                        event_type=event_type,
                        response_code=response.status_code,
                        response_body=response.text[:500]
                    )
                except Exception as e:
                    # Log the error
                    WebhookLog.objects.create(
                        webhook=webhook,
                        event_type=event_type,
                        response_code=None,
                        response_body=str(e)[:500]
                    )
    except Form.DoesNotExist:
        pass