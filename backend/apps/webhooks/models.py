# apps/webhooks/models.py
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from apps.forms.models import Form

User = get_user_model()

class Webhook(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='webhooks')
    name = models.CharField(max_length=100)
    url = models.URLField()
    secret = models.CharField(max_length=100, blank=True)
    events = models.JSONField(default=list)  # List of events to trigger on
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['form', 'is_active']),
            models.Index(fields=['is_active']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} for {self.form.title}"

class WebhookLog(models.Model):
    webhook = models.ForeignKey(Webhook, on_delete=models.CASCADE, related_name='logs')
    event_type = models.CharField(max_length=50)
    response_code = models.IntegerField(null=True, blank=True)
    response_body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['webhook', '-created_at']),
            models.Index(fields=['event_type']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"Log for {self.webhook.name} - {self.event_type}"