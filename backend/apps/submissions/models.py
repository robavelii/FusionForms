# apps/submissions/models.py
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from apps.forms.models import Form

User = get_user_model()

class Submission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='submissions')
    data = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    is_spam = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['form', 'created_at']),
            models.Index(fields=['form', '-created_at']),
            models.Index(fields=['ip_address']),
            models.Index(fields=['is_spam']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"Submission for {self.form.title}"

class SavedForm(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='saved_forms')
    data = models.JSONField(default=dict)
    session_key = models.CharField(max_length=40)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['form', 'session_key']
        indexes = [
            models.Index(fields=['session_key']),
        ]
    
    def __str__(self):
        return f"Saved form for {self.form.title}"